from .auth import SignUpView
from .posts import PostView, PostLikeView

post = PostView.as_view()
like = PostLikeView.as_view()
sign_up = SignUpView.as_view()
