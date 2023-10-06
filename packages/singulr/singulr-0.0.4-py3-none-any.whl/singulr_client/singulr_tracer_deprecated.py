# import json
# import logging
# from langchain.callbacks.tracers.schemas import Run
# from singulr_client.clients import singulr_ingestion_client
# from singulr_client.mapper.env_generator import EnvironmentGenerator
# from singulr_client.mapper.span_generator import SpanGenerator
# from singulr_client.payload.ingestion_payload import IngestionData
# from singulr_client.trace.trace import TraceTree
# from singulr_client.utils import generate_trace_id
# from typing import Dict
#
#
# # Created by msinghal at 05/10/23
# class SingulrTracerGenerator():
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.run_map: Dict[str, Run] = {}
#
#     def _log_trace_from_run(self, run: Run) -> None:
#         model_dict = SpanGenerator().process_model(run)
#         trace_id = generate_trace_id(model_dict)
#         environment = EnvironmentGenerator().process_environments(run)
#         root_span = SpanGenerator().process_span(run, trace_id)
#
#         if root_span is None:
#             return
#
#         model_trace = TraceTree(trace_id=trace_id,
#                                 environment=environment,
#                                 root_span=root_span)
#
#         trace = model_trace.to_json()
#         # json_string = json.dumps(trace)
#
#         ingestion_payload = IngestionData(trace_id, trace)
#         print("sending traces to ingestion service {}".format(json.dumps(ingestion_payload.to_dict())))
#         try:
#             response = singulr_ingestion_client.Ingestion_Client().ingest_payload(ingestion_payload.to_dict())
#         except:
#             import traceback
#             print("exception while tracing {}".format(traceback.print_exc()))
#             return None
#
#         if response.status_code == 200:
#             print("sent successfully")
#         else:
#             print(response.status_code)
#
#     def start_trace(self, run: Run) -> None:
#         """Start a trace for a run."""
#         if run.parent_run_id:
#             parent_run = self.run_map[str(run.parent_run_id)]
#             if parent_run:
#                 if hasattr(parent_run, "child_runs") and isinstance(parent_run.child_runs, list):
#                     parent_run.child_runs.append(run)
#                 else:
#                     setattr(parent_run, 'child_runs', [run])
#             else:
#                 logging.debug(f"Parent run with UUID {run.parent_run_id} not found.")
#         self.run_map[str(run.id)] = run
#
#     def end_trace(self, run: Run) -> None:
#         """End a trace for a run."""
#         if not run.parent_run_id:
#             self.run_map.get(str(run.id))
#             run.extra = self.run_map.get(str(run.id)).extra
#             self._persist_run(run)
#         else:
#             parent_run = self.run_map.get(str(run.parent_run_id))
#             if parent_run is None:
#                 logging.debug(f"Parent run with UUID {run.parent_run_id} not found.")
#             elif (
#                     hasattr(run, 'child_execution_order') and run.child_execution_order is not None
#                     and parent_run.child_execution_order is not None
#                     and run.child_execution_order > parent_run.child_execution_order
#             ):
#                 parent_run.child_execution_order = run.child_execution_order
#         self.run_map.pop(str(run.id))
#
#     def _persist_run(self, run: Run) -> None:
#         """Persist a run."""
#         self._log_trace_from_run(run)
