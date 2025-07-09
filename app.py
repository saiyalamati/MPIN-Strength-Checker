from flask import Flask, render_template, request

app = Flask(__name__)

def is_common_pin(pin):
    return pin in {
        "1234", "4321", "1111", "0000", "1212", "1122", "7777",
        "123456", "654321", "111111", "000000", "121212", "112233"
    }

def extract_substrings(date):
    return {
        date[:2], date[2:4], date[4:], date[:4], date[2:], date[-4:], date[-2:]
    }

def analyze_pin(pin, self_dob, spouse_dob, anniversary):
    reasons = []
    if is_common_pin(pin):
        reasons.append("COMMONLY_USED")
    
    def check(label, date):
        if date and date.isdigit() and len(date) == 8:
            if any(part in pin for part in extract_substrings(date)):
                reasons.append(label)

    check("DEMOGRAPHIC_DOB_SELF", self_dob)
    check("DEMOGRAPHIC_DOB_SPOUSE", spouse_dob)
    check("DEMOGRAPHIC_ANNIVERSARY", anniversary)

    status = "WEAK" if reasons else "STRONG"
    return status, reasons

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        pin = request.form.get("pin", "").strip()
        dob = request.form.get("dob", "").strip()
        spouse = request.form.get("spouse", "").strip()
        anniversary = request.form.get("anniversary", "").strip()

        if not pin.isdigit() or len(pin) not in {4, 6}:
            result = {"error": "Invalid PIN. Must be 4 or 6 digits."}
        else:
            strength, reasons = analyze_pin(pin, dob, spouse, anniversary)
            result = {
                "pin": pin,
                "status": strength,
                "reasons": reasons
            }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
