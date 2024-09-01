import allure
import requests
from config import BASE_URL, SHOULD_ATTACH
from common.allure_attach import attach
from endpoints.base_endpoint import BasePost


class BaseGetPost(BasePost):

    def _fetch_response(self, url: str, attach_name: str) -> None:
        """
        Get post or all posts
        """
        self.response = requests.get(url=url)
        self.response_json = self.response.json()
        self.validate_response()

        if SHOULD_ATTACH:
            attach(attach_name, self.response_json)


class GetSinglePost(BaseGetPost):
    def get_post(self, object_id: int) -> None:
        """
        Get one post by id
        """
        with allure.step(f"Get one post with id = {object_id}"):
            self._fetch_response(f"{BASE_URL}/{object_id}", "Single post")

    def check_id(self, object_id: int) -> None:
        """
        Checks response id
        """
        with allure.step(f"Check response id equal to {object_id}"):
            if self.response_json["id"] != object_id:
                self.errors.append(
                    f"Response id must be equal to {object_id}, not {self.response_json['id']}"
                )


class GetAllPosts(BaseGetPost):
    def get_posts(self) -> None:
        """
        Get all posts
        """
        with allure.step("Get all posts"):
            self._fetch_response(BASE_URL, "All posts")
