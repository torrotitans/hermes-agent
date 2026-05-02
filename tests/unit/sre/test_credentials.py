"""
FN:test_credentials.py
Unit tests for Torro credential pool.

Tests:
- TestCredential: Test Credential dataclass
- TestCredentialPool: Test CredentialPool class
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from sre.credentials import (
    Credential,
    CredentialPool,
)


class TestCredential:
    """Test Credential dataclass."""
    
    def test_credential_creation(self):
        """Test creating a Credential."""
        cred = Credential(
            credential_id="api_key",
            value="secret123"
        )
        assert cred.credential_id == "api_key"
        assert cred.value == "secret123"
        assert cred.expires_at is None
        assert cred.metadata == {}
    
    def test_credential_with_expiration(self):
        """Test creating a Credential with expiration."""
        expires_at = datetime.now() + timedelta(hours=1)
        cred = Credential(
            credential_id="api_key",
            value="secret123",
            expires_at=expires_at
        )
        assert cred.expires_at == expires_at
    
    def test_credential_with_metadata(self):
        """Test creating a Credential with metadata."""
        cred = Credential(
            credential_id="api_key",
            value="secret123",
            metadata={"scope": "read"}
        )
        assert cred.metadata == {"scope": "read"}
    
    def test_is_expired_false(self):
        """Test is_expired property when not expired."""
        expires_at = datetime.now() + timedelta(hours=1)
        cred = Credential(
            credential_id="api_key",
            value="secret123",
            expires_at=expires_at
        )
        assert cred.is_expired is False
    
    def test_is_expired_true(self):
        """Test is_expired property when expired."""
        expires_at = datetime.now() - timedelta(hours=1)
        cred = Credential(
            credential_id="api_key",
            value="secret123",
            expires_at=expires_at
        )
        assert cred.is_expired is True
    
    def test_is_expired_no_expiration(self):
        """Test is_expired property with no expiration."""
        cred = Credential(
            credential_id="api_key",
            value="secret123"
        )
        assert cred.is_expired is False


class TestCredentialPool:
    """Test CredentialPool class."""
    
    def test_credential_pool_init(self):
        """Test CredentialPool initialization."""
        pool = CredentialPool()
        assert pool._credentials == {}
        assert pool._in_use == set()
    
    def test_add_credential(self):
        """Test adding a credential."""
        pool = CredentialPool()
        pool.add_credential("api_key", "secret123")
        
        assert "api_key" in pool._credentials
        assert pool._credentials["api_key"].value == "secret123"
    
    def test_add_credential_with_expiration(self):
        """Test adding a credential with expiration."""
        pool = CredentialPool()
        pool.add_credential("api_key", "secret123", expires_in_seconds=3600)
        
        assert "api_key" in pool._credentials
        cred = pool._credentials["api_key"]
        assert cred.expires_at is not None
    
    def test_acquire_credential(self):
        """Test acquiring a credential."""
        pool = CredentialPool()
        pool.add_credential("api_key", "secret123")
        
        cred = pool.acquire("api_key")
        assert cred.credential_id == "api_key"
        assert cred.value == "secret123"
        assert "api_key" in pool._in_use
    
    def test_acquire_nonexistent_credential(self):
        """Test acquiring nonexistent credential."""
        pool = CredentialPool()
        
        with pytest.raises(KeyError):
            pool.acquire("nonexistent")
    
    def test_acquire_expired_credential(self):
        """Test acquiring expired credential."""
        pool = CredentialPool()
        # Add credential that's already expired
        cred = Credential(
            credential_id="api_key",
            value="secret123",
            expires_at=datetime.now() - timedelta(hours=1)
        )
        pool._credentials["api_key"] = cred
        
        with pytest.raises(ValueError):
            pool.acquire("api_key")
    
    def test_release_credential(self):
        """Test releasing a credential."""
        pool = CredentialPool()
        pool.add_credential("api_key", "secret123")
        
        cred = pool.acquire("api_key")
        assert "api_key" in pool._in_use
        
        pool.release(cred)
        assert "api_key" not in pool._in_use
    
    def test_rotate_credential(self):
        """Test rotating a credential."""
        pool = CredentialPool()
        pool.add_credential("api_key", "secret123")
        
        pool.rotate("api_key", "newsecret456")
        cred = pool._credentials["api_key"]
        assert cred.value == "newsecret456"
    
    def test_rotate_nonexistent_credential(self):
        """Test rotating nonexistent credential."""
        pool = CredentialPool()
        
        with pytest.raises(KeyError):
            pool.rotate("nonexistent", "newsecret")
    
    def test_remove_credential(self):
        """Test removing a credential."""
        pool = CredentialPool()
        pool.add_credential("api_key", "secret123")
        
        result = pool.remove("api_key")
        assert result is True
        assert "api_key" not in pool._credentials
    
    def test_remove_nonexistent_credential(self):
        """Test removing nonexistent credential."""
        pool = CredentialPool()
        
        result = pool.remove("nonexistent")
        assert result is False
    
    def test_get_stats(self):
        """Test getting pool statistics."""
        pool = CredentialPool()
        pool.add_credential("api_key1", "secret1")
        pool.add_credential("api_key2", "secret2")
        
        pool.acquire("api_key1")
        
        stats = pool.get_stats()
        assert stats["total_credentials"] == 2
        assert stats["in_use"] == 1
        assert stats["available"] == 1
    
    def test_get_stats_with_expired(self):
        """Test getting stats with expired credentials."""
        pool = CredentialPool()
        # Add credential that's already expired
        cred = Credential(
            credential_id="api_key",
            value="secret123",
            expires_at=datetime.now() - timedelta(hours=1)
        )
        pool._credentials["api_key"] = cred
        
        stats = pool.get_stats()
        assert stats["expired"] == 1
