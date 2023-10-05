import typer
import requests
import getpass

# class for login
class Login:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.login_url = 'https://asp-api.amalitech-dev.net/api/auth/login'

    def attempt_login(self):
        try:
            if self.password is None:
                self.password = getpass.getpass('Enter your password: ')

            student_data = {'email': self.email, 'password': self.password}
            login_response = requests.post(self.login_url, data=student_data)

            if login_response.status_code == 200:
                auth_token = login_response.json().get('tokens', {}).get('access', {}).get('token')
                if auth_token:
                    return auth_token
            elif login_response.status_code == 400:
                typer.echo("Login failed. Please check your credentials.")
            else:
                typer.echo(f"Login failed with status code {login_response.status_code}")
        except requests.RequestException as e:
            typer.echo(f"Login failed due to a network error: {e}")


