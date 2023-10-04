# Created by msinghal at 11/09/23
from pydantic import BaseModel, Field
import typing, hashlib, pickle
from langchain.callbacks.tracers.schemas import Run
from enum import Enum
import dataclasses
import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from singulr_client.utils import _safe_serialize


class StatusCode(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return str(self.value)


class MachineInfo:
    def __init__(self, operating_system="Linux", os_version="Ubuntu 20.04", total_memory=8192, cpu_info="Intel Core i7", num_cores=4, architecture="x86_64", network_interfaces=None):
        self.operating_system = operating_system
        self.os_version = os_version
        self.total_memory = total_memory
        self.cpu_info = cpu_info
        self.num_cores = num_cores
        self.architecture = architecture
        self.network_interfaces = network_interfaces if network_interfaces is not None else [NetworkInterface()]

    def to_dict(self):
        return {
            "operating_system": self.operating_system,
            "os_version": self.os_version,
            "total_memory": self.total_memory,
            "cpu_info": self.cpu_info,
            "num_cores": self.num_cores,
            "architecture": self.architecture,
            "network_interfaces": [network_interface.to_dict() for network_interface in self.network_interfaces]
        }

class NetworkInterface:
    def __init__(self, name="en0", mac="bc:d0:74:0e:e8:2c"):
        self.name = name
        self.mac = mac
        self.network = NetworkInfo()


    def to_dict(self):
        return {
            'name': self.name,
            'mac': self.mac,
            'network': self.network.to_dict() if self.network else None
        }
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_mac(self):
        return self.mac

    def set_mac(self, mac):
        self.mac = mac

    def get_network(self):
        return self.network

    def set_network(self, network):
        self.network = network
class NetworkInfo:
    def __init__(self, host_name="fin01.example.com", ip_address="192.168.2.5", subnet="192.168.2.0/24"):
        self.host_name = host_name
        self.ip_address = ip_address
        self.subnet = subnet

    def to_dict(self):
        return {
            "host_name": self.host_name,
            "ip_address": self.ip_address,
            "subnet": self.subnet
        }


class EnvironmentContext:
    def __init__(self, environment_variables=None, command_line_args=None, log_files=None):
        self.environment_variables = environment_variables if environment_variables is not None else {}
        self.command_line_args = command_line_args if command_line_args is not None else []
        self.log_files = log_files if log_files is not None else []

    def to_dict(self):
        return {
            "environment_variables": self.environment_variables,
            "command_line_args": self.command_line_args,
            "log_files": self.log_files
        }


class ProcessInfo:
    def __init__(self, process_path="python chat_bot_app.py", process_id=10000, status="running", listen_ports=None, environment_context=None):
        self.process_path = process_path
        self.process_id = process_id
        self.status = status
        self.listen_ports = listen_ports if listen_ports is not None else []
        self.environment_context = environment_context if environment_context is not None else EnvironmentContext()

    def to_dict(self):
        return {
            "process_path": self.process_path,
            "process_id": self.process_id,
            "status": self.status,
            "listen_ports": self.listen_ports,
            "environment_context": self.environment_context.to_dict()
        }


from typing import List, Dict, Optional, Any


class RuntimeEnvironment:
    def __init__(self, lang_runtime="python", lang_runtime_version="3.11.4", entry_point="main.py", virtual_environment="CONDA", environment="llm-security"):
        self.lang_runtime = lang_runtime
        self.lang_runtime_version = lang_runtime_version
        self.entry_point = entry_point
        self.virtual_environment = virtual_environment
        self.environment = environment

    def to_dict(self):
        return {
            "lang_runtime": self.lang_runtime,
            "lang_runtime_version": self.lang_runtime_version,
            "entry_point": self.entry_point,
            "virtual_environment": self.virtual_environment,
            "environment": self.environment
        }


class SecurityContext:
    def __init__(self, user_id="root", group_id="wheel"):
        self.user_id = user_id
        self.group_id = group_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "group_id": self.group_id
        }


class RequestSecurityContext:
    def __init__(self, user_id="amit", group_id="engineering"):
        self.user_id = user_id
        self.group_id = group_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "group_id": self.group_id
        }


