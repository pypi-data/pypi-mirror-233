
import abc
import asyncio
import json

from typing import Callable
from starlette.types import Scope
from starlette.types import Receive
from starlette.types import Send

from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import JSONResponse

from ezcx.webhooks.request import WebhookRequest
from ezcx.webhooks.response import WebhookResponse


class Router(abc.ABC):
    
    def __init__(self):
        self.routes = {}

    @abc.abstractmethod
    def get_handler(self, tag_or_scope) -> Callable:
        ...

    @staticmethod
    def asyncify(handler: Callable):
        if not asyncio.iscoroutinefunction(handler):
            async def coroutine(res, req):
                handler(res, req)
            return coroutine
        return handler


class PathRouter(Router):

    def register(self, path: str, handler: Callable):
        handler = self.asyncify(handler)
        self.routes[path] = handler

    def get_handler(self, scope: Scope):
        return self.routes[scope['path']]

class TagRouter(Router):

    def register(self, tag: str, handler: Callable):
        handler = self.asyncify(handler)
        self.routes[tag] = handler

    def get_handler(self, wh_request: WebhookRequest):
        return self.routes[wh_request.tag]


class Server:

    def __init__(self, router: Router):
        self.router = router

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope, receive)
        body = await request.json()
        wh_request = WebhookRequest(body)
        wh_response = WebhookResponse()
        if isinstance(self.router, TagRouter):
            handler = self.router.get_handler(wh_request)
        elif isinstance(self.router, PathRouter):
            handler = self.router.get_handler(scope)
        await handler(wh_response, wh_request)
        await JSONResponse(wh_response.to_dict())(scope, receive, send)

