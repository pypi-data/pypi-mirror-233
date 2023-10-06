from singulr_schemas import *
class Trace:
    """A simplification of WBTraceTree and Span to manage a trace - a collection of spans, their metadata and hierarchy.

    Args:
        name: (str) The name of the root span.
        kind: (str, optional) The kind of the root span.
        status_code: (str, optional) The status of the root span, either "error" or "success".
        status_message: (str, optional) Any status message associated with the root span.
        metadata: (dict, optional) Any additional metadata for the root span.
        start_time_ms: (int, optional) The start time of the root span in milliseconds.
        end_time_ms: (int, optional) The end time of the root span in milliseconds.
        inputs: (dict, optional) The named inputs of the root span.
        outputs: (dict, optional) The named outputs of the root span.
        model_dict: (dict, optional) A json serializable dictionary containing the model architecture details.

    Example:
        .. code-block:: python
        ```
        trace = Trace(
            name="My awesome Model",
            kind="LLM",
            status_code= "SUCCESS",
            metadata={"attr_1": 1, "attr_2": 2,},
            start_time_ms=int(round(time.time() * 1000)),
            end_time_ms=int(round(time.time() * 1000))+1000,
            inputs={"user": "How old is google?"},
            outputs={"assistant": "25 years old"},
            model_dict={"_kind": "openai", "api_type": "azure"}
              )
        run = wandb.init(project=<my_awesome_project>,)
        trace.log("my_trace")
        wandb.finish()
        ```
    """

    name = TraceAttribute()
    status_code = TraceAttribute()
    status_message = TraceAttribute()
    start_time_ms = TraceAttribute()
    end_time_ms = TraceAttribute()

    def __init__(
            self,
            name: str,
            kind: Optional[str] = None,
            status_code: Optional[str] = None,
            status_message: Optional[str] = None,
            metadata: Optional[dict] = None,
            start_time_ms: Optional[int] = None,
            end_time_ms: Optional[int] = None,
            inputs: Optional[dict] = None,
            outputs: Optional[dict] = None,
            model_dict: Optional[dict] = None,
    ):
        self._span = self._assert_and_create_span(
            name=name,
            kind=kind,
            status_code=status_code,
            status_message=status_message,
            metadata=metadata,
            start_time_ms=start_time_ms,
            end_time_ms=end_time_ms,
            inputs=inputs,
            outputs=outputs,
        )
        if model_dict is not None:
            assert isinstance(model_dict, dict), "Model dict must be a dictionary"
        self._model_dict = model_dict

    def _assert_and_create_span(
            self,
            name: str,
            kind: Optional[str] = None,
            status_code: Optional[str] = None,
            status_message: Optional[str] = None,
            metadata: Optional[dict] = None,
            start_time_ms: Optional[int] = None,
            end_time_ms: Optional[int] = None,
            inputs: Optional[dict] = None,
            outputs: Optional[dict] = None,
    ) -> Span:
        """Utility to assert the validity of the span parameters and create a span object.

        Args:
            name: The name of the span.
            kind: The kind of the span.
            status_code: The status code of the span.
            status_message: The status message of the span.
            metadata: Dictionary of metadata to be logged with the span.
            start_time_ms: Start time of the span in milliseconds.
            end_time_ms: End time of the span in milliseconds.
            inputs: Dictionary of inputs to be logged with the span.
            outputs: Dictionary of outputs to be logged with the span.

        Returns:
            A Span object.
        """
        if kind is not None:
            assert (
                    kind.upper() in SpanKind.__members__
            ), "Invalid span kind, can be one of 'LLM', 'AGENT', 'CHAIN', 'TOOL'"
            kind = SpanKind(kind.upper())
        if status_code is not None:
            assert (
                    status_code.upper() in StatusCode.__members__
            ), "Invalid status code, can be one of 'SUCCESS' or 'ERROR'"
            status_code = StatusCode(status_code.upper())
        if inputs is not None:
            assert isinstance(inputs, dict), "Inputs must be a dictionary"
        if outputs is not None:
            assert isinstance(outputs, dict), "Outputs must be a dictionary"
        if inputs or outputs:
            result = Result(inputs=inputs, outputs=outputs)
        else:
            result = None

        if metadata is not None:
            assert isinstance(metadata, dict), "Metadata must be a dictionary"

        return Span(
            name=name,
            span_kind=kind,
            status_code=status_code,
            status_message=status_message,
            attributes=metadata,
            start_time_ms=start_time_ms,
            end_time_ms=end_time_ms,
            results=[result] if result else None,
        )

    def add_child(
            self,
            child: "Trace",
    ) -> "Trace":
        """Utility to add a child span to the current span of the trace.

        Args:
            child: The child span to be added to the current span of the trace.

        Returns:
            The current trace object with the child span added to it.
        """
        self._span.add_child_span(child._span)
        if self._model_dict is not None and child._model_dict is not None:
            self._model_dict.update({child._span.name: child._model_dict})
        return self

    def add_inputs_and_outputs(self, inputs: dict, outputs: dict) -> "Trace":
        """Add a result to the span of the current trace.

        Args:
            inputs: Dictionary of inputs to be logged with the span.
            outputs: Dictionary of outputs to be logged with the span.

        Returns:
            The current trace object with the result added to it.
        """
        if self._span.results is None:
            result = Result(inputs=inputs, outputs=outputs)
            self._span.results = [result]
        else:
            result = Result(inputs=inputs, outputs=outputs)
            self._span.results.append(result)
        return self

    def add_metadata(self, metadata: dict) -> "Trace":
        """Add metadata to the span of the current trace."""
        if self._span.attributes is None:
            self._span.attributes = metadata
        else:
            self._span.attributes.update(metadata)
        return self

    @property
    def metadata(self) -> Optional[Dict[str, str]]:
        """Get the metadata of the trace.

        Returns:
            Dictionary of metadata.
        """
        return self._span.attributes

    @metadata.setter
    def metadata(self, value: Dict[str, str]) -> None:
        """Set the metadata of the trace.

        Args:
            value: Dictionary of metadata to be set.
        """
        if self._span.attributes is None:
            self._span.attributes = value
        else:
            self._span.attributes.update(value)

    @property
    def inputs(self) -> Optional[Dict[str, str]]:
        """Get the inputs of the trace.

        Returns:
            Dictionary of inputs.
        """
        return self._span.results[-1].inputs if self._span.results else None

    @inputs.setter
    def inputs(self, value: Dict[str, str]) -> None:
        """Set the inputs of the trace.

        Args:
            value: Dictionary of inputs to be set.
        """
        if self._span.results is None:
            result = Result(inputs=value, outputs={})
            self._span.results = [result]
        else:
            result = Result(inputs=value, outputs=self._span.results[-1].outputs)
            self._span.results.append(result)

    @property
    def outputs(self) -> Optional[Dict[str, str]]:
        """Get the outputs of the trace.

        Returns:
            Dictionary of outputs.
        """
        return self._span.results[-1].outputs if self._span.results else None

    @outputs.setter
    def outputs(self, value: Dict[str, str]) -> None:
        """Set the outputs of the trace.

        Args:
            value: Dictionary of outputs to be set.
        """
        if self._span.results is None:
            result = Result(inputs={}, outputs=value)
            self._span.results = [result]
        else:
            result = Result(inputs=self._span.results[-1].inputs, outputs=value)
            self._span.results.append(result)

    @property
    def kind(self) -> Optional[str]:
        """Get the kind of the trace.

        Returns:
            The kind of the trace.
        """
        return self._span.span_kind.value if self._span.span_kind else None

    @kind.setter
    def kind(self, value: str) -> None:
        """Set the kind of the trace.

        Args:
            value: The kind of the trace to be set.
        """
        assert (
                value.upper() in SpanKind.__members__
        ), "Invalid span kind, can be one of 'LLM', 'AGENT', 'CHAIN', 'TOOL'"
        self._span.span_kind = SpanKind(value.upper())