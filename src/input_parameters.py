

reasoning_input={
  "effort": "medium",
  "summary": "detailed"
}

tools_input=[
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

