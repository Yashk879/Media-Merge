
import os
import shutil
import subprocess
import secrets
from celery import shared_task
from django.conf import settings
from .models import MediaAsset
from .storage import upload_file

@shared_task
def process_asset(asset_id):
    asset = MediaAsset.objects.get(id=asset_id)
    asset.status = "processing"
    asset.save(update_fields=["status"])

    if not asset.original_file:
        asset.status = "failed"
        asset.save(update_fields=["status"])
        return

    source = asset.original_file.path
    output_dir = settings.HLS_ROOT / str(asset.id)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    playlist = output_dir / "index.m3u8"
    segment_pattern = output_dir / "segment_%03d.ts"

    # AES-128 HLS encryption key. In production, move key generation/storage
    # to a dedicated KMS/DRM/key service.
    key = secrets.token_bytes(16)
    key_path = output_dir / "enc.key"
    key_path.write_bytes(key)

    key_uri = "enc.key"
    key_info = output_dir / "key_info.txt"
    key_info.write_text(f"{key_uri}\n{key_path}\n", encoding="utf-8")

    cmd = [
        "ffmpeg", "-y", "-i", source,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-f", "hls", "-hls_time", "6", "-hls_playlist_type", "vod",
        "-hls_key_info_file", str(key_info),
        "-hls_segment_filename", str(segment_pattern),
        str(playlist),
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Upload segments and encrypted key first.
        upload_file(str(key_path), f"hls/{asset.id}/enc.key", "application/octet-stream")
        for path in output_dir.iterdir():
            if path.is_file() and path.suffix.lower() == ".ts":
                upload_file(str(path), f"hls/{asset.id}/{path.name}", "video/mp2t")

        # Keep the playlist for later signed URL rewriting by the stream API.
        upload_file(str(playlist), f"hls/{asset.id}/index.m3u8",
                    "application/vnd.apple.mpegurl")

        asset.hls_playlist = f"hls/{asset.id}/index.m3u8"
        asset.hls_master_key = f"hls/{asset.id}/enc.key"
        asset.status = "ready"
        asset.save(update_fields=["hls_playlist", "hls_master_key", "status"])
    except Exception:
        asset.status = "failed"
        asset.save(update_fields=["status"])
        raise
