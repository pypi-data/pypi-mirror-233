import asyncio
import uuid
from contextvars import ContextVar
from typing import TYPE_CHECKING, Dict, Optional, Union

from dotserve.session import HTTPSession, WebsocketSession
from lazify import LazyProxy

if TYPE_CHECKING:
    from dotserve.client.cloud import AppUser, PersistedAppUser
    from dotserve.emitter import BaseDotserveEmitter
    from dotserve.message import Message


class DotserveContextException(Exception):
    def __init__(self, msg="Dotserve context not found", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class DotserveContext:
    loop: asyncio.AbstractEventLoop
    emitter: "BaseDotserveEmitter"
    session: Union["HTTPSession", "WebsocketSession"]

    def __init__(self, session: Union["HTTPSession", "WebsocketSession"]):
        from dotserve.emitter import BaseDotserveEmitter, DotserveEmitter

        self.loop = asyncio.get_running_loop()
        self.session = session
        if isinstance(self.session, HTTPSession):
            self.emitter = BaseDotserveEmitter(self.session)
        elif isinstance(self.session, WebsocketSession):
            self.emitter = DotserveEmitter(self.session)


context_var: ContextVar[DotserveContext] = ContextVar("dotserve")


def init_ws_context(session_or_sid: Union[WebsocketSession, str]) -> DotserveContext:
    if not isinstance(session_or_sid, WebsocketSession):
        session = WebsocketSession.require(session_or_sid)
    else:
        session = session_or_sid
    context = DotserveContext(session)
    context_var.set(context)
    return context


def init_http_context(
    user: Optional[Union["AppUser", "PersistedAppUser"]] = None,
    auth_token: Optional[str] = None,
    user_env: Optional[Dict[str, str]] = None,
) -> DotserveContext:
    session = HTTPSession(
        id=str(uuid.uuid4()),
        token=auth_token,
        user=user,
        user_env=user_env,
    )
    context = DotserveContext(session)
    context_var.set(context)
    return context


def get_context() -> DotserveContext:
    try:
        return context_var.get()
    except LookupError:
        raise DotserveContextException()


context: DotserveContext = LazyProxy(get_context, enable_cache=False)
