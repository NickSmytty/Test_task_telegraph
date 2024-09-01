import allure
import requests
from psycopg2.extensions import cursor
from common.allure_attach import attach
from endpoints.base_endpoint import BasePost
from endpoints.get_post import GetSinglePost
from config import BASE_URL, SHOULD_ATTACH, generate_update_payload


class UpdatePost(BasePost):
    def __init__(self):
        super().__init__()
        self.payload = generate_update_payload()

    def update_post(self, object_id: int) -> None:
        """
        Update post by id
        """
        with allure.step(f"Update post with id = {object_id}"):
            self.response = requests.put(
                url=f"{BASE_URL}/{object_id}", json=self.payload
            )
            self.response_json = self.response.json()

            if SHOULD_ATTACH:
                attach("Update post", self.response_json)

    def check_all_updated_items(self) -> None:
        """
        Checks all updated items
        """
        with allure.step(
            f"Check that response after update contain items which has been updated"
        ):
            for key in self.payload:
                self.check_item(key)

    def check_item(self, name: str) -> None:
        """
        Check one item
        """
        if self.response_json[name] != self.payload[name]:
            error_message = f"Item {name} must be equal to {self.payload[name]} not {self.response_json[name]}"

            if name == "id":
                allure.dynamic.issue("https://jira/browse/FC-0001")
                self.xfails.append(error_message + ". BUG FC-0001")
            else:
                self.errors.append(error_message)

    def check_post_after_update(self, object_id: int) -> None:
        """
        Checks that a post has been updated using a GET request.
        Checks that status code of Get request is 200.
        Checks that GET response is equal to PUT response.
        """
        with allure.step(
            f"Check that GET response contain items which has been updated"
        ):
            post = GetSinglePost()

            post.get_post(object_id)
            post.check_status_code(200)
            self.get_response = post.response_json

            if self.get_response != self.payload:
                allure.dynamic.issue("https://jira/browse/FC-0001")

                if SHOULD_ATTACH:
                    attach("Payload to update", self.payload)
                    attach("Get response after update", self.get_response)

                self.xfails.append(
                    f"Get response after update must be equal to sent request. BUG FC-0001"
                )

    def check_updated_post_in_db(self, db_connection: cursor | None) -> None:
        """Checks that post has been updated in DB and all items"""
        if db_connection is not None:
            db_connection.execute(
                "SELECT * FROM posts WHERE id = %s", (self.response_json["id"],)
            )
            db_record = db_connection.fetchone()

            if not db_record:
                self.errors.append("Post not created in DB")
            else:
                for key in self.response_json:
                    if db_record[key] != self.response_json[key]:
                        self.errors.append(
                            f"Item {key} must be equal to {self.response_json[key]} not {db_record[key]}"
                        )
