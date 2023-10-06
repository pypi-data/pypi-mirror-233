# Created by msinghal at 11/09/23
from enum import Enum
from typing import List, Optional, Dict, Any
from singulr_client.span.result import Result
from singulr_client.span.primitive_attribute import PrimitiveAttribute
from dataclasses import dataclass, field
from pydantic import Field, BaseModel

class SpanType(Enum):
    UNKNOWN = "UNKNOWN"
    LLM = "LLM"
    CHAIN = "CHAIN"
    TOOL = "TOOL"
    AGENT = "AGENT"

    def __str__(self) -> str:
        return str(self.value)


class StatusCode(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return str(self.value)



class Span(object):
    def __init__(
        self,
        span_id: Optional[str] = None,
        name: Optional[str] = None,
        parent_span_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        start_time_millis: Optional[int] = None,
        end_time_millis: Optional[int] = None,
        status_code: Optional[StatusCode] = None,
        status_message: Optional[str] = None,
        type: Optional[SpanType] = None,
        sub_type: Optional[str] = None,
        attributes: Optional[List[PrimitiveAttribute]] = None,
        results: Optional[List[Result]] = None,
        child_spans: Optional[List["Span"]] = None,
    ):
        self.span_id = span_id
        self.name = name
        self.parent_span_id = parent_span_id
        self.trace_id = trace_id
        self.start_time_millis = start_time_millis
        self.end_time_millis = end_time_millis
        self.status_code = status_code
        self.status_message = status_message
        self.type = type
        self.sub_type = sub_type
        self.attributes = attributes if attributes is not None else []
        self.results = results if results is not None else []
        self.child_spans = child_spans if child_spans is not None else []

    def add_attribute(self, key: str, value: Any, at_type: str, type: str) -> None:
        # if self.attributes is None:
        #     self.attributes = {}
        # self.attributes[key] = value
        attr = {
            "@type": at_type,
            "key": key,
            "type": type,
            "value": value
        }
        return attr

    def add_named_result(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        if self.results is None:
            self.results = []
        self.results.append(Result(inputs, outputs))

    def add_child_span(self, span: "Span") -> None:
        if self.child_spans is None:
            self.child_spans = []
        self.child_spans.append(span)

    def get_span_id(self) -> Optional[str]:
        return self.span_id

    def set_span_id(self, span_id: str) -> None:
        self.span_id = span_id

    def get_name(self) -> Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_parent_span_id(self) -> Optional[str]:
        return self.parent_span_id

    def set_parent_span_id(self, parent_span_id: str) -> None:
        self.parent_span_id = parent_span_id

    def get_trace_id(self) -> Optional[str]:
        return self.trace_id

    def set_trace_id(self, trace_id: str) -> None:
        self.trace_id = trace_id

    def get_start_time_millis(self) -> Optional[int]:
        return self.start_time_millis

    def set_start_time_millis(self, start_time_millis: int) -> None:
        self.start_time_millis = start_time_millis

    def get_end_time_millis(self) -> Optional[int]:
        return self.end_time_millis

    def set_end_time_millis(self, end_time_millis: int) -> None:
        self.end_time_millis = end_time_millis

    def get_status_code(self) -> Optional[StatusCode]:
        return self.status_code

    def set_status_code(self, status_code: StatusCode) -> None:
        self.status_code = status_code

    def get_status_message(self) -> Optional[str]:
        return self.status_message

    def set_status_message(self, status_message: str) -> None:
        self.status_message = status_message

    def get_type(self) -> Optional[SpanType]:
        return self.type

    def set_type(self, type_: SpanType) -> None:
        self.type = type_

    def get_sub_type(self) -> Optional[str]:
        return self.sub_type

    def set_sub_type(self, sub_type: str) -> None:
        self.sub_type = sub_type

    def get_attributes(self) -> List[PrimitiveAttribute]:
        return self.attributes

    def set_attributes(self, attributes: List[PrimitiveAttribute]) -> None:
        self.attributes = attributes

    def get_results(self) -> List[Result]:
        return self.results

    def set_results(self, results: List[Result]) -> None:
        self.results = results

    def get_child_spans(self) -> List["Span"]:
        return self.child_spans

    def set_child_spans(self, child_spans: List["Span"]) -> None:
        self.child_spans = child_spans

    def to_dict(self):
        span_dict = {
            "span_id": self.span_id,
            "name": self.name,
            "parent_span_id": self.parent_span_id,
            "trace_id": self.trace_id,
            "start_time_millis": self.start_time_millis,
            "end_time_millis": self.end_time_millis,
            "status_code": self.status_code.value,
            "status_message": self.status_message,
            "type": self.type.value,
            "sub_type": self.sub_type,
            "attributes": [attr.to_dict() for attr in self.attributes],
            "results": [result.to_dict() for result in self.results],
            "child_spans": [span.to_dict() for span in self.child_spans],
        }
        # Remove fields with None values
        span_dict = {k: v for k, v in span_dict.items() if v is not None}
        return span_dict

