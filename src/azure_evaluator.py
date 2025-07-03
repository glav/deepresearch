#!/usr/bin/env python
"""
Azure AI Evaluation Component

This standalone script evaluates generative AI outputs using Azure AI evaluation metrics.
It processes JSONL files where each line is a JSON document with the structure:
{query: text, generated_text: text, reference_text: text}
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dotenv import load_dotenv
from azure.ai.evaluation import AzureOpenAIModelConfiguration

try:
    from azure.ai.evaluation import (
        evaluate,
        RelevanceEvaluator,
        CoherenceEvaluator,
        FluencyEvaluator,
        GroundednessEvaluator,
        BleuScoreEvaluator,
        RougeScoreEvaluator,
        F1ScoreEvaluator,
        GleuScoreEvaluator,
        MeteorScoreEvaluator,
        SimilarityEvaluator
    )
except ImportError:
    print("Error: azure-ai-evaluation package is not installed.")
    print("Please install it with: pip install azure-ai-evaluation")
    sys.exit(1)

# Load environment variables from .env file
def load_env():
    """Locate and load .env file, returning load status."""
    dotenv_path = None
    for path in [".env", "../.env"]:
        if os.path.exists(path):
            dotenv_path = path
            break
    env_loaded = load_dotenv(dotenv_path=dotenv_path, override=True)
    return env_loaded

# Load environment variables
load_env()

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Evaluate generative AI outputs using Azure AI evaluation metrics.")

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input JSONL file with query, generated_text, and reference_text fields"
    )

    # Get default output directory from environment variable
    default_output_dir = os.getenv("EVAL_OUTPUT_DIR", "./output")
    parser.add_argument(
        "--output",
        default=None,
        help=f"Path to save the evaluation results (default: creates a timestamped file in {default_output_dir}/)"
    )

    # Get default metrics from environment variable
    default_metrics = os.getenv("EVAL_DEFAULT_METRICS", "relevance,coherence,fluency,bleu,rouge")
    parser.add_argument(
        "--metrics",
        default=default_metrics,
        help=f"Comma-separated list of metrics to evaluate (default: {default_metrics})"
    )

    # Get default model endpoint from environment variable
    default_endpoint = os.getenv("EVAL_MODEL_ENDPOINT", None)
    parser.add_argument(
        "--model-endpoint",
        default=default_endpoint,
        help="Azure OpenAI endpoint for AI-assisted evaluators (required for relevance, coherence, fluency, etc.)"
    )

    # Get default model API key from environment variable
    default_api_key = os.getenv("EVAL_MODEL_API_KEY", None)
    parser.add_argument(
        "--model-api-key",
        default=default_api_key,
        help="Azure OpenAI API key for AI-assisted evaluators"
    )

    # Get default model deployment from environment variable
    default_deployment = os.getenv("EVAL_MODEL_DEPLOYMENT", None)
    parser.add_argument(
        "--model-deployment",
        default=default_deployment,
        help="Azure OpenAI deployment name for AI-assisted evaluators"
    )


    # Get default model api version from environment variable
    default_azure_api_version = os.getenv("EVAL_OPEN_AI_VERSION", None)
    parser.add_argument(
        "--api-version",
        default=default_azure_api_version,
        help="Azure OpenAI API version for AI-assisted evaluators (optional, defaults to latest if not set)"
    )
    # Get default verbose setting from environment variable
    default_verbose = os.getenv("EVAL_VERBOSE", "false").lower() == "true"
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=default_verbose,
        help="Enable verbose output"
    )

    return parser.parse_args()

def load_dataset(file_path: str) -> List[Dict[str, str]]:
    """
    Load and validate the dataset from either JSON or JSONL format.

    Args:
        file_path: Path to the JSON or JSONL file

    Returns:
        List of dictionaries containing query, generated_text, and reference_text
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    dataset = []

    try:
        # Determine file format based on extension
        if file_path.lower().endswith('.json'):
            # Handle JSON (array) format
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                if not isinstance(data, list):
                    raise ValueError("JSON file must contain an array of objects")

                for index, item in enumerate(data):
                    # Verify required fields are present
                    required_fields = ['query', 'generated_text', 'reference_text']
                    missing_fields = [field for field in required_fields if field not in item]

                    if missing_fields:
                        print(f"Warning: Item {index+1} is missing required fields: {', '.join(missing_fields)}")
                        continue

                    dataset.append(item)
        else:
            # Handle JSONL format (default)
            line_number = 0
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line_number += 1
                    if not line.strip():
                        continue

                    try:
                        item = json.loads(line)

                        # Verify required fields are present
                        required_fields = ['query', 'generated_text', 'reference_text']
                        missing_fields = [field for field in required_fields if field not in item]

                        if missing_fields:
                            print(f"Warning: Line {line_number} is missing required fields: {', '.join(missing_fields)}")
                            continue

                        dataset.append(item)
                    except json.JSONDecodeError:
                        print(f"Warning: Line {line_number} is not valid JSON and will be skipped")

    except Exception as e:
        raise RuntimeError(f"Error reading the input file: {str(e)}")

    if not dataset:
        raise ValueError("No valid data found in the input file")

    return dataset

