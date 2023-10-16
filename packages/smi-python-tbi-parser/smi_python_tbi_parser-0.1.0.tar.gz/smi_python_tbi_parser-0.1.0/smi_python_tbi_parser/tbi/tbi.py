from smi_python_commons.yaml.parser import parse_yaml_file

from smi_python_tbi_parser.tbi.changelog import Changelog
from smi_python_tbi_parser.tbi.external_process_engine import ExternalProcessingEngine


class Tbi:

    def __init__(self, data: dict):
        self.data: dict = data or {}

    def get_external_processing_engine(self):
        return ExternalProcessingEngine(self['external_processing_engine'])

    def get_name(self):
        return self['name']

    def get_description(self):
        return self['description']

    def get_authors(self):
        return self['authors']

    def get_materials(self):
        return self['materials']

    def get_changelog(self):
        return Changelog(self['changelog'])

    def __getitem__(self, key):
        return self.data[key]


def parse_tbi(file_name: str):
    return Tbi(parse_yaml_file(file_name))
