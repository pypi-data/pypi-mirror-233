from smi_python_tbi_parser.tbi.jenkins_pipeline import JenkinsPipeline


class ExternalProcessingEngineConfig:

    def __init__(self, data: dict):
        self.data: dict = data or {}

    def get_tbi_process_uri(self):
        return self['tbi_process_uri']

    def get_jenkins_pipeline(self):
        return JenkinsPipeline(self['jenkins_pipeline'])

    def __getitem__(self, key):
        return self.data[key]
