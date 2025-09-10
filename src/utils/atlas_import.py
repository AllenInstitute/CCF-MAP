import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

import boto3
from botocore.config import Config
from botocore import UNSIGNED
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig


def _normalize_prefix(location: str) -> str:
    return location.lstrip("/") if isinstance(location, str) else ""


@dataclass(frozen=True)
class AtlasManifest:
    raw: Dict[str, Any]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AtlasManifest":
        if not isinstance(d, dict):
            raise TypeError("manifest must be a dict")
        return cls(raw=d)

    def s3_prefixes(self) -> Set[str]:
        prefixes: Set[str] = set()
        def walk(o: Any):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == "location":
                        p = _normalize_prefix(str(v))
                        if p:
                            prefixes.add(p)
                    else:
                        walk(v)
            elif isinstance(o, list):
                for i in o: walk(i)
        walk(self.raw)
        return prefixes


def download_data_assets(
    prefixes: Iterable[str],
    bucket: str = 'allen-atlas-assets',
    dest_dir: Path | str = './data/',
    overwrite: bool = False,
    dry_run: bool = False,
    max_concurrency: int = 16,
    file_extensions: tuple = ('.nii.gz', '.csv')
) -> List[Path]:
    
    dest = Path(dest_dir).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    print(f"Destination directory: {dest}")

    session = boto3.Session()
    client_kwargs = {}
    client_kwargs["config"] = Config(signature_version=UNSIGNED)
    s3 = session.client("s3", **client_kwargs)

    transfer_cfg = TransferConfig(max_concurrency=max_concurrency)
    downloaded: List[Path] = []

    # normalize suffixes once (lowercase)
    normalized_suffixes = tuple(s.lower() for s in file_extensions)

    uniq_prefixes = sorted({p.strip("/") for p in prefixes if p and p.strip("/")})
    if not uniq_prefixes:
        print("Nothing to download.")
        return downloaded

    paginator = s3.get_paginator("list_objects_v2")
    for prefix in uniq_prefixes:
        found_any = False

        try:
            for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
                contents = page.get("Contents", [])
                if not contents:
                    continue
                found_any = True

                for obj in contents:
                    key = obj["Key"]
                    if key.endswith("/"):
                        continue

                    # suffix filter (case-insensitive)
                    if not key.lower().endswith(normalized_suffixes):
                        # Not one of the wanted types; skip.
                        continue

                    local_path = dest / key
                    local_path.parent.mkdir(parents=True, exist_ok=True)

                    if not overwrite and local_path.exists():
                        try:
                            if local_path.stat().st_size == obj.get("Size", -1):
                                continue
                        except OSError:
                            pass

                    if dry_run:
                        print(f"DRY RUN: would download s3://{bucket}/{key} -> {local_path}")
                        continue

                    try:
                        s3.download_file(
                            Bucket=bucket,
                            Key=key,
                            Filename=str(local_path),
                            Config=transfer_cfg,
                        )
                        downloaded.append(local_path)
                    except ClientError as e:
                        raise RuntimeError(f"Failed to download s3://{bucket}/{key}: {e}") from e

        except ClientError as e:
            raise RuntimeError(f"Failed listing s3://{bucket}/{prefix}: {e}") from e

        if not found_any:
            print(f"Warning: prefix not found or empty: s3://{bucket}/{prefix}")

    return downloaded

def get_latest_atlases():

    bucket="allen-atlas-assets"
    prefix="atlases/"
    dest=Path("./data/atlases")
    s3=boto3.client("s3", config=Config(signature_version=UNSIGNED))

    for obj in s3.list_objects_v2(Bucket=bucket, Prefix=prefix).get("Contents", []):
        k = obj["Key"]
        if k.endswith("/"): 
            continue
        p = dest / k[len(prefix):]         
        p.parent.mkdir(parents=True, exist_ok=True) 
        s3.download_file(bucket, k, str(p)) 
        print(f"Downloaded {str(p)}")

def download_atlas(
        species: str, 
        version: str = 2025):

    if species not in ['human', 'macaque', 'marmoset']:
       raise RuntimeError(f"Species should be one of 'human', 'macaque', 'marmoset', or 'all'")
    
    if species == 'all':
        species_set = ['human', 'macaque', 'marmoset']
    else:
        species_set = [species]

    for _species in species_set:
        manifest_filename = f"./data/atlases/hmba-adult-{species}-homba-atlas/{version}/manifest.json"
        with open(manifest_filename) as f:
            manifest_dict = json.load(f)
        manifest = AtlasManifest.from_dict(manifest_dict)

        filestem = manifest.s3_prefixes()

        download_data_assets(filestem)
    

if __name__ == "__main__":

    print('AtlasManifest: set of functions to download atlases and manifest from S3')
    