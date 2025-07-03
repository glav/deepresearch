import os
from openai import OpenAI
from input_parameters import research_input, reasoning_input, tools_input
from time import sleep
from output_processor import process_response_output, wait_for_response

def do_research():
  client = OpenAI()

  modelo3 = "o3-deep-research"
  modelo4="o4-mini-deep-research-2025-06-26"

  try:
    response = client.responses.create(
      model=modelo3,
      input=research_input,
      reasoning=reasoning_input,
      tools=tools_input,
      background=True
    )

    response, time_taken = wait_for_response(client, response)

    # Process and save output using the reusable output processor
    model_name = f"openai_{response.model.replace("-", "_")}"  # Convert model name for filename
    process_response_output(response,time_taken, f"{model_name}")

  except Exception as e:
      print(f"Error with OpenAI API: {e}")
      print("Please check your OpenAI configuration:")
      print("- OPENAI_API_KEY")
