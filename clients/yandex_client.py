import requests
from dataclasses import dataclass

from schemas import YandexUserData
from settings import Settings


@dataclass
class YandexClient:
    settings: Settings

    def get_user_info(self, code: str) -> YandexUserData:
        yandex_access_token = self._get_user_access_token(code=code)
        user_info = requests.get(
            url="https://login.yandex.ru/info?format=json",
            headers={"Authorization": f"OAuth {yandex_access_token}"}
        )
        print(f"\n4) Данные пользователя из yandex\nuser_info: {user_info.json()}\n")
        return YandexUserData(**user_info.json(), yandex_access_token=yandex_access_token)

    def _get_user_access_token(self, code: str) -> str:
        request_body = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.settings.YANDEX_CLIENT_ID,
            "client_secret": self.settings.YANDEX_SECRET_KEY,
        }

        print(f"""\n2) Запрос в yandex с испоьзованием полученного кода, а так же 
        client_id и client_secret, полученные из yandex ID\nrequest_body: {request_body}\n""")

        response = requests.post(
            self.settings.YANDEX_TOKEN_URI,
            data=request_body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        print(f"""\n3) Ответ из yandex, содержащий access_token для получения данных "
              f"о пользователе\nresponse: {response.json()}\n""")

        return response.json()["access_token"]
