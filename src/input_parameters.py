

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
    {
        "type": "function",
        "name": "get_document_city_location",
        "function": {
            "name": "get_document_city_location",
            "description": "Geo locates a document by its name to determine which Australian city it is located in. Returns one of: Sydney, Melbourne, Perth, Hobart, Brisbane, Adelaide.",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_name": {
                        "type": "string",
                        "description": "Document name to search for"
                    }
                },
                "required": ["document_name"]
            }
        }
    }
    # ,
    # {  # ADD MCP TOOL SUPPORT
    #     # Update to the location of *your* MCP server
    #     "type": "mcp",
    #     "name": "local_file_lookup",
    #     "description": "Access and search through local files and documents on the system. Use this when you need to find, read, or analyze files that are stored locally.",
    #     "server_label": "local_file_lookup",
    #     "server_url": "https://localhost:8080/mcp",
    #     "require_approval": "never",
    # }
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
