import sys
import time
from typing import Optional


class TerminalSpinner:
    """
    A simple terminal spinner that displays a rotating character at the same cursor position.
    Useful for indicating progress during long-running operations.
    """

    def __init__(self, spinner_chars: str = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏", message: str = "Processing"):
        """
        Initialize the spinner.

        Args:
            spinner_chars: String of characters to cycle through for the spinner animation
            message: Message to display alongside the spinner
        """
        self.spinner_chars = spinner_chars
        self.message = message
        self.current_index = 0
        self.is_spinning = False
        self._last_output_length = 0

    def update(self, message: Optional[str] = None) -> None:
        """
        Update the spinner to the next character and optionally update the message.

        Args:
            message: Optional new message to display
        """
        if message is not None:
            self.message = message

        # Clear the previous output
        if self._last_output_length > 0:
            sys.stdout.write('\r' + ' ' * self._last_output_length + '\r')

        # Get the current spinner character
        spinner_char = self.spinner_chars[self.current_index]

        # Create the output string
        output = f"{spinner_char} {self.message}"

        # Write the new output
        sys.stdout.write(output)
        sys.stdout.flush()

        # Update tracking variables
        self._last_output_length = len(output)
        self.current_index = (self.current_index + 1) % len(self.spinner_chars)
        self.is_spinning = True

    def stop(self, final_message: Optional[str] = None) -> None:
        """
        Stop the spinner and optionally display a final message.

        Args:
            final_message: Optional final message to display
        """
        if self.is_spinning:
            # Clear the spinner
            if self._last_output_length > 0:
                sys.stdout.write('\r' + ' ' * self._last_output_length + '\r')

            # Display final message if provided
            if final_message:
                sys.stdout.write(final_message + '\n')

            sys.stdout.flush()
            self.is_spinning = False
            self._last_output_length = 0

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically stop the spinner."""
        self.stop()


# Alternative spinner characters for different styles
SPINNER_STYLES = {
    'dots': "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
    'classic': "|/-\\",
    'arrows': "←↖↑↗→↘↓↙",
    'bounce': "⠁⠂⠄⠅⠇⠏⠟⠿⠾⠽⠻⠛⠓⠒⠐⠈",
    'simple': "◐◓◑◒",
    'clock': "🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛",
}


if __name__ == "__main__":
    # Demo of the spinner
    print("Testing spinner styles:")

    for style_name, chars in SPINNER_STYLES.items():
        print(f"\n{style_name.title()} style:")
        spinner = TerminalSpinner(chars, f"Testing {style_name} spinner")

        for i in range(10):
            spinner.update()
            time.sleep(0.2)

        spinner.stop(f"✓ {style_name.title()} spinner complete!")
        time.sleep(0.5)
