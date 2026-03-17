# 🚀 Fragment Stars Flask API

A simple Flask API for purchasing Telegram Stars and Premium via Fragment.

---

## ⚙️ `.env` Setup

Fill in the `.env` file in the project root:

```
SEED=word1 word2 word3 ... word24
FRAGMENT_COOKIES=stel_ssid=xxx; stel_token=xxx; stel_dt=xxx; stel_ton_token=xxx
PORT=8080
```

---

## 🔑 Variable Explanation

### `SEED`
- 24 words from a TON wallet
- single line separated by spaces
- used for:
  - purchases without KYC
  - checking balance

📌 example:
```
SEED=apple river stone table green light ...
```

---

### `FRAGMENT_COOKIES`
- cookies from the Fragment website
- required for KYC methods

📌 format:
```
stel_ssid=xxx; stel_token=xxx; stel_dt=xxx; stel_ton_token=xxx
```

---

### `PORT`
- server port (default `8080`)

---

## ▶️ Run Server

```bash
python app.py
```

Server will be available at:
```
http://127.0.0.1:8080
```

---

## 📡 Endpoints

---

### 🟢 1. API Check

```http
GET /ping
```

---

### 💰 2. Check Balance

```http
GET /balance
```

❗ Requires `SEED`

---

### 👤 3. Get User Info

```http
GET /user/<username>
```

📌 example:
```
/user/unbrokensociety
```

❗ Requires `FRAGMENT_COOKIES`

---

### ⭐ 4. Buy Stars (No KYC)

```http
POST /buy_stars_nokyc
```

Request body:
```json
{
  "username": "@username",
  "amount": 100
}
```

---

### ⭐ 5. Buy Stars (With KYC)

```http
POST /buy_stars
```

❗ Requires `SEED + COOKIES`

---

### 💎 6. Buy Premium (No KYC)

```http
POST /buy_premium_nokyc
```

```json
{
  "username": "@username",
  "duration": 3
}
```

📌 `duration`: 3 / 6 / 12 months

---

### 💎 7. Buy Premium (With KYC)

```http
POST /buy_premium
```

---

## 🧪 Python Request Example

```python
import requests

response = requests.post(
    "http://127.0.0.1:8080/buy_stars_nokyc",
    json={
        "username": "@username",
        "amount": 100
    }
)

print(response.json())
```

---

## 📤 Response Format

### ✅ Success
```json
{
  "success": true,
  "description": "Buy Stars",
  "data": {}
}
```

---

### ❌ Error
```json
{
  "success": false,
  "error": "Error"
}
```

---

## ⚠️ Error Handling

The API already handles:

- ❌ Invalid JSON → `400`
- ❌ Missing required fields → `400`
- ❌ Invalid number format → `400`
- ❌ Missing `SEED` → `500`
- ❌ Missing `FRAGMENT_COOKIES` → `500`
- ❌ Fragment API errors → `success: false`
- ❌ Other errors → logged and returned

---

## 🔄 Method Differences

| Method | Requires | Description |
|------|--------|---------|
| `_nokyc` | SEED | Fast, no Fragment authorization |
| `kyc` | SEED + COOKIES | Full access via account |

---

## 📌 Note

This is an unofficial implementation of the Fragment API.  
Use at your own risk.
