from .auth import SignUpView
from .posts import PostView

post = PostView.as_view()
sign_up = SignUpView.as_view()
