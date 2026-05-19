import importlib.util
import unittest
from pathlib import Path


def load_hotmail_helper():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "hotmail_helper.py"
    spec = importlib.util.spec_from_file_location("hotmail_helper", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hotmail_helper = load_hotmail_helper()


class HotmailHelperCliTest(unittest.TestCase):
    def test_normalize_server_port_uses_default_when_empty(self):
        self.assertEqual(hotmail_helper.normalize_server_port(None), 17373)
        self.assertEqual(hotmail_helper.normalize_server_port(""), 17373)

    def test_normalize_server_port_validates_range(self):
        self.assertEqual(hotmail_helper.normalize_server_port("18080"), 18080)
        with self.assertRaises(ValueError):
            hotmail_helper.normalize_server_port("0")
        with self.assertRaises(ValueError):
            hotmail_helper.normalize_server_port("70000")

    def test_resolve_server_config_reads_cli_and_environment(self):
        config = hotmail_helper.resolve_server_config(
            ["--port", "18080"],
            environ={},
        )
        self.assertEqual(config["host"], "127.0.0.1")
        self.assertEqual(config["port"], 18080)

        env_config = hotmail_helper.resolve_server_config(
            [],
            environ={"HOTMAIL_HELPER_HOST": "0.0.0.0", "HOTMAIL_HELPER_PORT": "19090"},
        )
        self.assertEqual(env_config["host"], "0.0.0.0")
        self.assertEqual(env_config["port"], 19090)


if __name__ == "__main__":
    unittest.main()
