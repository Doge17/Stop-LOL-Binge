import time
import subprocess
import psutil
import sys
import os

# --- Configuration ---
# The name of the League of Legends game process
LOL_PROCESS_NAME = "League of Legends.exe"
# The full path to the Cold Turkey Blocker executable
COLD_TURKEY_PATH = r"D:\Program Files\Cold Turkey\Cold Turkey Blocker.exe"
# Arguments for Cold Turkey Blocker
COLD_TURKEY_ARGS = ["-start", "Distractions", "-lock", "15"]
# How many games to play before triggering the command
GAMES_BEFORE_BLOCK = 2
# How often to check for the game process (in seconds)
POLL_INTERVAL = 30
# --- End Configuration ---

def find_process(process_name):
    """Checks if a process with the given name is running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def run_command(executable_path, args):
    """Runs the specified command."""
    try:
        command = [executable_path] + args
        print(f"Running command: {' '.join(command)}")
        # Use CREATE_NO_WINDOW on Windows to avoid popping up a cmd window
        creation_flags = 0
        if sys.platform == "win32":
            creation_flags = subprocess.CREATE_NO_WINDOW

        # Use shell=True if the path contains spaces and isn't handled correctly otherwise
        # Be cautious with shell=True if the path could be user-controlled
        # Using a raw string and direct list of args is generally safer
        if not os.path.exists(executable_path):
             print(f"Error: Executable not found at '{executable_path}'")
             return False

        subprocess.run(command, check=False, creationflags=creation_flags) # check=False allows script to continue if command fails
        print("Command executed.")
        return True
    except FileNotFoundError:
        print(f"Error: Could not find the executable at '{executable_path}'. Please check the COLD_TURKEY_PATH.")
        return False
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Main function to monitor games and trigger the command."""
    game_count = 0
    is_game_running = False
    print("--- League of Legends Game Tracker ---")
    print(f"Monitoring for '{LOL_PROCESS_NAME}'...")
    print(f"Will trigger block after {GAMES_BEFORE_BLOCK} games.")
    print(f"Checking every {POLL_INTERVAL} seconds.")
    print("Press Ctrl+C to stop the script.")

    try:
        while True:
            process_found = find_process(LOL_PROCESS_NAME)

            if process_found and not is_game_running:
                # Game just started
                is_game_running = True
                print(f"Detected League of Legends game start. (Game count: {game_count})")

            elif not process_found and is_game_running:
                # Game just ended
                is_game_running = False
                game_count += 1
                print(f"Detected League of Legends game end. Game count is now: {game_count}")

                # Check if the threshold is met
                if game_count >= GAMES_BEFORE_BLOCK:
                    print(f"Reached {GAMES_BEFORE_BLOCK} games. Triggering Cold Turkey Blocker...")
                    if run_command(COLD_TURKEY_PATH, COLD_TURKEY_ARGS):
                         # Reset the counter only if the command was successfully attempted
                         game_count = 0
                         print(f"Game counter reset. Waiting for the next {GAMES_BEFORE_BLOCK} games.")
                    else:
                         print("Command execution failed. Counter not reset. Check paths and permissions.")
                         # Decide if you want to retry or stop here. For now, we just notify.


            # Wait before the next check
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("Exiting game tracker.")


if __name__ == "__main__":
    # Check if Cold Turkey path exists before starting the loop
    if not os.path.exists(COLD_TURKEY_PATH):
         print(f"Error: The specified Cold Turkey path does not exist: '{COLD_TURKEY_PATH}'")
         print("Please correct the COLD_TURKEY_PATH variable in the script.")
    else:
         main()