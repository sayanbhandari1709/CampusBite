from flask import Flask, render_template, request, redirect
import smtplib
from email.message import EmailMessage
import urllib.parse

app = Flask(__name__)

# ---------------- STORAGE ----------------

orders = []
today_menu = ["Veg Thali", "Paneer Roll", "Biryani"]

# ---------------- EMAIL CONFIG ----------------

SENDER_EMAIL = "sayanbhandari1709@gmail.com"
SENDER_PASSWORD = "lyqo feuk vfbm hkrx"

# ---------------- SEND EMAIL ----------------

def send_menu_email(faculty_email):
    encoded_email = urllib.parse.quote(faculty_email)
    menu_link = f"http://127.0.0.1:5000/menu/{encoded_email}"

    msg = EmailMessage()
    msg["Subject"] = "CampusBite – Today's Menu"
    msg["From"] = SENDER_EMAIL
    msg["To"] = faculty_email

    msg.set_content(f"""
Hello Faculty,

Today's menu is ready.

Click the link below to view the menu and confirm if you want to eat today:

{menu_link}

CampusBite
""")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

# ---------------- FACULTY LOGIN ----------------

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        faculty_email = request.form.get("email")
        send_menu_email(faculty_email)
        return "Email sent successfully! Please check your inbox."
    return render_template("login.html")

# ---------------- MENU PAGE ----------------

@app.route("/menu/<path:faculty_email>")
def menu(faculty_email):
    faculty_email = urllib.parse.unquote(faculty_email)
    return render_template(
        "menu.html",
        email=faculty_email,
        menu=today_menu
    )

# ---------------- CONFIRM ORDER ----------------

@app.route("/confirm", methods=["POST"])
def confirm():
    faculty_email = request.form.get("email")
    decision = request.form.get("decision")
    if decision == "yes":
        orders.append({
            "email": faculty_email,
            "status": "Pending"
        })
        return "Booking confirmed!"
    return "Maybe next time"

# ---------------- VENDOR DASHBOARD ----------------

@app.route("/vendor")
def vendor():
    return render_template(
        "vendor.html",
        orders=orders
    )

# ---------------- VENDOR MENU EDITOR ----------------

@app.route("/vendor-menu", methods=["GET","POST"])
def vendor_menu():
    global today_menu
    if request.method == "POST":
        item1 = request.form.get("item1")
        item2 = request.form.get("item2")
        item3 = request.form.get("item3")
        today_menu = [item1, item2, item3]
        return redirect("/vendor-menu")
    return render_template(
        "vendor_menu.html",
        menu=today_menu
    )

# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)