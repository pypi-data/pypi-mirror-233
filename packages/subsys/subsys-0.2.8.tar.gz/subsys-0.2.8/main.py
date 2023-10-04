import typer
import os
import ctypes
import platform
import shutil
import gzip
import re
import datetime
import calc_hash
import tarfile
import tempfile
import get_snapshots
import requests
from Auth import Login

# creating an instance of Typer class
app = typer.Typer(name='subsys')

# variable initialization
control_folder_name= '.subsys'
config_file_name = 'config.txt'
assignment_file_name = 'assignment_info.txt'
current_time = datetime.datetime.now()
loggedIn = False

# decorator for defining init command
@app.command() 
def init(): 
    
    """ This command initialize a repo as .subsys in a project folder"""
    
    # check if the repo folder exist
    if os.path.exists(control_folder_name):
        typer.echo("Repository is already initialized")
    else:
        try:
            # check the operating system types and make a repo folder
            os.mkdir(control_folder_name)
            if platform.system() == "Windows":
                # set the folder attribute to be hidden on windows
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ret = ctypes.windll.kernel32.SetFileAttributesW(control_folder_name, FILE_ATTRIBUTE_HIDDEN)
                if ret == 0:
                    raise ctypes.WinError()
                typer.echo(f"The {control_folder_name} repo initialized successfully.")
                
            elif platform.system() == "Linux" or platform.system() == "Darwin":
             # Rename the folder with a dot prefix to make it hidden on Linux and macOS
                typer.echo(f"The {control_folder_name} repo initialized successfully.")
                
        except OSError as e:
            typer.echo(f"Failed to initialize the repo: {e}. An error occurred while accessing the OS information:")
        except Exception as e:
            typer.echo(f"An unexpected error occurred: {e}. Please report this issue for assistance")


# File path to store the loggedIn state
state_file_path = "login_state.txt"
Authentication_path = "user_token.txt"

# function to keep login state to a file
def write_logged_in_state(logged_in):
    with open(state_file_path, "w") as file:
        file.write(str(logged_in))

#function to read the login state       
def read_logged_in_state():
    try:
        with open(state_file_path, "r") as file:
            return file.read().strip() == "True"
    except FileNotFoundError:
        return False

# Initialize loggedIn from the file
loggedIn = read_logged_in_state()  

# function to keep token to a file
def get_auth_token(auth_token):
    with open(Authentication_path, "w") as f:
        f.write(str(auth_token))
            
# decorator for defining login
@app.command()
def login():
    """ This command allow users to login with the right credentials """
    # Access the global variable
    global loggedIn 
    
    # check if user is already logged in, if not, prompted to login 
    if loggedIn:
        typer.echo("You are already logged in.")
        return
    
    userEmail = typer.prompt('Enter your email')
    login_object = Login(userEmail, None)
    
    # Attempt login and get the authentication token, then Save the state to the file
    auth_token = login_object.attempt_login()
    if auth_token:
        typer.echo("Successfully logged in.")
        loggedIn = True
        write_logged_in_state(loggedIn) 
        get_auth_token(auth_token)
             

def config_file(config_data):
    
    """ this function configure the repo by saving/writing configuration data on config_file_name """
    
    # path to the configuration file
    config_path = os.path.join(control_folder_name, config_file_name)
    
    try:
        if not os.path.exists(control_folder_name):
            typer.echo("\nSeems your repo is not initialized.")
            typer.echo("Initialize the repo with subsys init command,\nThen proceed with configuration\n")
            
        # Write configuration data to the file
        with open(config_path, 'w') as file:
            file.write(f"Assignment_Code: {config_data['assignment_code']}\n")
            if 'student_id' in config_data:
                file.write(f"Student_ID: {config_data['student_id']}\n")
        typer.echo(f"repo configured successfully. Configuration saved to {config_path}")
    except Exception as e:
        typer.echo(f"An error occurred while configuring the repo: {e}")
            
    
