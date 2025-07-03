# Modifications Summary: Azure Evaluation

## Overview
Added an Azure AI evaluation component that can run as a standalone Python file to assess generative AI outputs using Azure's evaluation metrics.

## Key Components Added

### 1. Azure Evaluator Script
- Created `/src/azure_evaluator.py` - A standalone Python script that:
  - Loads and processes JSONL datasets with query, generated_text, and reference_text fields
  - Configures and runs multiple Azure AI evaluators (quality, similarity, etc.)
  - Generates detailed evaluation reports in JSON and Markdown formats
  - Provides a command-line interface for flexibility and ease of use

### 2. Sample Dataset
- Added `/data/sample_dataset.jsonl` with example entries for testing
- Each entry includes a query, AI-generated text, and reference text for evaluation

### 3. Documentation
- Created `/src/README_EVALUATOR.md` with comprehensive usage instructions
- Includes examples, input format specifications, and output descriptions

### 4. Dependencies
- Added `azure-ai-evaluation==1.9.0` to `requirements.txt`
- This package provides access to Azure's evaluation metrics including:
  - Quality evaluators (Relevance, Coherence, Fluency)
  - Textual similarity evaluators (BLEU, ROUGE, F1, etc.)
  - Other evaluators as needed

## Usage Example
```bash
# Basic usage
python src/azure_evaluator.py --input data/sample_dataset.jsonl

# Specify which metrics to use
python src/azure_evaluator.py --input data/sample_dataset.jsonl --metrics bleu,rouge,meteor

# For AI-assisted metrics, provide Azure OpenAI credentials
python src/azure_evaluator.py --input data/sample_dataset.jsonl --metrics relevance,coherence \
  --model-endpoint "https://your-endpoint.openai.azure.com/" \
  --model-api-key "your-api-key" \
  --model-deployment "your-deployment-name"
```

## Benefits
- Provides quantitative assessment of AI-generated content
- Enables comparison between different models or approaches
- Helps identify strengths and weaknesses in AI outputs
- Runs independently as a standalone tool but integrates with the project structure
