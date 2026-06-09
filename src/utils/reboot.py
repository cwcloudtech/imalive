import logging
import subprocess


_logger = logging.getLogger(__name__)


def reboot_host() -> None:
    try:
        subprocess.run(["sudo", "reboot"], check=False)
    except Exception as exc:
        _logger.error("Unable to execute reboot command: %s", exc)
