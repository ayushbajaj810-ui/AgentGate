"""Runs the 6 required test cases (+1 extra) on a fresh database and writes TEST_RESULTS.md"""
import os
from gatekeeper import Gatekeeper, ENROLMENT_NO, LIMIT
if os.path.exists("test.db"): os.remove("test.db")
gk = Gatekeeper("test.db")
gk.register("Asha", "ShopBot"); gk.register("Asha", "OldBot"); gk.revoke("Asha", "OldBot")
cases = [  # (name, customer, agent, action, amount, expected decision, expected rule)
 ("T1 known agent, read-only",      "Asha", "ShopBot", "view_order",  0,          "ALLOW", "R4"),
 ("T2 unknown agent",               "Asha", "RogueBot","place_order", 500,        "BLOCK", "R1"),
 ("T3 payment above limit",         "Asha", "ShopBot", "place_order", LIMIT+1000, "ASK CUSTOMER", "R5"),
 ("T4 payment below limit",         "Asha", "ShopBot", "place_order", LIMIT-1000, "ALLOW", "R5"),
 ("T5 revoked agent tries to act",  "Asha", "OldBot",  "place_order", 100,        "BLOCK", "R2"),
 ("T6 own case: refund request",    "Asha", "ShopBot", "refund",      300,        "ASK CUSTOMER", "R7"),
 ("T7 extra: Asha's agent acts for another customer", "Ravi", "ShopBot", "view_order", 0, "BLOCK", "R1"),
 ("T8 own verification: revoked agent attempts view_order", "Asha", "OldBot", "view_order", 0, "BLOCK", "R2"),
]
out = [f"Enrolment no: {ENROLMENT_NO}  |  Limit: {LIMIT}\n", "| Test | Request | Expected | Actual | Pass |", "|---|---|---|---|---|"]
for n, c, a, act, amt, ed, er in cases:
    r = gk.decide(c, a, act, amt)
    ok = (r["decision"], r["rule"]) == (ed, er)
    out.append(f"| {n} | {c}/{a}/{act}/{amt} | {ed} ({er}) | {r['decision']} ({r['rule']}) | {'PASS' if ok else 'FAIL'} |")
open("TEST_RESULTS.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
