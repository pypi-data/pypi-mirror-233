from abc import ABC
from contextlib import contextmanager
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.l11l1ll1l1111ll1Il1l1 import l1l11l11llll11llIl1l1, llll11111l111l11Il1l1
from reloadium.corium.ll1ll1l11lllllllIl1l1 import ll1llll1l1lll1llIl1l1, ll1ll1l11lllllllIl1l1
from reloadium.corium.ll11111llll11ll1Il1l1 import l1l111lll11llll1Il1l1, ll1lll11l111llllIl1l1
from reloadium.corium.ll1ll11ll111l111Il1l1 import l1llll11llll1l11Il1l1, ll1lll11111llll1Il1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.lib.l1lllll1111l1l1lIl1l1.l11111l11l1lll11Il1l1 import ll1l1l11lll11lllIl1l1


__RELOADIUM__ = True

l1l111llllll11l1Il1l1 = ll1ll1l11lllllllIl1l1.l111ll1l1111l11lIl1l1(__name__)


@dataclass
class l1l1l11l11l11111Il1l1:
    l11111l11l1lll11Il1l1: "ll1l1l11lll11lllIl1l1"
    l11l1ll1l1111ll1Il1l1: l1l11l11llll11llIl1l1

    ll11ll111lll1l11Il1l1: ClassVar[str] = NotImplemented
    lll1ll1111l1111lIl1l1: bool = field(init=False, default=False)

    ll1l1l11l1ll11l1Il1l1: ll1llll1l1lll1llIl1l1 = field(init=False)

    ll1l11lllll1111lIl1l1: bool = field(init=False, default=False)

    ll111ll111llll1lIl1l1 = False

    def __post_init__(lll11111ll1l11l1Il1l1) -> None:
        lll11111ll1l11l1Il1l1.ll1l1l11l1ll11l1Il1l1 = ll1ll1l11lllllllIl1l1.l111ll1l1111l11lIl1l1(lll11111ll1l11l1Il1l1.ll11ll111lll1l11Il1l1)
        lll11111ll1l11l1Il1l1.ll1l1l11l1ll11l1Il1l1.ll11llllll1l11llIl1l1('Creating extension')
        lll11111ll1l11l1Il1l1.l11111l11l1lll11Il1l1.l1l11l111l1ll1llIl1l1.llll11ll11l11lllIl1l1.l11lll1111ll11l1Il1l1(lll11111ll1l11l1Il1l1.ll1llll1l11l1lllIl1l1())
        lll11111ll1l11l1Il1l1.ll1l11lllll1111lIl1l1 = isinstance(lll11111ll1l11l1Il1l1.l11l1ll1l1111ll1Il1l1, llll11111l111l11Il1l1)

    def ll1llll1l11l1lllIl1l1(lll11111ll1l11l1Il1l1) -> List[Type[ll1lll11l111llllIl1l1]]:
        l1l1l11llll1llllIl1l1 = []
        ll11111llll11ll1Il1l1 = lll11111ll1l11l1Il1l1.ll1l11lllll1l111Il1l1()
        for ll1l11l111ll11llIl1l1 in ll11111llll11ll1Il1l1:
            ll1l11l111ll11llIl1l1.l11ll11l1ll1l11lIl1l1 = lll11111ll1l11l1Il1l1.ll11ll111lll1l11Il1l1

        l1l1l11llll1llllIl1l1.extend(ll11111llll11ll1Il1l1)
        return l1l1l11llll1llllIl1l1

    def l1l1lll11l1lll11Il1l1(lll11111ll1l11l1Il1l1) -> None:
        lll11111ll1l11l1Il1l1.lll1ll1111l1111lIl1l1 = True

    def l1l1ll11l11l11llIl1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: types.ModuleType) -> None:
        pass

    @classmethod
    def l1111l111l1lll11Il1l1(l1lll1111l11l1llIl1l1, ll11l1l11llllll1Il1l1: types.ModuleType) -> bool:
        if ( not hasattr(ll11l1l11llllll1Il1l1, '__name__')):
            return False

        l1l1l11llll1llllIl1l1 = ll11l1l11llllll1Il1l1.__name__.split('.')[0].lower() == l1lll1111l11l1llIl1l1.ll11ll111lll1l11Il1l1.lower()
        return l1l1l11llll1llllIl1l1

    def ll1l1llll111l11lIl1l1(lll11111ll1l11l1Il1l1) -> None:
        l1l111llllll11l1Il1l1.ll11llllll1l11llIl1l1(''.join(['Disabling extension ', '{:{}}'.format(lll11111ll1l11l1Il1l1.ll11ll111lll1l11Il1l1, '')]))

    @contextmanager
    def ll1l11ll1l1l1l11Il1l1(lll11111ll1l11l1Il1l1) -> Generator[None, None, None]:
        yield 

    def l1ll1l1ll11111l1Il1l1(lll11111ll1l11l1Il1l1) -> None:
        pass

    def ll1l11l1ll1ll1llIl1l1(lll11111ll1l11l1Il1l1, l111l1ll11l11111Il1l1: Exception) -> None:
        pass

    def lll1l11ll111l111Il1l1(lll11111ll1l11l1Il1l1, ll11ll1l111111llIl1l1: str, l1lll1111llll1llIl1l1: bool) -> Optional[l1llll11llll1l11Il1l1]:
        return None

    async def ll111lll11ll1111Il1l1(lll11111ll1l11l1Il1l1, ll11ll1l111111llIl1l1: str) -> Optional[ll1lll11111llll1Il1l1]:
        return None

    def ll1ll1111l111lllIl1l1(lll11111ll1l11l1Il1l1, ll11ll1l111111llIl1l1: str) -> Optional[l1llll11llll1l11Il1l1]:
        return None

    async def l1111lll1ll1ll11Il1l1(lll11111ll1l11l1Il1l1, ll11ll1l111111llIl1l1: str) -> Optional[ll1lll11111llll1Il1l1]:
        return None

    def l1l1l1lll1lll1llIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path) -> None:
        pass

    def l111lll1l111111lIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path) -> None:
        pass

    def llll111111llll1lIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path, ll1l11l1ll11l11lIl1l1: List[l1l111lll11llll1Il1l1]) -> None:
        pass

    def __eq__(lll11111ll1l11l1Il1l1, lllllll1l11ll11lIl1l1: Any) -> bool:
        return id(lllllll1l11ll11lIl1l1) == id(lll11111ll1l11l1Il1l1)

    def ll1l11lllll1l111Il1l1(lll11111ll1l11l1Il1l1) -> List[Type[ll1lll11l111llllIl1l1]]:
        return []

    def ll11llll111l11l1Il1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: types.ModuleType, ll11ll1l111111llIl1l1: str) -> bool:
        l1l1l11llll1llllIl1l1 = (hasattr(ll11l1l11llllll1Il1l1, '__name__') and ll11l1l11llllll1Il1l1.__name__ == ll11ll1l111111llIl1l1)
        return l1l1l11llll1llllIl1l1


@dataclass(repr=False)
class ll1l1l1ll11ll1l1Il1l1(l1llll11llll1l11Il1l1):
    l11111l1l111lll1Il1l1: l1l1l11l11l11111Il1l1

    def __repr__(lll11111ll1l11l1Il1l1) -> str:
        return 'ExtensionMemento'


@dataclass(repr=False)
class l1l11llll111l11lIl1l1(ll1lll11111llll1Il1l1):
    l11111l1l111lll1Il1l1: l1l1l11l11l11111Il1l1

    def __repr__(lll11111ll1l11l1Il1l1) -> str:
        return 'AsyncExtensionMemento'
