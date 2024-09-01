import allure
import requests
from config import BASE_URL
from psycopg2.extensions import cursor
from endpoints.base_endpoint import BasePost
from endpoints.get_post import GetSinglePost


class DeletePost(BasePost):

    def delete_post(self, object_id: int) -> None:
        """
        Delete post by id
        """
        with allure.step(f"Delete post with id = {object_id}"):
            self.response = requests.delete(url=f"{BASE_URL}/{object_id}")

    def check_get_after_delete(self, object_id: int) -> None:
        """
        Checks that a post has been deleted using a GET request.
        Checks that status code of Get request is 404.
        """
        with allure.step(f"Check that there is no post with id = {object_id}"):
            post = GetSinglePost()
            post.get_post(object_id)

            if post.response.status_code != 404:
                allure.dynamic.issue("https://jira/browse/FC-0000")
                self.xfails.append(
                    f"Status code must be {404}, not {post.response.status_code}. BUG FC-0000"
                )

    def check_deleted_post_in_db(
        self, object_id: int, db_connection: cursor | None
    ) -> None:
        """Checks that post has been deleted in DB"""
        if db_connection is not None:
            db_connection.execute("SELECT * FROM posts WHERE id = %s", (object_id,))
            db_record = db_connection.fetchone()

            if db_record is not None:
                self.errors.append(f"Post id = {object_id} not deleted from DB.")
