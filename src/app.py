from dotenv import load_dotenv
import os
from load_env import load_env
from openai import OpenAI
from basic_client import do_basic_completion
from deep_client import do_research

def main():
    # Load environment variables from .env files
    load_env()


    #do_basic_completion()
    do_research()


if __name__ == "__main__":
    main()
