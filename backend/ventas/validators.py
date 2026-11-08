import re

from rest_framework import serializers


def normalize_phone(value):
    """Normalize phone formatting while preserving the country code digits."""
    digits = re.sub(r"[^0-9]", "", str(value or ""))
    if not 8 <= len(digits) <= 15:
        raise serializers.ValidationError(
            "Ingrese un teléfono válido (entre 8 y 15 dígitos)."
        )
    return digits
