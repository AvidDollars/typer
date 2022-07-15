import pytest

from app.custom_exceptions import UserAlreadyRegisteredException


@pytest.mark.asyncio
async def test_invalid_arguments_for_user_registration(async_client):

    # PROVIDED NAME IS TOO SHORT
    name_is_short = dict(name="no", email="thisis.valid@email.com", password="abc123DEF")
    response = await async_client.post("/register/", json=name_is_short)
    assert response.status_code == 400
    assert response.json()["error"] == "value_error"

    # PROVIDED NAME HAS INVALID SYMBOL
    name_has_invalid_symbol = dict(name="inv@lid", email="thisis.valid@email.com", password="abc123DEF")
    response = await async_client.post("/register/", json=name_has_invalid_symbol)
    assert response.status_code == 400
    assert response.json()["error"] == "value_error"

    # EMAIL ADDRESS IS NOT VALID
    email_is_invalid = dict(name="John", email="inv@lid", password="abc123DEF")
    response = await async_client.post("/register/", json=email_is_invalid)
    assert response.status_code == 400
    assert response.json()["error"] == "value_error"

    # PASSWORD IS NOT STRONG ENOUGH
    email_is_invalid = dict(name="John", email="thisis.valid@email.com", password="w3ak_password")
    response = await async_client.post("/register/", json=email_is_invalid)
    assert response.status_code == 400
    assert response.json()["error"] == "value_error"


@pytest.mark.asyncio
async def test_user_already_exists(db_data, async_client):

    # PROVIDED NAME ALREADY EXISTS
    name_already_exists = dict(name="Lojza", email="thisis.valid@email.com", password="abc123DEF")
    response = await async_client.post("/register/", json=name_already_exists)

    exception = UserAlreadyRegisteredException()
    assert response.status_code == exception.status_code
    assert response.json()["detail"] == exception.detail

    # PROVIDED EMAIL ALREADY EXISTS
    email_already_exists = dict(name="Robin", email="kill.bill@domain.org", password="abc123DEF")
    response = await async_client.post("/register/", json=email_already_exists)

    exception = UserAlreadyRegisteredException()
    assert response.status_code == exception.status_code
    assert response.json()["detail"] == exception.detail


@pytest.mark.asyncio
async def test_registration_email_has_been_sent(db_data, async_client, fake_email_sender):

    # ALL FIELDS ARE VALID AND NEITHER NAME NOR EMAIL IS PRESENT IN THE DATABASE
    valid_registration_data = dict(name="Marty", email="thisis.valid@email.eu", password="abc123DEF")
    response = await async_client.post("/register/", json=valid_registration_data)

    assert response.status_code == 200
    assert response.json() == {"message": "email sent"}
    assert fake_email_sender["recipient"] == "thisis.valid@email.eu"
    assert "activation_token" in fake_email_sender
