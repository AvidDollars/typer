import pytest

from app.custom_exceptions import ActivationTokenNotFoundException, ActivationLinkExpiredException
from app.models.user import UserDb


@pytest.mark.asyncio
async def test_activation_of_freshly_registered_user(db_data, async_client, fake_email_sender):

    name_already_exists = dict(name="Marty", email="thisis.valid@email.eu", password="abc123DEF")
    await async_client.post("/register/", json=name_already_exists)

    token = fake_email_sender["activation_token"]
    response = await async_client.get(f"/activate/{token}")
    assert response.json() == {"message": "account was activated"}


@pytest.mark.asyncio
async def test_failed_activation(db_data, async_client):

    # ACTIVATION TOKEN DOES NOT EXIST
    nonexistent_token = "abc"
    response = await async_client.get(f"/activate/{nonexistent_token}")

    exception = ActivationTokenNotFoundException()
    assert response.status_code == exception.status_code
    assert response.json()["detail"] == exception.detail

    # USER IS REGISTERED BUT ACTIVATION TOKEN IS EXPIRED
    user_with_expired_activation_token = await db_data.read_resource(UserDb, filter_=UserDb.name == "marta")
    expired_token = user_with_expired_activation_token.activation_link

    exception = ActivationLinkExpiredException()
    response = await async_client.get(f"/activate/{expired_token}")

    assert response.status_code == exception.status_code
    assert response.json()["detail"] == exception.detail
