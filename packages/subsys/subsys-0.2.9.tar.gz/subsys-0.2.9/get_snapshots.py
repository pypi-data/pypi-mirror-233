import os
import typer
import requests
from Auth import Login
import mimetypes
control_folder_name = '.subsys'
url = 'https://asp-api.amalitech-dev.net/api/submission/create/'

# function that get token in a file
def get_token():
    for root, dir, file in os.walk('.', topdown=True):
        for value in file:
            if value == 'user_token.txt':
                item_path = os.path.join(root, value)
                with open(item_path, 'r') as fa:
                    token = fa.read().strip()
                    return token
            else:
                continue
 
# function iterate through all snasphots and submit one               
def get_zipped_file(snap_name):
    for root, dirs, files in os.walk('.', topdown=True):
        for snaps in dirs + files:
          if snaps == control_folder_name:
            folder_path = os.path.join(root, snaps)
            if os.path.isdir(folder_path):
                for dirpath, dirnames, filenames in os.walk(folder_path, topdown=True):
                    for filename in filenames:
                        if filename == 'config.txt':
                            config_file_path = os.path.join(folder_path, filename)
                            if os.path.isfile(config_file_path):
                                with open(config_file_path, 'r') as config_file:
                                    for line in config_file:
                                        if line.startswith('Assignment_Code'):
                                            assignment_code = line.split(':')[-1].strip()
                                            submission_url = f'{url}{assignment_code}'
                                            break             
                                        
                    for dir in dirnames:
                        if dir == 'snapshots':
                            config_dir_path = os.path.join(folder_path, dir)
                            zipped_file = os.listdir(config_dir_path)
                            if f'{snap_name}.tar.gz' in zipped_file:
                                auth_token = get_token()
                                header = {'authorization': f'Bearer {auth_token}'} 
                                mime_type, _ = mimetypes.guess_type(f'{snap_name}.tar.gz')
                                snap_path = os.path.join(config_dir_path, f'{snap_name}.tar.gz')
                                files_to_send = {'headFile': (os.path.basename(snap_path), open(snap_path, 'rb'), mime_type)}
                                submit_response = requests.post(submission_url, headers=header, files=files_to_send)
                                result = submit_response.json()['message']
                                typer.echo(result)
                                break
                            else:
                                typer.echo('Not found! Try again')
                                return
                                         
# function to get all zipped snapshot file               
def get_all_zipped_file(snap_name):
    
    for root, dirs, files in os.walk('.', topdown=True):
        for snaps in dirs + files:
          if snaps == control_folder_name:
            folder_path = os.path.join(root, snaps)
            if os.path.isdir(folder_path):
                for dirpath, dirnames, filenames in os.walk(folder_path, topdown=True):
                    for filename in filenames:
                        if filename == 'config.txt':
                            config_file_path = os.path.join(folder_path, filename)
                            if os.path.isfile(config_file_path):
                                with open(config_file_path, 'r') as config_file:
                                    for line in config_file:
                                        if line.startswith('Assignment_Code'):
                                            assignment_code = line.split(':')[-1].strip()
                                            submission_url = f'{url}{assignment_code}'
                                            break
                    for dir in dirnames:
                        try:
                            if dir == 'snapshots':
                                config_dir_path = os.path.join(folder_path, dir)
                                zipped_file = os.listdir(config_dir_path)
                                try:
                                    for item in zipped_file:
                                        if item and item.endswith('tar.gz'):
                                            auth_token = get_token()
                                            header = {'authorization': f'Bearer {auth_token}'}
                                            snap_path = os.path.join(config_dir_path, item)
                                            
                                            mime_type, _ = mimetypes.guess_type(f'{snap_name}.tar.gz')
                                            
                                            files_to_send = {'headFile': (os.path.basename(snap_path), open(snap_path, 'rb'), mime_type)}
                                            submit_response = requests.post(submission_url, headers=header, files=files_to_send)
                                            result = submit_response.json()['message']
                                            typer.echo(result)
                                except FileNotFoundError:
                                    typer.echo('File not found')
                        except Exception as e:
                            typer.echo(f'Error {e} occurred')
                                