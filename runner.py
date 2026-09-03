import json, hashlib
from pathlib import Path
from canonicalization.jcs import jcs_canonicalize, load_json
from policy import resolve_policy
from determination import determine

FIXTURES = sorted(Path("fixtures").glob("fixture-*.json"))

def main():
    out = Path("observed-artifacts"); (out/"determinations").mkdir(parents=True, exist_ok=True); (out/"witnesses").mkdir(exist_ok=True)
    rows=[]
    for fp in FIXTURES:
        f=load_json(fp.read_text())
        d=determine(f, ".")
        core={"fixture_id":f["fixture_id"],"input":f["input"],"determination":d,"contract_version":"0.1","toolchain_version":"a11-python-reference-0.1"}
        h=hashlib.sha256(jcs_canonicalize(core)).hexdigest()
        (out/"determinations"/(f["fixture_id"]+".json")).write_text(json.dumps(d,sort_keys=True,separators=(",",":")))
        (out/"witnesses"/(f["fixture_id"]+".json")).write_bytes(jcs_canonicalize(core))
        (out/"witnesses"/(f["fixture_id"]+".witness_digest_hex")).write_text(h+"\n")
        rows.append({"fixture_id":f["fixture_id"],"D_P":d,"H_W":h})
    (out/"summary.json").write_text(json.dumps({"fixtures":rows},indent=2,sort_keys=True))

if __name__ == "__main__": main()
