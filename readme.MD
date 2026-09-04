```markdown
# GST API Suite

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Render](https://img.shields.io/badge/deploy-Render-purple.svg)](https://render.com)

A production‑ready Flask‑based REST API for GSTIN, PAN, and business‑name lookups, aggregating data from **Razorpay** and **MastersIndia** upstream sources.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Reference](#api-reference)
  - [1. GSTIN Information](#1-gstin-information)
  - [2. PAN to GSTINs](#2-pan-to-gstins)
  - [3. GSTIN to PAN](#3-gstin-to-pan)
  - [4. Business Name → Detailed GSTINs](#4-business-name--detailed-gstins)
  - [5. Business Name → Active/Cancelled GSTINs](#5-business-name--activecancelled-gstins)
  - [6. GSTIN Detail (Razorpay)](#6-gstin-detail-razorpay)
  - [7. Combined Multi‑Parameter Search](#7-combined-multiparameter-search)
  - [Health / Info Endpoint](#health--info-endpoint)
- [Error Handling](#error-handling)
- [Deployment](#deployment)
- [Environment Variables](#environment-variables)
- [Dependencies](#dependencies)
- [Data Sources & Disclaimer](#data-sources--disclaimer)
- [License](#license)

---

## Overview

The **GST API Suite** provides a unified interface to query Indian GST registration data. It wraps two external providers:

- **Razorpay** – for direct GSTIN and PAN lookups.
- **MastersIndia** – for name‑based searches with extensive registration details.

All responses include developer credit and an optional owner field for branding.

---

## Features

- **GSTIN Lookup** – retrieve full details for a given GSTIN.
- **PAN Lookup** – list all GSTINs registered under a PAN.
- **GSTIN → PAN Extraction** – derive the PAN from a GSTIN structurally.
- **Business Name Search** – fetch detailed GSTIN information by company name.
- **Status‑Filtered Results** – separate active and cancelled GSTINs.
- **Combined Search** – query by name, GSTIN, and PAN simultaneously.
- **JSON Responses** – consistent, lightweight, and machine‑friendly.
- **Render‑Ready** – deploy instantly on Render with zero configuration.

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- `pip` package manager

### Installation

```bash
git clone https://github.com/yourusername/gst-api-suite.git
cd gst-api-suite
pip install -r requirements.txt
```

Run Locally

```bash
python main.py
```

The server will start at http://localhost:5000.
Test it with:

```bash
curl http://localhost:5000/
```

---

Configuration

Before deploying, set the OWNER variable in main.py:

```python
OWNER = "Your Company Name"
```

Alternatively, use an environment variable:

```bash
export OWNER="Your Company Name"
```

If not set, the owner field in responses will display "NOT SET - edit OWNER at top of file".

---

API Reference

All endpoints return JSON. Each successful response includes:

· developer – always "rehuu - https://t.me/RehuSzr"
· owner – the value you configured.

Error responses follow the same structure with an "error" field.

---

1. GSTIN Information

Retrieve complete GSTIN details from Razorpay.

Endpoint
GET /gstin/<gstin>

Path Parameter

Name Type Description
gstin string 15‑character GSTIN

Example Request

```
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

Endpoint
GET /pan/<pan>

Path Parameter

Name Type Description
pan string 10‑character PAN

Example Request

```
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

Endpoint
GET /gst-to-pan/<gstin>

Path Parameter

Name Type Description
gstin string 15‑character GSTIN

Example Request

```
GET /gst-to-pan/10ABCDE1234F1Z5
```

Example Response – same as /pan/ response.

Note: This does not independently verify the PAN; it is a structural extraction.

---

4. Business Name → Detailed GSTINs

Search by business name using MastersIndia and return full registration details.

Endpoint
GET /name-to-gstin?name=<company>

Query Parameter

Name Type Description
name string Business or trade name (URL‑encoded)

Example Request

```
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

Search by business name and get a simplified list divided by status.

Endpoint
GET /search-gstin?name=<company>

Query Parameter

Name Type Description
name string Business or trade name

Example Request

```
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

Endpoint
GET /gstin-detail/<gstin>

Path Parameter

Name Type Description
gstin string 15‑character GSTIN

Example Request

```
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
Supply any combination of query parameters – unused parameters are ignored.

Endpoint
GET /all-search?name=<value>&gstin=<value>&pan=<value>

Query Parameters (all optional)

Name Type Description
name string Business name
gstin string GSTIN
pan string PAN

Example Request

```
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

Health / Info Endpoint

Returns API metadata, version, and available endpoints.

Endpoint
GET /

Example Request

```
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

All errors return an appropriate HTTP status code (4xx/5xx) with a JSON body:

```json
{
  "error": "Descriptive error message",
  "developer": "rehuu - https://t.me/RehuSzr",
  "owner": "DemoOwner"
}
```

Common error scenarios:

· Missing required query parameters (e.g., name in /search-gstin)
· Invalid GSTIN format (in /gst-to-pan)
· Upstream service timeouts or failures

---

Deployment

Render

1. Fork/clone this repository to GitHub.
2. Create a new Web Service on Render.
3. Connect your repository.
4. Use the following settings:
   · Build Command: pip install -r requirements.txt
   · Start Command: python main.py
5. Optionally add the environment variable OWNER with your desired value.
6. Deploy – the API will be available at https://your-app.onrender.com.

Manual Deployment

You can also deploy on any platform that supports Python web applications.
Set the PORT environment variable to match your platform’s expectations.

---

Environment Variables

Variable Description Default
PORT Port on which the server listens 5000
OWNER Custom owner name for response branding "NOT SET..." (fallback)

---

Dependencies

· Flask – web framework
· Requests – HTTP client

Install them via pip install flask requests or use the provided requirements.txt.

---

Data Sources & Disclaimer

This API acts as an aggregator for third‑party services:

· Razorpay – provides direct GSTIN and PAN endpoints.
· MastersIndia – provides business‑name search capabilities.

All data is sourced from these external providers. The availability, accuracy, and structure of the data are subject to the providers’ terms and changes. This project does not guarantee the correctness or completeness of the returned information. Use at your own risk.

---

License

This project is licensed under the MIT License. See the LICENSE file for details. However, note that usage of the underlying upstream services is subject to their respective terms and conditions.

---

Developer: rehuu
Contributions & Feedback: Welcome via Issues and Pull Requests.

```
