from pwdlib import PasswordHash
password_hasher = PasswordHash.recommended()

def hash_password(plaintext_pwd: str) -> str:
    return password_hasher.hash(plaintext_pwd)

def verify_password(plaintext_pwd: str, hashed_password: str) -> bool:
    return password_hasher.verify(plaintext_pwd, hashed_password)