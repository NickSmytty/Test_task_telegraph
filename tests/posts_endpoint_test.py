import allure
from psycopg2.extensions import cursor
from endpoints.create_post import CreatePost
from endpoints.update_post import UpdatePost
from endpoints.delete_post import DeletePost
from endpoints.get_post import GetAllPosts, GetSinglePost


@allure.parent_suite("Common checks")
@allure.suite("Posts endpoints")
@allure.title("Get all posts")
def test_get_posts_request():
    """
    Tests send GET request for all posts.
    Checks response status code and checks all posts via schema.
    """
    status_code = 200
    post = GetAllPosts()

    post.get_posts()
    post.check_status_code(status_code)
    post.check_results()


@allure.parent_suite("Common checks")
@allure.suite("Posts endpoints")
@allure.title("Get one post")
def test_get_object_request(object_id: int):
    """
    Test send Get request for one post.
    Checks response status code and checks response id.
    """
    status_code = 200
    post = GetSinglePost()

    post.get_post(object_id)
    post.check_status_code(status_code)
    post.check_id(object_id)
    post.check_results()


@allure.parent_suite("Common checks")
@allure.suite("Posts endpoints")
@allure.title("Create post")
def test_create_object(db_connection_fake: cursor | None):
    """
    Test create new post.
    Checks response status code.
    Validate response via schema.
    Checks that all items is equal to sent payload.
    Checks one additional item (just to check possibility to do it).
    """
    post = CreatePost()

    post.new_post()
    post.check_status_code(code=201)
    post.validate_response()
    post.check_all_items()
    post.check_item(name="id")
    post.check_created_post_in_db(db_connection_fake)
    post.delete_post()
    post.check_results()


@allure.parent_suite("Common checks")
@allure.suite("Posts endpoints")
@allure.title("Update post")
def test_update_object(object_id: int, db_connection_fake: cursor | None):
    """
    Test update posts.
    Check response status code.
    Check that response after update contain items which has been updated.
    Check that GET response contain items which has been updated
    """
    post = UpdatePost()

    post.update_post(object_id=object_id)
    post.check_status_code(200)
    post.check_all_updated_items()
    post.check_post_after_update(object_id)
    post.check_updated_post_in_db(db_connection_fake)
    post.check_results()


@allure.parent_suite("Common checks")
@allure.suite("Posts endpoints")
@allure.title("Delete post")
def test_delete_object(object_id: int, db_connection_fake: cursor | None):
    """
    Test delete post.
    Check response status code.
    Check that there is no post with this id.
    """
    post = DeletePost()

    post.delete_post(object_id)
    post.check_status_code(200)
    post.check_get_after_delete(object_id)
    post.check_deleted_post_in_db(object_id, db_connection_fake)
    post.check_results()
