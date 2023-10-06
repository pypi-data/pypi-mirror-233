import sys

from reloadium.corium.l1l1ll1lll1111l1Il1l1.l1l1ll111111lll1Il1l1 import l1lllll1l11lll11Il1l1

__RELOADIUM__ = True

l1lllll1l11lll11Il1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class l1l1ll11111l1111Il1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = l1l1ll11111l1111Il1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
