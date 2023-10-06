import os
import json
import hashlib
import shutil

class Configs:
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir

    def create_config(self, name, password, backups=False, delete_after=None):
        config_dir = os.path.join(self.storage_dir, name)
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, f'{name}.qs')
        config_data = {
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'backups': backups,
            'delete_after': delete_after,
            'failed_attempts': 0,
        }
        with open(config_file, 'w') as f:
            json.dump(config_data, f)

    def add_api_key(self, config_name, service, api_key):
        config_dir = os.path.join(self.storage_dir, config_name)
        config_file = os.path.join(config_dir, f'{config_name}.qs')
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        if not config_data.get('password'):
            raise ValueError("Config is not password protected.")
        
        if self.verify_password(config_name, input("Enter password: ")):
            with open(config_file, 'a') as f:
                f.write(f"{{/\n<{service}>\n")
                f.write(f"  {len(self.list_api_keys(config_name, service)) + 1}.api - \"{api_key}\",\n")
                f.write("}\n")
        else:
            print("Incorrect password. API key not added.")
            config_data['failed_attempts'] += 1
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            if config_data.get('delete_after') is not None and config_data['failed_attempts'] >= config_data['delete_after']:
                self.delete_config(config_name)
                print(f"Config '{config_name}' deleted after {config_data['delete_after']} failed attempts.")

    def verify_password(self, config_name, password):
        config_dir = os.path.join(self.storage_dir, config_name)
        config_file = os.path.join(config_dir, f'{config_name}.qs')
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        stored_password_hash = config_data.get('password')
        entered_password_hash = hashlib.sha256(password.encode()).hexdigest()
        return stored_password_hash == entered_password_hash

    def list_api_keys(self, config_name, service):
        config_dir = os.path.join(self.storage_dir, config_name)
        config_file = os.path.join(config_dir, f'{config_name}.qs')
        api_keys = []

        with open(config_file, 'r') as f:
            lines = f.readlines()
            in_api_section = False
            for line in lines:
                line = line.strip()
                if line.startswith("<") and line.endswith(">"):
                    if line[1:-1] == service:
                        in_api_section = True
                    else:
                        in_api_section = False
                elif in_api_section and line.startswith("  "):
                    api_keys.append(line.split("-")[1].strip().strip('"'))

        return api_keys

    def import_file(self, config_name, file_name, content):
        config_dir = os.path.join(self.storage_dir, config_name)
        file_path = os.path.join(config_dir, f'{file_name}.qs')
        with open(file_path, 'w') as f:
            f.write(content)

    def get_file_content(self, config_name, file_name):
        config_dir = os.path.join(self.storage_dir, config_name)
        file_path = os.path.join(config_dir, f'{file_name}.qs')
        with open(file_path, 'r') as f:
            content = f.read()
        return content

    def backup_file(self, config_name, file_name):
        config_dir = os.path.join(self.storage_dir, config_name)
        file_path = os.path.join(config_dir, f'{file_name}.qs')
        backup_dir = os.path.join(config_dir, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        backup_file_path = os.path.join(backup_dir, f'{file_name}.bak')
        shutil.copy(file_path, backup_file_path)
        print(f"File '{file_name}' backed up to '{backup_file_path}'.")

    def delete_config(self, config_name):
        config_dir = os.path.join(self.storage_dir, config_name)
        shutil.rmtree(config_dir)
        print(f"Config '{config_name}' deleted.")