from flask import Blueprint

from .login.routes import LoginView, LogoutView
from .profile.routes import ProfileView, AddToFavoritesView, RemoveFromFavoritesView, InfoView
from .quotes.routes import QuotesView, VoteUpView, VoteDownView
bp = Blueprint('app', __name__)

bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
bp.add_url_rule('/profile', view_func=ProfileView.as_view('profile'))
bp.add_url_rule('/', view_func=QuotesView.as_view('quotes'))
bp.add_url_rule('/vote_up/<int:quote_id>', view_func=VoteUpView.as_view('vote_up'))
bp.add_url_rule('/vote_down/<int:quote_id>', view_func=VoteDownView.as_view('vote_down'))
bp.add_url_rule('/add_to_favorites/<int:quote_id>', view_func=AddToFavoritesView.as_view('add_favorite'))
bp.add_url_rule('/remove_from_favorites/<int:quote_id>', view_func=RemoveFromFavoritesView.as_view('remove_favorite'))
bp.add_url_rule('/info', view_func=InfoView.as_view('info'))
