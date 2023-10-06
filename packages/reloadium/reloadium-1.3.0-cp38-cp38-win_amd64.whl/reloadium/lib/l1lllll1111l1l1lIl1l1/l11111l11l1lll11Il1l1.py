from contextlib import contextmanager
from pathlib import Path
import sys
import types
from threading import Timer, Thread
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type, Set


import reloadium.lib.l1lllll1111l1l1lIl1l1.lllll11ll111l11lIl1l1
from reloadium.corium import l1l11ll1l1111lllIl1l1, l1l1l1lll11l1ll1Il1l1, l1l1ll1lll1111l1Il1l1
from reloadium.corium.l1llllll1ll1l11lIl1l1 import ll1llll1lllll11lIl1l1
from reloadium.corium.l11l1ll1l1111ll1Il1l1 import l1l11l11llll11llIl1l1, llll1ll1lll1l111Il1l1
from reloadium.corium.l1l1ll1lll1111l1Il1l1.l1lll1l1llll1111Il1l1 import llll1l11111l11llIl1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.ll1lll1111111l11Il1l1 import l1l11l1llll1l1llIl1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.l11111l1l111lll1Il1l1 import l1l1l11l11l11111Il1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.l1lll1111llll1l1Il1l1 import lll11111l1l1llllIl1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.ll111l11llll1l1lIl1l1 import ll11l1ll1l1llll1Il1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.ll1l1l1111lllll1Il1l1 import ll11l1l11ll1ll11Il1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.l1lllll11llllll1Il1l1 import l11l11ll1l11111lIl1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.ll1ll1llllll11llIl1l1 import lllll1lll11111l1Il1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.lll11ll1l11111llIl1l1 import l1llll11l1ll1l11Il1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.lll11l111ll111llIl1l1 import ll1ll1lll111ll11Il1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.l11ll1111111lll1Il1l1 import l111111ll1111lllIl1l1
from reloadium.corium.ll1ll1l11lllllllIl1l1 import ll1ll1l11lllllllIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.corium.l1l11l111l1ll1llIl1l1 import lll111llll1l1lllIl1l1
    from reloadium.corium.ll11111llll11ll1Il1l1 import l1l111lll11llll1Il1l1


__RELOADIUM__ = True

l1l111llllll11l1Il1l1 = ll1ll1l11lllllllIl1l1.l111ll1l1111l11lIl1l1(__name__)


