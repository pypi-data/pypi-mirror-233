# Created by msinghal at 23/09/23
import platform
import os, socket, psutil
from functools import lru_cache
from typing import Optional

def get_memory():
    try:
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total
    except ImportError:
        total_memory = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')

    return total_memory

def get_process():
    current_pid = os.getpid()
    current_process = psutil.Process(current_pid)
    return {"process_id": current_pid,
            "process_name" : current_process.name(),
            "process_status": current_process.status(),
            "process_start_time" : current_process.create_time()
            }
@lru_cache
def get_langchain_environment() -> Optional[str]:
    try:
        import langchain  # type: ignore

        return langchain.__version__
    except ImportError:
        return None
# @lru_cache(maxsize=1)
# def get_runtime_environment() -> dict:
#     """Get information about the environment."""
#     # Lazy import to avoid circular imports
#     from langchain import __version__
#     current_process_info = get_process()
#     return {
#         "library_version": __version__,
#         "library": "langchain",
#         "platform": platform.platform(),
#         "runtime": "python",
#         "runtime_version": platform.python_version(),
#         "platform_architecure": platform.architecture(),
#         "platform_node": platform.node(),
#         "platform_version": platform.version(),
#         "platform_cpu": os.cpu_count(),
#         "platform_memory": get_memory(),
#         "node_name": socket.gethostname(),
#         "node_ip": socket.gethostbyname(socket.gethostname()),
#         "node_fqdn": socket.getfqdn(),
#         "process_name": current_process_info["process_name"],
#         "process_id": current_process_info["process_id"],
#         "process_status": current_process_info["process_status"],
#         "process_start_time": current_process_info["process_start_time"],
#     }
#

@lru_cache
def get_runtime_environment() -> dict:
    """Get information about the environment."""
    # Lazy import to avoid circular imports
    from langsmith import __version__
    current_process_info = get_process()
    return {
        "sdk_version": __version__,
        "library": "singulr",
        "platform": platform.platform(),
        "runtime": "python",
        "runtime_version": platform.python_version(),
        "langchain_version": get_langchain_environment(),
        "platform_architecure": platform.architecture(),
        "platform_node": platform.node(),
        "platform_version": platform.version(),
        "platform_cpu": os.cpu_count(),
        "platform_memory": get_memory(),
        "node_name": socket.gethostname(),
        "node_ip": socket.gethostbyname(socket.gethostname()),
        "node_fqdn": socket.getfqdn(),
        "process_name": current_process_info["process_name"],
        "process_id":current_process_info["process_id"],
        "process_status": current_process_info["process_status"],
        "process_start_time": current_process_info["process_start_time"],
    }