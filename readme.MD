<!-- markdownlint-disable MD033 -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.0+-green?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/REST-API-brightgreen?style=for-the-badge&logo=fastapi&logoColor=white" alt="REST API">
  <img src="https://img.shields.io/badge/Deploy-Render-purple?style=for-the-badge&logo=render&logoColor=white" alt="Render">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
</p>

# GST API Suite

**A production‑grade microservice for real‑time GSTIN, PAN, and business‑name lookups**  
Aggregates data from **Razorpay** and **MastersIndia** to provide unified, fast, and reliable GST information.

---

## Overview

The **GST API Suite** is a lightweight, container‑ready Flask application that serves as a unified gateway for querying Indian GST registration data. It abstracts complexity by wrapping two reliable external APIs:

- **Razorpay** – for direct GSTIN and PAN lookups with detailed registration information.
- **MastersIndia** – for name‑based fuzzy searches returning extensive taxpayer details.

All responses are delivered in clean JSON, include developer credit, and allow you to brand the output with your own `owner` field—perfect for white‑label integrations.

---

## Key Features

- 🔍 **GSTIN Lookup** – retrieve full registration details for any valid GSTIN.
- 📋 **PAN Lookup** – list all GSTINs registered under a given PAN.
- 🔄 **GSTIN → PAN Extraction** – derive the PAN from a GSTIN structurally (no external verification).
- 🏢 **Business Name Search** – get detailed GSTIN data by company or trade name.
- ✅ **Status‑Filtered Results** – separate active and cancelled GSTINs in a single call.
- 🔗 **Combined Search** – query by name, GSTIN, and PAN simultaneously with one request.
- 📦 **Simple JSON Responses** – consistent, lightweight, and machine‑friendly.
- ⚡ **Optimised for Speed** – non‑blocking, with configurable timeouts.
- 🚀 **Render‑Ready** – deploy in minutes with zero configuration.
- 🧾 **Built‑in Developer Credit** – automatic attribution to `rehuu`.

---

## Technology Stack

