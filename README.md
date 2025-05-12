# League of Legends Game Tracker & Blocker Trigger

## Description

This Python script monitors your League of Legends game activity. It counts how many games you've completed since starting the script and automatically runs a predefined command-line action (like launching Cold Turkey Blocker to block distracting websites) after a specific number of games.

This is useful for setting limits on gaming sessions and automatically enabling focus tools.

## Features

* Monitors for the start and end of the main League of Legends game process (`League of Legends.exe`).
* Counts completed games during the current script session.
* Executes a customizable command-line action after a set number of games.
* Configurable:
    * Target game process name.
    * Path to the executable to run.
    * Arguments for the executable.
    * Number of games before triggering the action.
    * Process check frequency (polling interval).
* Resets the game counter after the action is triggered, allowing for repeated cycles.
* Basic error handling for file paths.
* Cross-platform (requires Python and `psutil`).

## Prerequisites

* **Python 3.x:** Download from [python.org](https://www.python.org/) if you don't have it installed.
* **`psutil` library:** Install using pip:
    ```bash
    pip install psutil
    ```
* **Target Application:** The application you want the script to trigger (e.g., Cold Turkey Blocker) must be installed and accessible from the path you specify.

## Installation

1.  Clone this repository or download the `lol_tracker.py` script to your computer.
    ```bash
    # Example if using git
    # git clone <repository_url>
    # cd <repository_directory>
    ```
2.  Install the required Python library:
    ```bash
    pip install psutil
    ```

## Configuration

Before running the script, you need to configure it by editing the `lol_tracker.py` file:

1.  Open `lol_tracker.py` with a text editor.
2.  Locate the `# --- Configuration ---` section near the top.
3.  Modify the following variables as needed:

    * `LOL_PROCESS_NAME`: The exact process name of the League of Legends game client *during a match*. Default is `"League of Legends.exe"`. You can verify this using your system's Task Manager (Details tab on Windows) while a game is active.
    * `COLD_TURKEY_PATH`: The **full, absolute path** to the executable file you want to run after the game limit is reached.
        * **Important for Windows:** Use a raw string `r"..."` to handle backslashes correctly, e.g., `r"C:\Program Files\YourApp\App.exe"`.
        * Default: `r"D:\Program Files\Cold Turkey\Cold Turkey Blocker.exe"`
    * `COLD_TURKEY_ARGS`: A Python list of strings, where each string is a separate command-line argument for the executable.
        * Default: `["-start", "Distractions", "-lock", "15"]`
    * `GAMES_BEFORE_BLOCK`: The number of completed LoL games required to trigger the command.
        * Default: `2`
    * `POLL_INTERVAL`: How often (in seconds) the script checks if the game process is running. Lower values are more responsive but use slightly more resources.
        * Default: `30`

4.  Save the changes to `lol_tracker.py`.

## Usage

1.  Open your terminal or command prompt.
2.  Navigate (`cd`) to the directory where you saved `lol_tracker.py`.
3.  Run the script using Python:
    ```bash
    python lol_tracker.py
    ```
4.  The script will start monitoring. **Keep the terminal window open** while you intend to track games. It will print messages indicating:
    * When it starts monitoring.
    * When a game starts and ends.
    * The current completed game count.
    * When the target number of games is reached and the command is executed.
    * When the counter resets.
5.  To stop the script manually, return to the terminal window and press `Ctrl+C`.

## How it Works

The script uses the `psutil` library to periodically scan the list of active processes on your system. It looks for a process matching `LOL_PROCESS_NAME`. It maintains state to detect transitions: when the process appears (game start) and when it disappears (game end). Upon detecting a game end, it increments a counter. When this counter reaches `GAMES_BEFORE_BLOCK`, it uses Python's built-in `subprocess` module to execute the command defined by `COLD_TURKEY_PATH` and `COLD_TURKEY_ARGS`. After attempting execution, it resets the game counter back to zero.

## Troubleshooting

* **Command Not Executing:**
    * Verify `COLD_TURKEY_PATH` is **exactly** correct. Check for typos. Use the `r"..."` format for Windows paths.
    * Ensure the executable file actually exists at that location. The script checks this at the start.
    * Verify `COLD_TURKEY_ARGS` are correct for the target application.
    * Check the script's console output for error messages like "Executable not found" or "Error running command".
    * Ensure the script/user has the necessary permissions to execute the target application.
* **Games Not Detected / Count Incorrect:**
    * Confirm `LOL_PROCESS_NAME` matches the *exact* process name shown in Task Manager (Details tab) while a game is running (not the launcher/client).
    * If detection seems delayed, you could slightly decrease `POLL_INTERVAL`, but 30 seconds is generally a good balance.
* **`psutil` Errors:**
    * Make sure you ran `pip install psutil` in your Python environment.
    * Try uninstalling and reinstalling it: `pip uninstall psutil` then `pip install psutil`.

## License
