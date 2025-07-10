# JSON Conversion Modifications

## Summary
Converted the sample dataset from JSONL to JSON format and updated the codebase to support both formats.

## Changes Made
1. Created a new JSON file from the JSONL file: `/data/sample_dataset.json`
2. Modified the `load_dataset` function in `src/azure_evaluator.py` to support both JSONL and JSON formats
3. Updated the README_EVALUATOR.md with information about the new JSON format support and updated all examples to use the JSON file

## Technical Details
- The new `load_dataset` function now checks the file extension to determine whether to load the file as JSON or JSONL
- For JSON files, it expects an array of objects, each with `query`, `generated_text`, and `reference_text` fields
- The JSONL handling remains unchanged, processing one JSON object per line
- All documentation examples have been updated to use the .json extension, but the code still supports both formats
