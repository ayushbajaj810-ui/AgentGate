# PROMPTS.md

Name: Ayush Bajaj   Enrolment no: PGD202571828   Company: Amazon (Amazon.in)
AI tool used: Antigravity / Claude
Date(s) of session: 19 Nov 2026

## Main instructions I gave the coding agent
Edit the wording to match what you REALLY typed. Do not list prompts you did not use.

1. **Brief and company.** "Here is my assignment brief (Agent Gatekeeper). My enrolment number ends in
   7-9, so my company type is an online store (view order, place order, return, refund). Which real
   company should I use?"  -> Chose Amazon, because it publicly blocks AI shopping agents.
2. **Research.** "Search for current news on Amazon blocking AI shopping agents so I have my own source
   for the report."  -> Found The Paypers / VKTR / The New Stack articles (Sept 2026).
3. **Rules.** "Design 6-8 rules: unknown agents blocked, revoked agents always blocked, read-only allowed,
   money actions above a limit need the customer's confirmation. Pick a limit and justify it."
   -> 8 rules in RULES.md, limit INR 2,000.
4. **Build.** "Build a small Python prototype: input = customer, agent, action, amount; output =
   ALLOW / ASK CUSTOMER / BLOCK with rule number; SQLite audit log with date and time; register and
   revoke agent with saved timestamp; show my enrolment number on the main screen; simple web page."
   -> gatekeeper.py (engine), app.py (web page).
5. **Tests.** "Write a script that runs 6 test cases (known read-only, unknown agent, payment above
   limit, payment below limit, revoked agent, one of my own) and prints expected vs actual."
   -> run_tests.py, TEST_RESULTS.md.

## One thing I checked or changed myself
- I read `gatekeeper.py` and traced the rule evaluation order: R1 (unknown) -> R2 (revoked) -> R3 (invalid request) -> Action rules (R4 to R7).
- To verify that security restrictions strictly supersede functional permissions, I added test case **T8** to `run_tests.py`: a revoked agent (`OldBot`) attempting a read-only request (`view_order`).
- Result: The request was strictly `BLOCK (R2)` rather than `ALLOW (R4)`, verifying that revocation takes precedence over read-only permissions. Test passed.
