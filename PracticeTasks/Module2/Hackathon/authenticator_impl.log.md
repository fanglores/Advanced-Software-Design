# Request
Напиши пример 2х микросервисов на FastAPI Python, которые запускаются через uvicorn. Первый app1 должен принимать запрос и токен сессии. Запрос имеет вид /logs/{podName}. Второй должен уметь авторизовывать и хранить Single Sing-On информацию. app1 для продолжения работы ходит к app2 и просит авторизовать.

# Response
Вот пример реализации двух микросервисов на **FastAPI**, которые взаимодействуют друг с другом:

1. **`app1`**: Принимает запросы от клиента, проверяет токен сессии, обращается к `app2` для проверки авторизации.
2. **`app2`**: Управляет авторизацией, проверяет токены, хранит Single Sign-On (SSO) информацию.

---

### **Директория проекта**
```
project/
├── app1/
│   ├── main.py
├── app2/
│   ├── main.py
├── requirements.txt
```

---

### **Код `app1/main.py`**

```python
from fastapi import FastAPI, HTTPException, Depends
import httpx

app = FastAPI()

AUTH_SERVICE_URL = "http://localhost:8001"  # URL второго микросервиса

@app.get("/logs/{pod_name}")
async def get_logs(pod_name: str, session_token: str):
    """
    Получает логи для указанного pod, проверяя токен с app2.
    """
    async with httpx.AsyncClient() as client:
        # Обращение к app2 для проверки токена
        auth_response = await client.post(
            f"{AUTH_SERVICE_URL}/auth/validate",
            json={"session_token": session_token}
        )
        if auth_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Unauthorized session token")
        
        auth_data = auth_response.json()
        if not auth_data.get("authorized", False):
            raise HTTPException(status_code=403, detail="Access denied")

    # Если авторизация успешна, вернуть логи (упрощённая заглушка)
    return {"pod_name": pod_name, "logs": f"Fake logs for pod {pod_name}"}
```

---

### **Код `app2/main.py`**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Хранилище сессий для SSO (упрощённое, для демонстрации)
sessions = {
    "valid-token-123": {"user_id": 1, "permissions": ["read_logs"]},
    "valid-token-456": {"user_id": 2, "permissions": ["read_logs", "write_logs"]},
}

class TokenValidationRequest(BaseModel):
    session_token: str

