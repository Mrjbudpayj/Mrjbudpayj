import json
from pathlib import Path


def render():
    s=json.loads(Path("observed-artifacts/summary.json").read_text())
    r=json.loads(Path("observed-artifacts/replay-summary.json").read_text())
    rows=[]
    for x in r["results"]:
        rows.append(f"| {x['fixture_id']} | {x['D_P']['reason_code']} | {x['D_R']['reason_code']} | {'PASS' if x['match'] else 'FAIL'} |")
    passed=bool(r["pass"])
    report="# RAR-0001\n\n"+f"**PASS:** {passed}\n\n"+"| Fixture | D_P | D_R | Result |\n|---|---|---|---|\n"+"\n".join(rows)+"\n"
    Path("observed-artifacts/RAR-0001.md").write_text(report)

if __name__ == "__main__": render()
