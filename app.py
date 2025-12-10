from flask import Flask, request, send_file, redirect
from datetime import datetime, timezone
import json
import os

app = Flask(__name__)

REDIRECT_MAP = {
    "lol-security-alert": "https://hcancaglar.github.io/phishing-lab/rito.html",
}


def classify(userAgent: str) -> str:
    uaLower = (userAgent or "").lower()

    botKeywords = [
        "googleimageproxy",            
        "microsoft defender smartscreen",
        "proofpoint url defense",
        "cisco ironport",
        "barracuda",
    ]

    if any(bot in uaLower for bot in botKeywords):
        return "AutoBot"
    else:
        return "HumanUser"


def log(eventType, campaign, classification, ip, userAgent, path):
    entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "ip": ip,
        "userAgent": userAgent,
        "event": eventType,          
        "campaign": campaign,       
        "classification": classification,  
        "url": path,
    }

    with open("events.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(entry)


@app.route("/pixel/<campaign>.gif")
def pixel(campaign):
    
    userAgent = request.headers.get("User-Agent", "")
    ip = request.remote_addr
    classification = classify(userAgent)
    log("open", campaign, classification, ip, userAgent, request.path)

   
    return send_file("pixel.gif", mimetype="image/gif")


@app.route("/click/<campaign>")
def click(campaign):
    
    userAgent = request.headers.get("User-Agent", "")
    ip = request.remote_addr
    classification = classify(userAgent)
    log("click", campaign, classification, ip, userAgent, request.path)

    target = REDIRECT_MAP.get(
        campaign,
        "https://hcancaglar.github.io/phishing-lab/",  # fallback
    )
    return redirect(target, code=302)


@app.route("/")
def home():
    return "Pixel Tracker is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
