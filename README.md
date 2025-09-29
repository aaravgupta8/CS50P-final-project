# Digital Declutter Assistant

### Video URL
[https://youtu.be/your-video-link-here](https://youtu.be/your-video-link-here)

---

## Introduction

The **Digital Declutter Assistant** is my final project for CS50P. It is a command-line Python program designed to help users automatically organize files on their computer into neat, category-based subfolders. The motivation for this project came from my own experience with cluttered folders such as Downloads, Desktop, or external drives, where hundreds or even thousands of files pile up without structure. Manually sorting them is tedious, error-prone, and easy to put off indefinitely. I wanted to build something that would solve this real-world problem in a safe, cross-platform, and user-friendly way.

This project not only demonstrates proficiency in Python fundamentals like file I/O, exceptions, command-line arguments, and testing, but also emphasizes good software engineering practices such as modular design, code documentation, and automated testing with pytest. The program has been tested on Windows and Linux environments and works consistently across platforms.

---

## Project Description

At its core, the Digital Declutter Assistant scans a source folder, classifies each file based on its extension, and then moves it into a corresponding subfolder such as `Images`, `Documents`, `Audio`, `Video`, `Archives`, `Code`, or `Other`. For example, all `.jpg` and `.png` files are sent to `Images`, while `.pdf` and `.docx` files are sent to `Documents`. Files that do not match any known extension are placed into `Other`.

The program supports two major modes:

- **Dry-run mode** (`--dry-run`): The program simulates the moves and shows the user what would happen without making any changes on disk. This allows for a safe preview and helps avoid mistakes.
- **Execute mode** (`--execute`): The program actually moves the files into the category subfolders. It also creates these subfolders automatically if they do not exist yet.

The tool is designed with safety in mind. If a destination file already exists, the program does not overwrite it but instead appends a counter, e.g., `file (2).jpg`. Files without sufficient read or write permissions are skipped gracefully, and errors are reported without crashing the program. Users can also exclude certain file types using glob patterns, e.g., `--exclude "*.exe" "*.iso"`.

To enhance the user experience, the program uses the external library **Rich** to display pretty, colored tables in the terminal. This makes it clear to see which files were moved, skipped, or planned.

---

## File Overview

- **`project.py`**: This is the main program. It contains all of the logic for scanning folders, categorizing files, moving them safely, handling errors, and generating reports. It defines several top-level functions, including:
  - `categorize_file`: Determines which category a file belongs to.
  - `move_file_safe`: Moves a file while handling duplicates and permission errors.
  - `scan_folder`: Walks through a folder and collects results for all files.
  - `generate_report`: Summarizes the run in terms of total files, moved, skipped, and errors.
  - `pretty_print`: Uses Rich to display a table with per-file results.
  - `main`: Handles command-line arguments and coordinates the workflow.

- **`test_project.py`**: This file contains unit tests written with `pytest`. The tests cover categorization, dry-run behavior, error handling when permissions are denied, and the ability to exclude files. The test suite ensures that the program behaves as expected and remains stable if extended in the future.

- **`requirements.txt`**: This file lists external dependencies. In this case, the only requirement is `rich`, which is responsible for colored output in the terminal. All other functionality relies on Python’s standard library.

- **`README.md`**: The file you are reading now, which documents the project thoroughly, including design decisions, installation instructions, and usage examples.

---

## Installation and Setup

1) Make sure Python 3.10 or higher is installed.  
   Check with:
   ```bash
   python --version
2) Clone the repository from GitHub:
   ```bash
   git clone https://github.com/aaravgupta8/CS50P-final-project.git
   cd CS50P-final-project

3) Install dependencies:
   ```bash
   pip install -r requirements.txt
4) Usage
   ```bash
   python project.py ~/Downloads --dry-run 
   python project.py ~/Downloads --execute
   python project.py ~/Downloads --dest ~/CleanedDownloads --execute
   python project.py ~/Downloads --execute --exclude "*.exe" "*.iso"
After execution, you will see subfolders such as:
Images/
Documents/
Audio/
Video/
Archives/
Code/
Other/

Running Tests
Make sure pytest is installed:
    ```bash
    pip install pytest
Run all tests:

bash
Copy code
pytest -v
Design Choices
One major design choice was whether to use only the Python standard library or include external packages. I decided to add Rich because it makes the output more user-friendly and visually engaging, which is important for a program that produces a lot of text. Without Rich, the program would still function correctly, but the user experience would be less polished.

Another choice was whether to copy or move files. I decided on moving by default because the goal of the project is decluttering. However, I included a --dest option so users can move files into a new destination folder instead of reorganizing the source folder in place. This provides flexibility and safety if a user wants to test the tool without altering the original directory.

The decision to include a dry-run mode was also critical. It provides peace of mind, especially when running the tool on large folders. Dry-run ensures that users can review the planned actions before committing to actual moves.

Conclusion
The Digital Declutter Assistant is a practical Python project that solves a common problem while showcasing core programming skills and good design practices. It highlights the importance of safety, usability, and testing in software development. I am proud of this project because it is both academically appropriate for CS50P and practically useful in everyday life. I hope that others who try it will find their folders a little cleaner and their workflow a little easier as a result.
