import pytest
from fastapi import status
from datetime import datetime, timedelta

pytestmark = pytest.mark.asyncio

# ================== Test Create Contact without Authorization ==================

async def test_create_contact_without_authorization(client, test_contact):
    response = client.post("/contacts", json=test_contact)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data

# ============================== Test Get Contacts =============================

async def test_get_contacts(client):
    response = client.get("/contacts/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["first_name"] == "John"

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
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# ================== Test Remove Contact without Authorization ==================

async def test_remove_contact_without_authorization(client, test_contact, user):
    response_create = client.post("/contacts", json=test_contact)
    data_create = response_create.json()
    contact_id = data_create["id"]
    response = client.delete(f"/contacts/{contact_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# ========================= Test Upcoming Birthdays ===========================

async def test_upcoming_birthdays(client):
    today = datetime.today().date()
    next_seven_days = today + timedelta(days=7)
    response = client.get("/contacts/birthdays/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
