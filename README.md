# Deep Research Tests

A sandbox project for experimenting with OpenAI's deep research models (o3-deep-research and o4-mini-deep-research). This project provides a framework for conducting structured research using AI models with custom prompts and tools.

## Overview

This project demonstrates how to use OpenAI's deep research capabilities to perform automated research tasks. It includes both basic and advanced research clients that can process complex queries and generate structured outputs with reasoning traces.

## Features

- **Deep Research Integration**: Utilizes OpenAI's o3-deep-research and o4-mini-deep-research models
- **Custom Prompts**: Configurable research prompts and system messages
- **Structured Output**: Generates organized markdown files with research results and reasoning
- **Background Processing**: Supports long-running research tasks with status monitoring
- **Flexible Tools**: Extensible tool configuration for different research scenarios

## Project Structure

```
deepresearch/
├── src/
│   ├── app.py              # Main application entry point
│   ├── basic_client.py     # Basic OpenAI completion client
│   ├── deep_client.py      # Deep research client with advanced features
│   ├── load_env.py         # Environment variable loader
│   └── prompts.py          # Research prompts and system messages
├── output/                 # Generated research outputs
│   ├── output_items.md     # Complete research results
│   └── reasoning.md        # Reasoning trace and analysis
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md              # This file
```

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key with access to deep research models

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
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Basic Usage

Run the main application:
```bash
python src/app.py
```

This will execute the deep research client with the configured prompts.

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

The research generates two main output files:

- **`output/output_items.md`**: Complete research results including all content types (text, web searches, etc.)
- **`output/reasoning.md`**: Detailed reasoning traces showing the model's thought process

## Configuration

### Model Selection

The project supports multiple deep research models:
- `o3-deep-research`: Advanced research model
- `o4-mini-deep-research-2025-06-26`: Lightweight research model

Configure the model in `src/deep_client.py`:
```python
modelo3 = "o3-deep-research"
modelo4 = "o4-mini-deep-research-2025-06-26"
```

### Research Parameters

Key parameters you can adjust:
- **Background processing**: Set `background=True` for long-running tasks
- **Tools**: Configure available research tools in `tools_input`
- **Reasoning**: Customize reasoning prompts for specific research styles

## Development

### Running in Development Mode

For development, install additional dependencies:
```bash
pip install -r requirements-dev.txt
```

### Project Components

- **`app.py`**: Main entry point that orchestrates the research process
- **`deep_client.py`**: Core research functionality with status monitoring
- **`basic_client.py`**: Simple completion client for basic tasks
- **`load_env.py`**: Environment configuration management
- **`prompts.py`**: Research prompt definitions and configurations

## Dependencies

Key dependencies include:
- `openai`: OpenAI API client
- `python-dotenv`: Environment variable management
- `tqdm`: Progress tracking
- `GitPython`: Git integration capabilities

## Examples

### Health Economics Research
```python
system_message = """
You are a professional researcher preparing a structured, data-driven report...
"""
user_query = "Research the economic impact of semaglutide on global healthcare systems."
```

### Creative Research
```python
system_message = "You are a dad joke researcher..."
user_query = "Research dad jokes about nerds."
```

## Output Format

Research results are structured with:
- **Item Types**: Different content categories (reasoning, web_search_call, text)
- **Summaries**: Key findings and insights
- **Status Updates**: Progress tracking throughout the research
- **Source Citations**: References and metadata

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is a sandbox for experimentation and learning purposes.

---

*Last updated: June 30, 2025*
