from prompts import dadjoke_system_message, dadjoke_user_query, example_system_message, example_user_query

research_input=[
  {
    "role": "developer",
    "content": [
      {
        "type": "input_text",
        "text": example_system_message,
      }
    ]
  },
  {
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": example_user_query,
      }
    ]
  }
]

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

