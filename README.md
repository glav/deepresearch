# Deep Research Tests

A comprehensive multi-provider research platform for experimenting with advanced AI research models. This project provides a unified framework for conducting structured research using multiple AI providers including OpenAI, Azure OpenAI, and Azure AI Foundry, with built-in evaluation capabilities.

## Overview

This project demonstrates how to use advanced AI research capabilities across multiple providers to perform automated research tasks. It includes multiple research clients, an evaluation system, and modular components that can process complex queries and generate structured outputs with reasoning traces.

## Features

- **Multi-Provider Support**: Integrates with OpenAI, Azure OpenAI, and Azure AI Foundry research models
- **Advanced Model Support**: Utilizes o3-deep-research, o4-mini-deep-research, and Azure model variants
- **AI Output Evaluation**: Built-in Azure AI evaluation system for assessing research quality
- **Custom Prompts**: Configurable research prompts and system messages for different research scenarios
- **Structured Output**: Generates organized markdown files with research results and reasoning traces
- **Background Processing**: Supports long-running research tasks with real-time status monitoring
- **Modular Architecture**: Reusable components for output processing and client management
- **Flexible Tools**: Extensible tool configuration for different research scenarios

## Project Structure

```
deepresearch/
├── src/
│   ├── app.py                    # Main application entry point
│   ├── basic_client.py           # Basic OpenAI completion client
│   ├── openai_deep_client.py     # OpenAI deep research client
│   ├── azure_deep_client.py      # Azure OpenAI deep research client
│   ├── aifoundry_deep_client.py  # Azure AI Foundry research client
│   ├── azure_evaluator.py        # Azure AI evaluation component
│   ├── output_processor.py       # Reusable output processing module
│   ├── terminal_spinner.py       # Terminal progress indicators
│   ├── models.py                 # Model configurations and mappings
│   ├── input_parameters.py       # Research input parameter definitions
│   ├── load_env.py               # Environment variable loader
│   ├── prompts.py                # Research prompts and system messages
│   └── README_EVALUATOR.md       # Azure evaluator documentation
├── experiments/                  # Research experiment results
│   └── experiment-1/             # Sample experiment outputs
├── output/                       # Generated research outputs
│   ├── output_items*.md          # Complete research results by provider
│   └── reasoning*.md             # Reasoning traces and analysis
├── data/                         # Sample datasets and test data
│   └── sample_dataset.json       # Sample evaluation dataset
├── .copilot/                     # Project modification documentation
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
└── README.md                     # This file
```

## Setup

### Prerequisites

- Python 3.8+
- API access to one or more of the following:
  - OpenAI API key with access to deep research models
  - Azure OpenAI endpoint and API key
  - Azure AI Foundry project endpoint and credentials

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd deepresearch
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the relevant provider credentials:

   **For OpenAI:**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   **For Azure OpenAI:**
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your_azure_api_key_here
   AZURE_OPENAI_API_VERSION=2024-12-01-preview
   ```

   **For Azure AI Foundry:**
   ```env
   PROJECT_ENDPOINT=your_project_endpoint
   BING_RESOURCE_NAME=your_bing_connection_name
   MODEL_DEPLOYMENT_NAME=your_model_deployment
   DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME=your_deep_research_model
   ```

## Usage

### Basic Usage

Run the main application:
```bash
python src/app.py
```

This will execute the configured research client. By default, it runs Azure OpenAI research, but you can modify `src/app.py` to use different providers:

```python
# Choose your research provider:
do_openai_research(prompts.example_system_message, prompts.example_user_query)     # OpenAI
do_azure_research(prompts.example_system_message, prompts.example_user_query)      # Azure OpenAI
do_aifoundry_research(prompts.example_system_message, prompts.example_user_query)  # Azure AI Foundry
```

### Provider-Specific Usage

**OpenAI Deep Research:**
```bash
# Modify app.py to uncomment the OpenAI client
python src/openai_deep_client.py
```

**Azure OpenAI Research:**
```bash
# Modify app.py to uncomment the Azure client
python src/azure_deep_client.py
```

**Azure AI Foundry Research:**
```bash
# Modify app.py to uncomment the AI Foundry client
python src/aifoundry_deep_client.py
```

### AI Output Evaluation

Evaluate the quality of generated research using the Azure AI evaluation component:

```bash
# Basic evaluation
python src/azure_evaluator.py --input data/sample_dataset.json

