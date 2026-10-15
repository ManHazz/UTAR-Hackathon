"""
AegisNode - Cryptographic Zero-Trust Audit Ledger
Provides non-repudiation, HMAC digital signatures, and tamper-evident logging for all agent findings.
Defends against history re-computation, genesis block tampering, and rollback attacks.
Strict enterprise compliance - Zero Emojis.
"""

import os
import hmac
import json
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

LEDGER_SIGNING_KEY = os.getenv("AEGISNODE_LEDGER_KEY", "aegisnode_soar_ledger_hmac_secret_2026").encode("utf-8")
LEDGER_STORE_PATH = Path(__file__).resolve().parent.parent / "data" / "audit_ledger.json"

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
    signature: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class AuditLedger:
    """Tamper-evident, HMAC-signed hash-chained ledger storing all multi-agent actions."""

    def __init__(self, signing_key: Optional[bytes] = None, storage_path: Optional[Path] = None):
        self.signing_key = signing_key or LEDGER_SIGNING_KEY
        self.storage_path = storage_path
        self.chain: List[AuditBlock] = []
        if self.storage_path is not None and self.storage_path.exists():
            self._load_or_initialize()
        else:
            self.reset()

    def reset(self):
        """Resets chain to fresh genesis block."""
        self.chain = []
        self._create_genesis_block()
        if self.storage_path is not None:
            self._persist()

    def _load_or_initialize(self):
        """Loads existing verified chain from disk or initializes a signed genesis block."""
        if self.storage_path and self.storage_path.exists():
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        loaded_blocks = []
                        for b in data:
                            loaded_blocks.append(AuditBlock(
                                index=b["index"],
                                timestamp=b["timestamp"],
                                agent=b["agent"],
                                action=b["action"],
                                target_id=b["target_id"],
                                details=b["details"],
                                prev_hash=b["prev_hash"],
                                block_hash=b["block_hash"],
                                signature=b.get("signature", "")
                            ))
                        self.chain = loaded_blocks
                        # If chain is valid, keep it; otherwise reinitialize
                        if self.verify_integrity()["valid"]:
                            return
            except Exception:
                pass

        self.reset()

    def _persist(self):
        """Atomically saves the verified chain to disk if storage_path is configured."""
        if not self.storage_path:
            return
        try:
            tmp = self.storage_path.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump([b.to_dict() for b in self.chain], f, indent=2)
            os.replace(tmp, self.storage_path)
        except Exception:
            pass

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
        sig = self._calculate_signature(block_hash)
        genesis_block = AuditBlock(
            index=0,
            timestamp=timestamp,
            agent="SYSTEM",
            action="GENESIS",
            target_id="ROOT",
            details=genesis_details,
            prev_hash="0" * 64,
            block_hash=block_hash,
            signature=sig
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

    def _calculate_signature(self, block_hash: str) -> str:
        """Signs the block hash using HMAC-SHA256 with the agent private secret."""
        return hmac.new(self.signing_key, block_hash.encode("utf-8"), hashlib.sha256).hexdigest()

    def record(
        self,
        agent: str,
        action: str,
        target_id: str,
        details: Dict[str, Any]
    ) -> AuditBlock:
        """
        Appends a new cryptographically signed verified event block to the ledger.
        Enforces idempotency: ignores exact duplicate requests on UI page reruns.
        """
        prev_block = self.chain[-1]

        # Idempotency check: if last block is identical in agent, action, target_id, and details, avoid duplicate
        if (
            prev_block.agent == agent
            and prev_block.action == action
            and prev_block.target_id == target_id
            and prev_block.details == details
        ):
            return prev_block

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
        signature = self._calculate_signature(block_hash)

        new_block = AuditBlock(
            index=index,
            timestamp=timestamp,
            agent=agent,
            action=action,
            target_id=target_id,
            details=details,
            prev_hash=prev_block.block_hash,
            block_hash=block_hash,
            signature=signature
        )
        self.chain.append(new_block)
        self._persist()
        return new_block

    def verify_integrity(self, expected_total_blocks: Optional[int] = None) -> Dict[str, Any]:
        """
        Validates the entire chain from Genesis to tip.
        Verifies block hashes, sequential links, and HMAC digital signatures.
        Detects genesis tampering, payload modifications, signature forgery, and rollback deletions.
        """
        if not self.chain:
            return {"valid": False, "reason": "Chain is empty"}

        # 1. Rollback / Truncation check
        if expected_total_blocks is not None and len(self.chain) != expected_total_blocks:
            return {
                "valid": False,
                "tampered_at_index": len(self.chain),
                "reason": f"Rollback detected: expected {expected_total_blocks} blocks but chain has {len(self.chain)}"
            }

        # 2. Genesis Block Check
        genesis = self.chain[0]
        if genesis.index != 0 or genesis.prev_hash != "0" * 64:
            return {
                "valid": False,
                "tampered_at_index": 0,
                "reason": "Genesis block structure tampered (index or prev_hash invalid)"
            }

        genesis_calc_hash = self._calculate_hash(
            index=0,
            timestamp=genesis.timestamp,
            agent=genesis.agent,
            action=genesis.action,
            target_id=genesis.target_id,
            details=genesis.details,
            prev_hash="0" * 64
        )
        if genesis.block_hash != genesis_calc_hash:
            return {
                "valid": False,
                "tampered_at_index": 0,
                "reason": "Genesis block payload modified"
            }

        genesis_expected_sig = self._calculate_signature(genesis.block_hash)
        if not hmac.compare_digest(genesis.signature, genesis_expected_sig):
            return {
                "valid": False,
                "tampered_at_index": 0,
                "reason": "Genesis digital signature invalid"
            }

        # 3. Subsequent Blocks Check
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            if curr.index != i:
                return {
                    "valid": False,
                    "tampered_at_index": i,
                    "reason": f"Block #{i} index sequence gap detected"
                }

            if curr.prev_hash != prev.block_hash:
                return {
                    "valid": False,
                    "tampered_at_index": i,
                    "reason": f"Block #{i} prev_hash does not match Block #{i-1} block_hash"
                }

            recalculated_hash = self._calculate_hash(
                index=curr.index,
                timestamp=curr.timestamp,
                agent=curr.agent,
                action=curr.action,
                target_id=curr.target_id,
                details=curr.details,
                prev_hash=curr.prev_hash
            )
            if curr.block_hash != recalculated_hash:
                return {
                    "valid": False,
                    "tampered_at_index": i,
                    "reason": f"Block #{i} payload hash mismatch (data was modified)"
                }

            expected_sig = self._calculate_signature(curr.block_hash)
            if not hmac.compare_digest(curr.signature, expected_sig):
                return {
                    "valid": False,
                    "tampered_at_index": i,
                    "reason": f"Block #{i} HMAC digital signature invalid (signature forgery or unauthorized re-hash)"
                }

        return {
            "valid": True,
            "total_blocks": len(self.chain),
            "latest_hash": self.chain[-1].block_hash if self.chain else None,
            "anchor_signature": self.chain[-1].signature[:16] if self.chain else None
        }

    def get_records(self) -> List[Dict[str, Any]]:
        return [b.to_dict() for b in self.chain]

    # Backward compatibility alias
    append_entry = record

