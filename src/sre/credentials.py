"""
FN:credentials.py
Credential pool for Torro agent framework SRE.

Classes:
- CredentialPool: Manages credential acquisition and rotation
- Credential: Credential data class

Functions:
- FN:acquire: Acquire credential from pool (lines 52-66)
- FN:release: Release credential back to pool (lines 68-80)
- FN:rotate: Rotate credential (lines 82-94)
"""

import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


@dataclass
class Credential:
    """Credential data class.
    
    Attributes:
        credential_id: Unique credential identifier
        value: Credential value (token, password, etc.)
        expires_at: Expiration timestamp
        metadata: Additional credential metadata
    """
    credential_id: str
    value: str
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_expired(self) -> bool:
        """Check if credential is expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at


class CredentialPool:
    """Manages credential acquisition and rotation.
    
    The CredentialPool provides a thread-safe mechanism for managing
    credentials with support for rotation and expiration tracking.
    
    Example:
        ```python
        pool = CredentialPool()
        
        # Add credentials
        pool.add_credential("api_key", "secret123")
        
        # Acquire a credential
        cred = pool.acquire("api_key")
        
        # Use credential...
        
        # Release back to pool
        pool.release(cred)
        ```
    """
    
    def __init__(self):
        """Initialize the credential pool."""
        self._credentials: Dict[str, Credential] = {}
        self._in_use: Set[str] = set()
        self._lock = threading.RLock()
        logger.info("FN:CredentialPool.__init__ Pool initialized")
    
    def add_credential(
        self,
        credential_id: str,
        value: str,
        expires_in_seconds: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """FN:add_credential Add a credential to the pool.
        
        Args:
            credential_id: Unique credential identifier
            value: Credential value
            expires_in_seconds: Seconds until expiration
            metadata: Additional metadata
        """
        expires_at = None
        if expires_in_seconds:
            expires_at = datetime.now() + timedelta(seconds=expires_in_seconds)
        
        cred = Credential(
            credential_id=credential_id,
            value=value,
            expires_at=expires_at,
            metadata=metadata or {}
        )
        
        with self._lock:
            self._credentials[credential_id] = cred
        
        logger.info("FN:CredentialPool.add_credential Added credential: %s", credential_id)
    
    def acquire(self, credential_id: str) -> Credential:
        """FN:acquire Acquire a credential from the pool.
        
        Args:
            credential_id: Credential identifier
            
        Returns:
            Credential object
            
        Raises:
            KeyError: If credential not found
        """
        with self._lock:
            if credential_id not in self._credentials:
                raise KeyError(f"Credential not found: {credential_id}")
            
            cred = self._credentials[credential_id]
            
            # Check expiration
            if cred.is_expired:
                logger.warning("FN:CredentialPool.acquire Expired credential: %s", credential_id)
                raise ValueError(f"Credential expired: {credential_id}")
            
            self._in_use.add(credential_id)
            logger.info("FN:CredentialPool.acquire Acquired credential: %s", credential_id)
            return cred
    
    def release(self, credential: Credential) -> None:
        """FN:release Release a credential back to the pool.
        
        Args:
            credential: Credential to release
        """
        with self._lock:
            credential_id = credential.credential_id
            if credential_id in self._in_use:
                self._in_use.remove(credential_id)
                logger.info("FN:CredentialPool.release Released credential: %s", credential_id)
    
    def rotate(self, credential_id: str, new_value: str) -> None:
        """FN:rotate Rotate a credential with a new value.
        
        Args:
            credential_id: Credential identifier
            new_value: New credential value
        """
        with self._lock:
            if credential_id not in self._credentials:
                raise KeyError(f"Credential not found: {credential_id}")
            
            old_cred = self._credentials[credential_id]
            new_cred = Credential(
                credential_id=credential_id,
                value=new_value,
                expires_at=old_cred.expires_at,
                metadata=old_cred.metadata
            )
            
            self._credentials[credential_id] = new_cred
            logger.info("FN:CredentialPool.rotate Rotated credential: %s", credential_id)
    
    def remove(self, credential_id: str) -> bool:
        """FN:remove Remove a credential from the pool.
        
        Args:
            credential_id: Credential identifier
            
        Returns:
            True if removed, False if not found
        """
        with self._lock:
            if credential_id in self._credentials:
                del self._credentials[credential_id]
                self._in_use.discard(credential_id)
                logger.info("FN:CredentialPool.remove Removed credential: %s", credential_id)
                return True
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """FN:get_stats Get credential pool statistics.
        
        Returns:
            Dict with pool stats
        """
        with self._lock:
            return {
                "total_credentials": len(self._credentials),
                "in_use": len(self._in_use),
                "available": len(self._credentials) - len(self._in_use),
                "expired": sum(1 for c in self._credentials.values() if c.is_expired),
            }