def configure_evaluators(metrics: List[str], model_config: Optional[Union[Dict[str, str], AzureOpenAIModelConfiguration]] = None) -> Dict[str, Any]:
    """
    Configure the evaluators based on the requested metrics.

    Args:
        metrics: List of metric names to configure
        model_config: Configuration for AI-assisted evaluators, either as AzureOpenAIModelConfiguration or dict (optional)

    Returns:
        Dictionary of configured evaluators
    """
    evaluators = {}

    # Define which evaluators need the model configuration
    ai_assisted_evaluators = {
        'relevance': RelevanceEvaluator,
        'coherence': CoherenceEvaluator,
        'fluency': FluencyEvaluator,
        'groundedness': GroundednessEvaluator,
        'similarity': SimilarityEvaluator
    }

    # Define NLP-based evaluators (don't need model config)
    nlp_evaluators = {
        'bleu': BleuScoreEvaluator,
        'rouge': RougeScoreEvaluator,
        'f1': F1ScoreEvaluator,
        'gleu': GleuScoreEvaluator,
        'meteor': MeteorScoreEvaluator
    }

    # Configure requested evaluators
    for metric in metrics:
        metric = metric.lower().strip()

        if metric in ai_assisted_evaluators:
            if not model_config:
                print(f"Warning: Skipping {metric} evaluator as no model configuration provided")
                continue

            evaluators[metric] = ai_assisted_evaluators[metric](model_config)

        elif metric in nlp_evaluators:
            evaluators[metric] = nlp_evaluators[metric]()

        else:
            print(f"Warning: Unknown evaluator '{metric}' will be skipped")

    return evaluators

