from typing import Dict
import asyncio
import logging
import requests
from requests.auth import HTTPBasicAuth
from ..models.pod import PodRef
from .pod import PodService
from ..config import _config

r_status = None
r_packages = None
datashield_packages = None

class RService:
    def __init__(self):
        self.pod = None
    
    async def get_status(self) -> Dict:
        """Fetches the status of the R server."""
        global r_status
        logging.info(f"Current R status: {r_status}")
        if r_status is not None:
            return r_status
        logging.info("Fetching R status")
        await self.connect()
        r_status = self._fetch("/rserver")
        return r_status

    async def get_packages(self) -> Dict:
        """Fetches the list of available packages."""
        global r_packages
        logging.info(f"Current R packages: {r_packages}")
        if r_packages is not None:
            return r_packages
        await self.connect()
        r_packages = self._fetch("/rserver/packages")
        return r_packages
    
    async def get_datashield_packages(self) -> Dict:
        """Fetches the list of available DataSHIELD packages."""
        global datashield_packages
        logging.info(f"Current DataSHIELD packages: {datashield_packages}")
        if datashield_packages is not None:
            return datashield_packages
        await self.connect()
        datashield_packages = self._fetch("/rserver/packages/_datashield")
        return datashield_packages

    async def connect(self):
        """Connects to the R server."""
        if self.pod is None:
            self.pod = await PodService().create_pod()
            await self._ensure_ready(self.pod)

    async def close(self):
        """Disconnects from the R server."""
        if self.pod is not None:
            await PodService().delete_pod(self.pod.name)
            self.pod = None

    async def _ensure_ready(self, pod: PodRef):
        """Ensures the R server is ready to receive requests."""
        ready = self._check(pod)
        attempts = 0
        while not ready and attempts < 10:
            await asyncio.sleep(1)
            ready = self._check(pod)
            attempts += 1
        logging.info(f"R Server ready: {ready} after {attempts} attempts")
        if not ready:
            raise Exception("R Server not ready")

    def _check(self, pod: PodRef) -> bool:
        """Checks if the R server is ready to receive requests."""
        url = f"http://{pod.ip}:{pod.port}/_check"
        logging.info(f"Checking {url}")
        try:
            response = requests.get(url)
            if response.status_code >= 200 and response.status_code < 300:
                return True
        except Exception as e:
            logging.error(f"Error checking R Server: {e}")
        return False
    
    def _fetch(self, path: str) -> Dict:
        """Fetches a path from the R server."""
        url = f"http://{self.pod.ip}:{self.pod.port}{path}"
        basicAuth = HTTPBasicAuth(_config.ROCK_ADMINISTRATOR_NAME if _config.ROCK_ADMINISTRATOR_NAME != "" else "administrator", 
                                  _config.ROCK_ADMINISTRATOR_PASSWORD if _config.ROCK_ADMINISTRATOR_PASSWORD != "" else "password")
        logging.info(f"Fetching {url}")
        response = requests.get(url, auth=basicAuth)
        response.raise_for_status()
        return response.json()