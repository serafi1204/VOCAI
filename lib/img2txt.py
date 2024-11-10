import os
import sys
import uuid
import zipfile
import json

import requests

apiKey = ''
with open('lib/apiKey.txt', 'r', encoding='utf-8') as f:
    apiKey = f.read()
    
# NVAI endpoint for the ocdrnet NIM
nvai_url="https://ai.api.nvidia.com/v1/cv/nvidia/ocdrnet"
header_auth = f"Bearer {apiKey}"


def _upload_asset(input, description):
    """
    Uploads an asset to the NVCF API.
    :param input: The binary asset to upload
    :param description: A description of the asset

    """
    assets_url = "https://api.nvcf.nvidia.com/v2/nvcf/assets"

    headers = {
        "Authorization": header_auth,
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    s3_headers = {
        "x-amz-meta-nvcf-asset-description": description,
        "content-type": "image/jpeg",
    }

    payload = {"contentType": "image/jpeg", "description": description}

    response = requests.post(assets_url, headers=headers, json=payload, timeout=30)

    response.raise_for_status()

    asset_url = response.json()["uploadUrl"]
    asset_id = response.json()["assetId"]

    response = requests.put(
        asset_url,
        data=input,
        headers=s3_headers,
        timeout=300,
    )

    response.raise_for_status()
    return uuid.UUID(asset_id)


def readImg(path):
    asset_id = _upload_asset(open(path, "rb"), "Input Image")
    inputs = {"image": f"{asset_id}", "render_label": False}
    asset_list = f"{asset_id}"
    headers = {
        "Content-Type": "application/json",
        "NVCF-INPUT-ASSET-REFERENCES": asset_list,
        "NVCF-FUNCTION-ASSET-IDS": asset_list,
        "Authorization": header_auth,
    }

    response = requests.post(nvai_url, headers=headers, json=inputs)
    with open(f"output.zip", "wb") as out:
        out.write(response.content)
        
    with zipfile.ZipFile(f"output.zip", "r") as z:
        resFile = [file for file  in z.namelist() if file.endswith('response')]
        if (len(resFile)==0): return -1
        
        res = z.read(resFile[0])
        resJson = json.loads(res)
        
    return resJson
