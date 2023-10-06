import asyncio
from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.ll1l111ll11lllllIl1l1 import l11l11llll111l11Il1l1
from reloadium.corium.l11l1ll1l1111ll1Il1l1 import llll11111l111l11Il1l1
from reloadium.lib.environ import env
from reloadium.corium.l1ll111lll1l1lllIl1l1 import ll1111111lllll11Il1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.l11111l1l111lll1Il1l1 import ll1l1l1ll11ll1l1Il1l1, l1l11llll111l11lIl1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.ll11ll11l1l1llllIl1l1 import l1111l11l1ll11l1Il1l1
from reloadium.corium.ll11111llll11ll1Il1l1 import l1l111lll11llll1Il1l1, l111l11llll1l1l1Il1l1, ll1lll11l111llllIl1l1, lll111llllll111lIl1l1, l1ll1l11llll11llIl1l1
from reloadium.corium.ll1ll11ll111l111Il1l1 import l1llll11llll1l11Il1l1, ll1lll11111llll1Il1l1
from reloadium.corium.llll1l11ll111l11Il1l1 import ll1l11ll1ll11lllIl1l1
from reloadium.corium.l1l1ll1lll1111l1Il1l1 import ll1ll1l11ll11ll1Il1l1
from dataclasses import dataclass, field


if (TYPE_CHECKING):
    from django.db import transaction
    from django.db.transaction import Atomic


__RELOADIUM__ = True


@dataclass(**l1ll1l11llll11llIl1l1)
class l1l11lll11ll1l1lIl1l1(lll111llllll111lIl1l1):
    llllll1ll11lll1lIl1l1 = 'Field'

    @classmethod
    def ll1111ll1l1lllllIl1l1(l1lll1111l11l1llIl1l1, lllll1l1l111111lIl1l1: ll1l11ll1ll11lllIl1l1.llllll1111111111Il1l1, llllll1111lll1llIl1l1: Any, ll11l1llll111l11Il1l1: l111l11llll1l1l1Il1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(llllll1111lll1llIl1l1, 'field') and isinstance(llllll1111lll1llIl1l1.field, Field))):
            return True

        return False

    def l1l111ll11ll11llIl1l1(lll11111ll1l11l1Il1l1, l1ll1l11111l1lllIl1l1: ll1lll11l111llllIl1l1) -> bool:
        return True

    @classmethod
    def l1l1lll1llll1111Il1l1(l1lll1111l11l1llIl1l1) -> int:
        return 200


@dataclass(repr=False)
class lll111l1l1ll111lIl1l1(ll1l1l1ll11ll1l1Il1l1):
    l11llll1ll1l111lIl1l1: "Atomic" = field(init=False)

    lll1l11111ll111lIl1l1: bool = field(init=False, default=False)

    def l11l1lll11lll111Il1l1(lll11111ll1l11l1Il1l1) -> None:
        super().l11l1lll11lll111Il1l1()
        from django.db import transaction

        lll11111ll1l11l1Il1l1.l11llll1ll1l111lIl1l1 = transaction.atomic()
        lll11111ll1l11l1Il1l1.l11llll1ll1l111lIl1l1.__enter__()

    def l111l1llllll1l1lIl1l1(lll11111ll1l11l1Il1l1) -> None:
        super().l111l1llllll1l1lIl1l1()
        if (lll11111ll1l11l1Il1l1.lll1l11111ll111lIl1l1):
            return 

        lll11111ll1l11l1Il1l1.lll1l11111ll111lIl1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        lll11111ll1l11l1Il1l1.l11llll1ll1l111lIl1l1.__exit__(None, None, None)

    def ll11l1l111l11lllIl1l1(lll11111ll1l11l1Il1l1) -> None:
        super().ll11l1l111l11lllIl1l1()

        if (lll11111ll1l11l1Il1l1.lll1l11111ll111lIl1l1):
            return 

        lll11111ll1l11l1Il1l1.lll1l11111ll111lIl1l1 = True
        lll11111ll1l11l1Il1l1.l11llll1ll1l111lIl1l1.__exit__(None, None, None)

    def __repr__(lll11111ll1l11l1Il1l1) -> str:
        return 'DbMemento'


