# Tool Execution Modifications

## Summary
Enhanced the `wait_for_response` function in `output_processor.py` to handle different types of tool execution during Azure OpenAI responses, including MCP tools and custom function tools.

## Key Insight
**Important Discovery**: MCP tools and custom function tools behave differently from hosted tools:
- **Hosted tools** (like `web_search_preview`): Trigger `"requires_action"` status
- **MCP/Custom tools**: Execute within the response stream while status remains `"in_progress"`

## Changes Made

### Modified `wait_for_response` function
- Added support for `"requires_action"` status for external tool calls
- Added detection of MCP/function tool calls in the output stream during `"in_progress"` status
- Enhanced status monitoring to handle both tool execution patterns
- Updated return type documentation to clarify it returns a tuple

### Added `_check_for_tool_calls_in_output` function
- Detects tool calls within the response output stream
- Looks for MCP tool calls, function calls, and general tool calls
- Provides logging when tool calls are found in the stream

### Added `_handle_tool_execution` function
- Processes responses that require external tool execution (hosted tools)
- Extracts tool calls from the `required_action` attribute
- Coordinates execution of multiple tool calls
- Submits tool outputs back to the Azure OpenAI API

### Added `_execute_tool_call` function
- Routes different tool types to appropriate handlers
- Now supports both `web_search_preview_2025_03_11` and `glavs_custom_search`
- Provides detailed logging of tool execution
- Returns formatted results for submission back to the API

### Added `_execute_custom_search` function
- Handles the custom search function defined in `input_parameters.py`
- Parses `search_term` parameter from arguments
- Returns structured search results
- Placeholder for actual search API integration

### Updated `_execute_web_search` function
- Enhanced to work with different argument formats
- Includes comprehensive error handling

## Tool Types Supported

### 1. Hosted Tools (External Execution)
- Status: `"requires_action"`
- Example: `web_search_preview_2025_03_11`
- Execution: External, requires submission back to API

### 2. MCP Tools (Stream Execution)
- Status: `"in_progress"`
- Type: `"mcp"`
- Execution: Handled by Azure OpenAI internally, appears in output stream

### 3. Custom Function Tools (Stream Execution)
- Status: `"in_progress"`
- Type: `"function"`
- Example: `glavs_custom_search`
- Execution: May require external handling depending on implementation

## Usage
The enhanced `wait_for_response` function now automatically handles both patterns:

1. **For hosted tools**: Detects `"requires_action"` → executes tools → submits results
2. **For MCP/custom tools**: Monitors output stream during `"in_progress"` → logs tool activity

## Future Enhancements
- Implement actual search API integration for `glavs_custom_search`
- Add real-time processing of MCP tool outputs
- Add configuration for different search providers
- Enhance error handling and retry logic for tool failures
- Add support for parallel tool execution
