import secrets
import logging
import asyncio
from fastapi import HTTPException
from ..config import _config
from ..models.pod import PodRef, PodRefs
from kubernetes import client, config


# Load Kubernetes in-cluster config (when running inside a pod)
try:
    config.load_incluster_config()
except config.config_exception.ConfigException:
    # Fallback to kubeconfig for local testing
    config.load_kube_config()

# Define Kubernetes API client
v1 = client.CoreV1Api()

class PodService:
    """Service for managing pods."""
    
    def __init__(self):
        pass

    async def create_pod(self, wait: bool = False) -> PodRef:
        """Creates a pod with the app image.

        Args:
            wait (bool): Whether to wait for the pod to be running before returning.

        Returns:
            PodRef: The pod descriptor.
        """
        pod_name = f"{_config.APP_BASENAME}-{secrets.token_hex(12)}"
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": pod_name},
            "spec": {
                "containers": [
                    {
                        "name": pod_name,
                        "image": _config.APP_IMAGE,
                        "ports": [
                            {
                                "containerPort": _config.APP_PORT
                            }
                        ],
                        "env": [
                            {
                                "name": "ROCK_ID",
                                "value": pod_name
                            },
                            {
                                "name": "ROCK_CLUSTER",
                                "value": _config.ROCK_CLUSTER
                            },
                            {
                                "name": "ROCK_ADMINISTRATOR_NAME",
                                "value": _config.ROCK_ADMINISTRATOR_NAME
                            },
                            {
                                "name": "ROCK_ADMINISTRATOR_PASSWORD",
                                "value": _config.ROCK_ADMINISTRATOR_PASSWORD
                            },
                            {
                                "name": "ROCK_MANAGER_NAME",
                                "value": _config.ROCK_MANAGER_NAME
                            },
                            {
                                "name": "ROCK_MANAGER_PASSWORD",
                                "value": _config.ROCK_MANAGER_PASSWORD
                            },
                            {
                                "name": "ROCK_USER_NAME",
                                "value": _config.ROCK_USER_NAME
                            },
                            {
                                "name": "ROCK_USER_PASSWORD",
                                "value": _config.ROCK_USER_PASSWORD
                            }
                        ]
                    }
                ]
            },
        }
        v1.create_namespaced_pod(namespace=_config.NAMESPACE, body=pod_manifest)
        logging.info(f"Pod {pod_name}@{_config.APP_IMAGE} created successfully")
        if wait:
            return await self.ensure_running_pod(pod_name)
        else:
            return await self.get_pod(pod_name)
    
    async def get_pod(self, pod_name: str) -> PodRef:
        """Fetches the status of a pod by name.
        
        Args:
            pod_name (str): The name of the pod.
        
        Returns:
            PodRef: The pod descriptor.
        """
        try:
            pod = v1.read_namespaced_pod(name=pod_name, namespace=_config.NAMESPACE)
            image = pod.spec.containers[0].image
            if image != _config.APP_IMAGE:
                raise HTTPException(status_code=404, detail="Pod not found")
            status = pod.status.phase  # Example statuses: Pending, Running, Succeeded, Failed
            ip = pod.status.pod_ip
            return PodRef(name=pod_name, image=_config.APP_IMAGE, status=status, ip=ip, port=_config.APP_PORT)
        
        except client.ApiException as e:
            if e.status == 404:
                raise HTTPException(status_code=404, detail="Pod not found")
            raise HTTPException(status_code=500, detail=f"Error retrieving pod status: {str(e)}")
        
    async def delete_pod(self, pod_name: str):
        """"Deletes a pod by name.

        Args:
            pod_name (str): The name of the pod.
        """
        pods = await self.list_pods()
        if pod_name not in [pod.name for pod in pods.items]:
            raise HTTPException(status_code=404, detail="Pod not found")
        v1.delete_namespaced_pod(name=pod_name, namespace=_config.NAMESPACE)
        logging.info(f"Pod {pod_name} deleted successfully")


    async def list_pods(self) -> PodRefs:
        """Lists all pods in the namespace with the app image.
        
        Returns:
            PodRefs: The list of pod descriptors.
        """
        pods = v1.list_namespaced_pod(namespace=_config.NAMESPACE)
        pod_list = [PodRef(name=pod.metadata.name, image=_config.APP_IMAGE, status=pod.status.phase, ip=pod.status.pod_ip, port=_config.APP_PORT) for pod in pods.items if pod.spec.containers[0].image == _config.APP_IMAGE]
        return PodRefs(items=pod_list)

    async def delete_pods(self):
        """Deletes all pods in the namespace with the app image."""
        pods = await self.list_pods()
        for pod in pods.items:
            v1.delete_namespaced_pod(name=pod.name, namespace=_config.NAMESPACE)
        logging.info("All pods deleted successfully")

    async def ensure_running_pod(self, pod_name: str) -> PodRef:
        """Ensures a pod is running and returns its pod descriptor.
        
        Args:
            pod_name (str): The name of the pod.
        
        Returns:
            PodRef: The pod descriptor
        """
        pod = await self.get_pod(pod_name)
        attempts = 0
        while pod.status != "Running":
            # sleep for a while and check again
            await asyncio.sleep(1)
            attempts += 1
            if attempts > 10:
                raise HTTPException(status_code=500, detail=f"Pod {pod_name} did not start in time")
            pod = await self.get_pod(pod_name)
        return pod