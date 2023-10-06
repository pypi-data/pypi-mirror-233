import os
import re
from .configs import Configs

class QSConfigFind:
    def __init__(self, folder):
        self.folder = folder
        self.configs = []

    def find_configs(self):
        for root, _, files in os.walk(self.folder):
            for filename in files:
                if filename.endswith(".qs"):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r') as file:
                        content = file.read()
                        if self.check_global_name(content):
                            config = Configs(file_path)
                            config.load()
                            self.configs.append(config)

    def check_global_name(self, content):
        match = re.search(fr'\*global_name\* ~ /"{self.global_name}"\.', content)
        return match is not None