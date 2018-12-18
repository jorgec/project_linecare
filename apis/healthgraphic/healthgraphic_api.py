import requests

class HealthGraphic:
    credentials = {
        'email': 'jorge@springvalley.tech',
        'password': 'a$dF1234$$'
    }
    endpoint = 'https://api.healthgraphic.com/v1'
    token = None

    def __init__(self):
        if not self.token:
            self.login()

    def login(self):
        request = requests.post(f'{self.endpoint}/login', data=self.credentials)
        if request.status_code == 200:
            self.token = request.json()['token']
            return self.token
        return False

