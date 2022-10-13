import pytest
from fastapi import status

from app.custom_exceptions import TextNotFoundException


@pytest.mark.asyncio
async def test_get_texts(db_data, async_client):

    # USER IS NOT LOGGED -> ONLY PUBLIC TEXTS WILL BE RETURNED
    response = await async_client.get("/texts/")
    assert response.status_code == 200
    assert len(response.json()) == 4

    # USER IS NOT LOGGED -> TESTING PAGINATION
    response = await async_client.get("/texts/?page=2&limit=2")
    assert len(response.json()) == 2

    # USER IS LOGGED -> ONLY HIS / HER TEXTS WILL BE RETURNED
    credentials = dict(email="loj.za@gmail.com", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    auth_header_value = " ".join(["Bearer", jwt_token])

    response = await async_client.get("/texts/", headers={"Authorization": auth_header_value})
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_public_text_by_id(db_data, async_client):
    all_public_texts = (await async_client.get("/texts/")).json()

    # PUBLIC TEXT CAN BE ACCESSED BY UNAUTHENTICATED USER
    public_text_id = all_public_texts[0]["id"]
    response = await async_client.get(f"/texts/{public_text_id}")

    assert response.status_code == 200
    assert response.json()["is_public"] is True

    credentials = dict(email="loj.za@gmail.com", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    auth_header_value = " ".join(["Bearer", jwt_token])

    # PUBLIC TEXT CAN BE ACCESSED BY AUTHENTICATED USER
    response = await async_client.get(f"/texts/{public_text_id}", headers={"Authorization": auth_header_value})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_private_text_by_id(db_data, async_client):

    # LOGGED USER CAN ACCESS ITS OWN PRIVATE TEXT
    credentials = dict(email="derek.uncle@mail.eu", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    auth_header_value = " ".join(["Bearer", jwt_token])
    response = await async_client.get("/texts/", headers={"Authorization": auth_header_value})
    text_id = response.json()[0]["id"]

    response = await async_client.get(f"/texts/{text_id}", headers={"Authorization": auth_header_value})
    assert response.status_code == 200

    # LOGGED USER CAN'T ACCESS PRIVATE TEXT OF OTHER USER
    credentials = dict(email="loj.za@gmail.com", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    auth_header_value = " ".join(["Bearer", jwt_token])

    exception = TextNotFoundException()
    response = await async_client.get(f"/texts/{text_id}", headers={"Authorization": auth_header_value})

    assert response.status_code == exception.status_code
    assert response.json()["detail"] == exception.detail

    # UNAUTHENTICATED USER CAN'T REACH PRIVATE TEXT
    response = await async_client.get(f"/texts/{text_id}")
    assert response.status_code == exception.status_code
    assert response.json()["detail"] == exception.detail


@pytest.mark.asyncio
async def test_post_new_text(db_data, async_client):

    # NEW TEXT IS SUCCESSFULLY ADDED BY LOGGED USER
    credentials = dict(email="loj.za@gmail.com", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    auth_header_value = " ".join(["Bearer", jwt_token])

    new_text = dict(name="new_text", content="new_content")
    response = await async_client.post("/texts/", headers={"Authorization": auth_header_value}, json=new_text)
    assert response.status_code == status.HTTP_201_CREATED

    response = await async_client.get("/texts/", headers={"Authorization": auth_header_value})
    assert len(response.json()) == 2

    # NEW TEXT HAS NO REQUIRED CONTENT
    new_text = dict(name="new_text")
    response = await async_client.post("/texts/", headers={"Authorization": auth_header_value}, json=new_text)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # UNAUTHENTICATED USER CAN'T ADD NEW TEXT
    new_text = dict(name="new_text_b", content="new_content")
    response = await async_client.post("/texts/", json=new_text)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_delete_text(db_data, async_client):

    # LOGGED USER CAN DELETE ITS OWN TEXT
    credentials = dict(email="derek.uncle@mail.eu", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    user_one_auth_header_value = " ".join(["Bearer", jwt_token])

    response = await async_client.get("/texts/", headers={"Authorization": user_one_auth_header_value})
    text_id = response.json()[0]["id"]
    text_id_two = response.json()[1]["id"]
    text_id_three = response.json()[2]["id"]

    deletion_response = await async_client.delete(f"/texts/{text_id}", headers={"Authorization": user_one_auth_header_value})
    assert deletion_response.status_code == status.HTTP_204_NO_CONTENT

    response = await async_client.get("/texts/", headers={"Authorization": user_one_auth_header_value})
    assert len(response.json()) == 2

    # LOGGED USER WITH NO MASTER ADMIN PRIVILEGE CAN'T DELETE TEXT OF OTHER USER
    credentials = dict(email="loj.za@gmail.com", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    auth_header_value = " ".join(["Bearer", jwt_token])

    exception = TextNotFoundException()
    deletion_response = await async_client.delete(f"/texts/{text_id_two}", headers={"Authorization": auth_header_value})
    assert deletion_response.status_code == exception.status_code
    assert deletion_response.json()["detail"] == exception.detail

    # MASTER ADMIN CAN DELETE ANY TEXT
    credentials = dict(email="terry.very@something.eu", password="abc123ABC")
    login_response = await async_client.post("/login/", json=credentials)
    jwt_token = login_response.json()["token"]
    auth_header_value = " ".join(["Bearer", jwt_token])

    deletion_response = await async_client.delete(f"/texts/{text_id_three}", headers={"Authorization": auth_header_value})
    assert deletion_response.status_code == status.HTTP_204_NO_CONTENT

    response = await async_client.get("/texts/", headers={"Authorization": user_one_auth_header_value})
    assert len(response.json()) == 1
