import httpx


class ApiAuth:
    __token = None

    def __init__(self, token):
        self.__token = self.__authenticate(token)

    def get_token(self):
        return self.__token

    def __authenticate(self, token):
        headers = {
            'Accept': 'application/json; version=3',
            'Authorization': f'Basic {token}',
        }
        response = httpx.post(
            'https://api.azionapi.net/tokens', headers=headers
        )

        if response.status_code == 200 | 201:
            return response.json()['token']
        else:
            raise Exception(
                'Não foi possível autenticar na API: ',
                response.status_code,
                response.text,
            )
