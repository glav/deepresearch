from dotenv import load_dotenv
import os
from load_env import load_env
from openai import OpenAI
from basic_client import do_basic_completion
from openai_deep_client import do_openai_research
from azure_deep_client import do_azure_research
from aifoundry_deep_client import do_aifoundry_research

def main():
    # Load environment variables from .env files
    load_env()


    #do_basic_completion()

    #do_openai_research()
    #do_azure_research()
    do_aifoundry_research()


if __name__ == "__main__":
    main()
