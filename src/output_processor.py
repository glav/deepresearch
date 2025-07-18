"""
Output processor module for handling deep research response outputs.

This module provides reusable functionality for processing different types of
output items from OpenAI deep research responses and generating markdown files.
"""

import os
from time import sleep
from datetime import datetime
from terminal_spinner import TerminalSpinner

def wait_for_response(client, response, interval: int = 2) -> any:
    """
    Wait for the response to complete by polling its status.

    Args:
        response: The OpenAI response object to check
        interval: Time in seconds to wait between status checks

    Returns:
        None - The function will block until the response is complete
    """
    start_time = datetime.now()

    last_status = ''
    spinner = TerminalSpinner(message="Research in progress")
    while response.status in {"queued", "in_progress"}:
        if response.status != last_status:
            spinner.update(f"Research in progress - Status: {response.status}")
            last_status = response.status
        else:
            spinner.update()
        sleep(interval)
        response = client.responses.retrieve(response.id)

    end_time = datetime.now()
    total_time = end_time - start_time
    spinner.stop("✓ Deep research complete!")
    print(f"Final status: {response.status}")
    print(f"Status check completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration: {total_time}")
    return response, total_time

def _extract_token_metrics(response) -> str:
    """
    Extract token usage metrics from the OpenAI response object.

    Args:
        response: The OpenAI response object

    Returns:
        String containing formatted token usage information
    """
    token_info = "Token usage not available"

    # Check for common token usage attributes
    if hasattr(response, 'usage') and response.usage:
        usage = response.usage
        if hasattr(usage, 'total_tokens'):
            parts = [f"Total: {usage.total_tokens}"]
            if hasattr(usage, 'prompt_tokens'):
                parts.append(f"Prompt: {usage.prompt_tokens}")
            if hasattr(usage, 'input_tokens'):
                parts.append(f"Input: {usage.input_tokens}")
            if hasattr(usage, 'output_tokens'):
                parts.append(f"Output: {usage.output_tokens}")
            if hasattr(usage, 'completion_tokens'):
                parts.append(f"Completion: {usage.completion_tokens}")
            if hasattr(usage, 'reasoning_tokens'):
                parts.append(f"Reasoning: {usage.reasoning_tokens}")
            token_info = "\n   - ".join(parts) + " tokens"
    elif hasattr(response, 'token_usage'):
        # Alternative token usage structure
        usage = response.token_usage
        if hasattr(usage, 'total'):
            token_info = f"  - Total: {usage.total} tokens"

    return token_info

def process_response_output(response, time_taken, model_suffix: str = "") -> None:
    """
    Process the output from a deep research response and generate a markdown file.

    Args:
        response: The OpenAI response object containing output items
        time_taken: Duration of the response processing
        model_suffix: Optional suffix to add to output filename (e.g., "-o3-model")

    Returns:
        None - File is written to the output directory
    """
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Extract token usage metrics
    token_metrics = _extract_token_metrics(response)

    job_status = "incomplete"
    if response.status not in {"succeeded", "completed"}:
        job_status = f"{response.status}: *{response.error.code}* - {response.error.message}"
    else:
        job_status = f"*{response.status}*"

    # Process all items consistently
    content = _process_all_items(response.output, time_taken, token_metrics, job_status)

    # Write single output file
    filename_suffix = f"-{model_suffix}" if model_suffix else ""
    output_file = os.path.join(output_dir, f"output_items{filename_suffix}.md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"File created: {output_file}")
    print(f"Token usage: {token_metrics}")


def _process_all_items(output_items, time_taken, token_metrics, job_status) -> str:
    """
    Process all output items into a single markdown document.

    Args:
        output_items: Iterable of output items from the response
        time_taken: Duration of the response processing
        token_metrics: String containing formatted token usage information

    Returns:
        String containing the complete markdown content
    """
    content = [f"# All Output Items \n - Job Status: {job_status}\n - Total Time: {time_taken}\n - Token Usage:\n   - {token_metrics}\n\n"]

    for item in output_items:
        content.append(f"## Item Type: {item.type}\n")

        # Process each item type with consistent formatting
        if item.type == "reasoning":
            item_content = _format_reasoning_item(item)
        elif item.type == "web_search_call":
            item_content = _format_web_search_item(item)
        else:
            item_content = _format_general_item(item)

        content.append(item_content)
        content.append("---\n")

    return "".join(content)


def _format_reasoning_item(item) -> str:
    """Format a reasoning item consistently."""
    parts = []

    if hasattr(item, 'summary') and item.summary:
        for summary in item.summary:
            parts.append(f"\n      - Summary: {summary.text}\n")

    if hasattr(item, 'status') and item.status:
        parts.append(f"\n      - Status: {item.status}\n")

    return "".join(parts) if parts else "  - No reasoning content available\n"


def _format_web_search_item(item) -> str:
    """Format a web search item consistently."""
    parts = []

    if hasattr(item, 'action') and item.action:
        for action in item.action:
            parts.append(f"  - Action: {action}\n")

    return "".join(parts) if parts else "  - No search actions available\n"


def _format_general_item(item) -> str:
    """Format any other item type consistently."""
    parts = []

    if hasattr(item, 'content') and item.content:
        for content_item in item.content:
            if hasattr(content_item, 'text'):
                parts.append(f"  - Content: {content_item.text}\n")
    elif hasattr(item, 'text'):
        parts.append(f"  - Text: {item.text}\n")

    return "".join(parts) if parts else "  - No content available\n"
