import os
import requests
from pathlib import Path

PINATA_API_URL = "https://api.pinata.cloud"
endpoint = "/pinning/pinFileToIPFS"
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as file_path:
        image_binary = file_path.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(
            ipfs_url + endpoint,
            files={"file": image_binary},
        )
        ipfs_hash = response.json()["Hash"]
        image_uri = f"ipfs://{ipfs_hash}"
        return image_uri


def upload_to_pinata(filepath):
    with Path(filepath).open("rb") as file_path:
        filename = filepath.split("/")[-1]
        image_binary = file_path.read()
        response = requests.post(
            PINATA_API_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        ipfs_hash = response.json()["IpfsHash"]
        image_uri = f"ipfs://{ipfs_hash}"
        return image_uri
