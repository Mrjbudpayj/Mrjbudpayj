import hashlib
import json
import pytest
from canonicalization.jcs import jcs_canonicalize, load_json
from policy import resolve_policy


def digest(obj):
    return hashlib.sha256(jcs_canonicalize(obj)).hexdigest()


def test_policy_digest_verifies_and_loads(tmp_path):
    p = {"version":"1.0","limits":{"transfer_max":1000},"mode":"standard"}
    d = digest(p)
    root = tmp_path / "corpus" / "policy-artifacts"
    root.mkdir(parents=True)
    (root / f"policy-1.0-{d}.json").write_text(json.dumps(p, indent=2), encoding="utf-8")
    assert resolve_policy("1.0", d, str(tmp_path / "corpus")) == p


def test_policy_digest_length_validation(tmp_path):
    with pytest.raises(ValueError): resolve_policy("1.0", "a" * 63, str(tmp_path))


def test_policy_digest_encoding_validation(tmp_path):
    with pytest.raises(ValueError): resolve_policy("1.0", "z" * 64, str(tmp_path))


def test_policy_digest_mismatch(tmp_path):
    root = tmp_path / "corpus" / "policy-artifacts"; root.mkdir(parents=True)
    (root / ("policy-1.0-" + "0"*64 + ".json")).write_text('{"version":"1.0"}', encoding="utf-8")
    with pytest.raises(ValueError, match="mismatch"): resolve_policy("1.0", "0"*64, str(tmp_path / "corpus"))


def test_missing_policy_artifact(tmp_path):
    with pytest.raises(FileNotFoundError): resolve_policy("1.0", "0"*64, str(tmp_path / "corpus"))


def test_jcs_policy_reordering_same_digest():
    a = {"b":2,"a":1}; b = {"a":1,"b":2}
    assert digest(a) == digest(b)


def test_jcs_policy_change_changes_digest():
    assert digest({"a":1}) != digest({"a":2})


def test_duplicate_json_members_rejected():
    with pytest.raises(ValueError): load_json('{"a":1,"a":2}')


def test_negative_zero():
    assert jcs_canonicalize(-0.0) == b"0"
    assert jcs_canonicalize({"amount": -0.0}) == b'{"amount":0}'


def test_nonfinite_rejected():
    with pytest.raises(ValueError): jcs_canonicalize(float("nan"))
    with pytest.raises(ValueError): jcs_canonicalize(float("inf"))
