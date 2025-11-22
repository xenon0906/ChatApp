"""
Tests for E2EE cryptography module.
Verifies key exchange and message encryption/decryption.
"""
import pytest
import sys
import os

# Add chatapp to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'chatapp'))

from crypto import ChatCrypto


def test_key_generation():
    """Test that keys are generated correctly."""
    crypto = ChatCrypto()

    # Check that keys exist
    assert crypto.private_key is not None
    assert crypto.public_key is not None

    # Check that public key can be exported
    pub_key_bytes = crypto.get_public_key_bytes()
    assert len(pub_key_bytes) == 32  # X25519 public keys are 32 bytes

    pub_key_b64 = crypto.get_public_key_b64()
    assert isinstance(pub_key_b64, str)
    assert len(pub_key_b64) > 0


def test_key_exchange():
    """Test that two parties can exchange keys and derive shared secret."""
    # Create two parties
    alice = ChatCrypto()
    bob = ChatCrypto()

    # Exchange public keys
    alice_pub = alice.get_public_key_b64()
    bob_pub = bob.get_public_key_b64()

    # Derive shared secrets
    alice.derive_shared_secret(bob_pub)
    bob.derive_shared_secret(alice_pub)

    # Both should have the same shared secret
    assert alice.shared_secret == bob.shared_secret
    assert alice.cipher is not None
    assert bob.cipher is not None


def test_message_encryption_decryption():
    """Test that messages can be encrypted and decrypted."""
    # Setup key exchange
    alice = ChatCrypto()
    bob = ChatCrypto()

    alice.derive_shared_secret(bob.get_public_key_b64())
    bob.derive_shared_secret(alice.get_public_key_b64())

    # Alice encrypts a message
    plaintext = "Hello, Bob! This is a secret message."
    encrypted = alice.encrypt_message(plaintext)

    assert isinstance(encrypted, str)
    assert encrypted != plaintext  # Should be encrypted

    # Bob decrypts the message
    decrypted = bob.decrypt_message(encrypted)

    assert decrypted == plaintext


def test_message_encryption_uniqueness():
    """Test that encrypting the same message twice produces different ciphertexts."""
    alice = ChatCrypto()
    bob = ChatCrypto()

    alice.derive_shared_secret(bob.get_public_key_b64())

    plaintext = "Same message"
    encrypted1 = alice.encrypt_message(plaintext)
    encrypted2 = alice.encrypt_message(plaintext)

    # Ciphertexts should be different due to random nonces
    assert encrypted1 != encrypted2


def test_tampered_message_detection():
    """Test that tampered messages are detected and fail decryption."""
    alice = ChatCrypto()
    bob = ChatCrypto()

    alice.derive_shared_secret(bob.get_public_key_b64())
    bob.derive_shared_secret(alice.get_public_key_b64())

    # Alice encrypts a message
    encrypted = alice.encrypt_message("Original message")

    # Tamper with the ciphertext (flip a bit)
    tampered = encrypted[:-1] + ("A" if encrypted[-1] != "A" else "B")

    # Bob tries to decrypt tampered message
    decrypted = bob.decrypt_message(tampered)

    # Should return None for tampered message
    assert decrypted is None


def test_encryption_without_key_exchange():
    """Test that encryption fails without key exchange."""
    crypto = ChatCrypto()

    with pytest.raises(RuntimeError):
        crypto.encrypt_message("This should fail")


def test_decryption_without_key_exchange():
    """Test that decryption fails without key exchange."""
    crypto = ChatCrypto()

    with pytest.raises(RuntimeError):
        crypto.decrypt_message("fake_encrypted_message")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
