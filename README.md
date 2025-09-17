# Python Plagiarism Detection Tool

## Overview

The Python Plagiarism Detection Tool is designed to identify potential plagiarism in Python code by comparing structural similarities rather than exact character matches. This approach helps in detecting plagiarism even when variable names, function names, and minor syntactic elements have been altered. The tool focuses on control structures, common Python methods, and statement patterns to find suspicious sections of code between a "suspect" assignment and a set of "original" assignments.

## Features

-   **Structural Comparison:** Ignores easily changed elements like variable names and focuses on the underlying structure of the code (e.g., loops, conditionals, function definitions).
-   **GitHub Integration:** Allows downloading multiple Python repositories from GitHub based on a search query to serve as a pool of "original" assignments for comparison.
-   **Local File Comparison:** Supports comparing a suspect assignment against a locally selected original zip file.
-   **Redundancy Removal:** Can use a "blank" assignment (an empty version of the suspect assignment) to remove common, non-plagiarized boilerplate code, reducing false positives.
-   **Interactive File Matching:** Provides an interactive prompt to confirm file matches between zip archives, ensuring accurate comparisons.
-   **Save/Load Functionality:** Saves the current session's settings (downloaded repositories, file paths, etc.) to allow resuming work without re-configuring.
-   **Detailed Output:** Clearly displays matched sections, including line numbers and the border lines of both the original and plagiarized code.
-   **Temporary File Management:** Manages and cleans up temporary download and extraction folders.

## How it Works

The tool operates in several key steps:

1.  **File Selection/Download:**
    *   **Suspect File:** The user selects a `.zip` archive containing the Python assignment to be checked for plagiarism.
    *   **Original Files:**
        *   The user can choose to download multiple Python projects from GitHub based on a search query (e.g., "Python assignment 101"). The tool will download these as `.zip` files.
        *   Alternatively, the user can select a local `.zip` file containing an "original" assignment for direct comparison.
    *   **Blank Assignment (Optional):** To reduce false positives, the user can provide a `.zip` archive of a "blank" or empty version of the suspect assignment. The tool will identify and remove lines identical to those in the blank assignment from the suspect code.

2.  **File Matching within Zips:**
    *   The tool extracts Python files (`.py`) from the selected zip archives.
    *   It then attempts to match corresponding files between the "original" and "suspect" sets based on shared prefixes in their filenames or a user-specified search string.
    *   The user interactively confirms if the suggested file matches are correct.

3.  **Line Vectorization:**
    *   For each Python file, lines of code are converted into "line vectors." These vectors are lists of numerical counts representing the occurrences of various control structures, operators, and common Python syntax elements (e.g., number of spaces, parentheses, keywords like `if`, `for`, `def`, `return`).
    *   Variable names and specific string literals are intentionally ignored to focus on code structure.

4.  **Structural Comparison:**
    *   The line vectors from the original files are stored in a specialized table (`sortlines`) where the vector itself acts as a key.
    *   The tool then iterates through the suspect file's line vectors. If a suspect line's vector matches a key in the original table, it indicates a structural similarity.
    *   It specifically looks for *consecutive sequences* of structurally similar lines (typically 2 or more) to identify potential plagiarized blocks.

5.  **Output:**
    *   When a significant match is found, the tool reports the original and plagiarized file paths.
    *   It then prints the line numbers and the actual code of the "border lines" (start and end) of the detected plagiarized section.

## Getting Started

### Prerequisites

-   Python 3.x
-   `requests` library (`pip install requests`)
-   `tkinter` (usually included with Python, but may need to be installed on some systems: `pip install tk` or `sudo apt-get install python3-tk`)

### Installation

1.  Clone this repository or download the `plagiarism_detector.py` script.
2.  Install the required Python libraries:
    ```bash
    pip install requests
    ```

### Running the Tool

1.  Navigate to the directory containing the script in your terminal.
2.  Run the script:
    ```bash
    python plagiarism_detector.py
    ```

3.  Follow the interactive prompts:
    *   **Save File:** If a `save.txt` exists, you'll be asked if you want to load previous settings.
    *   **Suspect Zip File:** A file dialog will open for you to select the `.zip` file containing the assignment you want to check for plagiarism.
    *   **Original Files:**
        *   You'll be asked if you want to download original files from GitHub. If yes, provide a search query (e.g., "python recursion assignment") and the number of repositories to download.
        *   If no, a file dialog will open to select a local original `.zip` file.
    *   **Blank Assignment (Optional):** You'll be asked if you want to provide a blank version of the suspect assignment to remove boilerplate code. If yes, a file dialog will open to select the empty assignment `.zip`.
    *   **Specific Assignment Search (Optional):** You can provide a string to filter for specific assignments within the zip files (e.g., "assignment1").
    *   **File Matching Confirmation:** For each pair of potentially matching files, you'll be asked to confirm if they are indeed the correct matches.

### Output Example

```
-----
Now showing original/repo_name/assignment.py and suspect/suspect_name/assignment.py from repo_name on github
-----
Match found at: 15 to 20 original lines, 25 to 30 plagiarised lines.

Original border lines:
    def calculate_sum(a, b):
        result = a + b
Plagiarised border lines:
    def get_total(x, y):
        total = x + y
```

## Folder Structure

The tool creates the following temporary folders (which are cleared on reset or exit):

-   `./github_downloads`: Stores `.zip` files downloaded from GitHub.
-   `./original`: Stores extracted Python files from the original assignments.
-   `./suspect`: Stores extracted Python files from the suspect assignment.

A `save.txt` file is also created to store session data.

## Important Notes

*   **Depiction is not Endorsement:** The tool identifies structural similarities. The presence of a match does not definitively prove plagiarism, but rather highlights areas that warrant further human inspection.
*   **False Positives/Negatives:** While the tool aims to be robust, some false positives (e.g., highly generic code snippets) or false negatives (e.g., extremely obfuscated code) may occur. Always use your judgment.
*   **Input Validation:** The tool includes basic input validation for zip files and numerical inputs, but always ensure you're providing appropriate files.
*   **Resource Usage:** Downloading many GitHub repositories can consume network bandwidth and disk space.

## Future Enhancements (Ideas)

*   **Visual Diff:** Integrate a visual diff tool to highlight the exact differences between matched lines.
*   **Similarity Score:** Implement a numerical similarity score for matched blocks to quantify the degree of plagiarism.
*   **GUI:** Develop a more user-friendly graphical interface with a file browser and integrated output display.
*   **Language Agnostic:** Extend the line vectorization to support other programming languages.
*   **Advanced Obfuscation Detection:** Implement more sophisticated algorithms to detect highly obfuscated plagiarism (e.g., reordered statements, complex transformations).
*   **Report Generation:** Generate a comprehensive report summarizing all detected matches.

## License

This project is open-source and available under the [MIT License](LICENSE).