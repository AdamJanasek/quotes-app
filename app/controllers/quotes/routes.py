import itertools
import operator

from flask import render_template, redirect, url_for, flash, request

from app.common.api_view import APIView
from app.common.extensions import check_logged, show_message
from app.controllers.quotes.model import Quote


class QuotesView(APIView):
    """Quotes class to return filtered query with given keyword.
    Inherits from APIView class.
    """
    template = "sites/quotes.html"
    # list of css classes to colour quote items
    quotes_classes = ['white-card', 'blue-card', 'green-card', 'red-card', 'yellow-card']

    def get(self):
        query = request.args
        keyword = query.get('keyword')

        if keyword:
            status_code, quotes = self.api.get_filtered_quotes(keyword=keyword)
        else:
            status_code, quotes = self.api.get_quotes()

        if status_code == 200:
            # todo: paginate
            try:
                data = self.parse(quotes.get('quotes'))
            except KeyError:
                data = []
                flash('Nothing found :(')
        else:
            flash(quotes.get('message'))
            data = []

        return render_template(self.template, quotes=data, keyword=keyword)

    def parse(self, data):
        # dict keys from response witch are used in frontend
        keys = ['id', 'author', 'body']
        f = operator.itemgetter(*keys)
        reduce_results = [Quote(*f(quote)) for quote in data]
        # join css classes with quote objects
        return [quote for quote in zip(itertools.cycle(self.quotes_classes), reduce_results)]


class VoteUpView(APIView):
    """Class to vote up.
    Inherits from APIView class.
    """
    @check_logged
    def get(self, quote_id):
        show_message(*self.api.up_vote(quote_id), 'Vote up to quote {}!'.format(quote_id))
        return redirect(url_for('app.quotes'))


class VoteDownView(APIView):
    """Class to vote down.
    Inherits from APIView class.
    """
    @check_logged
    def get(self, quote_id):
        show_message(*self.api.down_vote(quote_id), 'Vote down to quote {}!'.format(quote_id))
        return redirect(url_for('app.quotes'))
