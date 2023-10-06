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

    def add_value(self, config, service, name, value):
        config_dir = os.path.join(self.storage_dir, config)
        config_file = os.path.join(config_dir, f'{config}.qs')
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        if not config_data.get('password'):
            raise ValueError("Config is not password protected.")
        
        if self.verify_password(config, input("Enter password: ")):
            with open(config_file, 'a') as f:
                f.write(f"\n\n{{/\n<{service}>\n")
                f.write(f"  {name} - \"{value}\",\n")
                f.write("}\n")
        else:
            print("Incorrect password. Value not added.")
            config_data['failed_attempts'] += 1
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            if config_data.get('delete_after') is not None and config_data['failed_attempts'] >= config_data['delete_after']:
                self.delete_config(config)
                print(f"Config '{config}' deleted after {config_data['delete_after']} failed attempts.")

    def verify_password(self, config, password):
        config_dir = os.path.join(this.storage_dir, config)
        config_file = os.path.join(config_dir, f'{config}.qs')
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        stored_password_hash = config_data.get('password')
        entered_password_hash = hashlib.sha256(password.encode()).hexdigest()
        return stored_password_hash == entered_password_hash

    def list_values(self, config, service):
        config_dir = os.path.join(this.storage_dir, config)
        config_file = os.path.join(config_dir, f'{config}.qs')
        values = []

        with open(config_file, 'r') as f:
            lines = f.readlines()
            in_service_section = False
            for line in lines:
                line = line.strip()
                if line.startswith("<") and line.endswith(">"):
                    if line[1:-1] == service:
                        in_service_section = True
                    else:
                        in_service_section = False
                if in_service_section:
                    parts = line.split(" - ")
                    if len(parts) == 2:
                        key, val = parts
                        values.append((key.strip(), val.strip()))

        return values

    def import_value(self, config, service, name):
        config_dir = os.path.join(this.storage_dir, config)
        config_file = os.path.join(config_dir, f'{config}.qs')
        value = None

        with open(config_file, 'r') as f:
            lines = f.readlines()
            in_service_section = False
            for line in lines:
                line = line.strip()
                if line.startswith("<") and line.endswith(">"):
                    if line[1:-1] == service:
                        in_service_section = True
                    else:
                        in_service_section = False
                if in_service_section:
                    parts = line.split(" - ")
                    if len(parts) == 2:
                        key, val = parts
                        if key.strip() == name:
                            value = val.strip()
                            break

        return value

    def import_all_values(self, config, service):
        config_dir = os.path.join(this.storage_dir, config)
        config_file = os.path.join(config_dir, f'{config}.qs')
        values = {}

        with open(config_file, 'r') as f:
            lines = f.readlines()
            in_service_section = False
            for line in lines:
                line = line.strip()
                if line.startswith("<") and line.endswith(">"):
                    if line[1:-1] == service:
                        in_service_section = True
                    else:
                        in_service_section = False
                if in_service_section:
                    parts = line.split(" - ")
                    if len(parts) == 2:
                        key, val = parts
                        values[key.strip()] = val.strip()

        return values

    def import_config(self, config):
        config_dir = os.path.join(this.storage_dir, config)
        config_file = os.path.join(config_dir, f'{config}.qs')
        config_data = None

        with open(config_file, 'r') as f:
            config_data = json.load(f)

        return config_data

    def import_all_configs(self):
        config_dirs = [d for d in os.listdir(this.storage_dir) if os.path.isdir(os.path.join(this.storage_dir, d))]
        configs = {}

        for config in config_dirs:
            config_data = self.import_config(config)
            if config_data:
                configs[config] = config_data

        return configs

    def import_all_services(self, config):
        config_dir = os.path.join(this.storage_dir, config)
        config_file = os.path.join(config_dir, f'{config}.qs')
        services = []

        with open(config_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("<") and line.endswith(">"):
                    services.append(line[1:-1])

        return services

    def export_config(self, config, new_name):
        config_dir = os.path.join(this.storage_dir, config)
        new_config_dir = os.path.join(this.storage_dir, new_name)
        shutil.copytree(config_dir, new_config_dir)
        print(f"Configuration '{config}' exported as '{new_name}'.")

    def delete_value(self, config, service, name):
        config_dir = os.path.join(this.storage_dir, config)
        config_file = os.path.join(config_dir, f'{config}.qs')
        temp_file = os.path.join(config_dir, f'{config}_temp.qs')

        with open(config_file, 'r') as f, open(temp_file, 'w') as temp_f:
            lines = f.readlines()
            in_service_section = False
            for line in lines:
                line = line.strip()
                if line.startswith("<") and line.endswith(">"):
                    if line[1:-1] == service:
                        in_service_section = True
                    else:
                        in_service_section = False
                if in_service_section:
                    parts = line.split(" - ")
                    if len(parts) == 2:
                        key, val = parts
                        if key.strip() != name:
                            temp_f.write(f"{key} - {val}\n")
            shutil.move(temp_file, config_file)

    def delete_service(self, config, service):
        config_dir = os.path.join(this.storage_dir, config)
        config_file = os.path.join(config_dir, f'{config}.qs')
        temp_file = os.path.join(config_dir, f'{config}_temp.qs')

        with open(config_file, 'r') as f, open(temp_file, 'w') as temp_f:
            lines = f.readlines()
            in_service_section = False
            for line in lines:
                line = line.strip()
                if line.startswith("<") and line.endswith(">"):
                    if line[1:-1] == service:
                        in_service_section = True
                    else:
                        in_service_section = False
                if not in_service_section:
                    temp_f.write(f"{line}\n")
            shutil.move(temp_file, config_file)

    def delete_config(self, config):
        config_dir = os.path.join(this.storage_dir, config)
        shutil.rmtree(config_dir)
        print(f"Configuration '{config}' deleted.")

    def create_backup(self, config, service, name):
        config_dir = os.path.join(this.storage_dir, config)
        config_file = os.path.join(config_dir, f'{config}.qs')
        backup_dir = os.path.join(config_dir, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        backup_file_path = os.path.join(backup_dir, f'{service}_{name}.bak')
        with open(config_file, 'r') as f, open(backup_file_path, 'w') as b:
            lines = f.readlines()
            in_service_section = False
            for line in lines:
                line = line.strip()
                if line.startswith("<") and line.endswith(">"):
                    if line[1:-1] == service:
                        in_service_section = True
                    else:
                        in_service_section = False
                if in_service_section:
                    parts = line.split(" - ")
                    if len(parts) == 2:
                        key, val = parts
                        if key.strip() == name:
                            b.write(f"{key} - {val}\n")
        print(f"Value '{name}' in service '{service}' of configuration '{config}' backed up as '{backup_file_path}'.")