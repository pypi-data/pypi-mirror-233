import dataclasses
import types
from reloadium.lib.l1lllll1111l1l1lIl1l1.l11111l1l111lll1Il1l1 import l1l1l11l11l11111Il1l1
from reloadium.fast.l1lllll1111l1l1lIl1l1.lll11ll1l11111llIl1l1 import llll111lllll1l11Il1l1

from dataclasses import dataclass

__RELOADIUM__ = True

import types


@dataclass(repr=False, frozen=False)
class l1llll11l1ll1l11Il1l1(l1l1l11l11l11111Il1l1):
    ll11ll111lll1l11Il1l1 = 'Pytest'

    def l1l1ll11l11l11llIl1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: types.ModuleType) -> None:
        if (lll11111ll1l11l1Il1l1.ll11llll111l11l1Il1l1(ll11l1l11llllll1Il1l1, 'pytest')):
            lll11111ll1l11l1Il1l1.l11l11111l111ll1Il1l1(ll11l1l11llllll1Il1l1)

    def l11l11111l111ll1Il1l1(lll11111ll1l11l1Il1l1, ll11l1l11llllll1Il1l1: types.ModuleType) -> None:
        import _pytest.assertion.rewrite
        _pytest.assertion.rewrite.AssertionRewritingHook = llll111lllll1l11Il1l1  # type: ignore

