import re

def is_not_empty (var):
    if isinstance(var, bool):
        return var
    elif isinstance(var, int):
        return not var == 0
    elif isinstance(var, list) or isinstance(var, dict):
        return len(var) > 0
    empty_chars = ["", "null", "nil", "false", "none"]
    return var is not None and not any(c == "{}".format(var).lower() for c in empty_chars)

def is_true (var):
    if isinstance(var, bool):
        return var
    false_char = ["false", "ko", "no", "off"]
    return is_not_empty(var) and not any(c == "{}".format(var).lower() for c in false_char)

def is_false (var):
    return not is_true(var)

def is_empty (var):
    return not is_not_empty(var)

def is_empty_key(vdict, key):
    return is_empty(vdict) or not key in vdict or is_empty(vdict[key])

def is_not_empty_key(vdict, key):
    return not is_empty_key(vdict, key)

def del_key_if_exists(vdict, key):
    if is_not_empty_key(vdict, key):
        del vdict[key]

def get_or_else(vdict, key, default):
    return default if is_empty_key(vdict, key) else vdict[key]

def is_numeric (var):
    if isinstance(var, int):
        return True
    return is_not_empty(var) and str(var).isnumeric()

def is_not_numeric (var):
    return not is_numeric(var)

def is_disabled (var):
    return is_empty(var) or "changeit" in var

def is_enabled(var):
    return not is_disabled(var)

def is_uuid (var):
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89a-bA-B][0-9a-f]{3}-[0-9a-f]{12}$'
    return bool(re.match(pattern, var))

def is_not_uuid (var):
    return not is_uuid(var)

_allowed_chars_metric_pattern = re.compile(r'[^a-zA-Z0-9]')
def sanitize_metric_name(name: str):
    return re.sub(_allowed_chars_metric_pattern, '_', name)

def sanitize_header_name(name: str) -> str:
    return '-'.join(word.capitalize() for word in name.split('-'))
