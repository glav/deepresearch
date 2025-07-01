import os
from openai import OpenAI
from input_parameters import research_input, reasoning_input, tools_input
from time import sleep

def do_research():
  client = OpenAI()

  modelo3 = "o3-deep-research"
  modelo4="o4-mini-deep-research-2025-06-26"

  response = client.responses.create(
    model=modelo3,
    input=research_input,
    reasoning=reasoning_input,
    tools=tools_input,
    background=True
  )

  last_status = ''
  while response.status in {"queued", "in_progress"}:
    if response.status != last_status:
      print(f"Current status: {response.status}")
      last_status = response.status
    sleep(2)
    response = client.responses.retrieve(response.id)

  # Create output directory if it doesn't exist
  output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
  os.makedirs(output_dir, exist_ok=True)

  # Collect all output items
  all_items = []
  reasoning_items = []

  for item in response.output:
    # Add all items to the general list
    all_items.append(f"## Item Type: {item.type}\n")

    if item.type == "reasoning":
      reasoning_items.append(f"## Reasoning Item\n")
      if hasattr(item, 'summary'):
        for s in item.summary:
          all_items.append(f"  - SummaryText: [{s.text}]\n")
          reasoning_items.append(f"  - SummaryText: [{s.text}]\n")
      if hasattr(item, 'status'):
        all_items.append(f"  - Status: [{item.status}]\n")
        reasoning_items.append(f"  - Status: {item.status}\n")
      all_items.append("\n---\n")
      reasoning_items.append("\n---\n")

    elif item.type == "web_search_call":
      if hasattr(item, 'action') and item.action:
          for acts in item.action:
            all_items.append(f"  - {acts}\n")
      all_items.append("\n---\n")

    else:
      # Handle other item types
      if hasattr(item, 'content') and item.content:
        for content in item.content:
          if hasattr(content, 'text'):
            all_items.append(f"  - ContentText: [{content.text}]\n")
      elif hasattr(item, 'text'):
        all_items.append(f"  - ItemText: [{item.text}]\n")
      all_items.append("\n---\n")

  # Write output_items.md
  with open(os.path.join(output_dir, "output_items.md"), "w", encoding="utf-8") as f:
    f.write("# All Output Items\n\n")
    f.writelines(all_items)

  # Write reasoning.md
  with open(os.path.join(output_dir, "reasoning.md"), "w", encoding="utf-8") as f:
    f.write("# Reasoning Items\n\n")
    f.writelines(reasoning_items)

  print(f"Files created in {output_dir}:")
  print("- output_items.md")
  print("- reasoning.md")
