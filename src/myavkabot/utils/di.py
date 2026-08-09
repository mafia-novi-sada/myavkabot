from typing import Self

from dishka import Container, Provider, Scope, make_container, provide

from ..config import Config, get_config


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_config(self: Self) -> Config:
        return get_config()


di_container: Container = make_container(AppProvider())
