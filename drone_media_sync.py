import os
import time
from datetime import datetime
from impacket.smbconnection import SMBConnection
import xml.etree.ElementTree as ET


def load_settings(file_path="settings.xml"):
    tree = ET.parse(file_path)
    root = tree.getroot()

    smb_config = root.find('smb')
    drone_config = root.find('drone')

    return {
        "smb": {
            "server": smb_config.findtext('server'),
            "share": smb_config.findtext('share'),
            "base_folder": smb_config.findtext('baseFolder'),
            "username": smb_config.findtext('username', ""),
            "password": smb_config.findtext('password', "")
        },
        "drone": {
            "mount_path": drone_config.findtext('mountPath'),
            "media_folder": drone_config.findtext('mediaFolder')
        }
    }


def is_drone_mounted():
    media_dir = os.path.join(MOUNT_PATH, MEDIA_FOLDER)
    return os.path.ismount(MOUNT_PATH) and os.path.isdir(media_dir)


def connect_to_smb():
    try:
        conn = SMBConnection(
            remoteName=SMB_SERVER,
            remoteHost=SMB_SERVER,
            sess_port=445
        )
        conn.login(SMB_USERNAME, SMB_PASSWORD)
        print(f"🔗 Connected to SMB share at {SMB_SERVER}")
        return conn
    except Exception as e:
        print(f"❌ SMB connection failed: {e}")
        return None


def ensure_remote_path(conn, share_name, path):
    parts = path.strip('/').split('/')
    current_path = ''
    for part in parts:
        current_path = f"{current_path}/{part}" if current_path else part
        try:
            conn.createDirectory(share_name, current_path)
        except Exception:
            pass  # Directory may already exist


def copy_to_smb(local_dir, conn):
    upload_count = 0
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            rel_path = os.path.relpath(local_path, local_dir)
            remote_path = os.path.join(SMB_UPLOAD_FOLDER, rel_path).replace("\\", "/")
            remote_dir = os.path.dirname(remote_path)

            ensure_remote_path(conn, SMB_SHARE, remote_dir)

            print(f"📤 Uploading {remote_path}")
            with open(local_path, 'rb') as f:
                conn.putFile(SMB_SHARE, remote_path, f.read)
            upload_count += 1
    return upload_count


# Load settings
settings = load_settings()
SMB_SERVER = settings["smb"]["server"]
SMB_SHARE = settings["smb"]["share"]
BASE_FOLDER = settings["smb"]["base_folder"]
SMB_USERNAME = settings["smb"]["username"]
SMB_PASSWORD = settings["smb"]["password"]
MOUNT_PATH = settings["drone"]["mount_path"]
MEDIA_FOLDER = settings["drone"]["media_folder"]
DATE_FOLDER = datetime.now().strftime("%Y-%m-%d")
SMB_UPLOAD_FOLDER = f"{BASE_FOLDER}/{DATE_FOLDER}"


def main():
    print("🛫 Waiting for drone storage...")
    while not is_drone_mounted():
        time.sleep(2)

    print("📁 Drone storage detected!")
    media_path = os.path.join(MOUNT_PATH, MEDIA_FOLDER)
    if not os.path.exists(media_path):
        print("⚠️ Media folder not found.")
        return

    print("🔗 Connecting to SMB share...")
    conn = connect_to_smb()
    if not conn:
        print("❌ Unable to continue without SMB connection.")
        return

    uploaded = copy_to_smb(media_path, conn)
    conn.close()
    print(f"✅ Transfer complete! {uploaded} file(s) uploaded.")


if __name__ == "__main__":
    main()