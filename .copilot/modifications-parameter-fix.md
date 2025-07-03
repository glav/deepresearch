# Azure Evaluation Parameter Fix

## Error Fixed

Fixed an error related to Azure OpenAI API parameter compatibility:

```
Error code: 400 - {'error': {'message': "Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.", 'type': 'invalid_request_error', 'param': 'max_tokens', 'code': 'unsupported_parameter'}}
```

## Changes Made

1. Updated the `configure_evaluators` function to accept either a dictionary or an `AzureOpenAIModelConfiguration` object.
   - Modified the type hint from `Optional[Dict[str, str]]` to `Optional[Union[Dict[str, str], AzureOpenAIModelConfiguration]]`
   - Updated function documentation to reflect this change

2. Changed how the model configuration is created in the `main` function:
   - Replaced the dictionary construction with an `AzureOpenAIModelConfiguration` object
   - This ensures proper parameter compatibility with the latest Azure OpenAI API

## Why This Fixes The Issue

The Azure AI evaluation library has been updated to use newer Azure OpenAI API parameters, specifically replacing `max_tokens` with `max_completion_tokens`. By using the `AzureOpenAIModelConfiguration` class from the library instead of a raw dictionary, we ensure that the correct parameters are used when making API requests, regardless of API version.

The `AzureOpenAIModelConfiguration` class handles parameter mapping and compatibility automatically, so we don't need to worry about which specific parameters are supported in different API versions.

## Additional Notes

If you encounter similar errors in the future, check the Azure OpenAI API documentation for the latest parameter requirements and ensure that the Azure AI evaluation library is up to date:

```bash
pip install --upgrade azure-ai-evaluation
```
