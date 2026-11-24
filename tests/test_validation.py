import os
import unittest

class TestVllmServerIntegrity(unittest.TestCase):
    def test_readme_exists(self):
        self.assertTrue(os.path.exists("README.md"), "README.md must be present")

    def test_makefile_exists(self):
        self.assertTrue(os.path.exists("Makefile"), "Makefile must be present")

    def test_ci_workflow_exists(self):
        self.assertTrue(os.path.exists(".github/workflows/ci.yml"), "CI workflow must be present")

    def test_healthcheck_script_exists(self):
        self.assertTrue(os.path.exists("scripts/healthcheck.sh"), "Healthcheck script must be present")

    def test_environment_template_exists(self):
        self.assertTrue(os.path.exists("config/production.env.example"), "Env template must be present")

    def test_gitattributes_exists(self):
        self.assertTrue(os.path.exists(".gitattributes"), ".gitattributes must be present")

    def test_security_policy_exists(self):
        self.assertTrue(os.path.exists("SECURITY.md"), "SECURITY.md must be present")

    def test_architecture_diagram_exists(self):
        self.assertTrue(os.path.exists("docs/architecture.svg"), "docs/architecture.svg must be present")

    def test_dockerfile_configured(self):
        self.assertTrue(os.path.exists("Dockerfile"), "Dockerfile must be present")
        with open("Dockerfile", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("vllm.entrypoints.openai.api_server", content)
        self.assertIn("HEALTHCHECK", content)

    def test_docker_compose_configured(self):
        self.assertTrue(os.path.exists("docker-compose.yml"), "docker-compose.yml must be present")
        with open("docker-compose.yml", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("vllm-head:", content)
        self.assertIn("vllm-worker:", content)
        self.assertIn("driver: nvidia", content)
        self.assertIn("ray", content)

    def test_benchmark_script_exists(self):
        self.assertTrue(os.path.exists("benchmark_throughput.py"), "benchmark_throughput.py must be present")
        with open("benchmark_throughput.py", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("BenchmarkRunner", content)

if __name__ == "__main__":
    unittest.main()
