import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5",
}

MASTERS_HEADERS = {
    **HEADERS,
    "Origin": "https://www.mastersindia.co",
    "Referer": "https://www.mastersindia.co/gst-number-search-by-name-and-pan/",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
}

DEVELOPER_CREDIT = "rehuu - https://t.me/RehuSzr"

def add_credit(d):
    d["developer"] = DEVELOPER_CREDIT
    d["owner"] = OWNER if OWNER else "NOT SET - edit OWNER at top of file"
    return d

# ================================================================
# API 1: GSTIN Info (Razorpay)
# ================================================================
@app.route("/gstin/<gstin>", methods=["GET"])
def gstin_info(gstin):
    try:
        r = requests.get(f"https://razorpay.com/api/gstin/{gstin}", headers=HEADERS, timeout=15)
        return jsonify(add_credit({"source": "razorpay", "gstin": gstin, "data": r.json()}))
    except Exception as e:
        return jsonify(add_credit({"error": str(e)})), 500

# ================================================================
# API 2: PAN to All GSTINs (Razorpay) — GST to PAN bhi yahi hai
# ================================================================
@app.route("/pan/<pan>", methods=["GET"])
def pan_to_gst(pan):
    try:
        r = requests.get(f"https://razorpay.com/api/gstin/pan/{pan}", headers=HEADERS, timeout=15)
        data = r.json()
        return jsonify(add_credit({
            "source": "razorpay",
            "pan": pan,
            "total_gstins": data.get("count", 0),
            "gstins": data.get("items", []),
            "data": data
        }))
    except Exception as e:
        return jsonify(add_credit({"error": str(e)})), 500

@app.route("/gst-to-pan/<gstin>", methods=["GET"])
def gst_to_pan(gstin):
    """GSTIN se PAN extract karo (first 10 chars before last 5)"""
    if len(gstin) == 15:
        pan = gstin[2:12]
        return pan_to_gst(pan)
    return jsonify(add_credit({"error": "Invalid GSTIN format"})), 400

# ================================================================
# API 3: Name to Detailed GSTINs (MastersIndia)
# ================================================================
@app.route("/name-to-gstin", methods=["GET"])
def name_to_gstin():
    name = request.args.get("name", "")
    if not name:
        return jsonify(add_credit({"error": "name parameter required", "usage": "/name-to-gstin?name=Amazon"})), 400

    try:
        keyword = name.strip()
        keyword = keyword.replace(" ", "+")
        if not keyword.endswith("+"):
            keyword += "+"

        r = requests.get(
            f"https://blog-backend.mastersindia.co/api/v1/custom/search/name_and_pan/?keyword={keyword}",
            headers=MASTERS_HEADERS,
            timeout=20
        )
        data = r.json()

        gstins = []
        if data.get("success") and data.get("data"):
            for item in data["data"]:
                gstins.append({
                    "gstin": item.get("gstin", ""),
                    "legal_name": item.get("lgnm", ""),
                    "trade_name": item.get("tradeNam", ""),
                    "status": item.get("sts", ""),
                    "taxpayer_type": item.get("dty", ""),
                    "constitution": item.get("ctb", ""),
                    "registration_date": item.get("rgdt", ""),
                    "state_jurisdiction": item.get("stj", ""),
                    "state_code": item.get("stjCd", ""),
                    "central_jurisdiction": item.get("ctj", ""),
                    "central_code": item.get("ctjCd", ""),
                    "einvoice_status": item.get("einvoiceStatus", ""),
                    "nature_of_business": item.get("nba", []),
                    "principal_address": item.get("pradr", {}),
                    "additional_addresses": item.get("adadr", []),
                    "last_updated": item.get("lstupdt", ""),
                    "cancelled_date": item.get("cxdt", ""),
                })

        return jsonify(add_credit({
            "source": "mastersindia",
            "query": name,
            "total_gstins": len(gstins),
            "gstins": gstins
        }))
    except Exception as e:
        return jsonify(add_credit({"error": str(e)})), 500

