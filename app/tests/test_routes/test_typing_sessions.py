import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_typing_sessions_of_users(db_data, async_client):

    # USER IS LOGGED -> ALL HIS / HER TYPING SESSIONS WILL BE RETURNED
    credentials = dict(email="loj.za@gmail.com", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    auth_header_value = " ".join(["Bearer", jwt_token])

    response = await async_client.get("/typing-sessions/", headers={"Authorization": auth_header_value})
    all_user_one_sessions = response.json()
    assert len(all_user_one_sessions) == 2

    # LOGGED USER CAN ACCESS ITS OWN TYPING SESSION BY TEXT ID
    user_typing_session_id = all_user_one_sessions[0]["text_id"]
    response = await async_client.get(
        f"/typing-sessions/?text={user_typing_session_id}",
        headers={"Authorization": auth_header_value}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

    # LOGGED USER CAN'T ACCESS TYPING SESSION FROM OTHER USER
    credentials = dict(email="derek.uncle@mail.eu", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    auth_header_value = " ".join(["Bearer", jwt_token])

    response = await async_client.get(
        f"/typing-sessions/?text={user_typing_session_id}",
        headers={"Authorization": auth_header_value})

    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_user_can_create_typing_session(db_data, async_client):

    # USER IS LOGGED -> ALL HIS / HER TYPING SESSIONS WILL BE RETURNED
    credentials = dict(email="loj.za@gmail.com", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    auth_header_value = " ".join(["Bearer", jwt_token])

    response = await async_client.get("/typing-sessions/", headers={"Authorization": auth_header_value})
    all_user_sessions = len(response.json())

    response = await async_client.get("/texts/", headers={"Authorization": auth_header_value})
    text_id = response.json()[0]["id"]

    typing_session = dict(duration_in_seconds=100, text_id=text_id, stats={})
    response = await async_client.post(
        "/typing-sessions/",
        headers={"Authorization": auth_header_value},
        json=typing_session
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await async_client.get("/typing-sessions/", headers={"Authorization": auth_header_value})
    all_user_sessions_two = len(response.json())
    assert all_user_sessions + 1 == all_user_sessions_two
