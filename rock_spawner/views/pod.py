import secrets
import logging 
from fastapi import APIRouter, HTTPException
from kubernetes import client, config
from ..config import _config
from ..models.pod import PodRef, PodRefs

router = APIRouter()

# Load Kubernetes in-cluster config (when running inside a pod)
try:
    config.load_incluster_config()
except config.config_exception.ConfigException:
    # Fallback to kubeconfig for local testing
    config.load_kube_config()

# Define Kubernetes API client
v1 = client.CoreV1Api()

@router.post("/")
async def create_pod(name: str) -> PodRef:
    """Creates a Kubernetes pod."""
    # add random string to pod name to avoid conflicts
    pod_name = f"{name}-{secrets.token_hex(12)}"
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
                }
            ]
        },
    }
    v1.create_namespaced_pod(namespace=_config.NAMESPACE, body=pod_manifest)
    logging.info(f"Pod {pod_name}@{_config.APP_IMAGE} created successfully")
    #return PodRef(name=pod_name, image=_config.APP_IMAGE)
    return await get_pod(pod_name)

@router.delete("/{pod_name}", status_code=204)
async def delete_pod(pod_name: str):
    """Deletes a Kubernetes pod."""
    v1.delete_namespaced_pod(name=pod_name, namespace=_config.NAMESPACE)

@router.get("/{pod_name}")
async def get_pod(pod_name: str) -> PodRef:
    """Fetches the status of a specific Kubernetes pod."""
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

@router.get("/")
async def list_pods() -> PodRefs:
    """Lists all pods in the namespace."""
    pods = v1.list_namespaced_pod(namespace=_config.NAMESPACE)
    pod_list = [PodRef(name=pod.metadata.name, image=_config.APP_IMAGE, status=pod.status.phase, ip=pod.status.pod_ip, port=_config.APP_PORT) for pod in pods.items if pod.spec.containers[0].image == _config.APP_IMAGE]
    return PodRefs(items=pod_list)