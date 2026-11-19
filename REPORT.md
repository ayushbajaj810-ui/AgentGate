# Executive Report: AI Agent Gatekeeper for Amazon.in
**Student:** Ayush Bajaj | **Enrolment No:** PGD202571828 | **Domain:** Online E-Commerce Retail (Amazon.in)  
**Submission Date:** 20 November 2026 | **GitHub Repository:** `https://github.com/ayushbajaj810-ui/AgentGate`

---

## 1. Company Profile and Problem Statement

As autonomous AI agents (such as Meta’s Muse, Perplexity Shopping, and shopping co-pilots) emerge to perform automated browsing, product comparison, order placement, and returns on behalf of consumers, major digital platforms face unprecedented security and liability challenges. **Amazon (Amazon.in)**, the world’s leading e-commerce marketplace, recently enacted strict technical and policy blocks against external AI shopping agents.

This blanket ban mirrors protective actions taken across regulated industries:
- **JPMorgan Chase & Delta Air Lines:** Blocked consumer financial and booking bots to protect proprietary APIs, prevent scraping-induced outages, and safeguard user account credentials.
- **The "Wells Fargo Problem":** Highlights the severe accountability crisis when actions occur without auditable, customer-authorized consent. In automated delegation, if a customer revokes an agent's authority but the system lacks timestamped proof, liability for unauthorized transactions becomes legally contested.
- **The Meta Muse Incident (The Paypers / VKTR, Sept 2026):** Amazon blocked Meta's AI agent "Muse" from executing checkout actions due to security and commercial risks. Tellingly, competitor **Shopify** permitted Muse within 24 hours under controlled API boundaries, highlighting how outright blocking can alienate users and drive market share to competitors.

Rather than an outright block, an **Agent Gatekeeper** provides a mediated trust layer—enforcing explicit customer registration, immutable audit logging, instant revocation, and human-in-the-loop approvals for sensitive transactions.

---

## 2. Gatekeeper Security Rules & Financial Limit

The system enforces 8 sequential rules to balance customer autonomy with risk mitigation.

| # | Rule Identifier | Rule Definition | Gatekeeper Decision |
|---|---|---|---|
| **R1** | Unknown Agent | Agent not explicitly registered by the customer. | **BLOCK** |
| **R2** | Revoked Agent | Agent previously registered but subsequently revoked. | **BLOCK** |
| **R3** | Malformed Request | Missing fields, unrecognized actions, or negative transaction amounts. | **BLOCK** |
| **R4** | Read-Only Access | `view_order` queries containing zero financial commitment. | **ALLOW** |
| **R5** | Order Placement | `place_order` up to limit is approved; above limit requires explicit customer confirmation. | **ALLOW** / **ASK CUSTOMER** |
| **R6** | Product Returns | `return` up to limit is approved; above limit requires explicit customer confirmation. | **ALLOW** / **ASK CUSTOMER** |
| **R7** | Direct Refunds | `refund` transactions always require human customer authorization. | **ASK CUSTOMER** |
| **R8** | Audit Logging | Every request, registration, and revocation event is logged with ISO timestamps in SQLite. | *(System Logger)* |

### Spending Limit Justification (INR 2,000)
The threshold of **INR 2,000** was selected as a realistic benchmark for everyday, low-value consumables on Amazon.in (e.g., household supplies, books, groceries). Errors under INR 2,000 carry minimal risk and can be reversed cheaply without customer fatigue, whereas transactions exceeding INR 2,000 justify a one-tap manual confirmation to prevent substantial unintended expenditures.

---

## 3. Test Cases and Verification Results

The decision engine was evaluated using `run_tests.py` against a dedicated test database (`test.db`). All test cases completed with 100% pass rate.

**Enrolment No:** PGD202571828 | **Configured Limit:** INR 2,000

| Test | Scenario Description | Test Request Payload | Expected Output | Actual Output | Status |
|:---|:---|:---|:---|:---|:---:|
| **T1** | Known agent, read-only | `Asha/ShopBot/view_order/0` | ALLOW (R4) | ALLOW (R4) | **PASS** |
| **T2** | Unregistered rogue agent | `Asha/RogueBot/place_order/500` | BLOCK (R1) | BLOCK (R1) | **PASS** |
| **T3** | Order exceeding limit | `Asha/ShopBot/place_order/3000` | ASK CUSTOMER (R5) | ASK CUSTOMER (R5) | **PASS** |
| **T4** | Order within limit | `Asha/ShopBot/place_order/1000` | ALLOW (R5) | ALLOW (R5) | **PASS** |
| **T5** | Revoked agent order | `Asha/OldBot/place_order/100` | BLOCK (R2) | BLOCK (R2) | **PASS** |
| **T6** | Refund request | `Asha/ShopBot/refund/300` | ASK CUSTOMER (R7) | ASK CUSTOMER (R7) | **PASS** |
| **T7** | Cross-customer agent impersonation | `Ravi/ShopBot/view_order/0` | BLOCK (R1) | BLOCK (R1) | **PASS** |
| **T8** | Revoked agent read-only probe | `Asha/OldBot/view_order/0` | BLOCK (R2) | BLOCK (R2) | **PASS** |

*Verification Note (T8):* Confirmed that security revocation (R2) strictly supersedes read-only allowances (R4).

---

## 4. Trade-Off Analysis: Blanket Blocking vs. Controlled Gatekeeping

An outright ban on AI agents yields short-term security advantages at significant strategic expense:

- **Gains of Blanket Blocking:** Completely eliminates exposure to rogue bots, buggy third-party autonomous loops, API credential theft, and disputes over unauthorized payments. It preserves Amazon’s proprietary UI experience and retains customer traffic within its native ecosystem (such as Rufus AI).
- **Losses of Blanket Blocking:** Severely damages user retention among tech-forward shoppers who increasingly rely on personal agents for multi-store price comparisons and automated restocking. As demonstrated when Shopify integrated Meta Muse immediately after Amazon's block, rigid bans cause commercial defection, lost high-intent conversion data, and legal scrutiny regarding anti-competitive platform foreclosure.
- **The Gatekeeper Solution:** A calibrated gatekeeper strikes the optimal equilibrium. By enforcing **R1–R3** perimeter authentication, automated sub-limit actions (**R4–R6**), mandatory step-up human verification for anomalies/refunds (**R7**), and immutable audit logs (**R8**), Amazon safely embraces the autonomous commerce era while eliminating liability and customer risk.
