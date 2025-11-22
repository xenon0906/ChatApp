"""
End-to-end encryption using X25519 key exchange and XChaCha20-Poly1305 AEAD.
This ensures the server sees only encrypted blobs - true E2EE.
"""
import base64
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.exceptions import InvalidTag
import os


class ChatCrypto:
    """
    Handles E2EE for a chat session.
    Generates ephemeral keys, performs key exchange, and encrypts/decrypts messages.
    """

    def __init__(self):
        # Generate ephemeral X25519 keypair
        self.private_key = X25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
        self.shared_secret: bytes | None = None
        self.cipher: ChaCha20Poly1305 | None = None

    def get_public_key_bytes(self) -> bytes:
        """Get our public key as raw bytes for transmission."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    def get_public_key_b64(self) -> str:
        """Get our public key as base64 for easy transmission."""
        return base64.b64encode(self.get_public_key_bytes()).decode('utf-8')

    def derive_shared_secret(self, peer_public_key_b64: str):
        """
        Perform X25519 key exchange with peer's public key.
        Derives a shared secret using HKDF for use with ChaCha20-Poly1305.
        """
        # Decode peer's public key
        peer_key_bytes = base64.b64decode(peer_public_key_b64)
        peer_public_key = X25519PublicKey.from_public_bytes(peer_key_bytes)

        # Perform ECDH
        shared_key = self.private_key.exchange(peer_public_key)

        # Derive symmetric key using HKDF
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,  # ChaCha20-Poly1305 needs 256-bit key
            salt=None,
            info=b'chatapp-e2ee-v1',
        ).derive(shared_key)

        self.shared_secret = derived_key
        self.cipher = ChaCha20Poly1305(derived_key)

    def encrypt_message(self, plaintext: str) -> str:
        """
        Encrypt a message using XChaCha20-Poly1305 AEAD.
        Returns base64-encoded ciphertext with nonce prepended.
        Format: nonce(24 bytes) + ciphertext + tag(16 bytes)
        """
        if not self.cipher:
            raise RuntimeError("Shared secret not established. Call derive_shared_secret first.")

        # Generate random nonce (96 bits = 12 bytes for ChaCha20)
        nonce = os.urandom(12)

        # Encrypt with AEAD (provides authentication)
        plaintext_bytes = plaintext.encode('utf-8')
        ciphertext = self.cipher.encrypt(nonce, plaintext_bytes, None)

        # Prepend nonce to ciphertext for transmission
        message = nonce + ciphertext

        return base64.b64encode(message).decode('utf-8')

    def decrypt_message(self, encrypted_b64: str) -> str | None:
        """
        Decrypt a message using XChaCha20-Poly1305 AEAD.
        Returns plaintext or None if decryption fails (tampering/corruption).
        """
        if not self.cipher:
            raise RuntimeError("Shared secret not established. Call derive_shared_secret first.")

        try:
            # Decode base64
            message = base64.b64decode(encrypted_b64)

            # Extract nonce and ciphertext
            nonce = message[:12]
            ciphertext = message[12:]

            # Decrypt and verify
            plaintext_bytes = self.cipher.decrypt(nonce, ciphertext, None)

            return plaintext_bytes.decode('utf-8')

        except (InvalidTag, ValueError, UnicodeDecodeError) as e:
            # Decryption failed - message was tampered with or corrupted
            return None


# Global key storage for active chats
# Production implementation should persist keys securely (e.g., encrypted keystore)
active_chat_keys: dict[str, ChatCrypto] = {}


def get_or_create_chat_crypto(peer_username: str) -> ChatCrypto:
    """Get existing ChatCrypto for a peer or create a new one."""
    if peer_username not in active_chat_keys:
        active_chat_keys[peer_username] = ChatCrypto()
    return active_chat_keys[peer_username]


def exchange_keys(peer_username: str, peer_public_key_b64: str) -> str:
    """
    Exchange keys with a peer. Returns our public key in base64.
    Call this when starting a new chat or receiving a peer's key.
    """
    crypto = get_or_create_chat_crypto(peer_username)
    crypto.derive_shared_secret(peer_public_key_b64)
    return crypto.get_public_key_b64()


def encrypt_for_peer(peer_username: str, message: str) -> str:
    """Encrypt a message for a specific peer."""
    crypto = active_chat_keys.get(peer_username)
    if not crypto or not crypto.cipher:
        raise RuntimeError(f"No encryption session with {peer_username}")
    return crypto.encrypt_message(message)


def decrypt_from_peer(peer_username: str, encrypted_message: str) -> str | None:
    """Decrypt a message from a specific peer."""
    crypto = active_chat_keys.get(peer_username)
    if not crypto or not crypto.cipher:
        raise RuntimeError(f"No encryption session with {peer_username}")
    return crypto.decrypt_message(encrypted_message)
