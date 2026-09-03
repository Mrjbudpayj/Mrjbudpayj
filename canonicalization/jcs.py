"""RFC 8785 JCS boundary.

The implementation delegates canonicalization to the pinned, vetted rfc8785
package rather than maintaining a partial hand-written number/string encoder.
"""
import json
from typing import Any
import rfc8785


def _reject_duplicates(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError(f"duplicate JSON member: {k}")
        out[k] = v
    return out


def load_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=_reject_duplicates)


def jcs_canonicalize(value: Any) -> bytes:
    return rfc8785.dumps(value)
