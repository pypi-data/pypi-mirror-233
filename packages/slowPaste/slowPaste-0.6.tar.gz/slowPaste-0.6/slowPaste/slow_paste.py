import pyperclip
import pyautogui
import time
import random
import keyboard

def slow_type(text, speed=100): # Speed in WPM
    """
    Types out the given text slowly, simulating manual keyboard input.
    """
    for char in text:
        if keyboard.is_pressed('esc'):
            print("Typing canceled!")
            return

        # Calculate delay
        delay = 60.0 / (5 * speed)

        # Adjust delay by a random factor within ±20% 
        adjusted_delay = delay * random.uniform(0.8, 1.2)

        pyautogui.write(char)
        time.sleep(adjusted_delay)

def main(speed=100,text=""):
    time.sleep(2)
    # Enable pyautogui's fail-safe # 
    pyautogui.FAILSAFE = True

    # Get the current clipboard content
    if text=="":
        text = pyperclip.paste()
    try:
        # Type it out slowly
        slow_type(text, speed)
    except pyautogui.FailSafeException:
        print("Script halted due to escape mechanism (cursor in top-left corner).")

if __name__ == "__main__":
    main()

