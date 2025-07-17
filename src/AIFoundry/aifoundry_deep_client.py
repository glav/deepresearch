from datetime import datetime
import json
import os, time
from typing import List, Optional
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import DeepResearchTool, MessageRole, ThreadMessage, ListSortOrder
from terminal_spinner import TerminalSpinner
from output_processor import create_research_summary_aifoundry, ResponseFoundryMessage
from azure.ai.agents.models import FunctionTool, ToolSet
from AIFoundry.custom_tooling import get_document_city_location
from AIFoundry.aifoundry_client_helper import AIFoundryClientHelper

def do_aifoundry_research(system_prompt: str, user_query: str):
    print("AI Foundry Deep Research Client")

    foundryClientHelper = AIFoundryClientHelper()
    foundryClientHelper.initialise_client()

    # Add Deep Research and custom function tools to the toolset
    foundryClientHelper.add_deep_research_tool()
    #foundryClientHelper.add_document_city_function_tool()

    with foundryClientHelper.project_client:

        with foundryClientHelper.project_client.agents as agents_client:

            # NOTE: To add Deep Research to an existing agent, fetch it with `get_agent(agent_id)` and then,
            # update the agent with the Deep Research tool.
            agent = agents_client.create_agent(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                name="DeepResearchAgent",
                instructions=system_prompt,
                description="An agent that performs deep research and custom data analysis.",
                tools=foundryClientHelper.tool_definitions,
                toolset=foundryClientHelper.toolset,  # This needs to be set if using a custom tool like get_document_city_location however this breaks deep research
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

            # Enable automatic function calls for custom tools
            # If we provide a new tool definition in tools field and toolset, we need to add it in here so it can be called.
            foundryClientHelper.add_document_city_function_tool()
            if foundryClientHelper.toolset and foundryClientHelper.toolset.definitions and len(foundryClientHelper.toolset.definitions) > 0:
                agents_client.enable_auto_function_calls(foundryClientHelper.toolset)

            start_time = datetime.now()

            # Create and start the spinner
            spinner = TerminalSpinner(message="Deep research in progress")

            # Use create_and_process for automatic tool execution
            #run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

            run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

            end_time = datetime.now()
            total_time = end_time - start_time
            spinner.stop("✓ Deep research complete!")

            run_status = run.status.value.lower() if hasattr(run, 'status') else run.status.lower()
            print(f"Run finished with status: {run_status}, ID: {run.id}, Total duration: {total_time}")

            # Fetch all messages after completion in chronological order
            messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
            for msg in messages:
                all_messages.append(
                    ResponseFoundryMessage(
                        text_messages=msg.text_messages,
                        url_citation_annotations=msg.url_citation_annotations,
                        role=msg.role.value
                    )
                )

            if run.status == "failed":
                print(f"Run failed: {run.last_error}, Total duration: {total_time}")

            create_research_summary_aifoundry(all_messages, total_time, run.usage)

            # Clean-up and delete the agent once the run is finished.
            # NOTE: Comment out this line if you plan to reuse the agent later.
            agents_client.delete_agent(agent.id)
            print("Deleted agent")



