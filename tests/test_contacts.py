# import pickle
from datetime import timedelta, datetime

import pytest
from fastapi import status
# from unittest.mock import patch
# from services.auth import auth_service
# from unittest.mock import MagicMock, patch
# from sqlalchemy import select
# from database import User
# from datetime import date


pytestmark = pytest.mark.asyncio


# Перепишіть тест, видаливши заголовок Authorization
async def test_create_contact_without_access_token(client, test_contact):
    # Запит на створення контакту без access_token
    response = client.post("/contacts", json=test_contact)

    # Перевірка, що сервер правильно обробив запит та відправив 401 Unauthorized
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Not authenticated"


# ============================== Test Get Contacts =============================

async def test_get_contacts(client):
    response = client.get("/contacts/")
    assert response.status_code == status.HTTP_200_OK

# ================== Test Update Contact without Authorization ==================

async def test_update_contact_without_authorization(client, test_contact, user):
    response_create = client.post("/contacts", json=test_contact)
    data_create = response_create.json()
    contact_id = data_create["id"]
    updated_contact_data = {
        "first_name": "UpdatedJohn",
        "last_name": "UpdatedDoe",
        "email": "updatedjohndoe@example.com",
        "phone_number": "987654321",
        "birthday": "2001-01-01",
        "additional_data": "Updated additional data",
    }
    response = client.put(f"/contacts/{contact_id}", json=updated_contact_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

# ================== Test Remove Contact without Authorization ==================
async def test_remove_contact_without_authorization(client, test_contact, user):
    response_create = client.post("/contacts", json=test_contact)
    assert response_create.status_code == status.HTTP_201_CREATED  # Перевірка, що контакт був успішно створений
    data_create = response_create.json()
    contact_id = data_create["id"]
    response = client.delete(f"/contacts/{contact_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ========================= Test Upcoming Birthdays ===========================

async def test_upcoming_birthdays(client):
    today = datetime.today().date()
    next_seven_days = today + timedelta(days=7)
    response = client.get("/contacts/birthdays/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
