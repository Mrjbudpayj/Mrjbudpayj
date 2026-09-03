import hashlib
import re
from pathlib import Path
from canonicalization.jcs import jcs_canonicalize, load_json

HEX64_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def resolve_policy(policy_version: str, policy_digest: str, corpus_dir: str) -> dict:
    if len(policy_digest) != 64:
        raise ValueError(f"Invalid policy digest length: {len(policy_digest)}")
    if not HEX64_RE.fullmatch(policy_digest):
        raise ValueError(f"Invalid policy digest encoding: {policy_digest}")
    path = Path(corpus_dir) / "policy-artifacts" / f"policy-{policy_version}-{policy_digest.lower()}.json"
    if not path.exists():
        raise FileNotFoundError(str(path))
    data = load_json(path.read_text(encoding="utf-8"))
    computed = hashlib.sha256(jcs_canonicalize(data)).hexdigest()
    if computed.lower() != policy_digest.lower():
        raise ValueError(f"Policy digest mismatch: expected {policy_digest}, computed {computed}")
    return data
