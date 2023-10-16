import unittest

from smi_python_tbi_parser.tbi import parse_tbi


class ITExample(unittest.TestCase):

    def setUp(self):
        pass

    def test_example(self):
        tbi = parse_tbi("./test/resources/tbi-376bdfaa-1195-11ee-be56-0242ac120002.yaml")
        self.assertEqual(tbi['name'], "TBI name")
        self.assertEqual(tbi.get_name(), "TBI name")
        self.assertEqual(tbi['description'], "TBI description")
        self.assertEqual(tbi.get_description(), "TBI description")
        self.assertEqual(tbi['authors'][0], "Imre Tabur <imre.tabur@mail.ee>")
        self.assertEqual(tbi.get_authors()[0], "Imre Tabur <imre.tabur@mail.ee>")
        self.assertEqual(tbi['materials'][0], "example.doc")
        self.assertEqual(tbi.get_materials()[0], "example.doc")
        self.assertEqual(tbi['external_processing_engine']['config']['jenkins_pipeline']['tbi_dvc_path'],
                         "path/to/dvc (ML software config can also be there, because config is also data)")
        self.assertEqual(tbi.get_external_processing_engine()['config']['jenkins_pipeline']['tbi_dvc_path'],
                         "path/to/dvc (ML software config can also be there, because config is also data)")
        self.assertEqual(tbi.get_external_processing_engine().get_type(),
                         "Camunda (can be missing, for passing directly to Jenkins)")
        self.assertEqual(tbi.get_external_processing_engine().get_process_id(),
                         "MLSprint (can be missing, for passing directly to Jenkins)")
        self.assertEqual(tbi.get_external_processing_engine().get_config().get_tbi_process_uri(),
                         "url/uri/path/to/bpmn/file.bpmn (can be missing, for passing directly to Jenkins)")
        self.assertEqual(tbi.get_external_processing_engine().get_config().get_jenkins_pipeline().get_tbi_vcs_url(),
                         "https://example.com/tbi/git/repo/with/Jenkinsfile/pipeline.git  (can be missing, Jenkins already have pipeline execution configured)")

        self.assertEqual(tbi.get_external_processing_engine().get_config().get_jenkins_pipeline().get_tbi_dvc_path(),
                         "path/to/dvc (ML software config can also be there, because config is also data)")
        self.assertEqual(
            tbi.get_external_processing_engine().get_config().get_jenkins_pipeline().get_tbi_code_vcs_path(),
            "path/to/dvc_code (ML software to build, or use tbi_training_command and tbi_testing_command)")
        self.assertEqual(
            tbi.get_external_processing_engine().get_config().get_jenkins_pipeline().get_tbi_training_command(),
            "command (to execute for training)")
        self.assertEqual(
            tbi.get_external_processing_engine().get_config().get_jenkins_pipeline().get_tbi_validating_command(),
            "command (to execute for validating)")
        self.assertEqual(
            tbi.get_external_processing_engine().get_config().get_jenkins_pipeline().get_tbi_testing_command(),
            "command (to execute for testing)")
        self.assertEqual(
            tbi.get_external_processing_engine().get_config().get_jenkins_pipeline().get_tbi_config_vcs_path(),
            "path/to/config (ML software config to use, can be unset)")
        self.assertEqual(
            tbi.get_external_processing_engine().get_config().get_jenkins_pipeline().get_tbi_parallel_execution(),
            True)
        self.assertEqual(tbi.get_changelog().get_added()[0], "Added example thing")
        self.assertEqual(tbi.get_changelog().get_removed()[0], "Removed example thing")
        self.assertEqual(tbi.get_changelog().get_changed()[0], "Changed example thing")
        self.assertEqual(tbi.get_changelog().get_fixed()[0], "Fixed example thing")


if __name__ == '__main__':
    unittest.main()