@dataclass
class ll1l1l11lll11lllIl1l1:
    l1l11l111l1ll1llIl1l1: "lll111llll1l1lllIl1l1"

    l1lllll1111l1l1lIl1l1: List[l1l1l11l11l11111Il1l1] = field(init=False, default_factory=list)

    lll11llll11l111lIl1l1: List[types.ModuleType] = field(init=False, default_factory=list)

    llll1llll1111ll1Il1l1: List[Type[l1l1l11l11l11111Il1l1]] = field(init=False, default_factory=lambda :[ll11l1ll1l1llll1Il1l1, l11l11ll1l11111lIl1l1, l1l11l1llll1l1llIl1l1, ll1ll1lll111ll11Il1l1, lllll1lll11111l1Il1l1, ll11l1l11ll1ll11Il1l1, l1llll11l1ll1l11Il1l1, l111111ll1111lllIl1l1, lll11111l1l1llllIl1l1])




    l1l1ll1llll11ll1Il1l1: List[Type[l1l1l11l11l11111Il1l1]] = field(init=False, default_factory=list)
    ll11ll11lll111llIl1l1 = 5

    def __post_init__(lll11111ll1l11l1Il1l1) -> None:
        if (ll1llll1lllll11lIl1l1().l111l1l1lll1llllIl1l1.l1lll1111lll111lIl1l1):
            lll11111ll1l11l1Il1l1.llll1llll1111ll1Il1l1.remove(l1llll11l1ll1l11Il1l1)

        llll1l11111l11llIl1l1(l1l1l1111ll11lllIl1l1=lll11111ll1l11l1Il1l1.ll1111ll1111l1l1Il1l1, ll11ll1l111111llIl1l1='show-forbidden-dialog').start()

    def ll1111ll1111l1l1Il1l1(lll11111ll1l11l1Il1l1) -> None:
        l1l1ll1lll1111l1Il1l1.ll1ll1l11ll11ll1Il1l1.ll11l1ll1lll1111Il1l1(lll11111ll1l11l1Il1l1.ll11ll11lll111llIl1l1)

        lll11111ll1l11l1Il1l1.l1l11l111l1ll1llIl1l1.lll1ll111llllll1Il1l1.l1111l1l1l1l11llIl1l1()

        if ( not lll11111ll1l11l1Il1l1.l1l1ll1llll11ll1Il1l1):
            return 

        l1lllll1111l1l1lIl1l1 = [l1ll1l1l11ll1ll1Il1l1.ll11ll111lll1l11Il1l1 for l1ll1l1l11ll1ll1Il1l1 in lll11111ll1l11l1Il1l1.l1l1ll1llll11ll1Il1l1]
        lll11111ll1l11l1Il1l1.l1l11l111l1ll1llIl1l1.l1lll1111llll11lIl1l1.llllll1l1l1llll1Il1l1(llll1ll1lll1l111Il1l1.l11111l11l111l1lIl1l1, l1l1l1lll11l1ll1Il1l1.ll1l11lll1l1l11lIl1l1.l11l11l1l111llllIl1l1(l1lllll1111l1l1lIl1l1), 
ll1lll1ll111lll1Il1l1='')

    def l1ll1l1l1l1l1lllIl1l1(lll11111ll1l11l1Il1l1, ll11l1ll1111l1llIl1l1: types.ModuleType) -> None:
        for ll1l11ll11l11l11Il1l1 in lll11111ll1l11l1Il1l1.llll1llll1111ll1Il1l1.copy():
            if (ll1l11ll11l11l11Il1l1.l1111l111l1lll11Il1l1(ll11l1ll1111l1llIl1l1)):
                if (( not ll1l11ll11l11l11Il1l1.ll111ll111llll1lIl1l1 and lll11111ll1l11l1Il1l1.l1l11l111l1ll1llIl1l1.l1lll1111llll11lIl1l1.l11l1ll1l1111ll1Il1l1.lllll1111l111l11Il1l1([ll1l11ll11l11l11Il1l1.ll11ll111lll1l11Il1l1]) is False)):
                    lll11111ll1l11l1Il1l1.l1l1ll1llll11ll1Il1l1.append(ll1l11ll11l11l11Il1l1)
                    lll11111ll1l11l1Il1l1.llll1llll1111ll1Il1l1.remove(ll1l11ll11l11l11Il1l1)
                    continue
                lll11111ll1l11l1Il1l1.l1l1111l11lll11lIl1l1(ll1l11ll11l11l11Il1l1)

        if (ll11l1ll1111l1llIl1l1 in lll11111ll1l11l1Il1l1.lll11llll11l111lIl1l1):
            return 

        for l1ll11lll1l1ll11Il1l1 in lll11111ll1l11l1Il1l1.l1lllll1111l1l1lIl1l1.copy():
            l1ll11lll1l1ll11Il1l1.l1l1ll11l11l11llIl1l1(ll11l1ll1111l1llIl1l1)

        lll11111ll1l11l1Il1l1.lll11llll11l111lIl1l1.append(ll11l1ll1111l1llIl1l1)

    def l1l1111l11lll11lIl1l1(lll11111ll1l11l1Il1l1, ll1l11ll11l11l11Il1l1: Type[l1l1l11l11l11111Il1l1]) -> None:
        ll111111111l1l1lIl1l1 = ll1l11ll11l11l11Il1l1(lll11111ll1l11l1Il1l1, lll11111ll1l11l1Il1l1.l1l11l111l1ll1llIl1l1.l1lll1111llll11lIl1l1.l11l1ll1l1111ll1Il1l1)

        lll11111ll1l11l1Il1l1.l1l11l111l1ll1llIl1l1.ll1lllll1ll1l11lIl1l1.lll1l1l1ll111111Il1l1.l111l111lll11ll1Il1l1(l1l11ll1l1111lllIl1l1.l1111111llll11llIl1l1(ll111111111l1l1lIl1l1))
        ll111111111l1l1lIl1l1.l1ll1l1ll11111l1Il1l1()
        lll11111ll1l11l1Il1l1.l1lllll1111l1l1lIl1l1.append(ll111111111l1l1lIl1l1)

        if (ll1l11ll11l11l11Il1l1 in lll11111ll1l11l1Il1l1.llll1llll1111ll1Il1l1):
            lll11111ll1l11l1Il1l1.llll1llll1111ll1Il1l1.remove(ll1l11ll11l11l11Il1l1)

    @contextmanager
    def ll1l11ll1l1l1l11Il1l1(lll11111ll1l11l1Il1l1) -> Generator[None, None, None]:
        l11l1l1l11lll11lIl1l1 = [l1ll11lll1l1ll11Il1l1.ll1l11ll1l1l1l11Il1l1() for l1ll11lll1l1ll11Il1l1 in lll11111ll1l11l1Il1l1.l1lllll1111l1l1lIl1l1.copy()]

        for l111lllll1l1l1l1Il1l1 in l11l1l1l11lll11lIl1l1:
            l111lllll1l1l1l1Il1l1.__enter__()

        yield 

        for l111lllll1l1l1l1Il1l1 in l11l1l1l11lll11lIl1l1:
            l111lllll1l1l1l1Il1l1.__exit__(*sys.exc_info())

    def l111lll1l111111lIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path) -> None:
        for l1ll11lll1l1ll11Il1l1 in lll11111ll1l11l1Il1l1.l1lllll1111l1l1lIl1l1.copy():
            l1ll11lll1l1ll11Il1l1.l111lll1l111111lIl1l1(l1lllll1111l11l1Il1l1)

    def l1l1l1lll1lll1llIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path) -> None:
        for l1ll11lll1l1ll11Il1l1 in lll11111ll1l11l1Il1l1.l1lllll1111l1l1lIl1l1.copy():
            l1ll11lll1l1ll11Il1l1.l1l1l1lll1lll1llIl1l1(l1lllll1111l11l1Il1l1)

    def ll1l11l1ll1ll1llIl1l1(lll11111ll1l11l1Il1l1, l111l1ll11l11111Il1l1: Exception) -> None:
        for l1ll11lll1l1ll11Il1l1 in lll11111ll1l11l1Il1l1.l1lllll1111l1l1lIl1l1.copy():
            l1ll11lll1l1ll11Il1l1.ll1l11l1ll1ll1llIl1l1(l111l1ll11l11111Il1l1)

    def llll111111llll1lIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path, ll1l11l1ll11l11lIl1l1: List["l1l111lll11llll1Il1l1"]) -> None:
        for l1ll11lll1l1ll11Il1l1 in lll11111ll1l11l1Il1l1.l1lllll1111l1l1lIl1l1.copy():
            l1ll11lll1l1ll11Il1l1.llll111111llll1lIl1l1(l1lllll1111l11l1Il1l1, ll1l11l1ll11l11lIl1l1)

    def l1l11ll1l1ll1l1lIl1l1(lll11111ll1l11l1Il1l1) -> None:
        lll11111ll1l11l1Il1l1.l1lllll1111l1l1lIl1l1.clear()
