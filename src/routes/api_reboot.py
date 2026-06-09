import os

from fastapi import APIRouter, BackgroundTasks, Header
from fastapi.responses import JSONResponse

from utils.common import is_empty
from utils.counter import create_counter, increment_counter
from utils.otel import get_otel_tracer
from utils.reboot import reboot_host

router = APIRouter()
_counter = create_counter("reboot_api_counter", "Reboot API counter")
_passphrase_env = "IMALIVE_REBOOT_PASSPHRASE"

@router.post("")
def post_reboot(
    background_tasks: BackgroundTasks,
    x_reboot_passphrase: str = Header(default=None, alias="X-Reboot-Passphrase")
):
    with get_otel_tracer().start_as_current_span("imalive-reboot-post-route"):
        increment_counter(_counter)

        configured_passphrase = os.getenv(_passphrase_env)
        if is_empty(configured_passphrase):
            return JSONResponse(
                content={
                    "status": "ko",
                    "message": "Service Unavailable: Reboot endpoint is disabled"
                },
                status_code=503
            )

        if x_reboot_passphrase != configured_passphrase:
            return JSONResponse(
                content={
                    "status": "ko",
                    "message": "Forbidden: Incorrect or missing passphrase"
                },
                status_code=403
            )

        background_tasks.add_task(reboot_host)
        return JSONResponse(
            content={
                "status": "ok",
                "message": "Reboot initiated"
            },
            status_code=202
        )
