import os
import re

class Configs:
    def __init__(self, filename):
        self.filename = filename
        self.config_data = {}

    def load(self):
        try:
            with open(self.filename, 'r') as file:
                content = file.read()
                self.parse(content)
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")

    def parse(self, content):
        sections = re.split(r'(?={/\n<)', content)

        for section in sections:
            if section.strip():
                lines = section.strip().split('\n')
                section_name = lines[1].strip()[1:-1]
                section_data = {}
            
                for line in lines[2:]:
                    key_value = line.strip().split(' = ')
                    key = key_value[0].strip()[1:-1]
                    value = key_value[1].strip().strip('"\',')
                    section_data[key] = value

                self.config_data[section_name] = section_data

    def save(self):
        content = ""
        for section_name, section_data in self.config_data.items():
            content += f'{{/\n<{section_name}>\n'
            for key, value in section_data.items():
                content += f'  {key} = "{value}",\n'
            content = content.rstrip(',\n') + '\n}\n'

        with open(self.filename, 'w') as file:
            file.write(content)

    def get_section(self, section_name):
        return self.config_data.get(section_name, {})

    def set_section(self, section_name, section_data):
        self.config_data[section_name] = section_data

    def get_value(self, section_name, key):
        section = self.config_data.get(section_name, {})
        return section.get(key)

    def set_value(self, section_name, key, value):
        if section_name not in self.config_data:
            self.config_data[section_name] = {}
        self.config_data[section_name][key] = value

    def add_value(self, section_name, key, value):
        if section_name not in self.config_data:
            self.config_data[section_name] = {}
        if key not in self.config_data[section_name]:
            self.config_data[section_name][key] = value

    def add_service(self, section_name, service_name):
        self.add_value(section_name, service_name, "")

    def add_config(self, global_name):
        self.add_value("config", "*global_name*", f'"{global_name}".')

    def set_backup_time(self, hours):
        self.set_value("backups", "*backup_hours*", str(hours))

    def backup(self, enable=True):
        self.set_value("backups", "*backups*", "true" if enable else "false")