from dataclasses import dataclass

import httpx

from app.user.auth.schemas import GoogleUserData
from app.settings import Settings


@dataclass
class GoogleClient:
    settings: Settings

    async def get_user_info(self, code: str) -> GoogleUserData:
        google_access_token = await self._get_user_access_token(code=code)
        async with httpx.AsyncClient() as client:
            user_info = await client.get(
                url="https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {google_access_token}"},
            )
            return GoogleUserData(
                **user_info.json(), google_access_token=google_access_token
            )

    async def _get_user_access_token(self, code: str) -> str:
        request_body = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.settings.GOOGLE_TOKEN_URL, data=request_body
            )
            return response.json()["access_token"]
