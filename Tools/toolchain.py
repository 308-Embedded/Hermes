import requests
import sys
import time
import os
import subprocess
import tempfile

# === Configuration ===
OWNER = "308-Embedded"
REPO = "Embedded-SDK"
TOKEN = "11AVD2ETI0tkDSqdgbU57U_pJ3mpt6ivSco5EUNQMpF2KWzIDQB39hRXVEHXdcYQ382DPKJ67QpDl7tKDR"

# === Fetch Release Information ===
def fetch_release_info(owner, repo, tag, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Will raise an error for non-200 status codes
    return response.json()

# === Extract Asset ID from Release JSON ===
def extract_asset_id(release_json, asset_name):
    for asset in release_json.get("assets", []):
        if asset.get("name") == asset_name:
            return asset.get("id")
    return None

# === Download Asset Binary with Progress Bar ===
def download_asset(asset_id, owner, repo, token, asset_name):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/assets/{asset_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/octet-stream"
    }
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()  # Will raise an error for non-200 status codes
    
    total_size = int(response.headers.get('Content-Length', 0))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".tar.gz") as tmp_file:
        temp_path = tmp_file.name
        print(f"Downloading to temporary file: {temp_path}")
        
        downloaded = 0
        chunk_size = 8192
        for chunk in response.iter_content(chunk_size=chunk_size):
            tmp_file.write(chunk)
            downloaded += len(chunk)
            percent = (downloaded / total_size) * 100 if total_size > 0 else 0
            progress_bar(percent, downloaded, total_size)

    print(f"\n✅ Download completed: {asset_name}")
    return temp_path

# === Mimic Terminal Progress Bar ===
def progress_bar(percent, downloaded, total_size):
    bar_length = 40  # Length of the progress bar in characters
    block = int(round(bar_length * percent / 100))
    progress = "#" * block + "-" * (bar_length - block)
    sys.stdout.write(f"\r[{progress}] {percent:.2f}% ({downloaded / (1024*1024):.2f}MB / {total_size / (1024*1024):.2f}MB) ")
    sys.stdout.flush()

def decompress_and_move(tar_path, target_path):
    """Decompresses a .tar.gz file and moves its contents to the target path."""
    # Ensure the target directory exists
    if not os.path.exists(target_path):
        print(f"Creating directory: {target_path}")
        os.makedirs(target_path)

    print(f"Decompressing {tar_path} to {target_path}...")
    # Use --strip-components=1 to remove the top-level directory from the tarball
    subprocess.run(["tar", "-xzf", tar_path, "-C", target_path, "--strip-components=1"], check=True)
    print("✅ Decompression complete.")
        
# Main Script Logic
if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script requires sudo privileges to run.")
        sys.exit(1)
    try:
        TAG = "v1.0"
        print(f"Fetching release information for {REPO}:{TAG}...")
        TOKEN = "github_pat_" + TOKEN
        #download sysroot
        ASSET_NAME = "sysroot_v1.0.tar.gz"
        release_info = fetch_release_info(OWNER, REPO, TAG, TOKEN)
        asset_id = extract_asset_id(release_info, ASSET_NAME)
        if not asset_id:
            print(f"Error: Asset '{ASSET_NAME}' not found in release tag '{TAG}'.")
            sys.exit(1)
        print(f"Downloading asset '{ASSET_NAME}'...")
        temp_tar_path = download_asset(asset_id, OWNER, REPO, TOKEN, ASSET_NAME)
        decompress_and_move(temp_tar_path, "/.sdk")
        os.unlink(temp_tar_path) 

        #download compiler
        ASSET_NAME = "compiler_v1.0.tar.gz"
        release_info = fetch_release_info(OWNER, REPO, TAG, TOKEN)
        asset_id = extract_asset_id(release_info, ASSET_NAME)
        if not asset_id:
            print(f"Error: Asset '{ASSET_NAME}' not found in release tag '{TAG}'.")
            sys.exit(1)
        print(f"Downloading asset '{ASSET_NAME}'...")
        temp_tar_path = download_asset(asset_id, OWNER, REPO, TOKEN, ASSET_NAME)
        decompress_and_move(temp_tar_path, "/.sdk/compiler")
        os.unlink(temp_tar_path) 

        print("✅✅✅ Embedded SDK has been installed.✅✅✅")
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        sys.exit(1)
