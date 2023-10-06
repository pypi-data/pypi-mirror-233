# Created by msinghal at 11/09/23
import abc
from enum import Enum
from typing import Type

from typing_extensions import TypedDict
import attr

from pydantic import BaseModel


class AttributeType(str, Enum):
    UNKNOWN = "UNKNOWN"
    PRIMITIVE_STRING = "PRIMITIVE_STRING"
    PRIMITIVE_INT = "PRIMITIVE_INT"
    LLM_INVOCATION = "LLM_INVOCATION"
    PROMPT_TEMPLATE = "PROMPT_TEMPLATE"
    LLM_STATS = "LLM_STATS"

    def __str__(self) -> str:
        return str(self.value)


class Attribute(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_key(self) -> str:
        pass

    @abc.abstractmethod
    def get_type(self) -> AttributeType:
        pass


class BaseAttribute(Attribute):
    def __init__(self, key: str, type: AttributeType):
        self.key = key
        self.type = type

    def get_key(self) -> str:
        pass

    def get_type(self) -> AttributeType:
        pass

    def to_dict(self):
        return {
            "key": self.key,
            "type": self.type.value,
        }


class PrimitiveAttribute(BaseAttribute, metaclass=abc.ABCMeta):
    def __init__(self, key: str, type: AttributeType) -> object:
        super().__init__(key, type)

    def get_key(self) -> str:
        return self.key

    def get_type(self) -> AttributeType:
        return self.type

    def to_dict(self):
        return {
            "key": self.key,
            "type": self.type.value,
        }


class StringAttribute(PrimitiveAttribute):
    def __init__(self, key: str, value: str) -> object:
        super().__init__(key, AttributeType.PRIMITIVE_STRING)
        self.value = value

    def to_json(self):
        return {
            "@type": "string",
            "key": self.key,
            "type": self.type.value,
            "value": self.value
        }

    def to_dict(self):
        return {
            "@type": "str",
            "key": self.key,
            "type": self.type.value,
            "value": self.value
        }


class IntAttribute(PrimitiveAttribute):
    def __init__(self, key: str, value: int) -> object:
        super().__init__(key, AttributeType.PRIMITIVE_INT)
        self.type = AttributeType.PRIMITIVE_INT
        self.value: int = value

    def to_json(self):
        return {
            "@type": "int",
            "key": self.key,
            "type": self.type.value,
            "value": self.value
        }

    def to_dict(self):
        return {
            "@type": "int",
            "key": self.key,
            "type": self.type.value,
            "value": self.value
        }


if __name__ == '__main__':
    s = IntAttribute(key="execution_order", value=1)
    debug = True
