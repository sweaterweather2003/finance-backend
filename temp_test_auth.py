from fastapi.testclient import TestClient
import main

client = TestClient(main.app)
response = client.post('/auth/login', data={'username': 'admin', 'password': 'admin123'})
print(response.status_code)
print(response.text)
