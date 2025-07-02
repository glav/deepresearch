# Example Usage of output_processor

Here's how other modules can use the refactored output processing functionality:

```python
from output_processor import process_response_output
import os

# Example 1: Basic usage
def my_research_function():
    # ... get response from OpenAI ...
    output_dir = "my_output"
    process_response_output(response, output_dir)

# Example 2: With custom model suffix
def azure_research_function():
    # ... get response from Azure OpenAI ...
    output_dir = "/path/to/output"
    process_response_output(response, output_dir, "azure-gpt4")

# Example 3: In a different client module
def batch_research():
    responses = [response1, response2, response3]
    for i, response in enumerate(responses):
        output_dir = f"batch_output/run_{i}"
        process_response_output(response, output_dir, f"batch_{i}")
```

The refactored module provides:
- Clean separation of concerns
- Reusable across different client implementations
- Consistent output formatting
- Easy to test and maintain
- Support for custom filename suffixes
