# Endpoints
## Authentication
```bash
POST /api/auth/register
- Register a new user
- Request body: {username, email, password}
- Response: {user_id, password}

POST /api/auth/login
- Authenticate user
- Request body: {email, password}
- Response: {access_token, user_id}

POST /api/auth/logout
- Invalidate access token
- Headers: Authorization: Bearer {access_token}
```

## User
```bash
GET /api/users/{id}
- Get user profile
- Headers: Authorization: Bearer {access_token}
- Response: {id, username, email, created_at}

PUT /api/users/{id}
- Update user profile
- Headers: Authorization: Bearer {access_token}
- Request body: {username, email, password}

DELETE /api/users/{id}
- Delete user account
- Headers: Authorization: Bearer {access_token}
```