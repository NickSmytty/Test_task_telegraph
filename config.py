import random
import string


SHOULD_ATTACH = True

BASE_URL = "https://jsonplaceholder.typicode.com/posts"

DATABASE = ("your_database",)
USER = ("your_user",)
PASSWORD = ("your_password",)
HOST = ("localhost",)
PORT = ("5432",)

SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "required": ["userId", "id", "title", "body"],
}


def generate_random_string(length=10):
    return "".join(random.choice(string.ascii_letters) for i in range(length))


def generate_create_payload():
    return {
        "title": generate_random_string(),
        "body": generate_random_string(),
        "userId": random.randint(1, 1000),
    }


def generate_update_payload():
    return {
        "id": random.randint(1, 1000),
        "title": generate_random_string(),
        "body": generate_random_string(),
        "userId": random.randint(1, 1000),
    }
