import hashlib
import time
from typing import Any
from langchain.callbacks.tracers.schemas import Run

def _hash_id(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:16]


def _serialize_io(run_inputs: dict) -> dict:
    from google.protobuf.json_format import MessageToJson
    from google.protobuf.message import Message

    serialized_inputs = {}
    for key, value in run_inputs.items():
        if isinstance(value, Message):
            serialized_inputs[key] = MessageToJson(value)
        elif key == "input_documents":
            serialized_inputs.update(
                {f"input_document_{i}": json.dumps(doc) for i, doc in enumerate(value)}
            )
        else:
            serialized_inputs[key] = value
    return serialized_inputs


def _fallback_serialize(obj: Any) -> str:
    try:
        return f"<<non-serializable: {type(obj).__qualname__}>>"
    except Exception:
        return "<<non-serializable>>"


def _safe_serialize(obj: dict) -> str:
    try:
        return json.dumps(
            obj,
            skipkeys=True,
            default=_fallback_serialize,
        )
    except Exception:
        return "{}"

import json

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict') and callable(obj.to_dict):
            return obj.to_dict()
        elif isinstance(obj, list):
            return [self.default(item) for item in obj]
        return super().default(obj)

def generate_trace_id(run: Run):
    json_str = _safe_serialize(run)
    timestamp = str(time.time())  # Add a timestamp (current time) to the input string
    input_str = json_str + timestamp
    return _hash_id(input_str)