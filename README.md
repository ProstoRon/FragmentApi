# Fragment Stars Flask API

Простой Flask API для покупки Stars и Premium в Fragment.

---

## Запуск сервера

```bash
python app.py
```

Сервер будет доступен по адресу: `http://127.0.0.1:8080`

---

## Эндпоинты

### 1. Проверка баланса

```http
GET /balance
```

**Пример запроса (curl):**
```bash
curl http://127.0.0.1:8080/balance
```

### 2. Получение информации о пользователе

```http
POST /user_info
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "username": "@username"
}
```

**Пример curl:**
```bash
curl -X POST http://127.0.0.1:8080/user_info -H "Content-Type: application/json" -d "{\"username\":\"@username\"}"
```

### 3. Покупка Stars без KYC

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

**Пример curl:**
```bash
curl -X POST http://127.0.0.1:8080/buy_stars_nokyc -H "Content-Type: application/json" -d "{\"username\":\"@username\", \"amount\":100}"
```

### 4. Покупка Stars с cookies

```http
POST /buy_stars
```

**Тело запроса:**
```json
{
  "username": "@username",
  "amount": 100
}
```

### 5. Покупка Premium без KYC

```http
POST /buy_premium_nokyc
```

**Тело запроса:**
```json
{
  "username": "@username",
  "duration": 3
}
```

- `duration` — количество месяцев (3, 6 или 12)

### 6. Покупка Premium с cookies

```http
POST /buy_premium
```

**Тело запроса:**
```json
{
  "username": "@username",
  "duration": 3
}
```

## Пример запроса на Python

```python
import requests

requests.post(
    "http://127.0.0.1:8080/buy_stars_nokyc", # Энд-поинт 
    headers={"Content-Type": "application/json"}, # Обязательный хедер
    data='{"username":"@username","amount":100}' # Тело запроса
)
```
## Отличие методов с KYC и без

- **Без KYC** (`*_nokyc`) — выполняется только через SEED, не требует авторизации аккаунта через cookies, подходит для тестов и быстрых транзакций, но баланс проверяется на кошельке SEED.  
- **С KYC** (`*`) — использует cookies пользователя Fragment, позволяет покупать Stars/Premium с аккаунта пользователя, поддерживает скрытие отправителя (`show_sender=False`).