# ================================================================
# API 4: Name to GSTIN List (MastersIndia) — Sorted by Status
# ================================================================
@app.route("/search-gstin", methods=["GET"])
def search_gstin():
    name = request.args.get("name", "")
    if not name:
        return jsonify(add_credit({"error": "name parameter required"})), 400

    try:
        keyword = name.strip().replace(" ", "+") + "+"
        r = requests.get(
            f"https://blog-backend.mastersindia.co/api/v1/custom/search/name_and_pan/?keyword={keyword}",
            headers=MASTERS_HEADERS,
            timeout=20
        )
        data = r.json()

        active = []
        cancelled = []
        if data.get("success") and data.get("data"):
            for item in data["data"]:
                entry = {
                    "gstin": item.get("gstin", ""),
                    "legal_name": item.get("lgnm", ""),
                    "trade_name": item.get("tradeNam", ""),
                    "state_code": item.get("stjCd", ""),
                    "status": item.get("sts", ""),
                }
                if item.get("sts") == "Active":
                    active.append(entry)
                else:
                    cancelled.append(entry)

        return jsonify(add_credit({
            "source": "mastersindia",
            "query": name,
            "total": len(active) + len(cancelled),
            "active_gstins": active,
            "cancelled_gstins": cancelled
        }))
    except Exception as e:
        return jsonify(add_credit({"error": str(e)})), 500

# ================================================================
# API 5: GSTIN Info (MasterIndia via search workaround)
# ================================================================
@app.route("/gstin-detail/<gstin>", methods=["GET"])
def gstin_detail_masters(gstin):
    try:
        r1 = requests.get(f"https://razorpay.com/api/gstin/{gstin}", headers=HEADERS, timeout=10)
        razorpay_data = r1.json()
        masters_data = {"detail": "MastersIndia supports name search only, use /name-to-gstin for company name"}

        return jsonify(add_credit({
            "gstin": gstin,
            "razorpay_info": razorpay_data,
            "note": masters_data["detail"]
        }))
    except Exception as e:
        return jsonify(add_credit({"error": str(e)})), 500

# ================================================================
# API 6: Combined Multi-Source Search
# ================================================================
@app.route("/all-search", methods=["GET"])
def all_search():
    name = request.args.get("name", "")
    gstin = request.args.get("gstin", "")
    pan = request.args.get("pan", "")

    results = {}

    if gstin:
        try:
            r = requests.get(f"https://razorpay.com/api/gstin/{gstin}", headers=HEADERS, timeout=10)
            results["gstin_info_razorpay"] = r.json()
        except:
            results["gstin_info_razorpay"] = "error"

    if pan:
        try:
            r = requests.get(f"https://razorpay.com/api/gstin/pan/{pan}", headers=HEADERS, timeout=10)
            results["pan_search_razorpay"] = r.json()
        except:
            results["pan_search_razorpay"] = "error"

    if name:
        try:
            keyword = name.strip().replace(" ", "+") + "+"
            r = requests.get(
                f"https://blog-backend.mastersindia.co/api/v1/custom/search/name_and_pan/?keyword={keyword}",
                headers=MASTERS_HEADERS, timeout=10
            )
            results["name_search_mastersindia"] = r.json()
        except:
            results["name_search_mastersindia"] = "error"

    return jsonify(add_credit({
        "query_params": {"name": name, "gstin": gstin, "pan": pan},
        "results": results
    }))

# ================================================================
# API 7: Health / All Endpoints
# ================================================================
@app.route("/", methods=["GET"])
def home():
    return jsonify(add_credit({
        "app": "GST API Suite",
        "version": "3.0",
        "endpoints": {
            "1. GET /gstin/<gstin>": "GSTIN Info (Razorpay source)",
            "2. GET /pan/<pan>": "PAN -> All GSTINs (Razorpay source)",
            "3. GET /gst-to-pan/<gstin>": "GSTIN -> PAN (extract from GSTIN)",
            "4. GET /name-to-gstin?name=<company>": "Name -> Detailed GSTINs (MastersIndia)",
            "5. GET /search-gstin?name=<company>": "Name -> Active/Cancelled GSTIN List (MastersIndia)",
            "6. GET /gstin-detail/<gstin>": "GSTIN Detail via Razorpay",
            "7. GET /all-search": "Combined Multi-Source Search"
        },
        "example_calls": {
            "local": "http://localhost:5000/name-to-gstin?name=Amazon",
            "render": "https://your-app.onrender.com/name-to-gstin?name=Flipkart"
        }
    }))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
