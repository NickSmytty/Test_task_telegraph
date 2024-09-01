import allure
import requests
from psycopg2.extensions import cursor
from common.allure_attach import attach
from endpoints.base_endpoint import BasePost
from endpoints.delete_post import DeletePost
from config import BASE_URL, SHOULD_ATTACH, generate_create_payload


class CreatePost(BasePost):
    def __init__(self):
        super().__init__()
        self.payload = generate_create_payload()

    def new_post(self) -> None:
        """
        Send POST request
        """
        with allure.step("Create post"):
            self.response = requests.post(url=BASE_URL, json=self.payload)
            self.response_json = self.response.json()

            if SHOULD_ATTACH:
                attach("Create post", self.payload)
                attach("Post has been created", self.response_json)

            self.payload["id"] = self.response_json["id"]

    def check_all_items(self) -> None:
        """
        Checks all items in response
        """
        with allure.step("Check all items"):
            self.compare_keys(self.response_json, self.payload)

            for key in self.payload:
                self.check_item(key)

    def compare_keys(self, response_json: dict, payload: dict) -> None:
        """
        Compare keys from request and response
        """
        response_keys = set(response_json.keys())
        payload_keys = set(payload.keys())

        missing_keys = payload_keys - response_keys
        extra_keys = response_keys - payload_keys

        if missing_keys or extra_keys:
            self.errors.append(
                f"Keys mismatch between response and payload:\n"
                f"Missing keys in response: {', '.join(missing_keys)}\n"
                f"Extra keys in response: {', '.join(extra_keys)}\n"
            )

    def check_item(self, name: str) -> None:
        """
        Check one item
        """
        with allure.step(f"Check one item '{name}'"):
            if self.response_json[name] != self.payload[name]:
                self.errors.append(
                    f"Item {name} must be equal to {self.payload[name]} not {self.response_json[name]}"
                )

    def delete_post(self) -> None:
        """
        Delete created post
        """
        delete_post = DeletePost()
        delete_post.delete_post(self.response_json["id"])
        delete_post.check_status_code(200)

    def check_created_post_in_db(self, db_connection: cursor | None) -> None:
        """Checks that post has been created in DB and all items"""
        if db_connection is not None:
            db_connection.execute(
                "SELECT * FROM posts WHERE id = %s", (self.response.json()["id"],)
            )
            db_record = db_connection.fetchone()

            if not db_record:
                self.errors.append("Post not created in DB")
            else:
                for key in self.payload:
                    if db_record[key] != self.payload[key]:
                        self.errors.append(
                            f"Item {key} must be equal to {self.payload[key]} not {db_record[key]}"
                        )
