"""
Uruchomienie:  pip install flask  ->  python zadania.py  ->  http://127.0.0.1:5000
Konta:  alice / alice123 (id=1),  bob / bob123 (id=2),  admin / admin123 (id=3)
Po zepsuciu danych wystarczy zrestartować serwer (dane są tylko w pamięci).
"""
from flask import Flask, request, session, redirect, make_response, render_template_string, abort

app = Flask(__name__)
app.secret_key = "warsztat-secret"

USERS = {
    1: {"login": "alice", "password": "alice123", "role": "user"},
    2: {"login": "bob",   "password": "bob123",   "role": "user"},
    3: {"login": "admin", "password": "admin123", "role": "admin"},
}
INVOICES = {
    101: {"owner_id": 1, "title": "Faktura 101 (Alice)", "amount": "1 200 PLN"},
    102: {"owner_id": 1, "title": "Faktura 102 (Alice)", "amount": "350 PLN"},
    201: {"owner_id": 2, "title": "Faktura 201 (Bob, POUFNE)", "amount": "98 000 PLN"},
    202: {"owner_id": 2, "title": "Faktura 202 (Bob, POUFNE)", "amount": "4 500 PLN"},
}

PAGE = """
<!doctype html><title>Warsztat BAC</title>
<body style="font-family:sans-serif;max-width:640px;margin:2em auto">
<h2>Warsztat BAC</h2>
{% if user %}
  <p>Zalogowany: <b>{{ user.login }}</b> (id={{ uid }}) | <a href="/logout">wyloguj</a></p>
  <h3>Twoje faktury</h3>
  <ul>{% for i, inv in invoices %}<li><a href="/invoice/{{ i }}">{{ inv.title }}</a></li>{% endfor %}</ul>
  {% if user.role == 'admin' %}<p><a href="/admin">Panel administratora</a></p>{% endif %}
{% else %}
  <form method="post" action="/login">
    <input name="login" placeholder="login"> <input name="password" type="password" placeholder="hasło">
    <button>Zaloguj</button></form>
{% endif %}
</body>
"""

def current_user():
    uid = session.get("uid")
    return uid, USERS.get(uid)

@app.route("/")
def index():
    uid, user = current_user()
    mine = [(i, v) for i, v in INVOICES.items() if v["owner_id"] == uid] if user else []
    return render_template_string(PAGE, user=user, uid=uid, invoices=mine)

@app.route("/login", methods=["POST"])
def login():
    for uid, u in USERS.items():
        if u["login"] == request.form["login"] and u["password"] == request.form["password"]:
            session["uid"] = uid
            resp = make_response(redirect("/"))
            resp.set_cookie("is_admin", "true" if u["role"] == "admin" else "false")
            return resp
    return "Błędne dane", 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ======================= ZADANIE 1: faktury (funkcja invoice) =======================
@app.route("/invoice/<int:invoice_id>")
def invoice(invoice_id):
    uid, user = current_user()
    if not user:
        return redirect("/")
    inv = INVOICES.get(invoice_id)
    if not inv:
        abort(404)
    return f"<h3>{inv['title']}</h3><p>Kwota: {inv['amount']}</p><a href='/'>wróć</a>"

# ======================= ZADANIE 2: panel admina (admin_panel, admin_delete_invoice) =======================
@app.route("/admin")
def admin_panel():
    uid, user = current_user()
    if not user:
        return redirect("/")
    users = "".join(f"<li>{i}: {u['login']} ({u['role']})</li>" for i, u in USERS.items())
    invs = "".join(f"<li>{i}: {v['title']} <a href='/admin/delete-invoice/{i}'>usuń</a></li>"
                   for i, v in INVOICES.items())
    return (f"<h2>Panel administratora</h2><h3>Użytkownicy</h3><ul>{users}</ul>"
            f"<h3>Wszystkie faktury</h3><ul>{invs}</ul>")

@app.route("/admin/delete-invoice/<int:invoice_id>")
def admin_delete_invoice(invoice_id):
    uid, user = current_user()
    if not user:
        return redirect("/")
    if invoice_id not in INVOICES:
        abort(404)
    del INVOICES[invoice_id]
    return f"Faktura {invoice_id} usunięta. <a href='/'>wróć</a>"

# ======================= ZADANIE 3: reset hasła (funkcja reset_password) =======================
@app.route("/manage/reset-password/<int:target_id>")
def reset_password(target_id):
    uid, user = current_user()
    if not user:
        return redirect("/")
    if request.cookies.get("is_admin") != "true":
        return "Brak uprawnień", 403
    if target_id not in USERS:
        abort(404)
    USERS[target_id]["password"] = "reset123"
    return f"Hasło użytkownika {USERS[target_id]['login']} zresetowane do 'reset123'."

if __name__ == "__main__":
    app.run(debug=True)
