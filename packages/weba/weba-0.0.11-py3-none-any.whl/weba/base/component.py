import inspect
from functools import cached_property
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar, Union

from fastapi import Request, Response

from .page import Page

P = ParamSpec("P")
R = TypeVar("R")


class NewInitCaller(type):
    def __call__(cls_, *args: Any, **kwargs: Any):  # type: ignore  # noqa: N804
        # sourcery skip: instance-method-first-arg-name
        """Called when you call MyNewClass()"""
        obj = type.__call__(cls_, *args, **kwargs)
        obj.__init__(*args, **kwargs)

        if hasattr(obj, "_content") and not inspect.iscoroutinefunction(obj._content):
            if len(inspect.signature(obj._content).parameters) > 0:
                return obj._content(*args, **kwargs)
            else:
                return obj._content(*args, **kwargs)

        if hasattr(obj, "content") and not inspect.iscoroutinefunction(obj.content):
            if len(inspect.signature(obj.content).parameters) > 0:
                return obj.content(*args, **kwargs)
            else:
                return obj.content()

        return obj


class Component(object, metaclass=NewInitCaller):
    content: Callable[..., Any] | Callable[..., Coroutine[Any, Any, Any]]
    _content: Callable[..., Any] | Callable[..., Coroutine[Any, Any, Any]]

    def __init__(self, *args: Any, **kwargs: Any):
        self._args = args
        self._kwargs = kwargs

    def __await__(self) -> Any:
        if hasattr(self, "_content") and inspect.iscoroutinefunction(self._content):
            # check to see if content takes args
            if len(inspect.signature(self._content).parameters) > 0:
                return self._content(*self._args, **self._kwargs).__await__()
            else:
                return self._content().__await__()

        if hasattr(self, "content") and inspect.iscoroutinefunction(self.content):
            # check to see if content takes args
            if len(inspect.signature(self.content).parameters) > 0:
                return self.content(*self._args, **self._kwargs).__await__()
            else:
                return self.content().__await__()

    @cached_property
    def _parent(self) -> Union["Page", "Component", None]:
        return next((arg for arg in self._args if isinstance(arg, (Component, Page))), None)

    @property
    def request(self) -> Request | None:
        return self._kwargs.get("request") or (self._parent.request if self._parent else None)

    @property
    def response(self) -> Response | None:
        return self._kwargs.get("response") or (self._parent.response if self._parent else None)
