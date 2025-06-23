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
    def __init__(self, host :str, port:int = None):

        if not (
            host.startswith("http://") 
            or host.startswith("https://")
            ):
            host = "http://" + host
        self.base_url = host
        self.file_url = self.base_url + "files/" 

    def list(self) -> list[File]:
        res = httpx.get(self.file_url)
        data = json.loads(res.content)
        data = list(map(
            lambda file: File(id=file["id"], name=file["name"]),
            data))
        return data

    def create(self, file: File) -> tuple[UUID, bool]:
        try:
            res = httpx.post(self.file_url, data={"name":file.name, "content": file.content})
        except httpx.NetworkError as e:
            return None, False 
        
        data = json.loads(res.content)
        return data["id"], True

    def retrieve(self, id) -> File:
        res = httpx.get(self.file_url + f"{id}/")
        data = json.loads(res.content)
        return File(name=data["name"], id=data["id"], content=data["content"])

    def delete(self, id): 
        httpx.delete(self.file_url + f"{id}/")
    
    def login(self, username, password):
        ...