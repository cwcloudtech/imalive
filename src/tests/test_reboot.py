import os
import json

from unittest import TestCase
from unittest.mock import patch
from fastapi import BackgroundTasks

from routes.api_reboot import post_reboot

class TestReboot(TestCase):
    def test_post_reboot_disabled_when_passphrase_not_set(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("IMALIVE_REBOOT_PASSPHRASE", None)

            response = post_reboot(BackgroundTasks())

        payload = json.loads(response.body.decode("utf-8"))

        self.assertEqual(503, response.status_code)
        self.assertEqual("ko", payload["status"])
        self.assertEqual(
            "Service Unavailable: Reboot endpoint is disabled",
            payload["message"]
        )

    def test_post_reboot_forbidden_when_passphrase_is_missing(self):
        with patch.dict(os.environ, {"IMALIVE_REBOOT_PASSPHRASE": "secret"}, clear=False):
            response = post_reboot(BackgroundTasks())

        payload = json.loads(response.body.decode("utf-8"))

        self.assertEqual(403, response.status_code)
        self.assertEqual("ko", payload["status"])
        self.assertEqual(
            "Forbidden: Incorrect or missing passphrase",
            payload["message"]
        )

    def test_post_reboot_forbidden_when_passphrase_is_incorrect(self):
        with patch.dict(os.environ, {"IMALIVE_REBOOT_PASSPHRASE": "secret"}, clear=False):
            response = post_reboot(BackgroundTasks(), x_reboot_passphrase="invalid")

        payload = json.loads(response.body.decode("utf-8"))

        self.assertEqual(403, response.status_code)
        self.assertEqual("ko", payload["status"])
        self.assertEqual(
            "Forbidden: Incorrect or missing passphrase",
            payload["message"]
        )

    def test_post_reboot_accepted_when_passphrase_is_correct(self):
        with patch.dict(os.environ, {"IMALIVE_REBOOT_PASSPHRASE": "secret"}, clear=False):
            background_tasks = BackgroundTasks()
            with patch("routes.api_reboot.reboot_host") as reboot_host_mock:
                response = post_reboot(background_tasks, x_reboot_passphrase="secret")

        payload = json.loads(response.body.decode("utf-8"))

        self.assertEqual(202, response.status_code)
        self.assertEqual("ok", payload["status"])
        self.assertEqual("Reboot initiated", payload["message"])
        self.assertEqual(1, len(background_tasks.tasks))
        self.assertEqual(reboot_host_mock, background_tasks.tasks[0].func)
