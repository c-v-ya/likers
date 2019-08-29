from .auth import SignUpView
from .posts import PostView

post_list = PostView.as_view()
sign_up = SignUpView.as_view()
