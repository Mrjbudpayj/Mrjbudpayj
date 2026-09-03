import hashlib, json
from pathlib import Path
from canonicalization.jcs import jcs_canonicalize, load_json


def resolve_policy(version, digest):
    path=Path("policy-artifacts")/f"policy-{version}-{digest.lower()}.json"
    if not path.exists(): raise FileNotFoundError(path)
    data=load_json(path.read_text())
    if hashlib.sha256(jcs_canonicalize(data)).hexdigest() != digest.lower(): raise ValueError("policy digest mismatch")
    return data


def reconstruct_determination(fixture):
    x=fixture["input"]; p=resolve_policy(x["policy"]["version"],x["policy"]["digest"])
    if x["authority_valid"] is not True: return {"kind":"NOT_ADMIT","reason_code":"DENIED_AUTHORITY"}
    if x["amount"] > p["limits"]["transfer_max"]: return {"kind":"NOT_ADMIT","reason_code":"DENIED_POLICY_LIMIT"}
    if x["balance"] < x["amount"]: return {"kind":"NOT_ADMIT","reason_code":"DENIED_INSUFFICIENT_FUNDS"}
    if x["risk"] == "elevated": return {"kind":"NOT_ADMIT","reason_code":"DENIED_RISK"}
    return {"kind":"ADMIT","reason_code":"APPROVED"}


def main():
    s=load_json(Path("observed-artifacts/summary.json").read_text()); results=[]
    for row in s["fixtures"]:
        f=load_json(next(Path("fixtures").glob(row["fixture_id"]+".json")).read_text())
        dr=reconstruct_determination(f)
        results.append({"fixture_id":row["fixture_id"],"D_P":row["D_P"],"D_R":dr,"match":dr==row["D_P"]})
    Path("observed-artifacts/replay-summary.json").write_text(json.dumps({"results":results,"pass":all(r["match"] for r in results)},indent=2,sort_keys=True))

if __name__ == "__main__": main()
