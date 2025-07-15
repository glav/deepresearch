# Azure AI Agents Tools Fix

## Summary
Fixed the error "'tools' must be an array of objects" in the Azure AI Foundry client by correcting how tool definitions are handled when using the `tools` parameter approach.

## Problem
The application was failing with the error:
```
azure.core.exceptions.HttpResponseError: (UserError) 'tools' must be an array of objects
Code: UserError
Message: 'tools' must be an array of objects
```

## Root Cause
The issue was in how tool definitions were being collected and passed to the `create_agent()` method. The code was trying to use `self.deep_research_tool.definitions` but wasn't properly handling the format expected by the `tools` parameter.

## Changes Made

### 1. AIFoundryClientHelper (`src/AIFoundry/aifoundry_client_helper.py`)
- Removed the ToolSet approach and reverted to using `tool_definitions` list
- Updated `add_deep_research_tool()` method to properly extract definitions from the DeepResearchTool
- Added error handling for cases where tool definitions might not be available
- Updated `add_document_city_function_tool()` to use the tool definition creation function

### 2. AIFoundry Deep Client (`src/AIFoundry/aifoundry_deep_client.py`)
- Updated to use the `tools` parameter instead of `toolset` when creating the agent
- Removed the `enable_auto_function_calls()` call which was not compatible with the tools approach

## Result
The agent creation now works correctly and the Deep Research tool is properly attached. The application successfully starts processing requests as evidenced by the "Deep research in progress" status messages.

## Technical Details
The fix ensures that:
- `self.deep_research_tool.definitions` is properly extracted and added to `tool_definitions`
- Tool definitions are passed as a list to the `tools` parameter
- The format matches Azure AI Agents expectations for tool definition objects
