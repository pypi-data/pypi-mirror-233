# Created by msinghal at 04/10/23
from __future__ import annotations
import singulr_apis
import logging
import os
import weakref

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

from urllib3.util import Retry
from utils import get_runtime_environment

logger = logging.getLogger(__name__)


class Client:
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
        singulr_apis.create_run(run_create)

    def update_run(
            self,
            run_id,
            **kwargs: Any,
    ) -> None:
        print("client is making call to local server to update run {}".format(run_id))
        singulr_apis.update_run(run_id, kwargs)
