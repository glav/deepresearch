from datetime import datetime
import os, time
from typing import List, Optional
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import DeepResearchTool, MessageRole, ThreadMessage
from terminal_spinner import TerminalSpinner
from prompts import (
    deep_research_system_message,
    deep_research_user_query,
    deep_research_experiment_system_message,
    deep_research_epa_system_prompt,
    deep_research_epa_user_prompt,
    quick_system_message,
    quick_user_query,
)

class ResponseMessage:
    def __init__(self, text_messages: List, url_citation_annotations: Optional[any] = None):
        self.text_messages = text_messages
        self.url_citation_annotations = url_citation_annotations


def fetch_and_print_new_agent_response(
    thread_id: str,
    agents_client: AgentsClient,
    last_message_id: Optional[str] = None,
    all_messages: Optional[list[ResponseMessage]] = None,
) -> Optional[str]:
    response = agents_client.messages.get_last_message_by_role(
        thread_id=thread_id,
        role=MessageRole.AGENT,
    )
    if not response or response.id == last_message_id:
        return last_message_id  # No new content

    all_messages.append(
        ResponseMessage(
            text_messages=response.text_messages,
            url_citation_annotations=response.url_citation_annotations,
        )
    )

    return response.id


def create_research_summary(all_messages : List[ResponseMessage],time_taken, token_metrics) -> None:

    if not all_messages:
        print("No messages to summarize.")
        return

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"output_items_aifoundry_o3_deep_research.md")

    content = f"# All Output Items \n - Job Status: Complete\n - Total Time: {time_taken}\n"
    content += f"- Token Usage:\n   - prompt_tokens: {token_metrics.prompt_tokens}\n   - completion_tokens: {token_metrics.completion_tokens}\n"
    content += f"   - total_tokens: {token_metrics.total_tokens}\n\n"


    with open(output_file, "w", encoding="utf-8") as fp:
        fp.write(content)

        # Write individual output steps
        for i, msg in enumerate(all_messages):
            if i < len(all_messages) - 1:  # Not the final message
                fp.write(f"- Message {i + 1}:\n")
                for text in msg.text_messages:
                    fp.write(f"  - Text: {text.text.value}\n")
                if msg.url_citation_annotations:
                    for ann in msg.url_citation_annotations:
                        if ann.url_citation:
                            fp.write("  - URL Citation:\n")
                            if hasattr(ann.url_citation,'title'):
                                fp.write(f"    - Title: [{ann.url_citation.title}]\n")
                            if hasattr(ann.url_citation,'url'):
                                fp.write(f"    - Url:({ann.url_citation.url})\n")
                            if hasattr(ann.url_citation,'text'):
                                fp.write(f"    - Text: [{ann.url_citation.text}]\n")
                            if hasattr(ann.url_citation,'start_index'):
                                fp.write(f"    - Start Index:({ann.url_citation.start_index})\n")
                            if hasattr(ann.url_citation,'end_index'):
                                fp.write(f"    - End Index:({ann.url_citation.end_index})\n")
            else:
                fp.write("\n\n## Final Output\n")
                text_summary = "\n\n".join([t.text.value.strip() for t in msg.text_messages])
                fp.write(text_summary)

                # Write unique URL citations, if present
                if msg.url_citation_annotations:
                    fp.write("\n\n## References\n")
                    seen_urls = set()
                    for ann in msg.url_citation_annotations:
                        url = ann.url_citation.url
                        title = ann.url_citation.title or url
                        if url not in seen_urls:
                            fp.write(f"- [{title}]({url})\n")
                            seen_urls.add(url)

    print(f"Research summary written to '{output_file}'.")


def do_aifoundry_research():
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
    )

    # Create Agent with the Deep Research tool and process Agent run
    with project_client:

        with project_client.agents as agents_client:

            # Create a new agent that has the Deep Research tool attached.
            # NOTE: To add Deep Research to an existing agent, fetch it with `get_agent(agent_id)` and then,
            # update the agent with the Deep Research tool.
            agent = agents_client.create_agent(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                name="DeepResearchAgent",
                instructions=deep_research_epa_system_prompt,
                #instructions=quick_system_message,
                description="An agent that performs deep research using the Deep Research tool.",
                tools=deep_research_tool.definitions,
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
                    deep_research_epa_user_prompt
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
            while run_status in ("queued", "in_progress"):
                time.sleep(1)
                run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
                run_status = run.status.value.lower() if hasattr(run, 'status') else run.status.lower()

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
            print(f"Run finished with status: {run.status}, ID: {run.id}, Total duration: {total_time}")

            if run.status == "failed":
                print(f"Run failed: {run.last_error}, Total duration: {total_time}")

            create_research_summary(all_messages, total_time, run.usage)

            # Clean-up and delete the agent once the run is finished.
            # NOTE: Comment out this line if you plan to reuse the agent later.
            agents_client.delete_agent(agent.id)
            print("Deleted agent")
