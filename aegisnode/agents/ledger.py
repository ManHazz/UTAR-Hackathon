"""
AegisNode - Cryptographic Zero-Trust Audit Ledger
Provides non-repudiation and tamper-evident logging for all agent findings and actions.
Aligned with Zero-Trust architecture and ANON Cybersecurity Hackathon requirements.
"""

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class AuditBlock:
    index: int
    timestamp: str
    agent: str
    action: str
    target_id: str
    details: Dict[str, Any]
    prev_hash: str
    block_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class AuditLedger:
    """Tamper-evident, hash-chained ledger storing agent decisions."""
    
    def __init__(self):
        self.chain: List[AuditBlock] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        timestamp = datetime.now(timezone.utc).isoformat()
        genesis_details = {"message": "AegisNode Zero-Trust Genesis Block Initialized"}
        block_hash = self._calculate_hash(
            index=0,
            timestamp=timestamp,
            agent="SYSTEM",
            action="GENESIS",
            target_id="ROOT",
            details=genesis_details,
            prev_hash="0" * 64
        )
        genesis_block = AuditBlock(
            index=0,
            timestamp=timestamp,
            agent="SYSTEM",
            action="GENESIS",
            target_id="ROOT",
            details=genesis_details,
            prev_hash="0" * 64,
            block_hash=block_hash
        )
        self.chain.append(genesis_block)

    @staticmethod
    def _calculate_hash(
        index: int,
        timestamp: str,
        agent: str,
        action: str,
        target_id: str,
        details: Dict[str, Any],
        prev_hash: str
    ) -> str:
        serialized_details = json.dumps(details, sort_keys=True)
        raw_string = f"{index}|{timestamp}|{agent}|{action}|{target_id}|{serialized_details}|{prev_hash}"
        return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()

    def record(
        self,
        agent: str,
        action: str,
        target_id: str,
        details: Dict[str, Any]
    ) -> AuditBlock:
        """Appends a new verified event block to the ledger."""
        prev_block = self.chain[-1]
        index = prev_block.index + 1
        timestamp = datetime.now(timezone.utc).isoformat()
        
        block_hash = self._calculate_hash(
            index=index,
            timestamp=timestamp,
            agent=agent,
            action=action,
            target_id=target_id,
            details=details,
            prev_hash=prev_block.block_hash
        )

        new_block = AuditBlock(
            index=index,
            timestamp=timestamp,
            agent=agent,
            action=action,
            target_id=target_id,
            details=details,
            prev_hash=prev_block.block_hash,
            block_hash=block_hash
        )
        self.chain.append(new_block)
        return new_block

    def verify_integrity(self) -> Dict[str, Any]:
        """Validates the entire hash chain from Genesis to tip."""
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # Check prev_hash pointer
            if curr.prev_hash != prev.block_hash:
                return {
                    "valid": False,
                    "tampered_at_index": i,
                    "reason": f"Block #{i} prev_hash does not match Block #{i-1} block_hash"
                }

            # Recalculate hash to ensure payload hasn't been altered
            recalculated = self._calculate_hash(
                index=curr.index,
                timestamp=curr.timestamp,
                agent=curr.agent,
                action=curr.action,
                target_id=curr.target_id,
                details=curr.details,
                prev_hash=curr.prev_hash
            )
            if curr.block_hash != recalculated:
                return {
                    "valid": False,
                    "tampered_at_index": i,
                    "reason": f"Block #{i} payload hash mismatch (data was modified)"
                }

        return {
            "valid": True,
            "total_blocks": len(self.chain),
            "latest_hash": self.chain[-1].block_hash if self.chain else None
        }

    def get_records(self) -> List[Dict[str, Any]]:
        return [b.to_dict() for b in self.chain]
