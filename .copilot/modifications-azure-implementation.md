# Azure Implementation Modifications

## Summary
Created an Azure OpenAI implementation in `azure_deep_client.py` that mirrors the functionality of `deep_client.py` but uses Azure OpenAI services instead of standard OpenAI.

## Files Modified
- **Created**: `src/azure_deep_client.py`

## Key Changes and Features

### 1. Azure OpenAI Client Configuration
- Uses `AzureOpenAI` client instead of standard `OpenAI` client
- Requires environment variables:
  - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
  - `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
  - `AZURE_OPENAI_API_VERSION`: API version (defaults to "2024-12-01-preview")

### 2. Environment Loading
- Integrates with existing `load_env()` function to load environment variables
- Includes error handling for missing Azure configuration

### 3. Output File Differentiation
- Creates output files with "azure_" prefix:
  - `azure_output_items.md` instead of `output_items.md`
  - `azure_reasoning.md` instead of `reasoning.md`
- Headers include "Azure OpenAI" prefix for clear identification

### 4. Enhanced Error Handling
- Includes try-catch block for Azure-specific errors
- Provides helpful error messages with configuration requirements
- Lists required environment variables when errors occur

### 5. Status Reporting
- Enhanced status messages include "Azure OpenAI" prefix
- Same polling mechanism as original implementation

### 6. Maintained Functionality
- Identical research processing logic
- Same model support (o3-deep-research, o4-mini-deep-research-2025-06-26)
- Same input parameters (research_input, reasoning_input, tools_input)
- Same output parsing and file generation

## Usage
```python
from azure_deep_client import do_azure_research

# Make sure environment variables are set:
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_API_KEY=your-api-key
# AZURE_OPENAI_API_VERSION=2024-12-01-preview (optional)

do_azure_research()
```

## Dependencies
- Uses existing `azureopenai==0.0.1` package from requirements.txt
- Leverages existing `openai` package's `AzureOpenAI` client
- No additional dependencies required

## Benefits
- Allows using Azure OpenAI instead of standard OpenAI
- Maintains compatibility with existing input parameters and prompts
- Clear separation of outputs for comparison between services
- Robust error handling for Azure-specific configuration issues
