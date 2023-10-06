import typer
import os
import json
import boto3
from google.cloud import storage
import tqdm
import hashlib

app = typer.Typer()

@app.command(help="Add an S3 Folder.")
def add_s3_storage(bucket: str, access_key: str, secret_key: str, region: str, path=""):
    client = boto3.client(
      's3',
      aws_access_key_id=access_key,
      aws_secret_access_key=secret_key,
    )
    bucket = client.Bucket(bucket)
    if(not bucket.creation_date):
        typer.echo("Bucket does not exist.")
        return
    # Check that path must point to a folder and not a file
    if(path != "" and path[-1] != "/"):
        typer.echo("Path must point to a folder and not a file.")
        return
    config = {
        "type": "s3",
        "access_key": access_key,
        "secret_key": secret_key,
        "bucket": bucket,
        "region": region,
        "path": path
    }
    with open("config.json", "r") as f:
        config_file = json.loads(f.read())
        config_file["storages"].append(config)
    with open("config.json", "w") as f:
        f.write(json.dumps(config_file, indent=2))
    typer.echo("Added S3 storage.")

@app.command(help="Add a GCS Folder.")
def add_gcs_storage(bucket: str, creds_path: str, path="/"):
    client = storage.Client.from_service_account_json(creds_path)
    bucket = client.get_bucket(bucket)
    if(not bucket.exists()):
        typer.echo("Bucket does not exist.")
        return
    # Check that path must point to a folder and not a file
    if(path != "" and path[-1] != "/"):
        typer.echo("Path must point to a folder and not a file.")
        return
    config = {
        "type": "gcs",
        "creds_path": creds_path,
        "bucket": bucket,
        "path": path
    }
    with open("config.json", "r") as f:
        config_file = json.loads(f.read())
        config_file["storages"].append(config)
    with open("config.json", "w") as f:
        f.write(json.dumps(config_file, indent=2))
    typer.echo("Added GCS storage.")

@app.command(help="Pull all the storages from the cloud.")
def pull_storages():
    with open("config.json", "r") as f:
        config_file = json.loads(f.read())
        for storage in config_file["storages"]:
            if(storage["type"] == "s3"):
                client = boto3.client(
                  's3',
                  aws_access_key_id=storage["access_key"],
                  aws_secret_access_key=storage["secret_key"],
                )
                bucket = client.Bucket(storage["bucket"])
                for obj in tqdm.tqdm(bucket.objects.all(), desc=f"Pulling storages from {storage['type']}"):
                    if(obj.key[-1] == "/"):
                        os.makedirs("storages/" + obj.key, exist_ok=True)
                    else:
                        os.makedirs("storages/" + obj.key[:obj.key.rfind("/")], exist_ok=True)
                        # Download only if the file doesn't exist or if the file exists but the hash is different
                        if(not os.path.exists("storages/" + obj.key) or obj.e_tag != '"' + hashlib.md5(open("storages/" + obj.key, "rb").read()).hexdigest() + '"'):
                          bucket.download_file(obj.key, "storages/" + obj.key)

            elif(storage["type"] == "gcs"):
                client = storage.Client.from_service_account_json(storage["creds_path"])
                bucket = client.get_bucket(storage["bucket"])
                for blob in tqdm.tqdm(bucket.list_blobs(), desc=f"Pulling storages from {storage['type']}"):
                    if(blob.name[-1] == "/"):
                        os.makedirs("storages/" + blob.name, exist_ok=True)
                    else:
                        os.makedirs("storages/" + blob.name[:blob.name.rfind("/")], exist_ok=True)
                        # Download only if the file doesn't exist or if the file exists but the hash is different
                        if(not os.path.exists("storages/" + blob.name) or blob.etag != '"' + hashlib.md5(open("storages/" + blob.name, "rb").read()).hexdigest() + '"'):
                          blob.download_to_filename("storages/" + blob.name)


if __name__ == "__main__":
    app()