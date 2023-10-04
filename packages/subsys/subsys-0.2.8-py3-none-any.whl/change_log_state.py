import time
import os
import typer

# Set the timeout in seconds (3 hours)
timeout_seconds = 30
current_time_seconds = int(time.time())
simplify_time = int(current_time_seconds/timeout_seconds)

# Function to update the file with the specified state
def update_logged_in_state():
    
    workingDirectory = '.'
    for root,dir, files in os.walk(workingDirectory, topdown=True):
        for file in files:
            if file == 'login_state.txt':
                state_path = os.path.join(root, file)
                with open(state_path, 'r') as f:
                    state = f.read().strip()
                    if state == 'True':
                        update_file_timeUp = int(current_time_seconds/simplify_time)
                        if update_file_timeUp >= timeout_seconds:
                            time.sleep(timeout_seconds)
                            with open(state_path, 'w') as f:
                                f.write('False') 
            else:
                continue

 # Run the loop to periodically check and update the file
while True:
    update_logged_in_state()
    time.sleep(timeout_seconds)