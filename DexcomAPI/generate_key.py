import os
import secrets

secret_key = os.urandom(24)
print(f"Secret key: {secret_key}")

secret_key_hex = secrets.token_hex(24)
print(f"Secret key hex: {secret_key_hex}")