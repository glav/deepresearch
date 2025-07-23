from dotenv import load_dotenv
import os
from load_env import load_env
from openai import OpenAI
from basic_client import do_basic_completion
from openai_deep_client import do_openai_research
from azure_deep_client import do_azure_research
from AIFoundry.aifoundry_deep_client import do_aifoundry_research
import prompts

def main():
    # Load environment variables from .env files
    load_env()


    #do_basic_completion()

    #do_openai_research(prompts.example_system_message, prompts.example_user_query)
    #do_azure_research(prompts.cityquery_system_message, prompts.cityquery_user_query)
    do_azure_research(prompts.example_system_message, prompts.example_user_query)

    #do_aifoundry_research(prompts.cityquery_system_message, prompts.cityquery_user_query)
    #do_aifoundry_research(prompts.deepresearch_test_system_prompt, prompts.deepresearch_test_user_query)


if __name__ == "__main__":
    main()
