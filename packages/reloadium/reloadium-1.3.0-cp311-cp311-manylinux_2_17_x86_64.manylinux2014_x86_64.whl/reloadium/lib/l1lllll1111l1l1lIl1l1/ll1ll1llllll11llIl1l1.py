from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.l1lllll1111l1l1lIl1l1.l11111l1l111lll1Il1l1 import l1l1l11l11l11111Il1l1
from reloadium.corium.ll11111llll11ll1Il1l1 import l1l111lll11llll1Il1l1
from reloadium.corium.l1l1ll1lll1111l1Il1l1 import ll1ll1l11ll11ll1Il1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class lllll1lll11111l1Il1l1(l1l1l11l11l11111Il1l1):
    ll11ll111lll1l11Il1l1 = 'PyGame'

    ll111ll111llll1lIl1l1 = True

    l1111l11llll11llIl1l1: bool = field(init=False, default=False)

    def l1l1ll11l11l11llIl1l1(lll11111ll1l11l1Il1l1, l1l11111111ll1llIl1l1: types.ModuleType) -> None:
        if (lll11111ll1l11l1Il1l1.ll11llll111l11l1Il1l1(l1l11111111ll1llIl1l1, 'pygame.base')):
            lll11111ll1l11l1Il1l1.ll11111111lll1llIl1l1()

    def ll11111111lll1llIl1l1(lll11111ll1l11l1Il1l1) -> None:
        import pygame.display

        l11ll1llll11l111Il1l1 = pygame.display.update

        def l1l1llll111l1l1lIl1l1(*l11lll1llllllll1Il1l1: Any, **l111l11lll11l111Il1l1: Any) -> None:
            if (lll11111ll1l11l1Il1l1.l1111l11llll11llIl1l1):
                ll1ll1l11ll11ll1Il1l1.ll11l1ll1lll1111Il1l1(0.1)
                return None
            else:
                return l11ll1llll11l111Il1l1(*l11lll1llllllll1Il1l1, **l111l11lll11l111Il1l1)

        pygame.display.update = l1l1llll111l1l1lIl1l1

    def l111lll1l111111lIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path) -> None:
        lll11111ll1l11l1Il1l1.l1111l11llll11llIl1l1 = True

    def llll111111llll1lIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path, ll1l11l1ll11l11lIl1l1: List[l1l111lll11llll1Il1l1]) -> None:
        lll11111ll1l11l1Il1l1.l1111l11llll11llIl1l1 = False

    def ll1l11l1ll1ll1llIl1l1(lll11111ll1l11l1Il1l1, l111l1ll11l11111Il1l1: Exception) -> None:
        lll11111ll1l11l1Il1l1.l1111l11llll11llIl1l1 = False
