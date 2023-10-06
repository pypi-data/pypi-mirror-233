# Created by msinghal at 04/10/23
from __future__ import annotations
import singulr_client.clients.singulr_apis as singulr_apis
import logging
import os, json
import pandas as pd
import time
from datetime import datetime

from functools import lru_cache
from typing import (
    TYPE_CHECKING,
    Any,
    DefaultDict,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

from singulr_client.clients.utils import get_runtime_environment

logger = logging.getLogger(__name__)

def _serialize_json(obj: Any) -> str:
    """Serialize an object to JSON.

    Parameters
    ----------
    obj : Any
        The object to serialize.

    Returns
    -------
    str
        The serialized JSON string.

    Raises
    ------
    TypeError
        If the object type is not serializable.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return str(obj)

class LangChainRunClient:
    """Client for interacting with the Singulr SDK"""
    def create_run(
            self,
            name: str,
            inputs: Dict[str, Any],
            run_type: str,
            *,
            execution_order: Optional[int] = None,
            **kwargs: Any,
    ) -> None:
        project_name = kwargs.pop(
            "project_name",
            kwargs.pop(
                "session_name",
                os.environ.get(
                    # TODO: Deprecate LANGCHAIN_SESSION
                    "LANGCHAIN_PROJECT",
                    os.environ.get("LANGCHAIN_SESSION", "default"),
                ),
            ),
        )
        run_create = {
            **kwargs,
            "session_name": project_name,
            "name": name,
            "inputs": inputs,
            "run_type": run_type,
            "execution_order": execution_order if execution_order is not None else 1,
        }
        run_extra = cast(dict, run_create.setdefault("extra", {}))
        runtime = run_extra.setdefault("runtime", {})

        runtime_env = get_runtime_environment()
        run_extra["runtime"] = {**runtime_env, **runtime}
        print("client is making call to local server to create run {}".format(run_create))
        file_name = str(run_create["id"]) + "-" + str(int(time.time()))
        df = pd.DataFrame.from_dict([run_create])
        df = df.astype(str)
        df.to_parquet("~/Downloads/traces/create_event/{}.parquet".format(file_name), engine='pyarrow')
        return {"message": "Run created successfully"}
        #singulr_apis.create_run(json.dumps(run_create, default=_serialize_json))

    def update_run(
            self,
            run_id,
            **kwargs: Any,
    ) -> None:
        print("client is making call to local server to update run {}".format(run_id))
        file_name = str(kwargs["id"]) + "-" + str(int(time.time()))
        df = pd.DataFrame.from_dict([kwargs])
        df = df.astype(str)
        df.to_parquet("~/Downloads/traces/update_event/{}.parquet".format(file_name), engine='pyarrow')
        #singulr_apis.update_run(run_id, json.dumps(kwargs, default=_serialize_json))
        return {"message": f"Run {run_id} updated successfully"}

