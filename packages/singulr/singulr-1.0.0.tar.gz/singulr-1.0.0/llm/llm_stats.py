from singulr_client.span.primitive_attribute import BaseAttribute, AttributeType


class TokenUsage:
    def __init__(self):
        self.promptTokens: int = 0
        self.completionTokens: int = 0
        self.totalTokens: int = 0

    def get_prompt_tokens(self) -> int:
        return self.promptTokens

    def set_prompt_tokens(self, promptTokens: int):
        self.promptTokens = promptTokens

    def get_completion_tokens(self) -> int:
        return self.completionTokens

    def set_completion_tokens(self, completionTokens: int):
        self.completionTokens = completionTokens

    def get_total_tokens(self) -> int:
        return self.totalTokens

    def set_total_tokens(self, totalTokens: int):
        self.totalTokens = totalTokens


class LLMStats(BaseAttribute):
    LLM_OUTPUT = "llm_output"

    def __init__(self):
        self.subType: str = ""
        self.tokenUsage: TokenUsage = TokenUsage()
        self.modelName: str = ""

    def get_key(self) -> str:
        return self.LLM_OUTPUT

    def get_type(self):
        return AttributeType.LLM_STATS

    # Empty methods for serialization and deserialization
    def set_key(self, key: str):
        pass

    def set_type(self, type_):
        pass

    def get_sub_type(self) -> str:
        return self.subType

    def set_sub_type(self, subType: str):
        self.subType = subType

    def get_token_usage(self) -> TokenUsage:
        return self.tokenUsage

    def set_token_usage(self, tokenUsage: TokenUsage):
        self.tokenUsage = tokenUsage

    def get_model_name(self) -> str:
        return self.modelName

    def set_model_name(self, modelName: str):
        self.modelName = modelName
