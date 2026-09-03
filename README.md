# A11-1.0 Agentic Execution Contract Certification

Frozen certification baseline for deterministic reference execution, witness preservation, hash-chain integrity, and independent replay.

Pipeline: IMPLEMENT -> EXECUTE -> PRESERVE -> REPLAY -> COMPARE -> AUDIT -> RELEASE

Current state: implementation candidate committed on a branch; certification remains blocked until CI and replay produce observed evidence.

Frozen invariants:
- H_W = SHA256(JCS(W_core))
- policyDigest = SHA256(JCS(policyArtifact))
- expected_outcome_label is an oracle only
- Replay is independent reconstruction, not re-execution
