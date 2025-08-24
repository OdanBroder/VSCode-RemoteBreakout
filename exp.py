import subprocess
import sys
import json
import os
import shutil
import re

def generate_extension(config):
    # Construct the command to generate the extension
    command = [
        'yo',
        'code',
        '--extensionType=js',
        f'--extensionDisplayName={config["extensionDisplayName"]}',
        f'--extensionId={config["extensionId"]}',
        f'--extensionDescription={config["extensionDescription"]}',
        '--pkgManager=npm',
        '--gitInit=False'
    ]
    
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    try:
        process.communicate(input='y\n')  # Send 'y' to accept the prompt for JavaScript type checking
    except KeyboardInterrupt:
        process.terminate()
        sys.exit(1)
def update_extension(file_path, command):
    with open(file_path, 'r') as file:
        content = file.read()
    

    content = re.sub(r'let command\s*=\s*".*?";',
                    f'let command = "{command}";',
                    content)

    with open(file_path, 'w') as file:
        file.write(content)

def update_package(file_path, config):
    with open(file_path, 'r') as file:
        package_data = json.load(file)
    
    package_data['name'] = config['extensionId']
    package_data['publisher'] = config['extensionId']
    package_data['displayName'] = config['extensionDisplayName']
    package_data['description'] = config['extensionDescription']

    with open(file_path, 'w') as file:
        json.dump(package_data, file, indent=4)

def copy_files(src_folder, dest_folder):
    for file_name in os.listdir(src_folder):
        src_file = os.path.join(src_folder, file_name)
        dest_file = os.path.join(dest_folder, file_name)
        shutil.copyfile(src_file, dest_file)

def package_extension(extension_folder):
    command = ['vsce', 'package']
    process = subprocess.Popen(command, cwd=extension_folder, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        # Automatically respond 'y' to all prompts
        process.communicate(input='y\ny\ny\n')
    except KeyboardInterrupt:
        process.terminate()
        sys.exit(1)

def main():
    config_file = 'config/config.json'
    print(f"Loaded config: {config_file}")

    with open(config_file, 'r') as f:
        config = json.load(f)

    generate_extension(config)


    extension_id = config['extensionId']
    extension_folder = os.path.join(os.getcwd(), extension_id)
    files_folder = os.path.join(os.getcwd(), 'Extension')

    if not os.path.exists(extension_folder):
        print(f"Error: The folder {extension_folder} does not exist. Make sure stage1.py has run successfully.")
        return

    # Update extension.js in Files folder
    extension_js_path = os.path.join(files_folder, 'extension.js')
    if os.path.exists(extension_js_path):
        update_extension(extension_js_path, config['command'])
    else:
        print(f"Error: {extension_js_path} does not exist.")

    # Update package.json in Files folder
    package_json_path = os.path.join(files_folder, 'package.json')
    if os.path.exists(package_json_path):
        update_package(package_json_path, config)
    else:
        print(f"Error: {package_json_path} does not exist.")

    # Copy updated files from Files to the extension folder
    if os.path.exists(files_folder):
        copy_files(files_folder, extension_folder)
    else:
        print(f"Error: {files_folder} does not exist.")

    # Package the extension
    package_extension(extension_folder)

if __name__ == "__main__":
    main()