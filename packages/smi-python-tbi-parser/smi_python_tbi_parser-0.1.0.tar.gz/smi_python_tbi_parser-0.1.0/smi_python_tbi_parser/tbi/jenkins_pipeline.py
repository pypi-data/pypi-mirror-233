class JenkinsPipeline:

    def __init__(self, data: dict):
        self.data: dict = data or {}

    def get_tbi_vcs_url(self):
        return self['tbi_vcs_url']

    def get_tbi_dvc_path(self):
        return self['tbi_dvc_path']

    def get_tbi_code_vcs_path(self):
        return self['tbi_code_vcs_path']

    def get_tbi_training_command(self):
        return self['tbi_training_command']

    def get_tbi_validating_command(self):
        return self['tbi_validating_command']

    def get_tbi_testing_command(self):
        return self['tbi_testing_command']

    def get_tbi_config_vcs_path(self):
        return self['tbi_config_vcs_path']

    def get_tbi_parallel_execution(self):
        return self['tbi_parallel_execution']

    def __getitem__(self, key):
        return self.data[key]
