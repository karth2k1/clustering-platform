"""Encryption utilities for sensitive data like API keys"""
from cryptography.fernet import Fernet
from app.config import settings
import base64
import hashlib


def get_encryption_key() -> bytes:
    """Get encryption key from settings"""
    # Use SHA256 hash of the encryption key to ensure it's 32 bytes
    key_hash = hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key_hash)


def encrypt_data(data: str) -> bytes:
    """Encrypt sensitive data"""
    if not data:
        return b''
    f = Fernet(get_encryption_key())
    return f.encrypt(data.encode())


def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypt sensitive data"""
    if not encrypted_data:
        return ""
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted_data).decode()