# Specify evaluation metrics
python src/azure_evaluator.py --input data/sample_dataset.json --metrics relevance,coherence,bleu

# Use AI-assisted metrics (requires Azure OpenAI)
python src/azure_evaluator.py --input data/sample_dataset.json --metrics relevance,coherence \
  --model-endpoint "https://your-endpoint.openai.azure.com/" \
  --model-api-key "your-api-key" \
  --model-deployment "your-deployment-name"
```

See `src/README_EVALUATOR.md` for detailed evaluation documentation.

### Customizing Research

1. **Modify prompts**: Edit `src/prompts.py` to change the research focus:
   - `system_message`: Define the research assistant's role and behavior
   - `user_query`: Specify the research question or topic
   - `tools_input`: Configure available tools for the research

2. **Example prompt configurations**:
   ```python
   # Health economics research
   system_message = "You are a professional researcher preparing a structured, data-driven report..."
   user_query = "Research the economic impact of semaglutide on global healthcare systems."

   # Creative research
   system_message = "You are a dad joke researcher..."
   user_query = "Research dad jokes about nerds."
   ```

### Understanding Output

The research generates provider-specific output files in the `output/` directory:

**OpenAI Research Output:**
- **`output_items_openai_[model_name].md`**: Complete research results including all content types
- **`reasoning_openai_[model_name].md`**: Detailed reasoning traces showing the model's thought process

**Azure OpenAI Research Output:**
- **`output_items_azure_[model_name].md`**: Complete Azure research results
- **`reasoning_azure_[model_name].md`**: Azure reasoning traces

**Azure AI Foundry Research Output:**
- **`output_items_aifoundry_o3_deep_research.md`**: AI Foundry research results with token usage metrics

**Evaluation Output:**
- **`evaluation_results_[timestamp].json`**: Detailed evaluation metrics in JSON format
- **`evaluation_report_[timestamp].md`**: Human-readable evaluation report

Each output file includes comprehensive metadata, token usage statistics, and execution timing information.

## Configuration

### Model Selection

The project supports multiple research models across different providers:

**OpenAI Models:**
- `o3-deep-research`: Advanced research model with comprehensive capabilities
- `o4-mini-deep-research-2025-06-26`: Lightweight research model for faster execution

**Azure OpenAI Models:**
- `o3-mini`: Fast, efficient model for quick research tasks
- `o3-pro`: Professional-grade model with enhanced capabilities
- `o4-mini`: Latest generation lightweight model

**Azure AI Foundry Models:**
- Configurable deep research models with Bing integration
- Custom model deployments based on your AI Foundry setup

Configure the model in the respective client files:
```python
# In openai_deep_client.py
model = OPENAI_03  # or OPENAI_04_MINI

# In azure_deep_client.py
model = AZURE_03_MINI  # or AZURE_03_PRO, AZURE_04_MINI

