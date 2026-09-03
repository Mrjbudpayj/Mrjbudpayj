from policy import resolve_policy


def determine(fixture: dict, corpus_dir: str) -> dict:
    x = fixture["input"]
    p = resolve_policy(x["policy"]["version"], x["policy"]["digest"], corpus_dir)
    if not x["authority_valid"]:
        return {"kind":"NOT_ADMIT","reason_code":"DENIED_AUTHORITY"}
    if x["amount"] > p["limits"]["transfer_max"]:
        return {"kind":"NOT_ADMIT","reason_code":"DENIED_POLICY_LIMIT"}
    if x["balance"] < x["amount"]:
        return {"kind":"NOT_ADMIT","reason_code":"DENIED_INSUFFICIENT_FUNDS"}
    if x["risk"] == "elevated":
        return {"kind":"NOT_ADMIT","reason_code":"DENIED_RISK"}
    return {"kind":"ADMIT","reason_code":"APPROVED"}
