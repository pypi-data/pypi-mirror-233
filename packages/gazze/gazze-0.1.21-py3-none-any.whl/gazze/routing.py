from typing import (
    Any,
    Callable,
#     Coroutine,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
#     Tuple,
    Type,
    Union,
)
from gazze.utils import get_value_or_default
from starlette.routing import BaseRoute, Route
from gazze.types import DecoratedCallable#, IncEx
from gazze.params import Depends
from gazze.responses import JSONResponse
from starlette.responses import Response
from gazze.datastructures import Default, DefaultPlaceholder
from starlette.routing import Router


class GRouter(Router):

    def __init__(
        self,
        *,
        route_class: Type[Route] = Route,
        dependencies: Optional[Sequence[Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        routes: Optional[List[BaseRoute]] = None,
        redirect_slashes: bool = True,
    ) -> None:
        super().__init__(
            routes=routes,
            redirect_slashes=redirect_slashes,
        )
        self.route_class = route_class
        self.dependencies = list(dependencies or [])
        self.responses = responses or {}
        self.default_response_class = default_response_class

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Any = Default(None),
        dependencies: Optional[Sequence[Depends]] = None,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        methods: Optional[Union[Set[str], List[str]]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
        route_class_override: Optional[Type[Route]] = None,
    ) -> None:
        route_class = route_class_override or self.route_class
        responses = responses or {}
        combined_responses = {**self.responses, **responses}
        current_response_class = get_value_or_default(
            response_class, self.default_response_class
        )
        current_dependencies = self.dependencies.copy()
        if dependencies:
            current_dependencies.extend(dependencies)
        route = route_class(
            path,
            endpoint=endpoint,
            methods=methods,
        )
        self.routes.append(route)

    def api_route(
        self,
        path: str,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        methods: Optional[List[str]] = None,
        response_class: Type[Response] = Default(JSONResponse),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.add_api_route(
                path,
                func,
                dependencies=dependencies,
                responses=responses,
                methods=methods,
                response_class=response_class,
            )
            return func

        return decorator

    def get(
        self,
        path: str,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path, 
            methods=['GET'],
            dependencies=dependencies,
            response_class=response_class
        )
    
    def put(
        self,
        path: str,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path, 
            methods=['PUT'],
            dependencies=dependencies,
            response_class=response_class
        )
    
    def post(
        self,
        path: str,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path, 
            methods=['POST'],
            dependencies=dependencies,
            response_class=response_class
        )
    
    def delete(
        self,
        path: str,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path, 
            methods=['DELETE'],
            dependencies=dependencies,
            response_class=response_class
        )
    
    def options(
        self,
        path: str,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path, 
            methods=['OPTIONS'],
            dependencies=dependencies,
            response_class=response_class
        )

    def head(
        self,
        path: str,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path, 
            methods=['HEAD'],
            dependencies=dependencies,
            response_class=response_class
        )

    def patch(
        self,
        path: str,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path, 
            methods=['PATCH'],
            dependencies=dependencies,
            response_class=response_class
        )