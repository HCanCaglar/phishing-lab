from flask import Flask, request, send_file, redirect
from datetime import datetime, timezone
import json

app = Flask(__name__)

def classify(userAgent: str) -> str:
    uaLower = (userAgent or "").lower()

    botKeywords = [
        "googleimageproxy",             # Gmail image proxy
        "microsoft defender smartscreen",
        "proofpoint url defense",
        "cisco ironport",
        "barracuda",
    ]

    if any(bot in uaLower for bot in botKeywords):
        return "AutoBot"
    else:
        return "HumanUser"

def log(eventType, classification, ip, userAgent, path):
    log = {
        "time": datetime.now(timezone.utc).isoformat(),
        "ip": ip,
        "userAgent": userAgent,
        "event": eventType,      
        "classification": classification,  
        "url": path,

    }
    with open("events.log", "a") as f:
        f.write(json.dumps(log) + "\n")
    print(log)

@app.route("/logo.png")
def track():
    userAgent = request.headers.get("User-Agent", "")
    ip = request.remote_addr
    classification = classify(userAgent)
    log("open", classification, ip, userAgent, "/logo.png")
    return send_file("pixel.gif", mimetype="image/gif")

@app.route("/click")
def click():
    userAgent = request.headers.get("User-Agent", "")
    ip = request.remote_addr
    classification = classify(userAgent)
    log("click", classification, ip, userAgent, "/click")
    return redirect("https://hcancaglar.github.io/phishing-lab/rito.html", code=302)

@app.route("/")
def home():
    return "Pixel Tracker is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
