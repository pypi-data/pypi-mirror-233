from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import l1l1l1lll11l1ll1Il1l1, l1ll111lll1l1lllIl1l1, public, lll11ll11l1lllllIl1l1, l1l1ll1lll1111l1Il1l1
from reloadium.corium.l1l11lll111lllllIl1l1 import lllll1111l11l1l1Il1l1, ll1l1l11l1l1111lIl1l1
from reloadium.corium.l1ll111lll1l1lllIl1l1 import l11l1llll1111lllIl1l1, ll1111111lllll11Il1l1, lll1111l1llll11lIl1l1
from reloadium.corium.ll1l111ll11lllllIl1l1 import l11l11llll111l11Il1l1
from reloadium.corium.ll1ll1l11lllllllIl1l1 import ll1ll1l11lllllllIl1l1
from reloadium.corium.ll11lll111l11l1lIl1l1 import l111lll11llll1llIl1l1
from reloadium.corium.ll1ll11ll111l111Il1l1 import l1llll11llll1l11Il1l1, ll1lll11111llll1Il1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['l1111ll1l1111lllIl1l1', 'l1l11ll1l1111111Il1l1', 'lll1111lll1l1111Il1l1']


l1l111llllll11l1Il1l1 = ll1ll1l11lllllllIl1l1.l111ll1l1111l11lIl1l1(__name__)


class l1111ll1l1111lllIl1l1:
    @classmethod
    def ll1lllllll1lll11Il1l1(lll11111ll1l11l1Il1l1) -> Optional[FrameType]:
        llll11llll11l1l1Il1l1: FrameType = sys._getframe(2)
        l1l1l11llll1llllIl1l1 = next(l1l1ll1lll1111l1Il1l1.llll11llll11l1l1Il1l1.lll1l1l11l1lll11Il1l1(llll11llll11l1l1Il1l1))
        return l1l1l11llll1llllIl1l1


class l1l11ll1l1111111Il1l1(l1111ll1l1111lllIl1l1):
    @classmethod
    def l11l11l11111l11lIl1l1(l1lll1111l11l1llIl1l1, l11lll1llllllll1Il1l1: List[Any], l111l11lll11l111Il1l1: Dict[str, Any], lllll1l1l1l1l11lIl1l1: List[l1llll11llll1l11Il1l1]) -> Any:  # type: ignore
        with ll1111111lllll11Il1l1():
            assert l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l1ll1111lll1l1llIl1l1
            llll11llll11l1l1Il1l1 = l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l1ll1111lll1l1llIl1l1.ll11l11lll1l11l1Il1l1.l111llll11111l1lIl1l1()
            llll11llll11l1l1Il1l1.lllllll1llll1111Il1l1()

            llll111lll1111llIl1l1 = l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l1lll1l11lll111lIl1l1.l1ll11llll1111l1Il1l1(llll11llll11l1l1Il1l1.ll1llll1111l1lllIl1l1, llll11llll11l1l1Il1l1.llll1l1111llll1lIl1l1.l111llll1l111ll1Il1l1())
            assert llll111lll1111llIl1l1
            lll1ll111l111l1lIl1l1 = l1lll1111l11l1llIl1l1.ll1lllllll1lll11Il1l1()

            for l111ll1l11l111llIl1l1 in lllll1l1l1l1l11lIl1l1:
                l111ll1l11l111llIl1l1.l111l1llllll1l1lIl1l1()

            for l111ll1l11l111llIl1l1 in lllll1l1l1l1l11lIl1l1:
                l111ll1l11l111llIl1l1.ll11l1l111l11lllIl1l1()


        l1l1l11llll1llllIl1l1 = llll111lll1111llIl1l1(*l11lll1llllllll1Il1l1, **l111l11lll11l111Il1l1);        llll11llll11l1l1Il1l1.l1lll1l1llll1111Il1l1.additional_info.pydev_step_stop = lll1ll111l111l1lIl1l1  # type: ignore

        return l1l1l11llll1llllIl1l1

    @classmethod
    async def ll1ll11lll1l1ll1Il1l1(l1lll1111l11l1llIl1l1, l11lll1llllllll1Il1l1: List[Any], l111l11lll11l111Il1l1: Dict[str, Any], lllll1l1l1l1l11lIl1l1: List[ll1lll11111llll1Il1l1]) -> Any:  # type: ignore
        with ll1111111lllll11Il1l1():
            assert l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l1ll1111lll1l1llIl1l1
            llll11llll11l1l1Il1l1 = l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l1ll1111lll1l1llIl1l1.ll11l11lll1l11l1Il1l1.l111llll11111l1lIl1l1()
            llll11llll11l1l1Il1l1.lllllll1llll1111Il1l1()

            llll111lll1111llIl1l1 = l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l1lll1l11lll111lIl1l1.l1ll11llll1111l1Il1l1(llll11llll11l1l1Il1l1.ll1llll1111l1lllIl1l1, llll11llll11l1l1Il1l1.llll1l1111llll1lIl1l1.l111llll1l111ll1Il1l1())
            assert llll111lll1111llIl1l1
            lll1ll111l111l1lIl1l1 = l1lll1111l11l1llIl1l1.ll1lllllll1lll11Il1l1()

            for l111ll1l11l111llIl1l1 in lllll1l1l1l1l11lIl1l1:
                await l111ll1l11l111llIl1l1.l111l1llllll1l1lIl1l1()

            for l111ll1l11l111llIl1l1 in lllll1l1l1l1l11lIl1l1:
                await l111ll1l11l111llIl1l1.ll11l1l111l11lllIl1l1()


        l1l1l11llll1llllIl1l1 = await llll111lll1111llIl1l1(*l11lll1llllllll1Il1l1, **l111l11lll11l111Il1l1);        llll11llll11l1l1Il1l1.l1lll1l1llll1111Il1l1.additional_info.pydev_step_stop = lll1ll111l111l1lIl1l1  # type: ignore

        return l1l1l11llll1llllIl1l1