def run_evaluation(dataset: List[Dict[str, str]], evaluators: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Execute the evaluations on the dataset.

    Args:
        dataset: List of dictionaries containing query, generated_text, and reference_text
        evaluators: Dictionary of configured evaluators
        verbose: Whether to print verbose output

    Returns:
        Evaluation results
    """
    # Convert dataset to the format expected by the evaluate function
    jsonl_data = []
    for item in dataset:
        jsonl_data.append({
            "query": item["query"],
            "response": item["generated_text"],
            "ground_truth": item["reference_text"],
            "line_number": item.get("line_number")
        })

    # Create a temporary JSONL file for evaluate function
    temp_jsonl_path = "temp_dataset.jsonl"
    with open(temp_jsonl_path, 'w', encoding='utf-8') as f:
        for item in jsonl_data:
            f.write(json.dumps(item) + '\n')

    if verbose:
        print(f"Running evaluation with {len(evaluators)} evaluators on {len(dataset)} examples...")

    start_time = time.time()

    # Configure column mapping for each evaluator
    evaluator_config = {}
    for evaluator_name in evaluators:
        if evaluator_name in ["fluency"]:
            # Fluency only needs response
            evaluator_config[evaluator_name] = {
                "column_mapping": {
                    "response": "${data.response}",
                }
            }
        elif evaluator_name in ["bleu", "rouge", "f1", "gleu", "meteor", "similarity"]:
            # These need response and ground_truth
            evaluator_config[evaluator_name] = {
                "column_mapping": {
                    "response": "${data.response}",
                    "ground_truth": "${data.ground_truth}"
                }
            }
        else:
            # Most evaluators need query, response, and sometimes ground_truth
            evaluator_config[evaluator_name] = {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}",
                    "ground_truth": "${data.ground_truth}"
                }
            }
        evaluator_config[evaluator_name]["column_mapping"]["line_number"] = "${data.line_number}"

    try:
        # Run the evaluation
        results = evaluate(
            data=temp_jsonl_path,
            evaluators=evaluators,
            evaluator_config=evaluator_config,
            output_path="temp_results.json" if verbose else None
        )

        # Clean up the temporary file
        if os.path.exists(temp_jsonl_path):
            os.remove(temp_jsonl_path)

        if verbose:
            print(f"Evaluation completed in {time.time() - start_time:.2f} seconds")

        return results

    except Exception as e:
        print(f"Error during evaluation: {str(e)}")
        # Clean up the temporary file
        if os.path.exists(temp_jsonl_path):
            os.remove(temp_jsonl_path)
        raise

def generate_report(results: Dict[str, Any], metrics: list[str], output_path: Optional[str] = None) -> str:
    """
    Generate a report from the evaluation results.

    Args:
        results: Evaluation results
        output_path: Path to save the report (optional)

    Returns:
        Path to the saved report
    """
    # Create output directory if it doesn't exist
    if not output_path:
        # Use the output directory from environment variable if available
        output_dir = os.getenv("EVAL_OUTPUT_DIR", "./output")
        # Make sure the path is absolute
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), output_dir.lstrip("./"))

        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"evaluation_results_{timestamp}.json")

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Save the full results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Also create a markdown summary
    md_path = os.path.splitext(output_path)[0] + ".md"

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Azure AI Evaluation Results\n\n")
        f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

        f.write("## Summary\n\n")
        f.write("|Line Number| Metric | Value |\n")
        f.write("|--------|--------|-------|\n")

        # Extract and write the aggregate metrics

        for row in results['rows']:
            line_number = row.get('inputs.line_number', 'None')

            for metric_category in metrics:
                binary_result = "N/A"

                for item, value in row.items():
                    metric_name = None
                    metric_valeu = "N/A"

                    if item.startswith(f"outputs.{metric_category}.") or item.endswith("_result"):
                        metric_name = item

                        if isinstance(value, (int, float)):
                            metric_valeu = f"{value:.4f}"
                        else:
                            metric_valeu = str(value)

                    if metric_name is not None:
                        f.write(f"| {line_number} | {metric_name} | {metric_valeu} \n")

        f.write("\n## Detailed Results\n\n")
        f.write("Detailed results are available in the JSON file.\n")

    return output_path

def main():
    """Main function to orchestrate the evaluation process."""
    args = parse_arguments()

    try:
        # Load the dataset
        if args.verbose:
            print(f"Loading dataset from {args.input}...")

        dataset = load_dataset(args.input)

        if args.verbose:
            print(f"Loaded {len(dataset)} examples from the dataset")

        # Configure model for AI-assisted evaluators
        model_config = None
        if args.model_endpoint and args.model_api_key and args.model_deployment:
            model_config = AzureOpenAIModelConfiguration(
                azure_endpoint=args.model_endpoint,
                api_key=args.model_api_key,
                azure_deployment=args.model_deployment,
                api_version=args.api_version
            )

        # Configure evaluators
        metrics = [m.strip() for m in args.metrics.split(',')]

        if args.verbose:
            print(f"Configuring evaluators: {', '.join(metrics)}")

        evaluators = configure_evaluators(metrics, model_config)

        if not evaluators:
            print("Error: No valid evaluators configured. Exiting.")
            return 1

        # Run evaluation
        results = run_evaluation(dataset, evaluators, args.verbose)

        # Generate report
        report_path = generate_report(results, metrics, args.output)

        print(f"\nEvaluation complete!")
        print(f"Results saved to: {report_path}")
        print(f"Markdown summary: {os.path.splitext(report_path)[0] + '.md'}")

        # Print summary to console
        print("\nSummary of results:")

        for metric_name, metric_value in results['metrics'].items():
            if not metric_name.endswith("_binary_aggregate") and not metric_name.endswith("_reason"):
                if isinstance(metric_value, (int, float)):
                    print(f"  {metric_name}: {metric_value:.4f}")
                else:
                    print(f"  {metric_name}: {metric_value}")

        return 0

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
