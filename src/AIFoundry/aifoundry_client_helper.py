import os, time
import json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import DeepResearchTool, MessageRole, ThreadMessage
from terminal_spinner import TerminalSpinner
from azure.ai.agents.models import FunctionTool, ToolSet
from AIFoundry.custom_tooling import get_document_city_location

class AIFoundryClientHelper:
    """
    Context manager for AIFoundry client operations.
    It initializes the client and handles cleanup.
    """
    def __init__(self):
        self.conn_id = None
        self.project_client = None
        self.toolset = None

    def initialise_client(self):
      # Initialize AI Project Client with DefaultAzureCredential
      self.project_client = AIProjectClient(
          endpoint=os.environ["PROJECT_ENDPOINT"],
          credential=DefaultAzureCredential(),
      )

      self.conn_id = self.project_client.connections.get(name=os.environ["BING_RESOURCE_NAME"]).id

      # Initialize a Deep Research tool with Bing Connection ID and Deep Research model deployment name
      deep_research_tool = DeepResearchTool(
          bing_grounding_connection_id=self.conn_id,
          deep_research_model=os.environ["DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME"],
      )    # Create custom function tool
      custom_functions = {get_document_city_location}  # Set of your custom functions
      function_tool = FunctionTool(custom_functions)

      # Create toolset and add both tools
      self.toolset = ToolSet()
      self.toolset.add(deep_research_tool)  # Add existing deep research tool
      self.toolset.add(function_tool)       # Add custom function tool



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
          if tool_call.function.name == "get_document_city_location":
              # Parse the function arguments
              function_args = json.loads(tool_call.function.arguments)
              document_name = function_args.get("document_name", "")

              # Execute the function and get the result
              function_result = get_document_city_location(document_name)

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


