import os
from openai import AzureOpenAI
from input_parameters import reasoning_input, azure_openai_tools_input, openai_tools_input, form_research_input
from load_env import load_env
from time import sleep
from output_processor import process_response_output, wait_for_response
from models import AZURE_01_MINI, AZURE_03_PRO, AZURE_03_MINI, AZURE_04_MINI, PROVIDER_AZURE

def do_azure_research(system_prompt: str, user_query: str):
    model = AZURE_04_MINI # | AZURE_03_PRO, AZURE_03_MINI, AZURE_04_MINI, AZURE_01_MINI

    print(f"Azure OpenAI Research Client - {model}")

    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=PROVIDER_AZURE[model]["version"],  # Use the version from PROVIDER_AZURE

    )

    try:
        response = client.responses.create(
            model=PROVIDER_AZURE[model]["deployment_name"],  # Use deployment name from PROVIDER_AZURE
            input=form_research_input(system_prompt, user_query),
            reasoning=reasoning_input,
            #tools=azure_openai_tools_input,  # 03-mini, 03-pro, 04-mini do not support tools like openAI, need to provide my own implementation,
            background=True
        )

        response, time_taken = wait_for_response(client, response)

        # Process and save output using the reusable output processor
        model_name = f"azure_{response.model.replace("-", "_")}"  # Convert model name for filename
        process_response_output(response,time_taken, model_name)

    except Exception as e:
        print(f"Error with Azure OpenAI API: {e}")
        print("Please check your Azure OpenAI configuration:")
        print("- AZURE_OPENAI_ENDPOINT")
        print("- AZURE_OPENAI_API_KEY")
        print("- AZURE_OPENAI_API_VERSION (optional, defaults to 2024-12-01-preview)")

if __name__ == "__main__":
    do_azure_research()
