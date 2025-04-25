# erp-login-microservice

This service allows automation systems or external tools to **validate login credentials** by attempting a real login to the PSIT ERP portal. It does not store or cache any credentials or data.

Hosted at:  
🔗 [https://erp-login-microservice.vercel.app](https://erp-login-microservice.vercel.app)


## 🔧 API Usage

This microservice supports both **GET** and **POST** methods for login.

> ⚠️ **POST is recommended** for better security (credentials in the request body).

### `GET /login`

Pass credentials in the URL query parameters.

**Example:**

```
https://erp-login-microservice.vercel.app/login?username=22016XXXXXXXX&password=abcdefgh
```

### `POST /login`

Send credentials in a JSON body.

**Request:**
```http
POST /login
Content-Type: application/json
```

**Body:**
```json
{
  "username": "22016XXXXXXXX",
  "password": "abcdefgh"
}
```

✅ Success Response

```json
{
  "status": "success",
  "data": {
    "name": "Student Name",
    "roll": "XXXXXXXXXXXX",
    "branch": "Branch Name",
    "section": "Section Name",
    "email": "user@example.com",
    "mobile": "XXXXXXXXXX",
    "birthDate": "MM-DD-YYYY",
    "libraryCode": "XXXXXXX",
    "localAddress": "Address Line 1, Area",
    "permanentAddress": "Address Line 1, Area"
  }
}
```

❌ Error Response

If login fails due to incorrect credentials:

```json
{
  "status": "error",
  "msg": "Incorrect credentials"
}
```

If username or password is missing:

```json
{
  "status": "error",
  "msg": "Username and password required"
}
```
