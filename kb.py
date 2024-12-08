import json
import keyboard
import pyautogui
import tkinter as tk
import re
import time
import pyperclip


last_users_buffer_value = None


def load_languages():
    # Load language mappings from a JSON file
    with open('languages.json', 'r', encoding='utf-8') as file:
        uk_to_en = json.load(file)
    return uk_to_en["uk_to_en"]

def change_text(coppied_text, mapping):
    # Define regex for special characters
    special_chars = re.compile(r"[!@#$%^&*()_+{}\[\]:;<>,.?~\\/]")
    
    correct = ""
    for letter in coppied_text:
        if special_chars.match(letter):
            correct += letter
        elif letter == ' ':
            correct += ' '
        else:
            correct += mapping.get(letter, letter)  # Use get to handle characters not in the map
    return correct

def copy_text():
    global last_users_buffer_value
    last_users_buffer_value = pyperclip.paste()
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)  # Increase the sleep time to ensure the clipboard updates

def take_a_text():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    clipboard_content = ""
    try:
        clipboard_content = root.clipboard_get().strip()
    except tk.TclError:
        print("Failed to get clipboard content")
    return clipboard_content

def replace_text(correct_text):
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('delete')  # Clear the text area
    time.sleep(0.2)  # Ensure the text area is cleared
    # pyautogui.typewrite(correct_text, interval=0.01)
    keyboard.write(correct_text)
    time.sleep(0.5) 
    input("...")
    global last_users_buffer_value
    pyperclip.copy(last_users_buffer_value)
    # r = pyperclip.paste()
    # keyboard.write(r)

def execute_all():
    copy_text()
    coppied_text = take_a_text()
    if not coppied_text:
        print("No text found in clipboard.")
        return
    print("Copied text:", coppied_text)
    res = change_text(coppied_text, uk_to_en)
    print("Corrected text:", res)
    replace_text(res)



if __name__ == "__main__":
    uk_to_en = load_languages()

    keyboard.add_hotkey('ctrl', execute_all)  # Changed hotkey to avoid interference with normal 'ctrl' usage
    keyboard.wait()
