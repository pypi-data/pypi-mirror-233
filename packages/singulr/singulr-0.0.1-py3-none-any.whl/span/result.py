from singulr_client.span.content import KeyedContent
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union


class Result:
    def __init__(self):
        self.inputs: List[KeyedContent] = []
        self.outputs: List[KeyedContent] = []

    def get_inputs(self) -> List[KeyedContent]:
        return self.inputs

    def set_inputs(self, inputs: List[KeyedContent]) -> None:
        self.inputs = inputs

    def get_outputs(self) -> List[KeyedContent]:
        return self.outputs

    def set_outputs(self, outputs: List[KeyedContent]) -> None:
        self.outputs = outputs

    def to_dict(self) -> Dict[str, any]:
        result_dict = {
            "inputs": [input_item.to_dict() for input_item in self.inputs],
            "outputs": [output_item.to_dict() for output_item in self.outputs]
        }
        return result_dict
