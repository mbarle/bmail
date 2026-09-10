import os
from datetime import datetime, timezone

from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(
    __name__,
    static_folder="assets",
    static_url_path="/assets"
)

app.secret_key = os.environ.get("SECRET_KEY", "development-secret-key")


# Temporary in-memory storage.
# Messages disappear whenever the application restarts.
sporocila = []


@app.route("/")
def home():
    email = session.get("email")

    if email:
        user = {
            "email": email,
            "nickname": email.split("@")[0]
        }

        return render_template(
            "hello.html",
            logiran=True,
            user=user
        )

    return render_template(
        "hello.html",
        logiran=False
    )


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")

    if email:
        session["email"] = email

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/vnos", methods=["POST"])
def vnos():
    sender = session.get("email")

    if not sender:
        return redirect(url_for("home"))

    recipient = request.form.get("Naslovnik")
    message = request.form.get("Message")

    sporocila.append({
        "Posiljatelj": sender,
        "Naslovnik": recipient,
        "Message": message,
        "nastanek": datetime.now(timezone.utc)
    })

    return redirect(url_for("poslano"))


@app.route("/poslano")
def poslano():
    email = session.get("email")

    if not email:
        return redirect(url_for("home"))

    seznam_poslano = [
        sporocilo
        for sporocilo in sporocila
        if sporocilo["Posiljatelj"] == email
    ]

    return render_template(
        "Poslano.html",
        seznam_poslano=seznam_poslano
    )


@app.route("/prejeto")
def prejeto():
    email = session.get("email")

    if not email:
        return redirect(url_for("home"))

    seznam_prejeto = [
        sporocilo
        for sporocilo in sporocila
        if sporocilo["Naslovnik"] == email
    ]

    return render_template(
        "Prejeto.html",
        seznam_prejeto=seznam_prejeto
    )


if __name__ == "__main__":
    app.run(debug=True)