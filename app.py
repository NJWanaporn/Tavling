from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/google-creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("leads").sheet1  # ändra detta till ditt arknamn om det är något annat

@app.route("/")
def index():
    return """
    <form action="/submit" method="POST">
        <label>Namn:</label><br>
        <input type="text" name="namn" required><br><br>

        <label>Adress:</label><br>
        <input type="text" name="adress" required><br><br>

        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>

        <label>Födelsedag:</label><br>
        <input type="date" name="fodelsedag" required><br><br>

        <label>Telefon:</label><br>
        <input type="tel" name="telefon" required><br><br>

        <label>
            <input type="checkbox" name="samtycke" required> Jag godkänner villkoren
        </label><br><br>

        <button type="submit">Skicka</button>
    </form>
    """

@app.route("/submit", methods=["POST"])
def submit():
    if not request.form.get("samtycke"):
        return "Du måste godkänna villkoren."

    data = [
        request.form["namn"],
        request.form["adress"],
        request.form["email"],
        request.form["fodelsedag"],
        request.form["telefon"]
    ]

    sheet.append_row(data)
    return "Tack! Dina uppgifter har sparats."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
