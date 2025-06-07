from flask import Flask, request, redirect
import csv

app = Flask(__name__)

@app.route("/")
def form():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/submit", methods=["POST"])
def submit():
    if not request.form.get("samtycke"):
        return "Du måste godkänna villkoren."

    data = {
        "fornamn": request.form["fornamn"],
        "efternamn": request.form["efternamn"],
        "email": request.form["email"],
        "fodelsedag": request.form["fodelsedag"]
    }

    with open("leads.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

    return "Tack! Dina uppgifter har sparats."

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