@dataclass(repr=False)
class l111lllll111111lIl1l1(l1l11llll111l11lIl1l1):
    l11llll1ll1l111lIl1l1: "Atomic" = field(init=False)

    lll1l11111ll111lIl1l1: bool = field(init=False, default=False)

    async def l11l1lll11lll111Il1l1(lll11111ll1l11l1Il1l1) -> None:
        await super().l11l1lll11lll111Il1l1()
        from django.db import transaction
        from asgiref.sync import sync_to_async

        lll11111ll1l11l1Il1l1.l11llll1ll1l111lIl1l1 = transaction.atomic()


        with l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l11lll1l111l11l1Il1l1.lll1llll1111l1l1Il1l1(False):
            await sync_to_async(lll11111ll1l11l1Il1l1.l11llll1ll1l111lIl1l1.__enter__)()

    async def l111l1llllll1l1lIl1l1(lll11111ll1l11l1Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().l111l1llllll1l1lIl1l1()
        if (lll11111ll1l11l1Il1l1.lll1l11111ll111lIl1l1):
            return 

        lll11111ll1l11l1Il1l1.lll1l11111ll111lIl1l1 = True
        from django.db import transaction

        def ll11lll1l1l1l111Il1l1() -> None:
            transaction.set_rollback(True)
            lll11111ll1l11l1Il1l1.l11llll1ll1l111lIl1l1.__exit__(None, None, None)
        with l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l11lll1l111l11l1Il1l1.lll1llll1111l1l1Il1l1(False):
            await sync_to_async(ll11lll1l1l1l111Il1l1)()

    async def ll11l1l111l11lllIl1l1(lll11111ll1l11l1Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().ll11l1l111l11lllIl1l1()

        if (lll11111ll1l11l1Il1l1.lll1l11111ll111lIl1l1):
            return 

        lll11111ll1l11l1Il1l1.lll1l11111ll111lIl1l1 = True
        with l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l11lll1l111l11l1Il1l1.lll1llll1111l1l1Il1l1(False):
            await sync_to_async(lll11111ll1l11l1Il1l1.l11llll1ll1l111lIl1l1.__exit__)(None, None, None)

    def __repr__(lll11111ll1l11l1Il1l1) -> str:
        return 'AsyncDbMemento'


@dataclass
class l1l11l1llll1l1llIl1l1(l1111l11l1ll11l1Il1l1):
    ll11ll111lll1l11Il1l1 = 'Django'

    l1l1ll1l1lll1l1lIl1l1: Optional[int] = field(init=False)
    l1l111111111l1l1Il1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    l1111lllll1l1111Il1l1: Any = field(init=False, default=None)
    ll11ll11l11111l1Il1l1: Any = field(init=False, default=None)
    llll11lll1lll1l1Il1l1: Any = field(init=False, default=None)

    ll111ll111llll1lIl1l1 = True

    def __post_init__(lll11111ll1l11l1Il1l1) -> None:
        super().__post_init__()
        lll11111ll1l11l1Il1l1.l1l1ll1l1lll1l1lIl1l1 = None

    def ll1l11lllll1l111Il1l1(lll11111ll1l11l1Il1l1) -> List[Type[ll1lll11l111llllIl1l1]]:
        return [l1l11lll11ll1l1lIl1l1]

    def l1ll1l1ll11111l1Il1l1(lll11111ll1l11l1Il1l1) -> None:
        super().l1ll1l1ll11111l1Il1l1()
        if ('runserver' in sys.argv):
            sys.argv.append('--noreload')

    def l1l1ll11l11l11llIl1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: types.ModuleType) -> None:
        if (lll11111ll1l11l1Il1l1.ll11llll111l11l1Il1l1(ll11l1l11llllll1Il1l1, 'django.core.management.commands.runserver')):
            lll11111ll1l11l1Il1l1.l1ll111l1lll1ll1Il1l1()
            if ( not lll11111ll1l11l1Il1l1.ll1l11lllll1111lIl1l1):
                lll11111ll1l11l1Il1l1.ll11ll1llll11ll1Il1l1()

    def ll1l1llll111l11lIl1l1(lll11111ll1l11l1Il1l1) -> None:
        import django.core.management.commands.runserver

        django.core.management.commands.runserver.Command.handle = lll11111ll1l11l1Il1l1.l1111lllll1l1111Il1l1
        django.core.management.commands.runserver.Command.get_handler = lll11111ll1l11l1Il1l1.llll11lll1lll1l1Il1l1
        django.core.handlers.base.BaseHandler.get_response = lll11111ll1l11l1Il1l1.ll11ll11l11111l1Il1l1

    def lll1l11ll111l111Il1l1(lll11111ll1l11l1Il1l1, ll11ll1l111111llIl1l1: str, l1lll1111llll1llIl1l1: bool) -> Optional["l1llll11llll1l11Il1l1"]:
        if (lll11111ll1l11l1Il1l1.ll1l11lllll1111lIl1l1):
            return None

        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        if (l1lll1111llll1llIl1l1):
            return None
        else:
            l1l1l11llll1llllIl1l1 = lll111l1l1ll111lIl1l1(ll11ll1l111111llIl1l1=ll11ll1l111111llIl1l1, l11111l1l111lll1Il1l1=lll11111ll1l11l1Il1l1)
            l1l1l11llll1llllIl1l1.l11l1lll11lll111Il1l1()

        return l1l1l11llll1llllIl1l1

    async def ll111lll11ll1111Il1l1(lll11111ll1l11l1Il1l1, ll11ll1l111111llIl1l1: str) -> Optional["ll1lll11111llll1Il1l1"]:
        if (lll11111ll1l11l1Il1l1.ll1l11lllll1111lIl1l1):
            return None

        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        l1l1l11llll1llllIl1l1 = l111lllll111111lIl1l1(ll11ll1l111111llIl1l1=ll11ll1l111111llIl1l1, l11111l1l111lll1Il1l1=lll11111ll1l11l1Il1l1)
        await l1l1l11llll1llllIl1l1.l11l1lll11lll111Il1l1()
        return l1l1l11llll1llllIl1l1

    def l1ll111l1lll1ll1Il1l1(lll11111ll1l11l1Il1l1) -> None:
        import django.core.management.commands.runserver

        lll11111ll1l11l1Il1l1.l1111lllll1l1111Il1l1 = django.core.management.commands.runserver.Command.handle

        def l1l11l111111lll1Il1l1(*l11lll1llllllll1Il1l1: Any, **l1l1lll11l1l1ll1Il1l1: Any) -> Any:
            with ll1111111lllll11Il1l1():
                lll11111llllllllIl1l1 = l1l1lll11l1l1ll1Il1l1.get('addrport')
                if ( not lll11111llllllllIl1l1):
                    lll11111llllllllIl1l1 = django.core.management.commands.runserver.Command.default_port

                lll11111llllllllIl1l1 = lll11111llllllllIl1l1.split(':')[ - 1]
                lll11111llllllllIl1l1 = int(lll11111llllllllIl1l1)
                lll11111ll1l11l1Il1l1.l1l1ll1l1lll1l1lIl1l1 = lll11111llllllllIl1l1

            return lll11111ll1l11l1Il1l1.l1111lllll1l1111Il1l1(*l11lll1llllllll1Il1l1, **l1l1lll11l1l1ll1Il1l1)

        ll1ll1l11ll11ll1Il1l1.l1111l11llll111lIl1l1(django.core.management.commands.runserver.Command, 'handle', l1l11l111111lll1Il1l1)

    def ll11ll1llll11ll1Il1l1(lll11111ll1l11l1Il1l1) -> None:
        import django.core.management.commands.runserver

        lll11111ll1l11l1Il1l1.llll11lll1lll1l1Il1l1 = django.core.management.commands.runserver.Command.get_handler

        def l1l11l111111lll1Il1l1(*l11lll1llllllll1Il1l1: Any, **l1l1lll11l1l1ll1Il1l1: Any) -> Any:
            with ll1111111lllll11Il1l1():
                assert lll11111ll1l11l1Il1l1.l1l1ll1l1lll1l1lIl1l1
                lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1 = lll11111ll1l11l1Il1l1.lll1ll11111l1111Il1l1(lll11111ll1l11l1Il1l1.l1l1ll1l1lll1l1lIl1l1)
                if (env.page_reload_on_start):
                    lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1.l1ll111l1lll11llIl1l1(2.0)

            return lll11111ll1l11l1Il1l1.llll11lll1lll1l1Il1l1(*l11lll1llllllll1Il1l1, **l1l1lll11l1l1ll1Il1l1)

        ll1ll1l11ll11ll1Il1l1.l1111l11llll111lIl1l1(django.core.management.commands.runserver.Command, 'get_handler', l1l11l111111lll1Il1l1)

    def lll1ll1l1111llllIl1l1(lll11111ll1l11l1Il1l1) -> None:
        super().lll1ll1l1111llllIl1l1()

        import django.core.handlers.base

        lll11111ll1l11l1Il1l1.ll11ll11l11111l1Il1l1 = django.core.handlers.base.BaseHandler.get_response

        def l1l11l111111lll1Il1l1(l11l1l1l1lll1lllIl1l1: Any, lll1l1l1l1ll11llIl1l1: Any) -> Any:
            l1111lllll111lllIl1l1 = lll11111ll1l11l1Il1l1.ll11ll11l11111l1Il1l1(l11l1l1l1lll1lllIl1l1, lll1l1l1l1ll11llIl1l1)

            if ( not lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1):
                return l1111lllll111lllIl1l1

            lll1l11ll1l1llllIl1l1 = l1111lllll111lllIl1l1.get('content-type')

            if (( not lll1l11ll1l1llllIl1l1 or 'text/html' not in lll1l11ll1l1llllIl1l1)):
                return l1111lllll111lllIl1l1

            llll11l1l1lll1l1Il1l1 = l1111lllll111lllIl1l1.content

            if (isinstance(llll11l1l1lll1l1Il1l1, bytes)):
                llll11l1l1lll1l1Il1l1 = llll11l1l1lll1l1Il1l1.decode('utf-8')

            l111lll111ll1lllIl1l1 = lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1.ll111l1ll1111l1lIl1l1(llll11l1l1lll1l1Il1l1)

            l1111lllll111lllIl1l1.content = l111lll111ll1lllIl1l1.encode('utf-8')
            l1111lllll111lllIl1l1['content-length'] = str(len(l1111lllll111lllIl1l1.content)).encode('ascii')
            return l1111lllll111lllIl1l1

        django.core.handlers.base.BaseHandler.get_response = l1l11l111111lll1Il1l1  # type: ignore

    def l111lll1l111111lIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path) -> None:
        super().l111lll1l111111lIl1l1(l1lllll1111l11l1Il1l1)

        from django.apps.registry import Apps

        lll11111ll1l11l1Il1l1.l1l111111111l1l1Il1l1 = Apps.register_model

        def l1l111l1l11l1111Il1l1(*l11lll1llllllll1Il1l1: Any, **l111l11lll11l111Il1l1: Any) -> Any:
            pass

        Apps.register_model = l1l111l1l11l1111Il1l1

    def llll111111llll1lIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path, ll1l11l1ll11l11lIl1l1: List[l1l111lll11llll1Il1l1]) -> None:
        super().llll111111llll1lIl1l1(l1lllll1111l11l1Il1l1, ll1l11l1ll11l11lIl1l1)

        if ( not lll11111ll1l11l1Il1l1.l1l111111111l1l1Il1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = lll11111ll1l11l1Il1l1.l1l111111111l1l1Il1l1