# decorator for defining config command 
@app.command()
def config(
    assignment_code: str = typer.Option(None, "--code", help="Assignment Code"),
    student_id: str = typer.Option(None, "--student_id", help='Student Id'),
    interactive: bool = typer.Option(False, '-i', help="Enable interactive mode"),
): 
    
    """This command configures the repo by allowing students to enter student id and assignment code interactively"""
    # Access global variable
    global loggedIn
    # check if user logged in, if logged in, Allowed to configure the repo
    if loggedIn: 
        # check if the interactive mode is enable
        if interactive: 
            if assignment_code is None:
                assignment_code = typer.prompt("Enter the assignment code")
            if student_id is None:
                student_id = typer.prompt("Enter the student id")
                
            # create a dictionary variable to hold configured data
            config_data = {
                "assignment_code": assignment_code,
                "student_id": student_id
            }
                # Check if the file already exists
            config_path = os.path.join(control_folder_name, config_file_name)
            if os.path.exists(config_path):
                typer.echo('repo is already configured')
                return   
            # calling the config function and save data to file
            config_file(config_data)
            
                    
        else:
            # if not interactive provide the users option to config the repo
            if not interactive and assignment_code is None or assignment_code == '--help':
                typer.echo("Usage: subsys config [OPTIONS]\n")
                typer.echo("This function configures the repo by allowing students to enter student id\nand assignment code interactively\n")
                typer.echo("Options:\n --code TEXT\t\t Assignment Code  [REQUIRED]\n --student_id TEXT\t Student Id  [REQUIRED]\n -i\t\t\t Enable interactive\n --help \t\t Show this message and exit")
            else:
                config_data = {
                    "assignment_code": assignment_code,
                    }
                if student_id is not None:
                    config_data["student_id"] = student_id
                    # Check if the file already exists
                    config_path = os.path.join(control_folder_name, config_file_name)
                    if os.path.exists(config_path):
                        typer.echo('Repo is already configured')
                        return
                # call config_file function
                config_file(config_data)
    else:
        typer.echo("You must log in before configuring the repo.")
    

# function to ignore files/folders from working directory                
def subsys_ignore():
    ignored_file_list = []
    subsys_ignore_file = ".subsysignore"
    working_directory = os.listdir(".")
    
    for element in working_directory:
        if  subsys_ignore_file in element:
            with open(subsys_ignore_file, 'r') as ignore_file:
                for ignored_file in ignore_file:
                    if not ignored_file.startswith("#"):
                        ignored_file_list.append(ignored_file.strip())
    return ignored_file_list

