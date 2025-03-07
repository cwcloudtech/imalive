from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.counter import create_counter, increment_counter
from utils.otel import get_otel_tracer
from utils.manifests import get_manifest_as_dict

router = APIRouter()
_counter = create_counter("manifest_api_counter", "Manifest API counter")

@router.get("")
def get_manifest():
    with get_otel_tracer().start_as_current_span("imalive-manifest-route"):
        manifest = get_manifest_as_dict()
        increment_counter(_counter)
        if manifest['status'] == 'error':
            return JSONResponse(content=manifest, status_code=500)
        else:
            return manifest
