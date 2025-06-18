import json
import httpx
from uuid import UUID
from dataclasses import dataclass, field

@dataclass
class File:
    name: str
    id: UUID| None = field(default=None)
    content: bytes| None = field(default=None)

class APIService:
    base_url = "http://127.0.0.1:8000/api/v1/files/"

    def list(self) -> list[File]:
        res = httpx.get(self.base_url)
        data = json.loads(res.content)
        data = list(map(lambda file: File(id=file["id"], name=file["name"]), data))
        return data

    def create(self, file: File) -> tuple[UUID, bool]:
        try:
            res = httpx.post(self.base_url, data={"name":file.name, "content": file.content})
        except httpx.NetworkError as e:
            return None, False 
        
        data = json.loads(res.content)
        return data["id"], True

    def retrieve(self, id) -> File:
        res = httpx.get(self.base_url + f"{id}/")
        data = json.loads(res.content)
        return File(name=data["name"], id=data["id"], content=data["content"])
