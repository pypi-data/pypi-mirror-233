import asyncio
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)
from hypercorn.config import Config
from gazze.exceptions import RequestValidationError
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
from starlette.types import ASGIApp
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
    ) -> None:
        self.debug = debug
        self.title = title
        self.description = description
        self.version = version
        self.state: State = State()
        self.router: Router = Router()
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
        path: str,
        endpoint: Callable[..., Coroutine[Any, Any, Response]],
        methods: Optional[List[str]] = None,
    ) -> None:
        self.router.add_route(path=path, endpoint=endpoint, methods=methods)

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
    
    def run(self, config: Config = Config()):
        asyncio.run(serve(self, config, mode='asgi'))