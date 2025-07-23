import os

reasoning_input = {
    "effort": "medium",
    "summary": "detailed"
}


openai_tools_input=[
  {
    "type": "web_search_preview"
  },
  {
    "type": "code_interpreter",
    "container": {
      "type": "auto",
      "file_ids": []
    }
  }
]

azure_openai_tools_input = [
    # {
    #     "type": "function",
    #     "name": "get_document_city_location",
    #     "function": {
    #         "name": "get_document_city_location",
    #         "description": "Geo locates a document by its name to determine which Australian city it is located in. Returns one of: Sydney, Melbourne, Perth, Hobart, Brisbane, Adelaide.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "document_name": {
    #                     "type": "string",
    #                     "description": "Document name to search for"
    #                 }
    #             },
    #             "required": ["document_name"]
    #         }
    #     }
    # }
    # ,
    {  # ADD MCP TOOL SUPPORT
        # Update to the location of *your* MCP server
        "type": "mcp",
        "server_label": "tavily",
        "server_url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={os.getenv('TAVILY_API_KEY')}",
        "require_approval": "never",
    }
]


def form_research_input(system_prompt: str, user_query: str):
    return [
        {
            "role": "developer",
            "content": [
                {
                    "type": "input_text",
                    "text": system_prompt,
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": user_query,
                }
            ]
        }
    ]