| Layer          | Technology                         |
|----------------|------------------------------------|
| **Runtime**    | Python 3.9+                        |
| **Framework**  | Flask 2.0+                         |
| **HTTP Client**| Requests 2.28+                     |
| **Deployment** | Render, Docker, or any WSGI server |
| **Format**     | JSON                               |

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- `pip` (Python package manager)

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/gst-api-suite.git
cd gst-api-suite
pip install -r requirements.txt
```

Running Locally

Start the server with:

```bash
python main.py
```

The API will be available at http://localhost:5000.
Test it with:

```bash
curl http://localhost:5000/
```

---

Configuration

To personalise the owner field in all JSON responses, set the OWNER variable before running the app.

Option 1 – Hard‑code in main.py:

```python
OWNER = "Your Company Name"
```

Option 2 – Environment variable:

```bash
export OWNER="Your Company Name"
```

If not set, the default message "NOT SET - edit OWNER at top of file" will appear.

---

API Documentation

All endpoints return JSON.
Every successful response includes:

· developer – always "rehuu - https://t.me/RehuSzr"
· owner – the value you configured.

Errors are returned with appropriate HTTP status codes and an "error" field.

---

1. GSTIN Information

Retrieve complete GSTIN details from Razorpay.

Attribute Description
Endpoint GET /gstin/<gstin>
Path Parameter gstin – 15‑character GSTIN
Success Code 200 OK

Example Request

```http
GET /gstin/10ABCDE1234F1Z5
```

Example Response

```json
{
  "source": "razorpay",
  "gstin": "10ABCDE1234F1Z5",
  "data": {
    "gstin": "10ABCDE1234F1Z5",
    "legal_name": "ABC Electronics Private Limited",
    "trade_name": "ABC Electronics",
    "status": "Active",
    "taxpayer_type": "Regular",
    "constitution": "Private Limited Company",
    "registration_date": "01/07/2017",
    "state_jurisdiction": "Delhi West",
    "state_code": "10",
    "central_jurisdiction": "Delhi",
    "central_code": "1001",
    "einvoice_status": "Enabled",
    "nature_of_business": ["Manufacturing", "Trading"],
    "principal_address": {
      "address": "123, Industrial Area, Phase 1",
      "city": "New Delhi",
      "state": "Delhi",
      "pincode": "110001"
    },
    "additional_addresses": [
      {
        "address": "456, Warehouse Zone",
        "city": "Gurugram",
        "state": "Haryana",
        "pincode": "122001"
      }
    ],
    "last_updated": "2025-03-15 10:30:00",
    "cancelled_date": null
  },
  "developer": "rehuu - https://t.me/RehuSzr",
  "owner": "DemoOwner"
}
```

---

2. PAN to GSTINs

List all GST registrations associated with a PAN (from Razorpay).

Attribute Description
Endpoint GET /pan/<pan>
Path Parameter pan – 10‑character PAN
Success Code 200 OK

Example Request

```http
GET /pan/ABCDE1234F
```

Example Response

```json
{
  "source": "razorpay",
  "pan": "ABCDE1234F",
  "total_gstins": 2,
  "gstins": [
    {
      "gstin": "10ABCDE1234F1Z5",
      "legal_name": "ABC Electronics Private Limited",
      "status": "Active"
    },
    {
      "gstin": "22ABCDE1234F2Z6",
      "legal_name": "ABC Trading Company",
      "status": "Cancelled"
    }
  ],
  "data": {
    "count": 2,
    "items": [ ... ]
  },
  "developer": "rehuu - https://t.me/RehuSzr",
  "owner": "DemoOwner"
}
```

---

3. GSTIN to PAN

Extract the PAN from a GSTIN (characters 3–12) and perform a PAN lookup.

Attribute Description
Endpoint GET /gst-to-pan/<gstin>
Path Parameter gstin – 15‑character GSTIN
Success Code 200 OK

Example Request

```http
GET /gst-to-pan/10ABCDE1234F1Z5
```

Response – same as /pan/ (above).

⚠️ Note: This does not independently verify the PAN; it is a structural extraction only.

---

4. Business Name → Detailed GSTINs

Search by business name using MastersIndia and return full registration details.

Attribute Description
Endpoint GET /name-to-gstin?name=<company>
Query Parameter name – business or trade name (URL‑encoded)
Success Code 200 OK

Example Request

```http
GET /name-to-gstin?name=ABC%20Electronics
```

Example Response

```json
{
  "source": "mastersindia",
  "query": "ABC Electronics",
  "total_gstins": 1,
  "gstins": [
    {
      "gstin": "10ABCDE1234F1Z5",
      "legal_name": "ABC Electronics Private Limited",
      "trade_name": "ABC Electronics",
      "status": "Active",
      "taxpayer_type": "Regular",
      "constitution": "Private Limited Company",
      "registration_date": "01/07/2017",
      "state_jurisdiction": "Delhi West",
      "state_code": "10",
      "central_jurisdiction": "Delhi",
      "central_code": "1001",
      "einvoice_status": "Enabled",
      "nature_of_business": ["Manufacturing", "Trading"],
      "principal_address": { ... },
      "additional_addresses": [ ... ],
      "last_updated": "2025-03-15 10:30:00",
      "cancelled_date": null
    }
  ],
  "developer": "rehuu - https://t.me/RehuSzr",
  "owner": "DemoOwner"
}
```

---

5. Business Name → Active/Cancelled GSTINs

Search by business name and get a simplified list grouped by registration status.

Attribute Description
Endpoint GET /search-gstin?name=<company>
Query Parameter name – business or trade name
Success Code 200 OK

Example Request

```http
GET /search-gstin?name=ABC%20Electronics
```

Example Response

```json
{
  "source": "mastersindia",
  "query": "ABC Electronics",
  "total": 3,
  "active_gstins": [
    {
      "gstin": "10ABCDE1234F1Z5",
      "legal_name": "ABC Electronics Private Limited",
      "trade_name": "ABC Electronics",
      "state_code": "10",
      "status": "Active"
    },
    {
      "gstin": "12XYZ1234F1Z5",
      "legal_name": "ABC Solutions LLP",
      "trade_name": "ABC Solutions",
      "state_code": "12",
      "status": "Active"
    }
  ],
  "cancelled_gstins": [
    {
      "gstin": "22ABCDE1234F2Z6",
      "legal_name": "ABC Trading Company",
      "trade_name": "ABC Trading",
      "state_code": "22",
      "status": "Cancelled"
    }
  ],
  "developer": "rehuu - https://t.me/RehuSzr",
  "owner": "DemoOwner"
}
```

---

6. GSTIN Detail (Razorpay)

Fetches GSTIN details via Razorpay and includes a note about MastersIndia limitations.

Attribute Description
Endpoint GET /gstin-detail/<gstin>
Path Parameter gstin – 15‑character GSTIN
Success Code 200 OK

Example Request

```http
GET /gstin-detail/10ABCDE1234F1Z5
```

Example Response

```json
{
  "gstin": "10ABCDE1234F1Z5",
  "razorpay_info": {
    "gstin": "10ABCDE1234F1Z5",
    "legal_name": "ABC Electronics Private Limited",
    ...
  },
  "note": "MastersIndia supports name search only, use /name-to-gstin for company name",
  "developer": "rehuu - https://t.me/RehuSzr",
  "owner": "DemoOwner"
}
```

---

7. Combined Multi‑Parameter Search

Perform all three lookups (name, GSTIN, PAN) in a single call.
Unused parameters are ignored.

Attribute Description
Endpoint GET /all-search?name=<value>&gstin=<value>&pan=<value>
Query Parameters name, gstin, pan (all optional)
Success Code 200 OK

Example Request

```http
GET /all-search?name=ABC%20Electronics&pan=ABCDE1234F&gstin=10ABCDE1234F1Z5
```

Example Response

```json
{
  "query_params": {
    "name": "ABC Electronics",
    "gstin": "10ABCDE1234F1Z5",
    "pan": "ABCDE1234F"
  },
  "results": {
    "gstin_info_razorpay": { ... },
    "pan_search_razorpay": { ... },
    "name_search_mastersindia": { ... }
  },
  "developer": "rehuu - https://t.me/RehuSzr",
  "owner": "DemoOwner"
}
```

---

Root / Health Endpoint

Returns API metadata, version, and available endpoints.

Attribute Description
Endpoint GET /
Success Code 200 OK

Example Request

```http
GET /
```

Example Response

```json
{
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
  },
  "developer": "rehuu - https://t.me/RehuSzr",
  "owner": "DemoOwner"
}
```

---

Error Handling

All errors return an appropriate HTTP status code (4xx or 5xx) with a consistent JSON structure:

```json
{
  "error": "Human‑readable error message",
  "developer": "rehuu - https://t.me/RehuSzr",
  "owner": "DemoOwner"
}
```

Status Code Common Cause
400 Missing required parameter or invalid format
404 Resource not found (e.g., invalid GSTIN)
500 Upstream service failure or timeout

---

Deployment

Render (Recommended)

1. Push the repository to GitHub.
2. Create a new Web Service on Render.
3. Connect your GitHub repo.
4. Use the following settings:
   · Build Command: pip install -r requirements.txt
   · Start Command: python main.py
5. Add an optional environment variable OWNER for branding.
6. Click Deploy – your API will be live at https://your-app.onrender.com.

Manual / Other Platforms

· Set the PORT environment variable to match your platform’s expectation.
· Run python main.py or use a WSGI server like Gunicorn.

---

Environment Variables

Variable Description Default
PORT Port on which the server listens 5000
OWNER Custom owner name for response branding "NOT SET..." (fallback)

---

Dependencies

· Flask – lightweight WSGI web framework.
· Requests – elegant HTTP client.

Install all with:

```bash
pip install -r requirements.txt
```

---

Upstream Data Sources

This API acts as an aggregator; it does not host any GST data itself.
All information is fetched in real‑time from:

· Razorpay – GSTIN and PAN endpoints.
· MastersIndia – name‑based search API.

Please note:

· Data accuracy, completeness, and uptime depend entirely on these third‑party services.
· The API providers may change their endpoints, response schemas, or rate limits at any time.
· This project does not guarantee the reliability of the upstream services.

---

Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for:

· Bug fixes
· New data sources
· Performance improvements
· Documentation enhancements

Please ensure your code follows PEP 8 and includes appropriate comments.

---

Support & Feedback

· Developer: rehuu (Telegram)
· For general queries, open a GitHub issue.
· For feature requests or custom deployments, reach out directly.

---

License

This project is licensed under the MIT License – see the LICENSE file for details.
However, usage of the underlying upstream APIs is subject to their respective terms and conditions.

```
