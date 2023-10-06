import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.l1ll111lll1l1lllIl1l1 import ll1111111lllll11Il1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.l11111l1l111lll1Il1l1 import l1l1l11l11l11111Il1l1, ll1l1l1ll11ll1l1Il1l1
from reloadium.corium.ll1ll11ll111l111Il1l1 import l1llll11llll1l11Il1l1
from reloadium.corium.l1l1ll1lll1111l1Il1l1 import ll1ll1l11ll11ll1Il1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session


__RELOADIUM__ = True


@dataclass(repr=False)
class lll111l1l1ll111lIl1l1(ll1l1l1ll11ll1l1Il1l1):
    l11111l1l111lll1Il1l1: "ll1ll1lll111ll11Il1l1"
    ll11l11l1ll111llIl1l1: List["Transaction"] = field(init=False, default_factory=list)

    def l11l1lll11lll111Il1l1(lll11111ll1l11l1Il1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().l11l1lll11lll111Il1l1()

        l1l1l1ll1ll11lllIl1l1 = list(_sessions.values())

        for ll111111l1l1l11lIl1l1 in l1l1l1ll1ll11lllIl1l1:
            if ( not ll111111l1l1l11lIl1l1.is_active):
                continue

            l11l111l11l11lllIl1l1 = ll111111l1l1l11lIl1l1.begin_nested()
            lll11111ll1l11l1Il1l1.ll11l11l1ll111llIl1l1.append(l11l111l11l11lllIl1l1)

    def __repr__(lll11111ll1l11l1Il1l1) -> str:
        return 'DbMemento'

    def l111l1llllll1l1lIl1l1(lll11111ll1l11l1Il1l1) -> None:
        super().l111l1llllll1l1lIl1l1()

        while lll11111ll1l11l1Il1l1.ll11l11l1ll111llIl1l1:
            l11l111l11l11lllIl1l1 = lll11111ll1l11l1Il1l1.ll11l11l1ll111llIl1l1.pop()
            if (l11l111l11l11lllIl1l1.is_active):
                try:
                    l11l111l11l11lllIl1l1.rollback()
                except :
                    pass

    def ll11l1l111l11lllIl1l1(lll11111ll1l11l1Il1l1) -> None:
        super().ll11l1l111l11lllIl1l1()

        while lll11111ll1l11l1Il1l1.ll11l11l1ll111llIl1l1:
            l11l111l11l11lllIl1l1 = lll11111ll1l11l1Il1l1.ll11l11l1ll111llIl1l1.pop()
            if (l11l111l11l11lllIl1l1.is_active):
                try:
                    l11l111l11l11lllIl1l1.commit()
                except :
                    pass


@dataclass
class ll1ll1lll111ll11Il1l1(l1l1l11l11l11111Il1l1):
    ll11ll111lll1l11Il1l1 = 'Sqlalchemy'

    l1l1l1ll11lll111Il1l1: List["Engine"] = field(init=False, default_factory=list)
    l1l1l1ll1ll11lllIl1l1: Set["Session"] = field(init=False, default_factory=set)
    l1111l1l1l11l111Il1l1: Tuple[int, ...] = field(init=False)

    def l1l1ll11l11l11llIl1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: types.ModuleType) -> None:
        if (lll11111ll1l11l1Il1l1.ll11llll111l11l1Il1l1(ll11l1l11llllll1Il1l1, 'sqlalchemy')):
            lll11111ll1l11l1Il1l1.l11l1111llllll11Il1l1(ll11l1l11llllll1Il1l1)

        if (lll11111ll1l11l1Il1l1.ll11llll111l11l1Il1l1(ll11l1l11llllll1Il1l1, 'sqlalchemy.engine.base')):
            lll11111ll1l11l1Il1l1.l1l1l111l111l11lIl1l1(ll11l1l11llllll1Il1l1)

    def l11l1111llllll11Il1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: Any) -> None:
        llll11l1l1lll1l1Il1l1 = Path(ll11l1l11llllll1Il1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', llll11l1l1lll1l1Il1l1)[0]

        ll1111ll11lll11lIl1l1 = [int(l111l111lll1l11lIl1l1) for l111l111lll1l11lIl1l1 in __version__.split('.')]
        lll11111ll1l11l1Il1l1.l1111l1l1l11l111Il1l1 = tuple(ll1111ll11lll11lIl1l1)

    def lll1l11ll111l111Il1l1(lll11111ll1l11l1Il1l1, ll11ll1l111111llIl1l1: str, l1lll1111llll1llIl1l1: bool) -> Optional["l1llll11llll1l11Il1l1"]:
        l1l1l11llll1llllIl1l1 = lll111l1l1ll111lIl1l1(ll11ll1l111111llIl1l1=ll11ll1l111111llIl1l1, l11111l1l111lll1Il1l1=lll11111ll1l11l1Il1l1)
        l1l1l11llll1llllIl1l1.l11l1lll11lll111Il1l1()
        return l1l1l11llll1llllIl1l1

    def l1l1l111l111l11lIl1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: Any) -> None:
        l111lll1lll1lll1Il1l1 = locals().copy()

        l111lll1lll1lll1Il1l1.update({'original': ll11l1l11llllll1Il1l1.Engine.__init__, 'reloader_code': ll1111111lllll11Il1l1, 'engines': lll11111ll1l11l1Il1l1.l1l1l1ll11lll111Il1l1})





        ll1l1lll11lll1llIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        l1l1l111lll11l11Il1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (lll11111ll1l11l1Il1l1.l1111l1l1l11l111Il1l1 <= (1, 3, 24, )):
            exec(ll1l1lll11lll1llIl1l1, {**globals(), **l111lll1lll1lll1Il1l1}, l111lll1lll1lll1Il1l1)
        else:
            exec(l1l1l111lll11l11Il1l1, {**globals(), **l111lll1lll1lll1Il1l1}, l111lll1lll1lll1Il1l1)

        ll1ll1l11ll11ll1Il1l1.l1111l11llll111lIl1l1(ll11l1l11llllll1Il1l1.Engine, '__init__', l111lll1lll1lll1Il1l1['patched'])
