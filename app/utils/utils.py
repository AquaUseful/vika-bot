import json


# Check if object is json serializable
def is_jsonable(obj):
    try:
        json.dumps(obj)
    except (TypeError, OverflowError):
        return False
    return True
