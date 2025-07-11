from datetime import datetime
import json
import os, time
from typing import List, Optional
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import DeepResearchTool, MessageRole, ThreadMessage
from terminal_spinner import TerminalSpinner
from output_processor import create_research_summary_aifoundry, ResponseFoundryMessage
from azure.ai.agents.models import FunctionTool, ToolSet

# Example custom function you'd add to your file
def read_json_file(filename: str) -> str:
    """
    Reads a JSON file from the local filesystem and returns the contents.

    :param filename: The name of the JSON file to read
    :return: Contents of the JSON file as a string
    """
    # Your custom logic here
    import json

    result = {
        "dataset_name": f"dummy_dataset_{filename}",
        "description": "Contains mock data for testing purposes related to AI Foundry Deep Research",
    }
    return json.dumps(result)


def do_aifoundry_research(system_prompt: str, user_query: str):
    print("AI Foundry Deep Research Client")

    # Initialize AI Project Client with DefaultAzureCredential
    project_client = AIProjectClient(
        endpoint=os.environ["PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    conn_id = project_client.connections.get(name=os.environ["BING_RESOURCE_NAME"]).id

    # Initialize a Deep Research tool with Bing Connection ID and Deep Research model deployment name
    deep_research_tool = DeepResearchTool(
        bing_grounding_connection_id=conn_id,
        deep_research_model=os.environ["DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME"],
    )    # Create custom function tool
    custom_functions = {read_json_file}  # Set of your custom functions
    function_tool = FunctionTool(custom_functions)

    # Create toolset and add both tools
    toolset = ToolSet()
    toolset.add(deep_research_tool)  # Add existing deep research tool
    toolset.add(function_tool)       # Add custom function tool

    # Create Agent with the Deep Research tool and process Agent run
    with project_client:

        with project_client.agents as agents_client:

            # Enable auto function calls
            agents_client.enable_auto_function_calls(toolset)

            # Create a new agent that has the Deep Research tool attached.
            # NOTE: To add Deep Research to an existing agent, fetch it with `get_agent(agent_id)` and then,
            # update the agent with the Deep Research tool.
            agent = agents_client.create_agent(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                name="DeepResearchAgent",
                instructions=system_prompt,
                description="An agent that performs deep research and custom data analysis.",
                toolset=toolset,
            )

            # [END create_agent_with_deep_research_tool]
            print(f"Created agent, ID: {agent.id}")
            thread = agents_client.threads.create()
            print(f"Created thread, ID: {thread.id}")

            # Create message to thread
            message = agents_client.messages.create(
                thread_id=thread.id,
                role="user",
                content=(
                    user_query
                ),
            )
            print(f"Created message, ID: {message.id}")

            print(f"Start processing the message... this may take a few minutes to finish. Be patient!")
            all_messages = list()
            # Poll the run as long as run status is queued or in progress
            run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)
            last_message_id = None
            start_time = datetime.now()
            last_status = ''

            # Create and start the spinner
            spinner = TerminalSpinner(message="Deep research in progress")
            run_status = run.status.value.lower() if hasattr(run, 'status') else run.status.lower()
            while run_status in ("queued", "in_progress","requires_action"):
                time.sleep(1)
                run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
                spinner.update()
                run_status = run.status.value.lower() if hasattr(run, 'status') else run.status.lower()

                if run_status == "requires_action":
                    process_required_actions(run, thread.id, agents_client, spinner)

                last_message_id = fetch_and_print_new_agent_response(
                    thread_id=thread.id,
                    agents_client=agents_client,
                    last_message_id=last_message_id,
                    all_messages=all_messages,
                )

                # Update spinner with current status
                if last_status != run_status:
                    spinner.update(f"Deep research in progress - Status: {run_status}")
                    last_status = run_status
                else:
                    spinner.update()

            end_time = datetime.now()
            total_time = end_time - start_time
            spinner.stop("✓ Deep research complete!")
            print(f"Run finished with status: {run_status}, ID: {run.id}, Total duration: {total_time}")

            if run.status == "failed":
                print(f"Run failed: {run.last_error}, Total duration: {total_time}")

            create_research_summary_aifoundry(all_messages, total_time, run.usage)

            # Clean-up and delete the agent once the run is finished.
            # NOTE: Comment out this line if you plan to reuse the agent later.
            agents_client.delete_agent(agent.id)
            print("Deleted agent")



def fetch_and_print_new_agent_response(
    thread_id: str,
    agents_client: AgentsClient,
    last_message_id: Optional[str] = None,
    all_messages: Optional[list[ResponseFoundryMessage]] = None,
) -> Optional[str]:
    response = agents_client.messages.get_last_message_by_role(
        thread_id=thread_id,
        role=MessageRole.AGENT,
    )
    if not response or response.id == last_message_id:
        return last_message_id  # No new content

    all_messages.append(
        ResponseFoundryMessage(
            text_messages=response.text_messages,
            url_citation_annotations=response.url_citation_annotations,
        )
    )

    return response.id


def process_required_actions(run, thread_id: str, agents_client: AgentsClient, spinner: TerminalSpinner) -> int:
    """
    Process required tool actions for an agent run.

    :param run: The current agent run that requires action
    :param thread_id: ID of the thread being processed
    :param agents_client: The agents client for submitting tool outputs
    :return: Number of tool outputs processed
    """
    spinner.update(f"Run requires action, processing tool calls...")

    # Get the required actions from the run
    required_actions = run.required_action.submit_tool_outputs.tool_calls

    tool_outputs = []

    # Iterate through each tool call that needs to be processed
    for tool_call in required_actions:
        spinner.update(f"Processing tool call: {tool_call.id} - {tool_call.function.name}")

        # Execute the function based on the tool call
        if tool_call.function.name == "read_json_file":
            # Parse the function arguments
            function_args = json.loads(tool_call.function.arguments)
            filename = function_args.get("filename", "")

            # Execute the function and get the result
            function_result = read_json_file(filename)

            tool_output = {
                "tool_call_id": tool_call.id,
                "output": function_result
            }
        else:
            # Handle other potential function calls
            tool_output = {
                "tool_call_id": tool_call.id,
                "output": f"Unknown function: {tool_call.function.name}"
            }
        tool_outputs.append(tool_output)

    # Submit the tool outputs back to continue the run
    agents_client.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run.id,
        tool_outputs=tool_outputs
    )

    spinner.update(f"Submitted {len(tool_outputs)} tool outputs")
    return len(tool_outputs)


