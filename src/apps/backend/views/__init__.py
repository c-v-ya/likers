from .auth import SignUpView
from .posts import PostView, PostLikeView, PostUnlikeView

post = PostView.as_view()
like = PostLikeView.as_view()
unlike = PostUnlikeView.as_view()
sign_up = SignUpView.as_view()
