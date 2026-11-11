from pathlib import Path
from django.conf import settings
from django.core.files.storage import default_storage


def upload_file(local_path, object_key, content_type="application/octet-stream"):
    """
    Copy a local file into Django's MEDIA_ROOT.

    Returns the relative path of the stored file.
    """

    destination = Path(settings.MEDIA_ROOT) / object_key
    destination.parent.mkdir(parents=True, exist_ok=True)

    with open(local_path, "rb") as source:
        saved_path = default_storage.save(
            object_key,
            source
        )

    return saved_path


def presigned_url(object_key, expires=900):
    """
    Local filesystem replacement for an S3 presigned URL.

    Returns a relative media URL.
    """

    return f"{settings.MEDIA_URL}{object_key}"