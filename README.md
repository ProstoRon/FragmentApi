# 🚀 Fragment Stars Flask API

Простой Flask API для покупки Telegram Stars и Premium через Fragment.

---

## ⚙️ Настройка `.env`

Создай файл `.env` в корне проекта:

```
SEED=word1 word2 word3 ... word24
FRAGMENT_COOKIES=stel_ssid=xxx; stel_token=xxx; stel_dt=xxx; stel_ton_token=xxx
PORT=8080
```

---

## 🔑 Пояснение переменных

### `SEED`
- 24 слова от TON-кошелька
- строка через пробел (одна строка)
- используется для:
  - покупки без KYC
  - получения баланса

📌 пример:
```
SEED=apple river stone table green light ...
```

---

### `FRAGMENT_COOKIES`
- cookies с сайта Fragment
- нужны для методов с KYC

📌 формат:
```
stel_ssid=xxx; stel_token=xxx; stel_dt=xxx; stel_ton_token=xxx
```

---

### `PORT`
- порт сервера (по умолчанию `8080`)

---

## ▶️ Запуск сервера

```bash
python app.py
```

Сервер будет доступен по адресу:  
```
http://127.0.0.1:8080
```

---

## 📡 Эндпоинты

---

### 🟢 1. Проверка API

```http
GET /ping
```

---

### 💰 2. Проверка баланса

```http
GET /balance
```

❗ Требует `SEED`

---

### 👤 3. Получение информации о пользователе

```http
GET /user/<username>
```

📌 пример:
```
/user/kifazi
```

❗ Требует `FRAGMENT_COOKIES`

---

### ⭐ 4. Покупка Stars (без KYC)

```http
POST /buy_stars_nokyc
```

**Тело запроса:**
```json
{
  "username": "@username",
  "amount": 100
}
```

---

### ⭐ 5. Покупка Stars (с KYC)

```http
POST /buy_stars
```

❗ Требует `SEED + COOKIES`

---

### 💎 6. Покупка Premium (без KYC)

```http
POST /buy_premium_nokyc
```

```json
{
  "username": "@username",
  "duration": 3
}
```

📌 `duration`: 3 / 6 / 12 месяцев

---

### 💎 7. Покупка Premium (с KYC)

```http
POST /buy_premium
```

---

## 🧪 Пример запроса на Python

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

## 📤 Формат ответа

### ✅ Успех
```json
{
  "success": true,
  "description": "Buy Stars",
  "data": {}
}
```

---

### ❌ Ошибка
```json
{
  "success": false,
  "error": "Ошибка"
}
```

---

## ⚠️ Обработка ошибок

API уже обрабатывает:

- ❌ Неверный JSON → `400`
- ❌ Нет обязательных полей → `400`
- ❌ Неверный формат числа → `400`
- ❌ Нет `SEED` → `500`
- ❌ Нет `FRAGMENT_COOKIES` → `500`
- ❌ Ошибки Fragment API → `success: false`
- ❌ Любые другие ошибки → логируются и возвращаются

---

## 🔐 Безопасность

❗ **Никогда не публикуй:**
- `SEED`
- `FRAGMENT_COOKIES`

❗ Рекомендуется:
- использовать отдельный кошелёк
- не хранить `.env` в GitHub (`.gitignore`)

---

## 🔄 Отличие методов

| Метод | Требует | Описание |
|------|--------|---------|
| `_nokyc` | SEED | Быстро, без авторизации Fragment |
| обычные | SEED + COOKIES | Полный доступ через аккаунт |

---

## 🧠 Полезно знать

- `SEED` = доступ к TON кошельку  
- `COOKIES` = доступ к Fragment аккаунту  

👉 Вместе дают полный контроль над средствами

---

## 📌 Примечание

Это неофициальная реализация API Fragment.  
Используй на свой риск.
