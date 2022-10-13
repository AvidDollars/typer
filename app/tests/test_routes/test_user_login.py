import pytest

from app.custom_exceptions import \
    MissingCredentialsException, \
    AccountNotActivatedException, \
    InvalidCredentialsException


@pytest.mark.asyncio
async def test_invalid_arguments_for_user_login(db_data, async_client):

    # ONLY PASSWORD IS PROVIDED
    only_password = dict(password="abc123DEF")
    response = await async_client.post("/login/", json=only_password)

    exception = MissingCredentialsException()
    assert response.status_code == exception.status_code
    assert response.json()["detail"] == exception.detail

    # PASSWORD IS MISSING
    missing_password = dict(name="Thomas")
    response = await async_client.post("/login/", json=missing_password)

    assert response.status_code == 400
    assert response.json()["message"] == "field required"

    # CREDENTIALS ARE VALID BUT USER IS NOT ACTIVATED
    not_activated_user = dict(name="kAtY", email="katy.paty@hello.com", password="abc123ABC")
    response = await async_client.post("/login/", json=not_activated_user)

    exception = AccountNotActivatedException()
    assert response.status_code == exception.status_code
    assert response.json()["detail"] == exception.detail

    # INVALID PASSWORD PROVIDED
    invalid_password_provided = dict(name="guitarGuy", password="bad_password")
    response = await async_client.post("/login/", json=invalid_password_provided)

    exception = InvalidCredentialsException()
    assert response.status_code == exception.status_code
    assert response.json()["detail"] == exception.detail


@pytest.mark.asyncio
async def test_successful_user_login(db_data, async_client):

    # VALID EMAIL AND PASSWORD WAS PROVIDED AND USER IS ACTIVATED
    only_password = dict(email="learn.guitar@hello.net", password="abc123ABC")
    response = await async_client.post("/login/", json=only_password)

    assert response.status_code == 200
    assert "token" in response.json()

    # VALID NAME AND PASSWORD WAS PROVIDED AND USER IS ACTIVATED
    only_password = dict(name="guitarGuy", password="abc123ABC")
    response = await async_client.post("/login/", json=only_password)

    assert response.status_code == 200
    assert "token" in response.json()
