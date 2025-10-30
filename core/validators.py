from rest_framework import serializers
import os

def validate_file(uploaded_file):
    """
    Validate size and content type of uploaded_file (InMemoryUploadedFile or TemporaryUploadedFile).
    Raises serializers.ValidationError on invalid input.
    """
    # Size check
    max_size = 10 * 1024 * 1024
    if uploaded_file.size > max_size:
        # show both bytes and readable MB for helpful error
        mb_size = max_size / (1024 * 1024)
        raise serializers.ValidationError(
            f"File too large. Maximum allowed size is {mb_size:.1f} MB."
        )

    # Content-Type check (available on UploadedFile)
    allowed = [
    "image/png",
    "image/jpeg",
    "image/gif",
    "application/pdf",
    ]
    content_type = getattr(uploaded_file, "content_type", None)
    if content_type:
        if content_type not in allowed:
            raise serializers.ValidationError(
                "Unsupported file type. Allowed types: "
                + ", ".join(allowed)
            )
    else:
        # Fallback: check extension if no content_type (defensive)
        _, ext = os.path.splitext(getattr(uploaded_file, "name", "") or "")
        ext = ext.lower()
        # a minimal extension whitelist mapping (extend if you allow more)
        ext_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".pdf": "application/pdf",
        }
        if ext and ext_map.get(ext) not in allowed:
            raise serializers.ValidationError("Unsupported file extension.")
