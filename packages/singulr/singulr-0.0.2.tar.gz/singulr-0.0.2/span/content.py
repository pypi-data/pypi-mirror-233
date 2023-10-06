from enum import Enum
from typing import Optional, Union, Dict


class ContentType(str, Enum):
    GENERATION = "GENERATION"
    TEXT_DOCUMENT = "TEXT_DOCUMENT"


class KeyedContent:
    def __init__(self, key: str, content: str, content_type: ContentType):
        self.key: str = key
        self.content: str = content
        self.content_type: ContentType = content_type

    def __str__(self) -> str:
        return str(self.value)

    def to_json(self) -> dict:
        return self.value

    def to_dict(self):
        return {
            "key": self.key,
            "content_type": self.content_type.value,
            "content": self.content
        }


class GenerationDocument(KeyedContent):
    def __init__(self, key, content):
        super().__init__(key, content, ContentType.GENERATION)
        self.generation_info: GenerationInfo = GenerationInfo()

    def get_key(self) -> str:
        return self.key

    def get_content(self) -> str:
        return self.content

    def get_content_type(self) -> ContentType:
        return self.content_type

    def to_dict(self):
        return {
            "@type": "generation_content",
            "key": self.key,
            "content_type": self.content_type.value,
            "content": self.content
        }


class GenerationInfo:
    def __init__(self, finish_reason=None):
        self.finish_reason: Optional[str] = finish_reason

    def get_finish_reason(self) -> Optional[str]:
        return self.finish_reason


class TextDocument(KeyedContent):
    def __init__(self, key, content):
        super().__init__(key, content, ContentType.TEXT_DOCUMENT)
        self.document_type: DocumentType = DocumentType.TEXT
        self.metadata: DocumentMetadata = None

    def get_key(self) -> str:
        return self.key

    def get_content(self) -> str:
        return self.content

    def get_content_type(self) -> ContentType:
        return self.content_type

    def to_dict(self):
        return {
            "@type": "text_content",
            "key": self.key,
            "content_type": self.content_type.value,
            "content": self.content,
            "document_type": self.document_type.value,
            "metadata": self.metadata.to_dict() if self.metadata else None
        }


class DocumentMetadata:
    def __init__(self):
        self.source: Optional[str] = None
        self.pointer: Optional[int] = None

    def get_source(self) -> Optional[str]:
        return self.source

    def get_pointer(self) -> Optional[int]:
        return self.pointer


    def to_dict(self) -> Dict[str, any]:
        metadata_dict = {
            "source": self.source,
            "pointer": self.pointer
        }
        # Remove fields with None values
        metadata_dict = {k: v for k, v in metadata_dict.items() if v is not None}
        return metadata_dict


class DocumentType(Enum):
    TEXT = "TEXT"
    ADDRESSABLE_CTX_DOCUMENT = "ADDRESSABLE_CTX_DOCUMENT"
