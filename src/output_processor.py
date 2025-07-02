"""
Output processor module for handling deep research response outputs.

This module provides reusable functionality for processing different types of
output items from OpenAI deep research responses and generating markdown files.
"""

import os
from typing import List, Tuple
from time import sleep

def wait_for_response(client, response, interval: int = 2) -> any:
    """
    Wait for the response to complete by polling its status.

    Args:
        response: The OpenAI response object to check
        interval: Time in seconds to wait between status checks

    Returns:
        None - The function will block until the response is complete
    """
    last_status = ''
    while response.status in {"queued", "in_progress"}:
        if response.status != last_status:
            print(f"Current status: {response.status}")
            last_status = response.status
        sleep(interval)
        response = client.responses.retrieve(response.id)
    print(f"Final status: {response.status}")
    return response

def process_response_output(response, model_suffix: str = "") -> None:
    """
    Process the output from a deep research response and generate markdown files.

    Args:
        response: The OpenAI response object containing output items
        output_dir: Directory path where output files will be created
        model_suffix: Optional suffix to add to output filenames (e.g., "-o3-model")

    Returns:
        None - Files are written to the output directory
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Collect all output items
    all_items, reasoning_items = _collect_output_items(response.output)

    # Write output files
    _write_output_files(output_dir, all_items, reasoning_items, model_suffix)

    # Print confirmation
    filename_suffix = f"-{model_suffix}" if model_suffix else ""
    print(f"Files created in {output_dir}:")
    print(f"- output_items{filename_suffix}.md")
    print(f"- reasoning{filename_suffix}.md")


def _collect_output_items(output_items) -> Tuple[List[str], List[str]]:
    """
    Collect and format output items into markdown content.

    Args:
        output_items: Iterable of output items from the response

    Returns:
        Tuple of (all_items, reasoning_items) as lists of markdown strings
    """
    all_items = []
    reasoning_items = []

    for item in output_items:
        # Add all items to the general list
        all_items.append(f"## Item Type: {item.type}\n")

        if item.type == "reasoning":
            reasoning_content = _process_reasoning_item(item)
            all_items.extend(reasoning_content)
            reasoning_items.append(f"## Reasoning Item\n")
            reasoning_items.extend(reasoning_content[1:])  # Skip the type header for reasoning file

        elif item.type == "web_search_call":
            web_search_content = _process_web_search_item(item)
            all_items.extend(web_search_content)

        else:
            other_content = _process_other_item(item)
            all_items.extend(other_content)

    return all_items, reasoning_items


def _process_reasoning_item(item) -> List[str]:
    """Process a reasoning type item and return formatted content."""
    content = []

    if hasattr(item, 'summary') and item.summary:
        for s in item.summary:
            content.append(f"  - SummaryText: [{s.text}]\n")

    if hasattr(item, 'status'):
        content.append(f"  - Status: [{item.status}]\n")

    content.append("\n---\n")
    return content


def _process_web_search_item(item) -> List[str]:
    """Process a web_search_call type item and return formatted content."""
    content = []

    if hasattr(item, 'action') and item.action:
        for acts in item.action:
            content.append(f"  - {acts}\n")

    content.append("\n---\n")
    return content


def _process_other_item(item) -> List[str]:
    """Process other types of items and return formatted content."""
    content = []

    if hasattr(item, 'content') and item.content:
        for content_item in item.content:
            if hasattr(content_item, 'text'):
                content.append(f"  - ContentText: [{content_item.text}]\n")
    elif hasattr(item, 'text'):
        content.append(f"  - ItemText: [{item.text}]\n")

    content.append("\n---\n")
    return content


def _write_output_files(output_dir: str, all_items: List[str], reasoning_items: List[str], model_suffix: str) -> None:
    """Write the collected items to markdown files."""
    filename_suffix = f"-{model_suffix}" if model_suffix else ""

    # Write output_items.md
    output_items_file = os.path.join(output_dir, f"output_items{filename_suffix}.md")
    with open(output_items_file, "w", encoding="utf-8") as f:
        f.write("# All Output Items\n\n")
        f.writelines(all_items)

    # Write reasoning.md
    reasoning_file = os.path.join(output_dir, f"reasoning{filename_suffix}.md")
    with open(reasoning_file, "w", encoding="utf-8") as f:
        f.write("# Reasoning Items\n\n")
        f.writelines(reasoning_items)