# decorator defining snap function   
@app.command()
def snap(
    name: str = typer.Option(..., "--name", help="Snapshot name"),
):
    """ This command captures the state of the project at different stages in the form of snapshots """
    
    
    if not os.path.exists(control_folder_name):
        typer.echo("The repo is not initialized, initialize the repo with {subsys init}")
        return  # Exit the function if the repo is not initialized
        
    # Construct the snapshot path
    snapshot_folder = os.path.join(control_folder_name, 'snapshots')
    os.makedirs(snapshot_folder, exist_ok=True)
    snapshot_path = os.path.join(snapshot_folder, f'{name}')
    
    snapshot_hash = set()
    ignored_files_list = subsys_ignore() # call subsys_ignore function
    temp_dir = tempfile.mkdtemp() # create a temporary folder
    copied_dirs = set()    # variable that Keep track of directories that have already been copied to temp_dir

    # Writing the working directory products to snapshot path
    with open(snapshot_path, 'w', encoding='utf-8') as directory:
        for root, dirs, files in os.walk('.', topdown=True):
            for value in dirs + files:
                try:
                    # exclude some files/directories not to be include in the snapshot
                    if value == '.subsys' or value == '.subsysignore' or value == 'snapshots' or value == 'login_state.txt' or value == 'user_token.txt':
                        continue
                    if value.endswith('.tar.gz') or value == 'config.txt':
                        continue
                    if any(ignored_file in value for ignored_file in ignored_files_list):
                        continue
                    new_value = value
    
                    # Construct source and destination paths
                    source_path = os.path.join(root, new_value)
                    destination_path = os.path.join(temp_dir, root, new_value)
                    # Check if the source/destination paths already exists, and skip if it does
                    if os.path.isdir(source_path) and os.path.exists(destination_path):
                        continue
                    # Check if the directory/file has already been copied
                    if os.path.exists(source_path) and destination_path not in copied_dirs:
                        try:    
                            if os.path.isdir(source_path):
                                os.makedirs(destination_path, exist_ok=True)
                                shutil.copytree(source_path, destination_path)
                            else:
                                shutil.copy(source_path, destination_path)
                        except FileExistsError:
                            continue
                        
                        # read destination path and calculate hash
                        with open(destination_path, 'rb') as contents:
                            for filename in contents:
                                snapshot_hash.add(calc_hash.calculate_file_hash(filename))
                                        
                    try:
                        if os.path.isfile(destination_path) or os.path.isdir(destination_path):
                            with open(destination_path, 'rb') as f:
                                data = f.read()
                                directory.write(f'{data}\n')
                    except PermissionError:
                        continue   
                except FileNotFoundError:
                    continue            
    # read the snapshot path             
    with open(snapshot_path, 'rb') as directory:
        directory.read()
         
    # list all snapshot files in snapshot folder and compress them                                      
    snapshot_files = os.listdir('.subsys\snapshots')
    if f"{name}.tar.gz" not in snapshot_files and re.search("^[a-z-_0-9]*$", name):
        common_hashes_in_set = snapshot_hash.intersection(check_data_exist())
        for new_snap in snapshot_hash:
            if new_snap not in common_hashes_in_set:
                shutil.make_archive(snapshot_path, 'gztar', temp_dir)
                typer.echo(f"The '{name}' snapshot created successfully")
                os.remove(snapshot_path)
                break
            else:
                os.remove(snapshot_path)
                typer.echo("Same contents found")
                break
              
                
    elif f"{name}.tar.gz" in snapshot_files:
        os.remove(snapshot_path)
        typer.echo("The file exists")
    elif re.search("[A-Z]", name):
        os.remove(snapshot_path)
        typer.echo("The snapshot name has a capital letter; make it lowercase.")
    else:
        os.remove(snapshot_path)
        typer.echo("Invalid snapshot name. The name should consist of lowercase letters, hyphens, or underscores.")

def check_data_exist():
    item_file = set()
    temp_dir = tempfile.mkdtemp()
    
    for root, dirs, files in os.walk('.', topdown=True):
        for directory in dirs + files:
            if directory == 'snapshots':
                dirPath = os.path.join(root,directory)
                for snapshot_file in os.listdir(dirPath):
                    if snapshot_file.endswith('.tar.gz'):
                        snapshot_file_path = os.path.join(dirPath, snapshot_file)
                        with tarfile.open(snapshot_file_path, 'r:gz') as tar:
                            tar.extractall(path=temp_dir)
    
    for root, dirs, files in os.walk(temp_dir, topdown=True):
        for item in dirs:
            filepath = os.path.join(root, item)
            rel_path = os.path.relpath(filepath, temp_dir)
            target_dir = os.path.join(".", rel_path)
            os.makedirs(target_dir, exist_ok=True)

        for item in files:
            item_path = os.path.join(root, item)
            try:
                with open(item_path, 'rb') as contents:
                    for item in contents:
                        hashed_file = calc_hash.calculate_file_hash(item)
                        item_file.add(hashed_file)
            except PermissionError:
                continue
    # Clean up the temporary directory
    shutil.rmtree(temp_dir)
    
    return item_file


# decorator defining submit function
@app.command()
def submit(snapshot_name: str = typer.Option(None, '--name', help = "Submit zipped snapshot")):
    
    """ This command submit individual or multiple snapshot files"""
    
    # path to the configuration file
    config_path = os.path.join(control_folder_name, config_file_name)
    if not os.path.exists(control_folder_name):
        typer.echo("The repo is not initialized, initialize the repo with {subsys init}") 
    elif not os.path.exists(config_path):
        typer.echo('The repo is not Configured, Type {subsys config --help}, then follow the rules to configure the repo')
    else:
        if snapshot_name is None:
            get_snapshots.get_all_zipped_file(snapshot_name)
        else:
            get_snapshots.get_zipped_file(snapshot_name)


if __name__ == '__main__':
    app()
