from typing import Sequence, Type, Union
from flask_restful import Api
from flask_apispec import FlaskApiSpec
from flask_restful import Resource as _Resource
from flask_apispec import MethodResource


class Resource(MethodResource, _Resource):
    pass


def register_resource(
    resource: Type[Resource],
    paths: Union[str, Sequence[str]],
    api: Api,
    apidoc: FlaskApiSpec,
):
    if isinstance(paths, str):
        paths = (paths,)
    api.add_resource(resource, *paths)
    apidoc.register(resource)