class lll1111lll1l1111Il1l1(l1111ll1l1111lllIl1l1):
    @classmethod
    def l11l11l11111l11lIl1l1(l1lll1111l11l1llIl1l1) -> Optional[ModuleType]:  # type: ignore
        with ll1111111lllll11Il1l1():
            assert l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l1ll1111lll1l1llIl1l1
            llll11llll11l1l1Il1l1 = l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.l1ll1111lll1l1llIl1l1.ll11l11lll1l11l1Il1l1.l111llll11111l1lIl1l1()

            l1111ll1l1l1l1l1Il1l1 = Path(llll11llll11l1l1Il1l1.llllll1111lll1llIl1l1.f_globals['__spec__'].origin).absolute()
            ll1ll111lllll11lIl1l1 = llll11llll11l1l1Il1l1.llllll1111lll1llIl1l1.f_globals['__name__']
            llll11llll11l1l1Il1l1.lllllll1llll1111Il1l1()
            l1111l1lllll1l1lIl1l1 = l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.llll1l1l11l1111lIl1l1.l11l11ll111ll11lIl1l1(l1111ll1l1l1l1l1Il1l1)

            if ( not l1111l1lllll1l1lIl1l1):
                l1l111llllll11l1Il1l1.ll111l111l111l11Il1l1('Could not retrieve src.', llllll1111111l1lIl1l1={'file': l111lll11llll1llIl1l1.l1lllll1111l11l1Il1l1(l1111ll1l1l1l1l1Il1l1), 
'fullname': l111lll11llll1llIl1l1.ll1ll111lllll11lIl1l1(ll1ll111lllll11lIl1l1)})

            assert l1111l1lllll1l1lIl1l1

        try:
            l1111l1lllll1l1lIl1l1.l11l1l111ll11l1lIl1l1()
            l1111l1lllll1l1lIl1l1.l111l111ll1l111lIl1l1(ll11lll11ll11ll1Il1l1=False)
            l1111l1lllll1l1lIl1l1.l11l1ll11111l111Il1l1(ll11lll11ll11ll1Il1l1=False)
        except l11l1llll1111lllIl1l1 as l1ll1l1l11ll1ll1Il1l1:
            llll11llll11l1l1Il1l1.l1ll1l1lll11lll1Il1l1(l1ll1l1l11ll1ll1Il1l1)
            return None

        import importlib.util

        l11l1111lll1l111Il1l1 = llll11llll11l1l1Il1l1.llllll1111lll1llIl1l1.f_locals['__spec__']
        ll11l1l11llllll1Il1l1 = importlib.util.module_from_spec(l11l1111lll1l111Il1l1)

        l1111l1lllll1l1lIl1l1.ll1lllll1l11l111Il1l1(ll11l1l11llllll1Il1l1)
        return ll11l1l11llllll1Il1l1


ll1l1l11l1l1111lIl1l1.l111lll1l1ll11l1Il1l1(lllll1111l11l1l1Il1l1.ll1l11l11l1llll1Il1l1, l1l11ll1l1111111Il1l1.l11l11l11111l11lIl1l1)
ll1l1l11l1l1111lIl1l1.l111lll1l1ll11l1Il1l1(lllll1111l11l1l1Il1l1.l11l111l1l11l1llIl1l1, l1l11ll1l1111111Il1l1.ll1ll11lll1l1ll1Il1l1)
ll1l1l11l1l1111lIl1l1.l111lll1l1ll11l1Il1l1(lllll1111l11l1l1Il1l1.ll111ll1l1l111l1Il1l1, lll1111lll1l1111Il1l1.l11l11l11111l11lIl1l1)
