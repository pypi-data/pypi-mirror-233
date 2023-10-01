# slowPaste

Simulate human-like typing using Python with the added feature of adjustable speed.

## Features:
- Simulates slow typing to mimic human input.
- Adjustable typing speed in Words Per Minute (WPM).
- Cancel typing mid-way with the `esc` key.
- PyAutoGUI fail-safe: Move your cursor to the top-left corner to halt the script immediately.
- Types out content from your clipboard.

## Installation:

You can install slowPaste directly from GitHub using pip:

```bash
pip install slowPaste
```

## Usage:

1. **Install the Package**: Install the slowPaste package using pip.
2. **Copy Text**: Copy the text you want to be typed out to the clipboard.
3. **Run the Script with Desired Speed**: Run the script using a Python interpreter and specify the desired typing speed in WPM.
   ```python
   from slowPaste import slow_paste
   slow_paste.main(100)  # Replace 100 with your desired speed in WPM
   ```
4. **Focus on Input Field**: After running the script, focus on the input field (e.g., text editor, browser) where you want the text to be typed.
5. **Start Typing**: The script will begin typing out the content from the clipboard after a delay of 2 seconds.

## Adjusting Speed & Text Input:

- The main function accepts a speed parameter representing the typing speed in Words Per Minute (WPM). The default value is 100 WPM. It also accepts an optional text parameter for manual input, with the default being the content currently copied to the clipboard.
- You can adjust it by passing the desired speed value and text string when calling the main function.
  ```python
  slow_paste.main(150, text="Hello, world!")  # Types the provided text at 150 WPM. If text is not provided, it types the clipboard content.
  ```

## Script Breakdown:
- `slow_paste()`: The main function that slowly types out the text. It accepts a speed parameter to adjust the typing speed.
- `main()`: Reads the clipboard content and initiates the typing, it also accepts a speed parameter.

## Safety:
- Move the cursor to the top-left corner of the screen to trigger PyAutoGUI's fail-safe and halt the script.

## Contributing:
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License:
[MIT](https://choosealicense.com/licenses/mit/)