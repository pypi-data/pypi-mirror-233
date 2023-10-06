import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.lib.l1lllll1111l1l1lIl1l1.l11111l1l111lll1Il1l1 import l1l1l11l11l11111Il1l1
from reloadium.lib import l11l1llll1ll1lllIl1l1

from dataclasses import dataclass

if (TYPE_CHECKING):
    ...


__RELOADIUM__ = True


@dataclass
class l111111ll1111lllIl1l1(l1l1l11l11l11111Il1l1):
    ll11ll111lll1l11Il1l1 = 'Multiprocessing'

    ll111ll111llll1lIl1l1 = True

    def __post_init__(lll11111ll1l11l1Il1l1) -> None:
        super().__post_init__()

    def l1l1ll11l11l11llIl1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: types.ModuleType) -> None:
        if (lll11111ll1l11l1Il1l1.ll11llll111l11l1Il1l1(ll11l1l11llllll1Il1l1, 'multiprocessing.popen_spawn_posix')):
            lll11111ll1l11l1Il1l1.l1l11ll1l111l11lIl1l1(ll11l1l11llllll1Il1l1)

        if (lll11111ll1l11l1Il1l1.ll11llll111l11l1Il1l1(ll11l1l11llllll1Il1l1, 'multiprocessing.popen_spawn_win32')):
            lll11111ll1l11l1Il1l1.lll1l111llll1111Il1l1(ll11l1l11llllll1Il1l1)

    def l1l11ll1l111l11lIl1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = l11l1llll1ll1lllIl1l1.l11ll1111111lll1Il1l1.l1ll1l1l1l1l11llIl1l1  # type: ignore

    def lll1l111llll1111Il1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = l11l1llll1ll1lllIl1l1.l11ll1111111lll1Il1l1.__init__  # type: ignore
