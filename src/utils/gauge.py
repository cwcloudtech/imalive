import re

from prometheus_client import Gauge
from opentelemetry.metrics import Observation

from utils.common import is_not_empty, sanitize_metric_name
from utils.otel import get_otel_meter

_numeric_value_pattern = r"-?\d+\.?\d*"
_current_gauge_values = {}
_current_gauge_labels = {}

def create_gauge(name, description, labels = []):
    name = sanitize_metric_name(name)
    _current_gauge_values[name] = 0.0

    def observable_gauge_func(_):
        yield Observation(_current_gauge_values[name], _current_gauge_labels[name])

    get_otel_meter().create_observable_gauge(
        name = name,
        description = description,
        callbacks=[observable_gauge_func]
    )

    return Gauge(
        name,
        description,
        labelnames=labels
    ) if is_not_empty(labels) else Gauge(
        name,
        description
    )

def set_gauge(gauge, value, labels = {}):
    match = re.search(_numeric_value_pattern, "{}".format(value))

    if match:
        val = float(match.group())
        if is_not_empty(labels) and isinstance(labels, dict):
            gauge.labels(**labels).set(val)
            _current_gauge_labels[gauge._name] = labels
        else:
            gauge.set(val)
            _current_gauge_labels[gauge._name] = {}
        _current_gauge_values[gauge._name] = val
