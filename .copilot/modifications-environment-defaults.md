# Environment Variable Integration for Evaluation

## Summary of Changes
Updated the Azure AI Evaluator to use environment variables from `.env` as defaults when no command-line arguments are provided.

## Details
The following changes were made to ensure that the evaluation configuration in the `.env` file is used as defaults:

1. Added `dotenv` import and initialization to load environment variables at startup
2. Modified the `parse_arguments()` function to use environment variables as defaults:
   - `EVAL_MODEL_ENDPOINT` → `--model-endpoint`
   - `EVAL_MODEL_API_KEY` → `--model-api-key`
   - `EVAL_MODEL_DEPLOYMENT` → `--model-deployment`
   - `EVAL_DEFAULT_METRICS` → `--metrics`
   - `EVAL_OUTPUT_DIR` → Used in output path generation
   - `EVAL_VERBOSE` → `--verbose` flag

3. Updated the `generate_report()` function to use the `EVAL_OUTPUT_DIR` environment variable when determining where to save output files

## Usage Impact
These changes allow users to:
1. Set default configuration in the `.env` file
2. Override defaults via command-line arguments when needed
3. Run the evaluator with minimal arguments while still having proper configuration

For example, instead of:
```bash
python src/azure_evaluator.py --input data/sample_dataset.json --metrics relevance,coherence,fluency --model-endpoint "https://aoai-evaltest.openai.azure.com/" --model-api-key "edeb0c60252941f3806e0b9667afb830" --model-deployment "gpt-4o-mini"
```

Users can now simply run:
```bash
python src/azure_evaluator.py --input data/sample_dataset.json
```

The evaluator will use the values from the `.env` file for all other parameters.
