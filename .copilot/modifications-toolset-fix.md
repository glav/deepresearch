# ToolSet Fix Modifications

## Summary
Fixed errors in the `aifoundry_deep_client.py` file related to adding custom function tools to the AI Foundry agent.

## Changes Made

### 1. Fixed ToolSet method call
- **File**: `/workspaces/deepresearch/src/aifoundry_deep_client.py`
- **Issue**: `ToolSet` object was using incorrect method `add_tool()`
- **Fix**: Changed `toolset.add_tool(deep_research_tool)` to `toolset.add(deep_research_tool)`

### 2. Moved enable_auto_function_calls
- **File**: `/workspaces/deepresearch/src/aifoundry_deep_client.py`
- **Issue**: `agents_client.enable_auto_function_calls(toolset)` was called before `agents_client` was defined
- **Fix**: Moved the call inside the context manager where `agents_client` is available

### 3. Updated agent creation
- **File**: `/workspaces/deepresearch/src/aifoundry_deep_client.py`
- **Issue**: Agent was still using `tools=deep_research_tool.definitions` instead of the toolset
- **Fix**: Changed to use `toolset=toolset` parameter and updated description

## Error Resolved
```
AttributeError: 'ToolSet' object has no attribute 'add_tool'. Did you mean: 'get_tool'?
```

## Result
The AI Foundry agent now properly supports both:
- Deep Research tool (for Bing search and research capabilities)
- Custom function tool (with the `analyze_research_data` function)

The agent can now automatically execute both types of tools when needed during conversations.
