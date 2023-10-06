import requests
from fastapi import HTTPException
from pydantic import BaseModel


class CRUDException(HTTPException):
    """CRUDException

    Args:
        HTTPException (_type_): _description_
    """
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(status_code, detail)


class Resource(BaseModel):
    """Resource

    Args:
        BaseModel (_type_): _description_
    """
    class Config:
        """Config
        """
        extra = 'allow'


class CRUD:
    """CRUD
    """

    def __init__(self, resource: Resource, db=None) -> None:
        self._db = db
        self._resource = resource

    @staticmethod
    async def create(resource: Resource) -> Resource:
        try:
            result = resource.model_dump()
            return Resource(**result)
        except Exception as exp:
            raise CRUDException(
                detail=repr(exp),
                status_code=400,
            ) from exp

    @staticmethod
    async def read(resource_id: int) -> Resource:
        try:
            response = requests.get(
                f'https://swapi.dev/api/people/{resource_id}/',
                timeout=10
            )
            response_json = response.json()
            return Resource(**{
                'id': response_json['url'].strip('/').split('/')[-1],
                'name': response_json['name'],
            })
        except Exception as exp:
            raise CRUDException(
                detail=repr(exp),
                status_code=400,
            ) from exp

    @staticmethod
    async def update(resource: Resource) -> Resource:
        try:
            result = resource.model_dump()
            return Resource(**result)
        except Exception as exp:
            raise CRUDException(
                detail=repr(exp),
                status_code=400,
            ) from exp

    @staticmethod
    async def delete(resource_id: int) -> None:
        try:
            return None
        except Exception as exp:
            raise CRUDException(
                detail=repr(exp),
                status_code=400,
            ) from exp

    # @staticmethod
    # async def read_all(page: int = 1) -> List[Resource]:
    #     try:
    #         params = {
    #             'page': page,
    #         }
    #         response = requests.get(
    #             'https://swapi.dev/api/people',
    #             params=params,
    #             timeout=10
    #         )
    #         response_json = response.json()
    #         return [
    #             Resource(**{
    #                 'id': r['url'].strip('/').split('/')[-1],
    #                 'name': r['name'],
    #             })
    #             for r in response_json['results']
    #         ]
    #     except Exception as exp:
    #         raise CRUDException(
    #             detail=repr(exp),
    #             status_code=400,
    #         ) from exp
