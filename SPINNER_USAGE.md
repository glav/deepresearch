# Terminal Spinner Usage Examples

## Basic Usage

```python
from terminal_spinner import TerminalSpinner

# Create a spinner with default settings
spinner = TerminalSpinner()

# Update the spinner (call this in your loop)
for i in range(20):
    spinner.update()
    time.sleep(0.1)  # Simulate work

# Stop the spinner
spinner.stop("✓ Operation complete!")
```

## Custom Message and Characters

```python
# Create spinner with custom message and characters
spinner = TerminalSpinner(
    spinner_chars="|/-\\",
    message="Processing data"
)

# Update with dynamic messages
for i in range(10):
    spinner.update(f"Processing item {i+1}/10")
    time.sleep(0.2)

spinner.stop("✓ All items processed!")
```

## Using as Context Manager

```python
# Automatically handles cleanup
with TerminalSpinner("Loading...") as spinner:
    for i in range(15):
        spinner.update()
        time.sleep(0.1)
    # Spinner automatically stops when exiting context
```

## Using Predefined Styles

```python
from terminal_spinner import TerminalSpinner, SPINNER_STYLES

# Use a predefined style
spinner = TerminalSpinner(
    spinner_chars=SPINNER_STYLES['dots'],
    message="Deep thinking"
)

# Or classic style
spinner = TerminalSpinner(
    spinner_chars=SPINNER_STYLES['classic'],
    message="Working"
)
```

## Integration in Deep Research

The spinner is now integrated into the AI Foundry deep research client and will automatically show progress during research operations:

- Shows "Deep research in progress" message
- Updates with current status when it changes
- Displays completion message when finished
- Provides visual feedback during long-running operations

The spinner enhances user experience by providing clear visual indication that the system is actively working on the research task.