class FileSystemInfo:
    def __init__(self, working_directory="/apps/app1", total_disk_space_mbs=102400, file_system_paths=None):
        self.working_directory = working_directory
        self.total_disk_space_mbs = total_disk_space_mbs
        self.file_system_paths = file_system_paths if file_system_paths is not None else []

    def to_dict(self):
        return {
            "working_directory": self.working_directory,
            "total_disk_space_mbs": self.total_disk_space_mbs,
            "file_system_paths": self.file_system_paths
        }


class DeploymentInfo:
    def __init__(self, name="SampleDeployment", version="1.0.0", deployment_environment="Production", metadata=None):
        self.name = name
        self.version = version
        self.deployment_environment = deployment_environment
        self.metadata = metadata if metadata is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "deployment_environment": self.deployment_environment,
            "metadata": self.metadata
        }


class FrameworkInfo:
    def __init__(self, used_frameworks=None, dependencies=None):
        self.used_frameworks = used_frameworks if used_frameworks is not None else []
        self.dependencies = dependencies if dependencies is not None else []

    def to_dict(self):
        return {
            "used_frameworks": self.used_frameworks,
            "dependencies": self.dependencies
        }


class AppFrameworkMetadata:
    def __init__(self, key="frameworkKey1", value="frameworkValue1", tags=None):
        self.key = key
        self.value = value
        self.tags = tags if tags is not None else []

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "tags": self.tags
        }


class ApplicationFramework:
    def __init__(self, app_framework="LANG_CHAIN", version="1.0", app_framework_metadata=None):
        self.app_framework = app_framework
        self.version = version
        self.app_framework_metadata = app_framework_metadata if app_framework_metadata is not None else []

    def to_dict(self):
        return {
            "app_framework": self.app_framework,
            "version": self.version,
            "app_framework_metadata": [metadata.to_dict() for metadata in self.app_framework_metadata]
        }


class Metadata:
    def __init__(self, key="k1", value="value1", tags=None):
        self.key = key
        self.value = value
        self.tags = tags if tags is not None else []

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "tags": self.tags
        }


class ApplicationMetadata:
    def __init__(self, name="app1", version="1.0", description="", owner="madan", metadata=None):
        self.name = name
        self.version = version
        self.description = description
        self.owner = owner
        self.metadata = metadata if metadata is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "owner": self.owner,
            "metadata": [metadata.to_dict() for metadata in self.metadata]
        }


class Environment:
    def __init__(self, machine=None, networks=None, process=None, runtime_environment=None,
                 security_context=None, request_security_context=None,
                 file_system=None, deployment=None, framework=None,
                 application_framework=None, application_metadata=None):
        self.machine = machine if machine else MachineInfo()
        self.networks = networks if networks else [NetworkInfo()]
        self.process = process if process else ProcessInfo()
        self.runtime_environment = runtime_environment if runtime_environment else RuntimeEnvironment()
        self.security_context = security_context if security_context else SecurityContext()
        self.request_security_context = request_security_context if request_security_context else RequestSecurityContext()
        self.file_system = file_system if file_system else FileSystemInfo()
        self.deployment = deployment if deployment else DeploymentInfo()
        self.framework = framework if framework else FrameworkInfo()
        self.application_framework = application_framework if application_framework else ApplicationFramework()
        self.application_metadata = application_metadata if application_metadata else ApplicationMetadata()

    def to_dict(self):
        return {
            "machine": self.machine.to_dict() if self.machine is not None else None,
            "networks": [network.to_dict() for network in self.networks],
            "process": self.process.to_dict() if self.process is not None else None,
            "runtime_environment": self.runtime_environment.to_dict() if self.runtime_environment is not None else None,
            "security_context": self.security_context.to_dict() if self.security_context is not None else None,
            "request_security_context": self.request_security_context.to_dict() if self.request_security_context else None,
            "file_system": self.file_system.to_dict() if self.file_system is not None else None,
            "deployment": self.deployment.to_dict() if self.deployment is not None else None,
            "framework": self.framework.to_dict() if self.framework is not None else None,
            "application_framework": self.application_framework.to_dict() if self.application_framework is not None else None,
            "application_metadata": self.application_metadata.to_dict() if self.application_metadata is not None else None
        }

    def add_attribute(self, key: str, value: Any) -> None:
        if self.attributes is None:
            self.attributes = {}
        self.attributes[key] = value
