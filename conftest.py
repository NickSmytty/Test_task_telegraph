import pytest
import random
import psycopg2
from psycopg2.extensions import cursor
from endpoints.create_post import CreatePost
from endpoints.delete_post import DeletePost
from config import DATABASE, PASSWORD, USER, HOST, PORT

# разобраться с БД , описание функций, юнит тесты, залить на гит


@pytest.fixture(scope="session")
def object_id() -> int:
    """
    Fixture create post and return to the tests.
    After using delete this post
    """
    create_post = CreatePost()

    create_post.new_post()
    create_post.check_status_code(201)
    create_post.check_results()

    create_post_id = random.randint(1, 100)  # The API does not save created posts.
    yield create_post_id  # yield create_post.response_json['id']

    delete_post = DeletePost()
    delete_post.delete_post(create_post.response_json["id"])
    delete_post.check_status_code(200)


@pytest.fixture(scope="session")
def db_connection() -> cursor:
    """
    Open connection to DB.
    Return connection ti the test.
    Close connection after tests.
    """
    connection = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
    )
    cursor_db = connection.cursor()
    yield cursor_db

    cursor_db.close()
    connection.close()


@pytest.fixture(scope="session")
def db_connection_fake() -> None:
    """
    Return None.
    """
    return None
