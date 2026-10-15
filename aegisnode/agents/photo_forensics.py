"""
AegisNode - Proof-of-Delivery (POD) Visual Forensics & Replay Defense
Implements fail-closed image decoding, Laplacian edge variance, and perceptual difference hashing (dHash).
Detects synthetic captures, floor-mat obscuration, and photo replay attacks across shipments.
Strict enterprise compliance - Zero Emojis.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

REGISTRY_FILE = Path(__file__).resolve().parent.parent / "data" / "photo_registry.json"

def _compute_dhash(gray_image) -> str:
    """
    Computes a 64-bit difference hash (dHash) from a grayscale OpenCV image.
    Resizes to 9x8 and compares horizontal gradient intensity.
    """
    import cv2
    resized = cv2.resize(gray_image, (9, 8), interpolation=cv2.INTER_AREA)
    difference = resized[:, 1:] > resized[:, :-1]
    # Pack 64 booleans into 16-hex characters
    decimal_val = 0
    hex_str = []
    for index, val in enumerate(difference.flatten()):
        if val:
            decimal_val += 2 ** (index % 4)
        if index % 4 == 3:
            hex_str.append(hex(decimal_val)[2:])
            decimal_val = 0
    return "".join(hex_str)

def _hamming_distance(hash1: str, hash2: str) -> int:
    """Calculates bitwise Hamming distance between two 16-hex character hashes."""
    if len(hash1) != len(hash2):
        return 64
    val1 = int(hash1, 16)
    val2 = int(hash2, 16)
    return bin(val1 ^ val2).count("1")

class PhotoForensicsEngine:
    """Analyzes raw POD photo bytes, evaluates texture variance, and enforces replay defense."""

    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or REGISTRY_FILE
        self._registry: Dict[str, Dict[str, Any]] = self._load_registry()

    def _load_registry(self) -> Dict[str, Dict[str, Any]]:
        if not self.registry_path.exists():
            return {}
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_registry(self):
        try:
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(self._registry, f, indent=2)
        except Exception:
            pass

    def clear_registry(self):
        """Clears the replay registry (used for test teardown)."""
        self._registry = {}
        if self.registry_path.exists():
            try:
                os.remove(self.registry_path)
            except Exception:
                pass

    def analyze_photo_bytes(
        self,
        image_bytes: bytes,
        shipment_id: str = "UNKNOWN",
        variance_threshold: float = 55.0,
        brightness_threshold: float = 35.0
    ) -> Dict[str, Any]:
        """
        Analyzes uploaded photo bytes with strict FAIL-CLOSED security rules.
        Rejects invalid bytes, zero-length files, low-texture floor mats, and replayed photos.
        """
        # Rule 1: Fail closed on empty or invalid byte lengths
        if not image_bytes or len(image_bytes) < 64:
            return {
                "valid": False,
                "status": "REJECTED_PAYLOAD",
                "photo_status": "FORGED",
                "variance": 0.0,
                "brightness": 0.0,
                "dhash": "",
                "is_replay": False,
                "anomaly_score": 1.0,
                "message": "Empty or corrupted image payload. Fails closed."
            }

        if len(image_bytes) > 15 * 1024 * 1024:
            return {
                "valid": False,
                "status": "PAYLOAD_TOO_LARGE",
                "photo_status": "FORGED",
                "variance": 0.0,
                "brightness": 0.0,
                "dhash": "",
                "is_replay": False,
                "anomaly_score": 1.0,
                "message": "Payload exceeds 15MB limit. Fails closed."
            }

        try:
            import cv2
            import numpy as np

            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Rule 2: Fail closed if raster decoding fails (garbage bytes)
            if img is None:
                return {
                    "valid": False,
                    "status": "DECODE_FAILURE",
                    "photo_status": "FORGED",
                    "variance": 0.0,
                    "brightness": 0.0,
                    "dhash": "",
                    "is_replay": False,
                    "anomaly_score": 1.0,
                    "message": "Raster decode failure. Uploaded bytes are not a valid JPEG/PNG."
                }

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            variance = float(cv2.Laplacian(gray, cv2.CV_64F).var())
            brightness = float(np.mean(gray))
            dhash_str = _compute_dhash(gray)

            # Rule 3: Replay Attack Defense (Perceptual hash collision across shipments)
            is_replay = False
            collided_shipment = ""
            for reg_hash, reg_meta in self._registry.items():
                if reg_meta.get("shipment_id") != shipment_id:
                    dist = _hamming_distance(dhash_str, reg_hash)
                    if dist <= 3:  # Perceptual hash collision threshold
                        is_replay = True
                        collided_shipment = reg_meta.get("shipment_id", "HISTORICAL")
                        break

            if is_replay:
                return {
                    "valid": False,
                    "status": "REPLAY_ATTACK",
                    "photo_status": "FORGED",
                    "variance": round(variance, 1),
                    "brightness": round(brightness, 1),
                    "dhash": dhash_str,
                    "is_replay": True,
                    "anomaly_score": 0.98,
                    "message": f"Perceptual hash match with shipment {collided_shipment}. Recycled image detected."
                }

            # Rule 4: Sensor obscuration, blank image, or dark floor mat
            if variance < variance_threshold or brightness < brightness_threshold or variance == 0.0:
                return {
                    "valid": False,
                    "status": "TEXTURE_DEFICIT",
                    "photo_status": "FORGED",
                    "variance": round(variance, 1),
                    "brightness": round(brightness, 1),
                    "dhash": dhash_str,
                    "is_replay": False,
                    "anomaly_score": 0.92,
                    "message": f"Optical texture ({variance:.1f}) below edge threshold ({variance_threshold}). Floor mat or covered sensor."
                }

            # Passed all zero-trust checks: register hash to prevent future replay
            self._registry[dhash_str] = {
                "shipment_id": shipment_id,
                "variance": round(variance, 1),
                "timestamp": str(os.path.getmtime(self.registry_path) if self.registry_path.exists() else 0)
            }
            self._save_registry()

            return {
                "valid": True,
                "status": "VERIFIED",
                "photo_status": "VALID",
                "variance": round(variance, 1),
                "brightness": round(brightness, 1),
                "dhash": dhash_str,
                "is_replay": False,
                "anomaly_score": 0.04,
                "message": "Optical edge entropy and texture verified. Zero replay anomaly."
            }

        except Exception as exc:
            # Rule 5: Strict Fail-Closed on any unhandled forensic exception
            return {
                "valid": False,
                "status": "FORENSIC_EXCEPTION",
                "photo_status": "FORGED",
                "variance": 0.0,
                "brightness": 0.0,
                "dhash": "",
                "is_replay": False,
                "anomaly_score": 1.0,
                "message": f"Forensic analysis error: {str(exc)}. Failing closed."
            }

_GLOBAL_PHOTO_ENGINE = PhotoForensicsEngine()

def get_photo_engine() -> PhotoForensicsEngine:
    return _GLOBAL_PHOTO_ENGINE
