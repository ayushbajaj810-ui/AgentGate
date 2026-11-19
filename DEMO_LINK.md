# Demonstration Video Information (Part E)

**Student:** Ayush Bajaj | **Enrolment No:** PGD202571828 | **Domain:** Amazon.in

### 1. Pre-generated Assets Included in Submission
- `demo.mp4`: Base video container in submission directory.
- `narration.m4a`: Spoken demonstration voiceover generated with enrolment number and test walkthrough.
- `preview.html`: Live interactive demonstration dashboard showing real-time agent registration, decision engine outputs, and audit logs.
- `walkthrough.html`: 2-minute visual slide walkthrough matching the script.

### 2. Video Demonstration Script (2 Minutes)
1. **0:00 - 0:15:** "Hello, I am Ayush Bajaj, enrolment number PGD202571828. This is the Agent Gatekeeper prototype for Amazon.in."
2. **0:15 - 0:35:** Explain the 8 rules: unknown agents blocked (R1), revoked agents blocked (R2), read-only allowed (R4), limit INR 2,000 (R5/R6), refunds always ask (R7), audit logging (R8).
3. **0:35 - 1:35:** Walkthrough of operations:
   - Register `ShopBot` for `Asha`
   - `view_order` -> `ALLOW (R4)`
   - Unregistered `RogueBot` -> `BLOCK (R1)`
   - `place_order` INR 3,000 -> `ASK CUSTOMER (R5)`
   - `place_order` INR 1,000 -> `ALLOW (R5)`
   - Revoke `ShopBot`, then retry `place_order` -> `BLOCK (R2)`
   - `refund` INR 300 -> `ASK CUSTOMER (R7)`
4. **1:35 - 1:55:** Highlight Registered Agents table (timestamped revocation) and Audit Log. Explain resolution to the Wells Fargo unauthorized transactions dispute.
5. **1:55 - 2:00:** Verification of 8/8 test suite passing. Conclude.

### 3. Optional Video Link (if hosted online)
- Google Drive / YouTube Link: *(If uploading online, paste your shared link here)*
