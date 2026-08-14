import os
import glob
import stat
import posixpath
import paramiko
from pathlib import Path
from dotenv import load_dotenv
from common.logger import write_log

load_dotenv()

def connect_sftp():
    host = os.getenv("SFTP_HOST")
    username = os.getenv("SFTP_USER")
    pem_file = os.getenv("PEM_FILE")
    port = int(os.getenv("SFTP_PORT", 22))

    if not host or not username or not pem_file:
        raise ValueError("Missing values in .env :- SFTP_HOST / SFTP_USER / PEM_FILE")

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=username, key_filename=os.path.expanduser(pem_file))

    write_log(f"Connected to SFTP host :- {host} successfully")

    return client, client.open_sftp()



# Download all files from the SFTP folder into InputFiles

def download_files_from_sftp(local_folder,remote_folder):

    if not remote_folder:
        raise ValueError("Missing value in .env :- REMOTE_PATH")

    client = None
    downloaded_files = []

    try:
        client, sftp = connect_sftp()
        os.makedirs(local_folder, exist_ok=True)

        for entry in sftp.listdir_attr(remote_folder):
            # Only plain files are downloaded, sub folders are skipped
            if stat.S_ISDIR(entry.st_mode):
                write_log(f"Skipping folder :- {entry.filename}")
                continue

            remote_file = posixpath.join(remote_folder, entry.filename)
            local_file = os.path.join(str(local_folder), entry.filename)

            write_log(f"Downloading :- {remote_file}")
            sftp.get(remote_file, local_file)
            downloaded_files.append(local_file)

        write_log(f"Downloaded {len(downloaded_files)} file(s) from :- {remote_folder} to :- {local_folder}")

    except Exception as e:
        write_log(f"Failed to download files from SFTP and error is :- {e}", level="ERROR")

    finally:
        if client is not None:
            client.close()

    return downloaded_files
   
def upload_processed_files_to_sftp(local_folder,remote_folder):
    if not remote_folder:
            raise ValueError("Missing value in .env :- REMOTE_PATH")
    client = None
    Uploaded_files = []  
    try:  
        local_folder = Path(local_folder)
        client,sftp = connect_sftp()

        for file in local_folder.rglob("*"):
            if not file.is_file():
                continue

            remote_file = posixpath.join(remote_folder, file.name)

            write_log(f"Uploading: {file} → {remote_file}")

            try:
                sftp.put(str(file), remote_file)
                Uploaded_files.append(file)
                
                write_log(f"Uploaded {len(Uploaded_files)} file(s) from :- {local_folder} to :- {remote_folder}")
                
            except Exception as e:
                write_log(f"[ERROR] Upload failed | File: {file} | Destination: {remote_file} | Error: {e}")
    except Exception as e:
        write_log(f"Failed to upload files from SFTP and error is :- {e}", level="ERROR")
                   
# Runs only when this file is executed directly, not when main.py imports it
if __name__ == "__main__":
    download_files_from_sftp()
