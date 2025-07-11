# Evaluation Configuration

## Summary of Changes
Added a new section in the `.env` file for evaluation configuration parameters.

## Details
Added the following parameters to the `.env` file:

1. `EVAL_MODEL_ENDPOINT` - Using the same Azure OpenAI endpoint as the main configuration
2. `EVAL_MODEL_API_KEY` - Using the same Azure OpenAI API key as the main configuration
3. `EVAL_MODEL_DEPLOYMENT` - Set to "gpt-4o-mini" as the default model for evaluation
4. `EVAL_DEFAULT_METRICS` - Set to "relevance,coherence,fluency,bleu,rouge" for standard evaluation
5. `EVAL_OUTPUT_DIR` - Set to "./output" to match the existing output directory in the project
6. `EVAL_VERBOSE` - Set to "false" by default to minimize console output

These parameters align with the functionality observed in `azure_evaluator.py` and provide default values that can be overridden via command-line arguments when running the evaluator.

## Purpose
This configuration section centralizes the evaluation settings, making it easier to:
- Configure the Azure AI evaluation process without modifying code
- Ensure consistent evaluation parameters across multiple runs
- Quickly adjust settings for different evaluation scenarios

The parameters reflect the options available in the Azure AI Evaluation SDK and match the command-line parameters described in the evaluator's documentation.
