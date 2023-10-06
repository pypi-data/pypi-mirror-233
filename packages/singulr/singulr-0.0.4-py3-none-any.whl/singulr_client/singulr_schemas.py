from pydantic import BaseModel, Field
import typing, hashlib, pickle
from langchain.callbacks.tracers.schemas import Run
from enum import Enum
import dataclasses
import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from singulr_client.utils import _safe_serialize
from singulr_client.env.environment import Environment


class StatusCode(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return str(self.value)


class StatusCode(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return str(self.value)


class SpanKind(str, Enum):
    LLM = "LLM"
    CHAIN = "CHAIN"
    AGENT = "AGENT"
    TOOL = "TOOL"

    def __str__(self) -> str:
        return str(self.value)


@dataclass()
class Result:
    inputs: Optional[Dict[str, Any]] = field(default=None)
    outputs: Optional[Dict[str, Any]] = field(default=None)


@dataclass()
class Span:
    span_id: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    parent_span_id: Optional[str] = field(default=None)
    trace_id: Optional[str] = field(default=None)
    start_time_millis: Optional[int] = field(default=None)
    end_time_millis: Optional[int] = field(default=None)
    status_code: Optional[StatusCode] = field(default=None)
    status_message: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    sub_type: Optional[str] = field(default=None)
    attributes: Optional[Dict[str, Any]] = field(default=None)
    results: Optional[List[Result]] = field(default=None)
    child_spans: Optional[List["Span"]] = field(default=None)

    def add_attribute(self, key: str, value: Any, at_type: str, type: str) -> None:
        # if self.attributes is None:
        #     self.attributes = {}
        # self.attributes[key] = value
        attribute = {
            "@type": at_type,
            "key": key,
            "type": value,
            "value": value
        }
        return attribute

    def add_named_result(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        if self.results is None:
            self.results = []
        self.results.append(Result(inputs, outputs))

    def add_child_span(self, span: "Span") -> None:
        if self.child_spans is None:
            self.child_spans = []
        self.child_spans.append(span)


@dataclass()
class TraceTree:
    trace_id: str = field(default=None)
    environment: Environment = Field(default_factory={})
    root_span: Span = field(default=None)


class TraceAttribute:
    """Descriptor for accessing and setting attributes of the `Trace` class."""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: "Trace", owner: type) -> Any:
        return getattr(instance._span, self.name)

    def __set__(self, instance: "Trace", value: Any) -> None:
        setattr(instance._span, self.name, value)


def _hash_id(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:16]


def generate_env_variables(run: Run):
    return {}


class SingulrTraceTree():
    """Media object for trace tree data.

    Arguments:
        root_span (Span): The root span of the trace tree.
        model_dict (dict, optional): A dictionary containing the model dump.
            NOTE: model_dict is a completely-user-defined dict. The UI will render
            a JSON viewer for this dict, giving special treatment to dictionaries
            with a `_kind` key. This is because model vendors have such different
            serialization formats that we need to be flexible here.
    """

    def __init__(
            self,
            root_span: Span,
            model_dict: typing.Optional[dict] = None,
            environment_info: Environment = None
    ):
        super().__init__()
        self._root_span = root_span
        self._model_dict = model_dict
        self._environment_info = environment_info

    def generate_trace_id(self, run: Run):
        json_str = _safe_serialize(run)
        return _hash_id(json_str)

    def to_json(self) -> dict:
        res = {}
        if self._model_dict is not None:
            res["trace_id"] = self.generate_trace_id(self._model_dict)
            res["model_dict_dumps"] = _safe_serialize(self._model_dict)
        res["root_span_dumps"] = _safe_serialize(dataclasses.asdict(self._root_span))
        environment = _safe_serialize(dataclasses.asdict(self._environment_info))
        trace_tree = {"trace_id": res["trace_id"], "root_span": res["root_span_dumps"], "environment": environment}
        print("trace_tree: \n {}".format(trace_tree))
        return trace_tree

    def is_bound(self) -> bool:
        return True
