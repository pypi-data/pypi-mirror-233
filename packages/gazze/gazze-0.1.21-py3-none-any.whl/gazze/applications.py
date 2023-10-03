import asyncio
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Sequence,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)
from gazze.exceptions import RequestValidationError
from gazze.datastructures import Default, DefaultPlaceholder
from gazze.types import DecoratedCallable, IncEx
from gazze.responses import JSONResponse
from gazze.routing import GRouter
from gazze.params import Depends
from gazze.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from starlette.routing import Route, Router
from starlette.applications import Starlette
from starlette.datastructures import State
from starlette.middleware import Middleware
from starlette.responses import Response
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
from gazze.middleware.asyncexitstack import AsyncExitStackMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send
# from starlette.types import ASGIApp, Lifespan, Receive, Scope, Send
from starlette.requests import Request
from starlette.exceptions import HTTPException
from hypercorn.asyncio import serve

AppType = TypeVar("AppType", bound="Gazze")

class Gazze(Starlette):
    def __init__(
        self: AppType,
        debug: bool = False,
        title: str = "Gazze",
        description: str = "",
        version: str = "0.1.0",
        exception_handlers: Optional[
            Dict[
                Union[int, Type[Exception]],
                Callable[[Request, Any], Coroutine[Any, Any, Response]],
            ]
        ] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> None:
        self.debug = debug
        self.title = title
        self.description = description
        self.version = version
        self.state: State = State()
        self.router: GRouter = GRouter()
        self.default_response_class = default_response_class
        self.response_class = response_class
        self.dependencies = dependencies
        self.dependency_overrides: Dict[Callable[..., Any], Callable[..., Any]] = {}
        self.exception_handlers: Dict[
            Any, Callable[[Request, Any], Union[Response, Awaitable[Response]]]
        ] = ({} if exception_handlers is None else dict(exception_handlers))
        self.exception_handlers.setdefault(HTTPException, http_exception_handler)
        self.exception_handlers.setdefault(
            RequestValidationError, request_validation_exception_handler
        )
        self.user_middleware: List[Middleware] = []
        self.middleware_stack: Union[ASGIApp, None] = None

    def add_route(
        self,
        *,
        path: str,
        endpoint: Callable[..., Coroutine[Any, Any, Response]],
        methods: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> None:
        self.router.add_route(
            path=path, 
            endpoint=endpoint, 
            methods=methods, 
            dependencies=dependencies,
            response_class=response_class
        )

    def build_middleware_stack(self) -> ASGIApp:
        debug = self.debug
        error_handler = None
        exception_handlers = {}

        for key, value in self.exception_handlers.items():
            if key in (500, Exception):
                error_handler = value
            else:
                exception_handlers[key] = value

        middleware = (
            [Middleware(ServerErrorMiddleware, handler=error_handler, debug=debug)]
            + self.user_middleware
            + [
                Middleware(
                    ExceptionMiddleware, handlers=exception_handlers, debug=debug
                ),
                Middleware(AsyncExitStackMiddleware),
            ]
        )

        app = self.router
        for cls, options in reversed(middleware):
            app = cls(app=app, **options)
        return app
    
    def get(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.router.get(
            path=path, 
            dependencies=dependencies,
            response_class=response_class
        )

    def put(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.router.put(
            path=path, 
            dependencies=dependencies,
            response_class=response_class
        )

    def post(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.router.post(
            path=path, 
            dependencies=dependencies,
            response_class=response_class
        )

    def delete(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.router.delete(
            path=path, 
            dependencies=dependencies,
            response_class=response_class
        )

    def options(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.router.options(
            path=path, 
            dependencies=dependencies,
            response_class=response_class
        )

    def head(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.router.head(
            path=path, 
            dependencies=dependencies,
            response_class=response_class
        )

    def patch(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.router.patch(
            path=path, 
            dependencies=dependencies,
            response_class=response_class
        )