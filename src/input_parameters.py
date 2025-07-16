

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
        "name": "glavs_custom_search",
        "function": {
            "name": "glavs_custom_search",
            "description": "Search for information on the web using a custom search engine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "Term or query to search for"
                    }
                },
                "required": ["search_term"]
            }
        }
    },
    {  # ADD MCP TOOL SUPPORT
        # Update to the location of *your* MCP server
        "type": "mcp",
        "server_label": "local_file_lookup",
        "server_url": "https://<your_mcp_server>/sse/",
        "require_approval": "never"
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
