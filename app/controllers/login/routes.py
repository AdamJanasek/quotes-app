from flask import render_template, request, redirect, url_for, session

from app.common.api_view import APIView


class LoginView(APIView):
    """Login class. Allows user login with POST method.
    Set a boolean variable @User-Token after successful login.
    Inherits from APIView class.
    """
    template = "sites/login.html"

    def get(self):
        return render_template(self.template)

    def post(self):
        data = request.form
        code, response = self.api.login(data.get('login'), data.get('password'))

        if not response.get('message'):
            session['User-Token'] = True
            return redirect(url_for('app.profile'))

        return render_template(self.template, message=response.get('message'))


class LogoutView(APIView):
    """Logout class. Remove variable from session.
    Inherits from APIView class.
    """
    def get(self):
        del session['User-Token']
        self.api.logout()
        return redirect(url_for('app.quotes'))