@app.post("/auth/validate")
async def validate_token(request: TokenValidationRequest):
    """
    Проверяет валидность токена и возвращает информацию о сессии.
    """
    token_data = sessions.get(request.session_token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid session token")
    
    return {"authorized": True, "user_id": token_data["user_id"], "permissions": token_data["permissions"]}
```

---

### **Файл `requirements.txt`**
```plaintext
fastapi==0.95.2
uvicorn==0.22.0
httpx==0.24.0
```

---

### **Запуск микросервисов**

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите оба микросервиса в отдельных терминалах:

   - Для `app1` (порт 8000):
     ```bash
     uvicorn app1.main:app --host 0.0.0.0 --port 8000
     ```
   - Для `app2` (порт 8001):
     ```bash
     uvicorn app2.main:app --host 0.0.0.0 --port 8001
     ```

---

### **Пример запроса**

1. Отправьте запрос в `app1`, передав валидный токен:
   ```bash
   curl -X GET "http://localhost:8000/logs/my-pod" -H "session_token: valid-token-123"
   ```

2. Если токен валиден, получите ответ:
   ```json
   {
       "pod_name": "my-pod",
       "logs": "Fake logs for pod my-pod"
   }
   ```

3. Если токен невалиден:
   ```json
   {
       "detail": "Unauthorized session token"
   }
   ``` 

Этот пример демонстрирует базовую архитектуру для взаимодействия между микросервисами на FastAPI с использованием валидации сессий.

# Request
Нужно чтобы токен проверялся по-настоящему. И были максимально заиспользованны механизмы FastAPI

# Response
Для реализации проверки токена "по-настоящему" с использованием механизмов **FastAPI** нужно сделать следующее:

1. Использовать **`Depends`** для инъекции зависимостей (например, проверки токенов).
2. В `app2` создать отдельный механизм обработки токенов с использованием хранилища, например, Redis или in-memory (для упрощения примера).
3. В `app1` проверять токены через запросы к `app2` или посредством асинхронного вызова функции.

Вот обновленный пример с учетом этих требований:

---

### **Директория проекта**
```
project/
├── app1/
│   ├── main.py
├── app2/
│   ├── main.py
├── requirements.txt
```

---

### **Код `app2/main.py`**

`app2` отвечает за управление сессиями и токенами. Здесь используются зависимости FastAPI для упрощения аутентификации.

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import uuid

app = FastAPI()

# Простое хранилище токенов (имитация реальной базы данных)
# Ключ - токен, значение - информация о сессии
tokens_db = {}

# Конфигурация токена
TOKEN_EXPIRATION_MINUTES = 30


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenValidationRequest(BaseModel):
    session_token: str


def create_token(username: str) -> str:
    """Создаёт новый токен и сохраняет его в хранилище."""
    token = str(uuid.uuid4())
    tokens_db[token] = {
        "username": username,
        "expires_at": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES),
    }
    return token


def validate_token(token: str):
    """Проверяет валидность токена."""
    session = tokens_db.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid token")
    if session["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")
    return session


@app.post("/auth/login")
async def login(request: TokenRequest):
    """
    Имитация входа: создаёт новый токен для пользователя.
    """
    if request.username == "user" and request.password == "password":  # Условие входа
        token = create_token(request.username)
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/auth/validate")
async def validate(request: TokenValidationRequest):
    """
    Проверяет токен и возвращает информацию о пользователе.
    """
    session = validate_token(request.session_token)
    return {"authorized": True, "username": session["username"]}


@app.get("/auth/session")
async def get_session_data(token: str = Depends(validate_token)):
    """
    Получение информации о текущей сессии.
    """
    return token
```

---

### **Код `app1/main.py`**

`app1` обращается к `app2` для проверки токенов через асинхронные HTTP-запросы. Используются зависимости для удобной проверки токена.

```python
from fastapi import FastAPI, HTTPException, Depends
import httpx
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# Указываем адрес auth-сервиса
AUTH_SERVICE_URL = "http://localhost:8001"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{AUTH_SERVICE_URL}/auth/login")


async def authenticate_token(token: str = Depends(oauth2_scheme)):
    """
    Проверяет токен через `app2`.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/auth/validate", json={"session_token": token})
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Unauthorized token")
        return response.json()


@app.get("/logs/{pod_name}")
async def get_logs(pod_name: str, auth: dict = Depends(authenticate_token)):
    """
    Получение логов с проверкой токена.
    """
    username = auth.get("username")
    return {
        "message": f"Hello, {username}! Here are the logs for {pod_name}.",
        "logs": f"Fake logs for pod {pod_name}",
    }
```

---

### **Файл `requirements.txt`**

```plaintext
fastapi==0.95.2
uvicorn==0.22.0
httpx==0.24.0
python-multipart==0.0.6
```

---

### **Запуск микросервисов**

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите оба сервиса:
   - `app2`:
     ```bash
     uvicorn app2.main:app --host 0.0.0.0 --port 8001
     ```
   - `app1`:
     ```bash
     uvicorn app1.main:app --host 0.0.0.0 --port 8000
     ```

---

### **Пример работы**

1. Получите токен в `app2`:
   ```bash
   curl -X POST "http://localhost:8001/auth/login" -H "Content-Type: application/json" -d '{"username": "user", "password": "password"}'
   ```
   Ответ:
   ```json
   {
       "token": "some-unique-token"
   }
   ```

2. Используйте токен для доступа к логам через `app1`:
   ```bash
   curl -X GET "http://localhost:8000/logs/my-pod" -H "Authorization: Bearer some-unique-token"
   ```
   Ответ:
   ```json
   {
       "message": "Hello, user! Here are the logs for my-pod.",
       "logs": "Fake logs for pod my-pod"
   }
   ```

3. Если токен недействителен:
   ```bash
   curl -X GET "http://localhost:8000/logs/my-pod" -H "Authorization: Bearer invalid-token"
   ```
   Ответ:
   ```json
   {
       "detail": "Unauthorized token"
   }
   ```

---

### Основные механизмы FastAPI

- **`Depends`** используется для инъекции токенов.
- **OAuth2PasswordBearer** помогает автоматически обрабатывать авторизацию через Bearer токены.
- Асинхронные запросы через `httpx` позволяют минимизировать задержки при обращении между микросервисами.

# Request
Нет. Напиши пример для боевого запроса. Не надо использовать заглушки для аутентификации. Нам пришел запрос, мы должны из него получить сессию, аутентифицировать её. Если аутентификация успешна, но мы возвращаем логи как Success

# Response
Для боевого сценария нам нужно корректно обработать запрос, извлечь сессию (например, из токена), проверить её с помощью реального механизма аутентификации (например, через базу данных или Redis), и вернуть результат. Этот пример подразумевает, что у нас есть:

1. Реальная база данных или другое хранилище сессий.
2. Проверка сессий через токены, извлечённые из заголовка `Authorization`.

---

### **Директория проекта**
```
project/
├── app1/
│   ├── main.py
├── app2/
│   ├── main.py
├── requirements.txt
```

---

### **Код `app2/main.py`**

Этот сервис выполняет аутентификацию на основе сессий. Реализация предполагает использование Redis как хранилища сессий.

```python
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
import redis
import json

app = FastAPI()

# Настройки Redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Утилита для извлечения токена из заголовка Authorization
def get_token_from_request(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    return auth_header.split(" ")[1]


def validate_token(token: str):
    """
    Проверяет токен в Redis.
    """
    session_data = redis_client.get(token)
    if not session_data:
        raise HTTPException(status_code=401, detail="Session not found or expired")
    return json.loads(session_data)


@app.post("/auth/validate")
async def validate(request: Request):
    """
    Валидация токена и возврат информации о сессии.
    """
    token = get_token_from_request(request)
    session = validate_token(token)
    return {"success": True, "session": session}


@app.post("/auth/session")
async def create_session(username: str):
    """
    Создаёт новую сессию (эмуляция входа).
    """
    import uuid
    session_token = str(uuid.uuid4())
    session_data = {"username": username, "roles": ["reader"], "active": True}
    redis_client.setex(session_token, 3600, json.dumps(session_data))  # Токен живёт 1 час
    return {"token": session_token, "session": session_data}
```

---

### **Код `app1/main.py`**

Этот сервис использует `app2` для проверки токена и возвращает логи в случае успешной аутентификации.

```python
from fastapi import FastAPI, HTTPException, Depends, Request
import httpx

app = FastAPI()

AUTH_SERVICE_URL = "http://localhost:8001"  # Ссылка на сервис авторизации


async def authenticate_token(request: Request):
    """
    Проверка токена через запрос в app2.
    """
    async with httpx.AsyncClient() as client:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Authorization header missing")
        response = await client.post(f"{AUTH_SERVICE_URL}/auth/validate", headers={"Authorization": token})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Unauthorized")
        return response.json()


@app.get("/logs/{pod_name}")
async def get_logs(pod_name: str, auth: dict = Depends(authenticate_token)):
    """
    Возвращает логи при успешной аутентификации.
    """
    username = auth["session"]["username"]
    return {
        "status": "success",
        "message": f"User {username} authenticated successfully.",
        "pod_name": pod_name,
        "logs": f"Logs for {pod_name}"
    }
```

---

### **Файл `requirements.txt`**

```plaintext
fastapi==0.95.2
uvicorn==0.22.0
httpx==0.24.0
redis==5.0.0
python-multipart==0.0.6
```

---

### **Настройка Redis**

1. Установите Redis, если его нет:
   ```bash
   sudo apt update
   sudo apt install redis
   ```

2. Запустите Redis:
   ```bash
   redis-server
   ```

---

### **Запуск микросервисов**

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите оба сервиса:

   - `app2`:
     ```bash
     uvicorn app2.main:app --host 0.0.0.0 --port 8001
     ```

   - `app1`:
     ```bash
     uvicorn app1.main:app --host 0.0.0.0 --port 8000
     ```

---

### **Пример работы**

1. Создайте новую сессию через `app2`:
   ```bash
   curl -X POST "http://localhost:8001/auth/session" -d "username=user"
   ```

   Ответ:
   ```json
   {
       "token": "some-unique-token",
       "session": {
           "username": "user",
           "roles": ["reader"],
           "active": true
       }
   }
   ```

2. Используйте токен для запроса логов через `app1`:
   ```bash
   curl -X GET "http://localhost:8000/logs/my-pod" -H "Authorization: Bearer some-unique-token"
   ```

   Ответ:
   ```json
   {
       "status": "success",
       "message": "User user authenticated successfully.",
       "pod_name": "my-pod",
       "logs": "Logs for my-pod"
   }
   ```

3. Если токен недействителен или отсутствует:
   ```bash
   curl -X GET "http://localhost:8000/logs/my-pod" -H "Authorization: Bearer invalid-token"
   ```

   Ответ:
   ```json
   {
       "detail": "Unauthorized"
   }
   ```

---

### Особенности реализации

1. **`Redis`** используется для хранения сессий с TTL.
2. В `app2` проверяются токены с использованием Redis.
3. Логи возвращаются только после успешной аутентификации.
4. Реализована архитектура взаимодействия через HTTP-запросы между `app1` и `app2`.

# Request
Нет, давай без Redis и убери излишние комментарии.

# Response
### **Код `app2/main.py`**

```python
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid

app = FastAPI()

# Хранилище сессий (в памяти для демонстрации)
sessions = {}

TOKEN_LIFETIME_MINUTES = 30

class SessionData(BaseModel):
    username: str
    expires_at: datetime

def create_session(username: str) -> str:
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=TOKEN_LIFETIME_MINUTES)
    sessions[token] = SessionData(username=username, expires_at=expires_at)
    return token

def validate_token(token: str) -> SessionData:
    session = sessions.get(token)
    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return session

@app.post("/auth/login")
def login(username: str):
    token = create_session(username)
    return {"token": token}

@app.post("/auth/validate")
def validate(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token = auth_header.split(" ")[1]
    session = validate_token(token)
    return {"success": True, "username": session.username}
```

---

### **Код `app1/main.py`**

```python
from fastapi import FastAPI, HTTPException, Depends, Request
import httpx

app = FastAPI()
AUTH_SERVICE_URL = "http://localhost:8001"

async def authenticate_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/auth/validate", headers={"Authorization": auth_header})
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return response.json()

@app.get("/logs/{pod_name}")
async def get_logs(pod_name: str, auth: dict = Depends(authenticate_token)):
    return {
        "status": "success",
        "message": f"User {auth['username']} authenticated.",
        "pod_name": pod_name,
        "logs": f"Logs for pod {pod_name}",
    }
```

---

### **Файл `requirements.txt`**

```plaintext
fastapi==0.95.2
uvicorn==0.22.0
httpx==0.24.0
python-multipart==0.0.6
```

---

### **Запуск сервисов**

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите сервисы:
   - `app2`:
     ```bash
     uvicorn app2.main:app --host 0.0.0.0 --port 8001
     ```
   - `app1`:
     ```bash
     uvicorn app1.main:app --host 0.0.0.0 --port 8000
     ```

---

### **Пример работы**

1. Создайте токен:
   ```bash
   curl -X POST "http://localhost:8001/auth/login" -d "username=user"
   ```
   Ответ:
   ```json
   {
       "token": "some-unique-token"
   }
   ```

2. Используйте токен:
   ```bash
   curl -X GET "http://localhost:8000/logs/my-pod" -H "Authorization: Bearer some-unique-token"
   ```
   Ответ:
   ```json
   {
       "status": "success",
       "message": "User user authenticated.",
       "pod_name": "my-pod",
       "logs": "Logs for pod my-pod"
   }
   ```

3. При использовании неверного токена:
   ```bash
   curl -X GET "http://localhost:8000/logs/my-pod" -H "Authorization: Bearer invalid-token"
   ```
   Ответ:
   ```json
   {
       "detail": "Unauthorized"
   }
   ```
   
# Request
Ещё раз объясни зачем и как работает Depends

# Response
`Depends` — это механизм **FastAPI** для реализации **внедрения зависимостей** (dependency injection). Он позволяет удобно вызывать функции, которые выполняют подготовительные задачи или проверки, и передавать их результаты обработчикам запросов. Это помогает повторно использовать код и разделять обязанности в приложении.

---

### **Зачем нужен `Depends`**

1. **Повторное использование кода.**
   - Например, проверку аутентификации можно вынести в отдельную функцию и использовать её в нескольких маршрутах.
   
2. **Изоляция логики.**
   - Проверка токенов, подключение к базе данных, обработка данных или конфигураций изолируются в зависимости.

3. **Удобство тестирования.**
   - Зависимости можно подменить в тестах, чтобы имитировать различные сценарии.

4. **Упрощение модульного кода.**
   - Логику проверок и обработки можно описать отдельно от маршрутов.

---

### **Как работает `Depends`**

#### Основная идея

- **Зависимость** — это функция, которая выполняет некоторую работу и возвращает данные. FastAPI вызывает её автоматически, когда она нужна обработчику.
- Обработчик запроса принимает результат выполнения зависимости в виде параметра.

---

#### Пример 1: Проверка токена

1. **Зависимость** — функция, которая проверяет токен.
2. **Результат функции** передаётся в обработчик запроса.

```python
from fastapi import FastAPI, HTTPException, Depends, Request

app = FastAPI()

async def authenticate_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    token = auth_header.split(" ")[1]
    if token != "valid-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"username": "test_user"}

@app.get("/secure-data")
async def secure_data(auth: dict = Depends(authenticate_token)):
    return {"message": f"Hello, {auth['username']}!"}
```

1. **Что происходит?**
   - Когда вызывается `/secure-data`, FastAPI автоматически вызывает `authenticate_token`, чтобы проверить токен.
   - Если токен валиден, результат функции (`{"username": "test_user"}`) передаётся в обработчик как параметр `auth`.

2. **Как `Depends` облегчает код?**
   - Проверка токена вынесена в отдельную функцию и может быть использована в других маршрутах.

---

#### Пример 2: Подключение к базе данных

1. Зависимость создаёт подключение к базе.
2. Подключение автоматически передаётся обработчику.

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = {"connection": "Database Connection"}  # Пример "подключения"
    try:
        yield db
    finally:
        print("Closing database connection")  # Закрытие соединения

@app.get("/data")
def read_data(db: dict = Depends(get_db)):
    return {"db_status": "connected", "db_info": db["connection"]}
```

1. **Что происходит?**
   - FastAPI вызывает функцию `get_db`, чтобы получить "подключение" к базе данных.
   - Результат (словарь) передаётся в обработчик как параметр `db`.

2. **Почему используется `yield`?**
   - Это позволяет освободить ресурсы (например, закрыть подключение к базе) после завершения запроса.

---

#### Пример 3: Зависимость с параметрами

Иногда зависимости принимают входные параметры, которые контролируют их поведение.

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_pagination_params(limit: int = 10, offset: int = 0):
    return {"limit": limit, "offset": offset}

@app.get("/items/")
def read_items(params: dict = Depends(get_pagination_params)):
    return {"items": ["item1", "item2", "item3"][params["offset"]:params["limit"]]}

# GET /items/?limit=2&offset=1
# Ответ: {"items": ["item2", "item3"]}
```

1. **Что происходит?**
   - FastAPI вызывает `get_pagination_params`, передавая параметры из запроса (`limit` и `offset`).
   - Обработчик получает результат функции (`{"limit": 2, "offset": 1}`) как параметр.

---

### Когда использовать `Depends`

1. **Проверка токенов или аутентификация.**
   - Отделить логику проверки токенов или ролей пользователя.

2. **Подключение к ресурсам.**
   - Работа с базой данных, API других сервисов, кешем.

3. **Фильтры или валидация данных.**
   - Предобработка параметров запроса или данных тела.

4. **Конфигурация.**
   - Передача настроек приложения в маршруты.

---

### Важные особенности `Depends`

1. **Асинхронность.**
   - Зависимости могут быть обычными функциями или асинхронными (определяются через `async def`).
   
2. **Рекурсивные зависимости.**
   - Зависимость может использовать другие зависимости.
   
   ```python
   def get_user(auth: dict = Depends(authenticate_token)):
       return {"username": auth["username"]}

   @app.get("/profile")
   def get_profile(user: dict = Depends(get_user)):
       return {"profile": f"Profile of {user['username']}"}
   ```

3. **Передача параметров.**
   - Зависимости принимают параметры, которые FastAPI автоматически заполняет из запроса.

`Depends` делает код чище, помогает разделять логику и поддерживать её в долгосрочной перспективе.
