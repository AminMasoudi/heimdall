import json
import httpx
from uuid import UUID
from dataclasses import dataclass, field


@dataclass
class File:
    name: str
    id: UUID | None = field(default=None)
    content: bytes | None = field(default=None)


class APIService:
    def __init__(self, host: str):
        if not (host.startswith("http://") or host.startswith("https://")):
            host = "http://" + host
        self.base_url = host
        self.file_url = self.base_url + "/api/v1/files/"
        self.auth_url = self.base_url + "/api/v1/token/"
        self.client = httpx.Client()

    def authenticate(self, access_token, refresh_token):
        assert access_token is not None, "Couldn't find Access Token"
        assert refresh_token is not None, "Couldn't find Refresh Token"

        authenticated, token = self.verify(
            access_token=access_token, refresh_token=refresh_token
        )
        if not authenticated:
            raise Exception("failed to authenticate. login again")
        self.client = httpx.Client(headers={"Authorization": "Bearer " + token})

    def list(self) -> list[File]:
        res = self.client.get(self.file_url)
        data = json.loads(res.content)
        data = list(map(lambda file: File(id=file["id"], name=file["name"]), data))
        return data

    def create(self, file: File) -> tuple[UUID, bool]:
        try:
            res = self.client.post(
                self.file_url, data={"name": file.name, "content": file.content}
            )
        except httpx.NetworkError as e:
            return None, False

        data = json.loads(res.content)
        return data["id"], True

    def retrieve(self, id) -> File:
        res = self.client.get(self.file_url + f"{id}/")
        data = json.loads(res.content)
        return File(name=data["name"], id=data["id"], content=data["content"])

    def delete(self, id):
        self.client.delete(self.file_url + f"{id}/")

    def login(self, username, password) -> tuple[str, str]:
        res = httpx.post(
            self.auth_url, data={"username": username, "password": password}
        )
        data = json.loads(res.content)
        if res.status_code == 200:
            access = data["access"]
            refresh = data["refresh"]
            return access, refresh
        raise Exception(data["detail"])

    def verify(self, access_token: str, refresh_token: str) -> tuple[bool, str]:
        if self.__verify_token(access_token):
            return True, access_token
        return self.__refresh(refresh_token)

    def __verify_token(self, token: str) -> bool:
        res = httpx.post(self.auth_url + "verify/", data={"token": token})
        return res.status_code == 200

    def __refresh(self, refresh_token: str) -> tuple[bool, str]:
        if not self.__verify_token(refresh_token):
            return False, "Not a valid refresh token"
        res = httpx.post(self.auth_url + "refresh/", data={"refresh": refresh_token})
        if res.status_code == 200:
            access_token = json.loads(res.content)["access"]
            return True, access_token
        return False, "failed to refresh token"
