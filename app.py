"""Simple web page for the Agent Gatekeeper.
Run: python app.py
Opens automatically on http://localhost:8000 (or 8001 if 8000 is busy).
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import html
import sys
from gatekeeper import Gatekeeper, ENROLMENT_NO, COMPANY, LIMIT

gk = Gatekeeper()
last = ""

def page():
    rows = "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in r) + "</tr>" for r in gk.audit_log())
    ags = "".join("<tr>" + "".join(f"<td>{html.escape(str(c or '-'))}</td>" for c in r) + "</tr>" for r in gk.agents())
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agent Gatekeeper - {html.escape(COMPANY)}</title>
<style>
 body{{font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;max-width:960px;margin:2rem auto;padding:0 1.5rem;color:#1e293b;background:#f8fafc}}
 h1{{margin:0 0 .25rem 0;color:#0f172a;font-size:26px}}
 .sub{{color:#475569;margin-bottom:1.5rem;padding-bottom:.75rem;border-bottom:1px solid #e2e8f0;font-size:15px}}
 form{{display:flex;flex-wrap:wrap;gap:.6rem;margin:.75rem 0 1.5rem;align-items:center}}
 input,select,button{{font:inherit;padding:.5rem .75rem;border:1px solid #cbd5e1;border-radius:6px;background:#fff}}
 button{{background:#0f172a;color:#fff;cursor:pointer;font-weight:600;border:none;transition:background .15s}}
 button:hover{{background:#334155}}
 .btn-revoke{{background:#dc2626}} .btn-revoke:hover{{background:#b91c1c}}
 .btn-quick{{background:#e2e8f0;color:#1e293b;font-size:13px;padding:.3rem .6rem;border:1px solid #cbd5e1}}
 .btn-quick:hover{{background:#cbd5e1}}
 table{{border-collapse:collapse;width:100%;font-size:13.5px;background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.06);margin-bottom:2rem}}
 td,th{{border:1px solid #e2e8f0;padding:.55rem .75rem;text-align:left}}
 th{{background:#f1f5f9;font-weight:600;color:#334155}}
 tr:nth-child(even){{background:#f8fafc}}
 .res{{padding:.9rem 1.25rem;border-left:5px solid #2563eb;background:#eff6ff;margin-bottom:1.75rem;border-radius:0 6px 6px 0;color:#1e40af;font-size:15px}}
 .quick-bar{{margin-bottom:1rem;display:flex;flex-wrap:wrap;gap:.4rem;align-items:center;background:#fff;padding:.75rem;border-radius:6px;border:1px solid #e2e8f0}}
</style>
</head>
<body>
<h1>Agent Gatekeeper</h1>
<div class="sub">Company: <b>{html.escape(COMPANY)}</b> &middot; Enrolment no: <b style="color:#2563eb">{html.escape(ENROLMENT_NO)}</b> &middot; Spending Limit: <b>INR {LIMIT}</b></div>

{f'<div class="res">{last}</div>' if last else ''}

<div class="quick-bar">
 <b>Quick Fill:</b>
 <button type="button" class="btn-quick" onclick="fill('Asha','ShopBot','view_order',0)">1. view_order (0)</button>
 <button type="button" class="btn-quick" onclick="fill('Asha','RogueBot','place_order',500)">2. Unknown RogueBot (500)</button>
 <button type="button" class="btn-quick" onclick="fill('Asha','ShopBot','place_order',3000)">3. Over limit (3000)</button>
 <button type="button" class="btn-quick" onclick="fill('Asha','ShopBot','place_order',1000)">4. Under limit (1000)</button>
 <button type="button" class="btn-quick" onclick="fill('Asha','ShopBot','refund',300)">5. Refund (300)</button>
</div>

<h3>Register or revoke an agent</h3>
<form method="post" action="/agent">
 <input id="reg_cust" name="customer" placeholder="Customer" value="Asha" required>
 <input id="reg_agent" name="agent" placeholder="Agent name" value="ShopBot" required>
 <button name="op" value="register">Register agent</button>
 <button name="op" value="revoke" class="btn-revoke">Revoke agent</button>
</form>

<h3>Send a request from an agent</h3>
<form method="post" action="/request">
 <input id="req_cust" name="customer" placeholder="Customer" value="Asha" required>
 <input id="req_agent" name="agent" placeholder="Agent name" value="ShopBot" required>
 <select id="req_act" name="action">
   <option value="view_order">view_order</option>
   <option value="place_order" selected>place_order</option>
   <option value="return">return</option>
   <option value="refund">refund</option>
 </select>
 <input id="req_amt" name="amount" type="number" step="any" value="1000" min="0">
 <button>Decide</button>
</form>

<h3>Registered agents</h3>
<table>
 <tr><th>Customer</th><th>Agent</th><th>Registered</th><th>Revoked</th></tr>
 {ags if ags else '<tr><td colspan=4 style="text-align:center;color:#94a3b8">No agents registered yet</td></tr>'}
</table>

<h3>Audit log (latest 50)</h3>
<table>
 <tr><th>Time</th><th>Customer</th><th>Agent</th><th>Action</th><th>Amount</th><th>Decision</th><th>Rule</th><th>Reason</th></tr>
 {rows if rows else '<tr><td colspan=8 style="text-align:center;color:#94a3b8">Audit log is empty</td></tr>'}
</table>

<script>
function fill(c, a, act, amt) {{
  document.getElementById('req_cust').value = c;
  document.getElementById('req_agent').value = a;
  document.getElementById('req_act').value = act;
  document.getElementById('req_amt').value = amt;
}}
</script>
</body>
</html>
"""

class H(BaseHTTPRequestHandler):
    def _send(self):
        b = page().encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        self._send()

    def do_POST(self):
        global last
        f = {k: v[0] for k, v in parse_qs(self.rfile.read(int(self.headers["Content-Length"])).decode()).items()}
        c, a = f.get("customer", "").strip(), f.get("agent", "").strip()
        if self.path == "/agent":
            if f.get("op") == "register":
                ts = gk.register(c, a)
                last = f"Registered <b>{html.escape(a)}</b> for customer <b>{html.escape(c)}</b> at {ts}"
            else:
                t = gk.revoke(c, a)
                last = f"Revoked <b>{html.escape(a)}</b> at {t}" if t else f"No active agent <b>{html.escape(a)}</b> found to revoke"
        else:
            try:
                amt = float(f.get("amount") or 0)
            except ValueError:
                amt = -1
            r = gk.decide(c, a, f.get("action"), amt)
            last = f"<b>{r['decision']}</b> (rule {r['rule']}): {html.escape(r['reason'])}"
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

def run_server():
    # If a specific port was requested via command line
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        server = HTTPServer(("0.0.0.0", port), H)
        print(f"Server started on http://localhost:{port}")
        server.serve_forever()
        return

    # Try port 8000 first, if busy try 8001, 8002...
    for port in (8000, 8001, 8002, 8003, 8080):
        try:
            server = HTTPServer(("0.0.0.0", port), H)
            print(f"Server started on http://localhost:{port}")
            server.serve_forever()
            return
        except OSError:
            continue
    print("Could not find an open port.")

if __name__ == "__main__":
    run_server()
