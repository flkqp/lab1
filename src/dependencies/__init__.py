from .common_dependencies import get_posts
from .repositories_dependencies import get_post_repository
from .controllers_dependencies import get_post_controller

__all__ = [
    "get_posts",
    "get_post_repository",
    "get_post_controller",
]