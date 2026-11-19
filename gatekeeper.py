"""Agent Gatekeeper - decision engine for Amazon (online store).
Decides ALLOW / ASK CUSTOMER / BLOCK for requests made by a customer's AI agent.
"""
import sqlite3, datetime, os

ENROLMENT_NO = "PGD202571828"   # <-- shown on the main screen
COMPANY = "Amazon (Amazon.in)"
LIMIT = 2000            # INR; money actions above this need the customer's confirmation
ACTIONS = {"view_order", "place_order", "return", "refund"}

ALLOW, ASK, BLOCK = "ALLOW", "ASK CUSTOMER", "BLOCK"

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(DB_DIR, "gatekeeper.db")

def now():
    return datetime.datetime.now().isoformat(sep=" ", timespec="seconds")

class Gatekeeper:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = DEFAULT_DB
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS agents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT, agent TEXT, registered_at TEXT, revoked_at TEXT);
        CREATE TABLE IF NOT EXISTS audit(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, customer TEXT, agent TEXT, action TEXT, amount REAL,
            decision TEXT, rule TEXT, reason TEXT);
        """)

    # ---- agent registry (the "Wells Fargo problem": record + prove revocation)
    def register(self, customer, agent):
        ts = now()
        self.db.execute("INSERT INTO agents(customer,agent,registered_at) VALUES(?,?,?)",
                        (customer, agent, ts))
        self._log(ts, customer, agent, "REGISTER", None, "EVENT", "-", "Agent registered by customer")
        return ts

    def revoke(self, customer, agent):
        ts = now()
        cur = self.db.execute(
            "UPDATE agents SET revoked_at=? WHERE customer=? AND agent=? AND revoked_at IS NULL",
            (ts, customer, agent))
        self._log(ts, customer, agent, "REVOKE", None, "EVENT", "-",
                  "Agent access revoked" if cur.rowcount else "Revoke requested but no active agent found")
        return ts if cur.rowcount else None

    def _status(self, customer, agent):
        """Latest registration for this customer+agent: None / 'active' / 'revoked'."""
        row = self.db.execute(
            "SELECT revoked_at FROM agents WHERE customer=? AND agent=? ORDER BY id DESC LIMIT 1",
            (customer, agent)).fetchone()
        if row is None: return None
        return "revoked" if row[0] else "active"

    # ---- the rules
    def decide(self, customer, agent, action, amount=0):
        status = self._status(customer, agent)
        if status is None:
            d = (BLOCK, "R1", "Unknown agent: not registered by this customer")
        elif status == "revoked":
            d = (BLOCK, "R2", "Agent access was revoked by the customer")
        elif (action not in ACTIONS or not customer or not agent
              or not isinstance(amount, (int, float)) or amount < 0):
            d = (BLOCK, "R3", "Invalid request (bad action, missing field or negative amount)")
        elif action == "view_order":
            d = (ALLOW, "R4", "Read-only action")
        elif action == "place_order":
            d = (ALLOW, "R5", f"Purchase within limit of {LIMIT}") if amount <= LIMIT else \
                (ASK, "R5", f"Purchase above limit of {LIMIT}: customer must confirm")
        elif action == "return":
            d = (ALLOW, "R6", f"Return within limit of {LIMIT}") if amount <= LIMIT else \
                (ASK, "R6", f"Return above limit of {LIMIT}: customer must confirm")
        else:  # refund
            d = (ASK, "R7", "Refunds always need the customer's confirmation")
        self._log(now(), customer, agent, action, amount, *d)   # R8: every decision is logged
        return {"decision": d[0], "rule": d[1], "reason": d[2]}

    def _log(self, ts, customer, agent, action, amount, decision, rule, reason):
        self.db.execute("INSERT INTO audit(ts,customer,agent,action,amount,decision,rule,reason) "
                        "VALUES(?,?,?,?,?,?,?,?)", (ts, customer, agent, action, amount, decision, rule, reason))
        self.db.commit()

    def audit_log(self, limit=50):
        return self.db.execute("SELECT ts,customer,agent,action,amount,decision,rule,reason "
                               "FROM audit ORDER BY id DESC LIMIT ?", (limit,)).fetchall()

    def agents(self):
        return self.db.execute("SELECT customer,agent,registered_at,revoked_at FROM agents ORDER BY id DESC").fetchall()
