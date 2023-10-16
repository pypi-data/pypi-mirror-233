from smi_python_tbi_parser.tbi.external_processing_engine_config import ExternalProcessingEngineConfig


class ExternalProcessingEngine:

    def __init__(self, data: dict):
        self.data: dict = data or {}

    def get_type(self):
        return self['type']

    def get_process_id(self):
        return self['process_id']

    def get_config(self):
        return ExternalProcessingEngineConfig(self['config'])

    def __getitem__(self, key):
        return self.data[key]
