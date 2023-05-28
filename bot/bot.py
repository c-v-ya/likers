import logging
from enum import Enum
from typing import Literal

import requests
from faker import Faker

from settings import BOT_SETTINGS, SERVER_URL

log = logging.getLogger(__file__)


class MethodName(Enum):
    GET: str = "get"
    POST: str = "post"


METHODS = {
    MethodName.GET: requests.get,
    MethodName.POST: requests.post,
}


class Bot:
    # Bot for automated API usage
    faker = Faker()
    NUMBER_OF_USERS: int
    MAX_POSTS_PER_USER: int
    MAX_LIKES_PER_USER: int

    def __init__(self):
        self.users = dict()
        # Set every field from settings to the bot instance
        for key, val in BOT_SETTINGS.items():
            setattr(self, key, val)

    def complete_flow(self):
        self.create_users()
        self.get_tokens()
        self.perform_posting()
        self.perform_liking()

    def create_users(self):
        log.info(f"Create {self.NUMBER_OF_USERS} users")
        for _ in range(self.NUMBER_OF_USERS):
            username = self.faker.user_name()
            password = self.faker.password()
            payload = {
                "username": username,
                "first_name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "email": self.faker.email(),
                "password": password,
            }
            if not self._make_request(MethodName.POST, "/sign-up/", payload=payload):
                continue

            log.info(f"User {username} signed up")
            self.users[username] = {"token": None, "password": password}

    def get_tokens(self):
        log.info("Get tokens for users")
        for username, user_data in self.users.items():
            payload = {"username": username, "password": user_data.get("password")}
            if not (response := self._make_request(MethodName.POST, "/token/", payload=payload)):
                continue

            user_data["token"] = response.json().get("access")
            log.info(f"Saved token for {username}")

    def perform_posting(self):
        log.info("Perform posting")
        for username, user_data in self.users.items():
            total_posts = self.faker.random_int(1, self.MAX_POSTS_PER_USER, 1)
            token = user_data.get("token")
            for _ in range(total_posts):
                payload = {"text": self.faker.text()}
                if not self._make_request(
                    MethodName.POST, "/posts/", payload=payload, auth_token=token
                ):
                    continue

                user_data["total_posts"] = total_posts
                log.info(f"Created {total_posts} posts as {username}")

    def perform_liking(self):
        log.info("Perform liking")
        # Next user to perform a like is the user who has most posts
        sorted_users = sorted(
            self.users,
            key=lambda _user: self.users.get(_user, {}).get("total_posts", []),
            reverse=True,
        )
        for user in sorted_users:
            likes_count = 0
            liked_posts = []  # Remember the posts user liked
            likes_goal = self.MAX_LIKES_PER_USER

            # Auth and utility stuff
            token = self.users.get(user, {}).get("token")
            error = False  # If something goes wrong, we're not stuck in a loop

            friends = list(self.users.keys())  # Friends to like their posts
            friends.remove(user)  # Don't like own posts
            while friends and likes_count < likes_goal and not error:
                # Randomly chose a friend to like his posts
                friend = self.faker.random_choices(friends, 1)[0]
                if not (
                    response := self._make_request(
                        MethodName.GET, f"/{friend}/posts/", auth_token=token
                    )
                ):
                    friends.remove(friend)
                    continue

                friend_posts = response.json()
                # Like posts by friends who have at least one post with 0 likes
                if all([post.get("likes_count") > 0 for post in friend_posts]):
                    log.info(f"Every post by {friend} has at least one like")
                    friends.remove(friend)
                    continue

                while likes_count < likes_goal and friend_posts and not error:
                    # Randomly choose a post to like
                    post = self.faker.random_choices(friend_posts, 1)[0]
                    post_id = post.get("id")
                    # Don't like a post user already seen
                    friend_posts.remove(
                        [post for post in friend_posts if post.get("id") == post_id][0]
                    )
                    # Don't like a post twice
                    if post_id in liked_posts:
                        continue

                    if not (
                        self._make_request(
                            MethodName.POST, f"/{friend}/posts/{post_id}/like/", auth_token=token
                        )
                    ):
                        error = True
                        continue

                    likes_count += 1
                    liked_posts.append(post_id)
                    log.info(
                        f"{user} liked post {post_id}"
                        f' by {post.get("author", {}).get("username", {})}'
                        f' it now has {post.get("likes_count") + 1} likes'
                    )

    @staticmethod
    def _make_request(
        method: Literal[MethodName.GET, MethodName.POST],
        endpoint: str,
        payload: dict | None = None,
        auth_token: str = "",
    ):
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else None
        error_msg = f"Error making {method} request to {endpoint}"
        try:
            response = METHODS[method](f"{SERVER_URL}{endpoint}", headers=headers, json=payload)
            if response.ok:
                return response
        except (KeyError, requests.exceptions.RequestException):
            log.error(error_msg, exc_info=True)

        log.error(error_msg)
