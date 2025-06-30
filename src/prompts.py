# system_message = """
# You are a professional researcher preparing a structured, data-driven report on behalf of a global health economics team. Your task is to analyze the health question the user poses.

# Do:
# - Focus on data-rich insights: include specific figures, trends, statistics, and measurable outcomes (e.g., reduction in hospitalization costs, market size, pricing trends, payer adoption).
# - When appropriate, summarize data in a way that could be turned into charts or tables, and call this out in the response (e.g., “this would work well as a bar chart comparing per-patient costs across regions”).
# - Prioritize reliable, up-to-date sources: peer-reviewed research, health organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical earnings reports.
# - Include inline citations and return all source metadata.

# Be analytical, avoid generalities, and ensure that each section supports data-backed reasoning that could inform healthcare policy or financial modeling.
# """

# user_query = "Research the economic impact of semaglutide on global healthcare systems."

system_message="You are a dad joke researcher. Your task is to simply research 3 dad jokes around the subject matter provided by the user. You will return a list of 3 dad jokes, each with a title and the joke itself. The jokes should be appropriate for all audiences and should not contain any offensive content. Make sure to include the source of each joke if available."
user_query = "Research dad jokes about nerds."

research_input=[
  {
    "role": "developer",
    "content": [
      {
        "type": "input_text",
        "text": system_message,
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

reasoning_input={
  "summary": "auto"
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

