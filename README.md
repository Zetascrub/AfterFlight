# 🛸 Drone Media Uploader — SkySync

Automatically sync media from your drone's internal storage to an SMB share when connected. Ideal for hands-off backups after flying missions.

## ✨ Features

- Automatically detects when your drone is mounted
- Supports anonymous or credentialed SMB uploads
- Creates dated folders for each session (e.g. `Drone Footage/2025-04-08/`)
- Fully configurable via external `settings.xml`
- Command-line friendly with emoji feedback 😎

---

## ⚙️ Requirements

- Python 3.7+
- [`impacket`](https://github.com/fortra/impacket)

Install dependencies:
```bash
pip install -r requirements.txt
```

## 📁 Configuration

Before running, copy the sample config and fill in your details:

```bash
cp settings.example.xml settings.xml
```

Edit `settings.xml`:

```
<config>
    <smb>
        <server>IP/SERVER</server>
        <share>SHARE</share>
        <baseFolder>SHARE FOLDER</baseFolder>
        <username></username>
        <password></password>
    </smb>
    <drone>
        <mountPath>DRONE PATH</mountPath>
        <mediaFolder>DCIM</mediaFolder>
    </drone>
</config>

```

## 🚀 Usage

Connect your drone via USB (ensure it mounts properly), then run:

```bash
python drone_sync.py
```

Or you can run the above command and it'll wait till it detects the paths specified in the settings.xml file you created. Then upload all files from its DCIM folder into the SMB share inside a date-based subfolder.
>>>>>>> a9b0998 (Initial Upload)