# In aifoundry_deep_client.py
# Model configured via environment variables
```

### Research Parameters

Key parameters you can adjust across all providers:
- **Background processing**: Set `background=True` for long-running tasks
- **Tools**: Configure available research tools (varies by provider)
- **Reasoning**: Customize reasoning prompts for specific research styles
- **Model selection**: Choose appropriate model for your use case and performance needs

## Development

### Running in Development Mode

For development, install additional dependencies:
```bash
pip install -r requirements-dev.txt
```

### Project Components

- **`app.py`**: Main entry point that orchestrates the research process across providers
- **`openai_deep_client.py`**: OpenAI deep research client with response processing
- **`azure_deep_client.py`**: Azure OpenAI research client with Azure-specific configurations
- **`aifoundry_deep_client.py`**: Azure AI Foundry client with agent-based research
- **`azure_evaluator.py`**: Standalone evaluation component for AI output assessment
- **`output_processor.py`**: Reusable module for processing and formatting research outputs
- **`terminal_spinner.py`**: Progress indicators for long-running research tasks
- **`models.py`**: Model configurations and provider mappings
- **`basic_client.py`**: Simple completion client for basic tasks
- **`load_env.py`**: Environment configuration management
- **`prompts.py`**: Research prompt definitions and configurations
- **`input_parameters.py`**: Parameter definitions for research inputs

## Dependencies

Key dependencies include:
- **Core Libraries:**
  - `openai`: OpenAI API client for OpenAI and Azure OpenAI services
  - `azure-ai-projects`: Azure AI Foundry project integration
  - `azure-ai-agents`: Azure AI agent framework for foundry clients
  - `azure-ai-evaluation`: Azure AI evaluation metrics and tools
  - `azure-identity`: Azure authentication and credential management
- **Utilities:**
  - `python-dotenv`: Environment variable management
  - `tqdm`: Progress tracking for research operations
  - `GitPython`: Git integration capabilities
- **Development:**
  - Additional packages in `requirements-dev.txt` for development workflows

## Examples

### Multi-Provider Research Comparison
```python
# Health economics research across providers
system_message = """
You are a professional researcher preparing a structured, data-driven report...
"""
user_query = "Research the economic impact of semaglutide on global healthcare systems."

# Run the same research across different providers for comparison
do_openai_research(system_message, user_query)
do_azure_research(system_message, user_query)
do_aifoundry_research(system_message, user_query)
```

### Specialized Research Scenarios
```python
# Environmental research with EPA focus
deep_research_epa_system_prompt = """
You are an AI agent that assists in deep research experiments based on
Environmental Protection Authority information and documentation...
"""
epa_query = "Are there any Proposal Elements with Greenhouse Gas Emissions
that involve electricity generation for Hope Downs?"

# Creative research
dadjoke_system_message = "You are a dad joke researcher..."
dadjoke_user_query = "Research dad jokes about nerds."
```

## Output Format

Research results are structured with comprehensive metadata and multiple content types:

### Content Types by Provider
- **OpenAI/Azure OpenAI**: Text responses, web searches, reasoning traces, code interpreter calls
- **Azure AI Foundry**: Agent responses, URL citations, deep research tool outputs
- **All Providers**: Token usage metrics, execution timing, status updates

### Output Structure
- **Item Types**: Different content categories (reasoning, web_search_call, text, code_interpreter_call)
- **Summaries**: Key findings and insights with structured data presentation
- **Status Updates**: Real-time progress tracking throughout the research process
- **Source Citations**: References, URLs, and metadata for all retrieved information
- **Performance Metrics**: Token usage, execution time, and provider-specific statistics

### Evaluation Metrics
When using the Azure evaluator component:
- **Quality Metrics**: Relevance, Coherence, Fluency scores
- **Similarity Metrics**: BLEU, ROUGE, F1, METEOR scores
- **Custom Metrics**: Configurable evaluation criteria based on research needs

## Experiments

The `experiments/` directory contains sample research runs demonstrating:
- **experiment-1/**: Comparative outputs across OpenAI models (o3, o4-mini) showing different research approaches
- Provider-specific output formats and reasoning patterns
- Performance comparisons between model variants
- Real-world research scenarios with actual data and citations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly across multiple providers
5. Update documentation as needed
6. Submit a pull request

When contributing:
- Test changes with multiple AI providers when applicable
- Update the `.copilot/` documentation for significant modifications
- Follow the existing code patterns for new client implementations
- Ensure new features work with the modular output processing system

## License

This project is a sandbox for experimentation and learning purposes with advanced AI research capabilities.

---

*Last updated: July 11, 2025*
