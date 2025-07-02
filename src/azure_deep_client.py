import os
from openai import AzureOpenAI
from input_parameters import research_input, reasoning_input, tools_input
from load_env import load_env
from time import sleep
from output_processor import process_response_output, wait_for_response

def do_azure_research():
    # Load environment variables
    load_env()

    # Azure OpenAI deep research models
    modelo3 = "o3-pro"
    modelo3Version = "2025-04-01-preview"
    modelo3Mini = "o3-mini"
    modelo3MiniVersion = "2025-04-01-preview"

    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=modelo3MiniVersion
        #api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    )


    try:
        response = client.responses.create(
            #model=modelo3,
            model=modelo3Mini,
            input=research_input,
            reasoning=reasoning_input,
            #tools=tools_input,
            background=True
        )

        response = wait_for_response(client, response)

        # Process and save output using the reusable output processor
        model_name = f"azure_{response.model.replace("-", "_")}"  # Convert model name for filename
        process_response_output(response, f"{model_name}")

    except Exception as e:
        print(f"Error with Azure OpenAI API: {e}")
        print("Please check your Azure OpenAI configuration:")
        print("- AZURE_OPENAI_ENDPOINT")
        print("- AZURE_OPENAI_API_KEY")
        print("- AZURE_OPENAI_API_VERSION (optional, defaults to 2024-12-01-preview)")

if __name__ == "__main__":
    do_azure_research()
