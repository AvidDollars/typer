import asyncio
import json
from os import path

import pytest
import os
from httpx import AsyncClient

from .. import main
from ..constants import TEST_DB_SEED_DIR
from ..containers import Container
from ..models.text import TextDb
from ..models.text_rating import TextRatingDb
from ..models.typing_session import TypingSessionDb
from ..models.user import UserDb
from ..repositories import CrudOperations


@pytest.fixture(scope="session")
async def db_data():
    yield await populate_test_db()
    os.remove("testing.db")


@pytest.fixture
async def async_client():
    async with AsyncClient(app=main.app, base_url="http://localhost:8000") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


async def populate_test_db():
    """
    populates testing database with a data
    """

    testing_db = Container().db()  # @inject was not working
    await testing_db.initialize()

    crud_operations = CrudOperations(db=testing_db)

    # CREATING USERS
    with open(path.join(TEST_DB_SEED_DIR, "users.json")) as users_data:
        users: list[dict] = json.load(users_data)

    # to be used as foreign key in other tables
    user_ids, text_ids = [], []

    for index, user in enumerate(users):
        hashed_password = Container().hashing_service().hash(user["password"])
        user.update(password=hashed_password)
        user = UserDb(**user)

        await crud_operations.create_resource(user)
        user_ids.append(user.id)

    # CREATING TEXTS
    with open(path.join(TEST_DB_SEED_DIR, "texts.json")) as texts_data:
        texts: list[dict] = json.load(texts_data)

    text_idx = 0

    # first 4 users will have text added
    for counter, user_id in enumerate(user_ids[:4], 1):
        for _ in range(counter):
            text = texts[text_idx]
            text.update(added_by=user_id)
            text = TextDb(**text)
            await crud_operations.create_resource(text)

            text_ids.append(text.id)
            text_idx += 1

    # CREATING TYPING SESSIONS
    with open(path.join(TEST_DB_SEED_DIR, "typing_sessions.json")) as typing_sessions_data:
        typing_sessions: list[dict] = json.load(typing_sessions_data)

    for user_id, text_id, typing_session in zip(user_ids[::2], text_ids[::-2], typing_sessions[::2]):
        typing_session.update(user_id=user_id, text_id=text_id)
        typing_session = TypingSessionDb(**typing_session)
        await crud_operations.create_resource(typing_session)

    for user_id, text_id, typing_session in zip(user_ids[::2], text_ids[::2], typing_sessions[::-2]):
        typing_session.update(user_id=user_id, text_id=text_id)
        typing_session = TypingSessionDb(**typing_session)
        await crud_operations.create_resource(typing_session)

    # CREATING TEXT RATINGS
    with open(path.join(TEST_DB_SEED_DIR, "text_ratings.json")) as text_ratings_data:
        text_ratings: list[dict] = json.load(text_ratings_data)

    for user_id, text_id, text_rating in zip(user_ids[::2], text_ids[::-2], text_ratings[::2]):
        text_rating.update(rated_by=user_id, rated_text=text_id)
        text_rating = TextRatingDb(**text_rating)
        await crud_operations.create_resource(text_rating)

    for user_id, text_id, text_rating in zip(user_ids[::-2], text_ids[::-2], text_ratings[::-2]):
        text_rating.update(rated_by=user_id, rated_text=text_id)
        text_rating = TextRatingDb(**text_rating)
        await crud_operations.create_resource(text_rating)