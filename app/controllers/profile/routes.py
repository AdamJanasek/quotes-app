from collections import namedtuple

from flask import render_template, redirect, url_for

from app.common.api_view import APIView
from app.common.extensions import login_required, check_logged, show_message


class ProfileView(APIView):
    """Profile class to manage favorites quotes.
    Inherits from APIView class.
    """
    template = "sites/profile.html"

    @login_required
    def get(self):

        def parse(_data):
            quote = namedtuple('Quote', ['id', 'text'])

            # get all favorites from activities
            _favorites = [quote(d.get('trackable_id'), d.get('trackable_value'))
                          for d in _data if d.get('action') == 'favorited']

            # get all unfavorites from activities
            _no_favorites = [quote(d.get('trackable_id'), d.get('trackable_value'))
                             for d in _data if d.get('action') == 'unfavorited']

            # return difference from two sets
            return set(_favorites) - set(_no_favorites)

        status_code, favorites = self.api.get_favorites()

        if status_code == 200:
            # todo: paginate
            data = parse(favorites.get('activities'))
            return render_template(self.template, favorites=data)

        elif status_code == 404:
            return redirect(url_for('app.login'))


class AddToFavoritesView(APIView):
    """Class to add quote to favorites.
     Inherits from APIView class.
     """
    @check_logged
    def get(self, quote_id):
        show_message(*self.api.add_to_favorites(quote_id), 'Add to favorites {}!'.format(quote_id))
        return redirect(url_for('app.profile'))


class RemoveFromFavoritesView(APIView):
    """Class to remove quote to favorites.
    Inherits from APIView class.
    """
    @check_logged
    def get(self, quote_id):
        show_message(*self.api.remove_from_favorites(quote_id), 'Remove from favorites {}!'.format(quote_id))
        return redirect(url_for('app.profile'))


class InfoView(APIView):
    """Info class to only show info page.
    Inherits from APIView class.
    """
    template = "sites/info.html"

    def get(self):
        return render_template(self.template)
