from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.corium.ll1ll1l11lllllllIl1l1 import ll1ll1l11lllllllIl1l1
from reloadium.lib.environ import env
from reloadium.corium.l1ll111lll1l1lllIl1l1 import ll1111111lllll11Il1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.ll11ll11l1l1llllIl1l1 import l1111l11l1ll11l1Il1l1
from reloadium.corium.ll11111llll11ll1Il1l1 import l111l11llll1l1l1Il1l1, ll1lll11l111llllIl1l1, lll111llllll111lIl1l1, l1ll1l11llll11llIl1l1
from reloadium.corium.llll1l11ll111l11Il1l1 import ll1l11ll1ll11lllIl1l1
from reloadium.corium.l1l1ll1lll1111l1Il1l1 import ll1ll1l11ll11ll1Il1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True

l1l111llllll11l1Il1l1 = ll1ll1l11lllllllIl1l1.l111ll1l1111l11lIl1l1(__name__)


@dataclass(**l1ll1l11llll11llIl1l1)
class l1l111ll111ll11lIl1l1(lll111llllll111lIl1l1):
    llllll1ll11lll1lIl1l1 = 'FlaskApp'

    @classmethod
    def ll1111ll1l1lllllIl1l1(l1lll1111l11l1llIl1l1, lllll1l1l111111lIl1l1: ll1l11ll1ll11lllIl1l1.llllll1111111111Il1l1, llllll1111lll1llIl1l1: Any, ll11l1llll111l11Il1l1: l111l11llll1l1l1Il1l1) -> bool:
        import flask

        if (isinstance(llllll1111lll1llIl1l1, flask.Flask)):
            return True

        return False

    def l111l11l111ll11lIl1l1(lll11111ll1l11l1Il1l1) -> bool:
        return True

    @classmethod
    def l1l1lll1llll1111Il1l1(l1lll1111l11l1llIl1l1) -> int:
        return (super().l1l1lll1llll1111Il1l1() + 10)


@dataclass(**l1ll1l11llll11llIl1l1)
class l1l1l1l1lll1l1l1Il1l1(lll111llllll111lIl1l1):
    llllll1ll11lll1lIl1l1 = 'Request'

    @classmethod
    def ll1111ll1l1lllllIl1l1(l1lll1111l11l1llIl1l1, lllll1l1l111111lIl1l1: ll1l11ll1ll11lllIl1l1.llllll1111111111Il1l1, llllll1111lll1llIl1l1: Any, ll11l1llll111l11Il1l1: l111l11llll1l1l1Il1l1) -> bool:
        if (repr(llllll1111lll1llIl1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def l111l11l111ll11lIl1l1(lll11111ll1l11l1Il1l1) -> bool:
        return True

    @classmethod
    def l1l1lll1llll1111Il1l1(l1lll1111l11l1llIl1l1) -> int:

        return int(10000000000.0)


@dataclass
class ll11l1ll1l1llll1Il1l1(l1111l11l1ll11l1Il1l1):
    ll11ll111lll1l11Il1l1 = 'Flask'

    l11llll1llll11l1Il1l1: Any = field(init=False, default=None)
    l111llllll1l1ll1Il1l1: Any = field(init=False, default=None)
    ll11ll11ll1l1l1lIl1l1: Any = field(init=False, default=None)
    l1111ll111l111l1Il1l1: Any = field(init=False, default=None)

    @contextmanager
    def ll1l11ll1l1l1l11Il1l1(lll11111ll1l11l1Il1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def lll1llll1lll111lIl1l1(*l11lll1llllllll1Il1l1: Any, **l111l11lll11l111Il1l1: Any) -> Any:
            def l11lll111111ll11Il1l1(llll11l1l1111l11Il1l1: Any) -> Any:
                return llll11l1l1111l11Il1l1

            return l11lll111111ll11Il1l1

        ll1l1ll11ll11l11Il1l1 = FlaskLib.route
        FlaskLib.route = lll1llll1lll111lIl1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = ll1l1ll11ll11l11Il1l1  # type: ignore

    def ll1l11lllll1l111Il1l1(lll11111ll1l11l1Il1l1) -> List[Type[ll1lll11l111llllIl1l1]]:
        return [l1l111ll111ll11lIl1l1, l1l1l1l1lll1l1l1Il1l1]

    def l1l1ll11l11l11llIl1l1(lll11111ll1l11l1Il1l1, l1l11111111ll1llIl1l1: types.ModuleType) -> None:
        if (lll11111ll1l11l1Il1l1.ll11llll111l11l1Il1l1(l1l11111111ll1llIl1l1, 'flask.app')):
            lll11111ll1l11l1Il1l1.lll1l1l11lll1l1lIl1l1()
            lll11111ll1l11l1Il1l1.l1llllll11l11111Il1l1()
            lll11111ll1l11l1Il1l1.ll1l1111l1l11l11Il1l1()

        if (lll11111ll1l11l1Il1l1.ll11llll111l11l1Il1l1(l1l11111111ll1llIl1l1, 'flask.cli')):
            lll11111ll1l11l1Il1l1.ll1lll1l11lll1llIl1l1()

    def ll1l1llll111l11lIl1l1(lll11111ll1l11l1Il1l1) -> None:
        super().ll1l1llll111l11lIl1l1()
        try:
            import flask.app  # type: ignore
            import werkzeug.serving  # type: ignore
            import flask.cli  # type: ignore
            flask.app.Flask.dispatch_request = lll11111ll1l11l1Il1l1.l1111ll111l111l1Il1l1
            werkzeug.serving.run_simple = lll11111ll1l11l1Il1l1.l11llll1llll11l1Il1l1
            flask.cli.run_simple = lll11111ll1l11l1Il1l1.l11llll1llll11l1Il1l1
            flask.app.Flask.__init__ = lll11111ll1l11l1Il1l1.l111llllll1l1ll1Il1l1
        except ImportError:
            pass

        if (lll11111ll1l11l1Il1l1.ll11ll11ll1l1l1lIl1l1):
            try:
                import waitress  # type: ignore
                waitress.serve = lll11111ll1l11l1Il1l1.ll11ll11ll1l1l1lIl1l1
            except ImportError:
                pass

    def lll1l1l11lll1l1lIl1l1(lll11111ll1l11l1Il1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        lll11111ll1l11l1Il1l1.l11llll1llll11l1Il1l1 = werkzeug.serving.run_simple

        def l1l11l111111lll1Il1l1(*l11lll1llllllll1Il1l1: Any, **l111l11lll11l111Il1l1: Any) -> Any:
            with ll1111111lllll11Il1l1():
                lll11111llllllllIl1l1 = l111l11lll11l111Il1l1.get('port')
                if ( not lll11111llllllllIl1l1):
                    lll11111llllllllIl1l1 = l11lll1llllllll1Il1l1[1]

                lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1 = lll11111ll1l11l1Il1l1.lll1ll11111l1111Il1l1(lll11111llllllllIl1l1)
                if (env.page_reload_on_start):
                    lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1.l1ll111l1lll11llIl1l1(1.0)
            lll11111ll1l11l1Il1l1.l11llll1llll11l1Il1l1(*l11lll1llllllll1Il1l1, **l111l11lll11l111Il1l1)

        ll1ll1l11ll11ll1Il1l1.l1111l11llll111lIl1l1(werkzeug.serving, 'run_simple', l1l11l111111lll1Il1l1)
        ll1ll1l11ll11ll1Il1l1.l1111l11llll111lIl1l1(flask.cli, 'run_simple', l1l11l111111lll1Il1l1)

    def ll1l1111l1l11l11Il1l1(lll11111ll1l11l1Il1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        lll11111ll1l11l1Il1l1.l111llllll1l1ll1Il1l1 = flask.app.Flask.__init__

        def l1l11l111111lll1Il1l1(lll1l111ll1l111lIl1l1: Any, *l11lll1llllllll1Il1l1: Any, **l111l11lll11l111Il1l1: Any) -> Any:
            lll11111ll1l11l1Il1l1.l111llllll1l1ll1Il1l1(lll1l111ll1l111lIl1l1, *l11lll1llllllll1Il1l1, **l111l11lll11l111Il1l1)
            with ll1111111lllll11Il1l1():
                lll1l111ll1l111lIl1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        ll1ll1l11ll11ll1Il1l1.l1111l11llll111lIl1l1(flask.app.Flask, '__init__', l1l11l111111lll1Il1l1)

    def l1llllll11l11111Il1l1(lll11111ll1l11l1Il1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        lll11111ll1l11l1Il1l1.ll11ll11ll1l1l1lIl1l1 = waitress.serve


        def l1l11l111111lll1Il1l1(*l11lll1llllllll1Il1l1: Any, **l111l11lll11l111Il1l1: Any) -> Any:
            with ll1111111lllll11Il1l1():
                lll11111llllllllIl1l1 = l111l11lll11l111Il1l1.get('port')
                if ( not lll11111llllllllIl1l1):
                    lll11111llllllllIl1l1 = int(l11lll1llllllll1Il1l1[1])

                lll11111llllllllIl1l1 = int(lll11111llllllllIl1l1)

                lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1 = lll11111ll1l11l1Il1l1.lll1ll11111l1111Il1l1(lll11111llllllllIl1l1)
                if (env.page_reload_on_start):
                    lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1.l1ll111l1lll11llIl1l1(1.0)

            lll11111ll1l11l1Il1l1.ll11ll11ll1l1l1lIl1l1(*l11lll1llllllll1Il1l1, **l111l11lll11l111Il1l1)

        ll1ll1l11ll11ll1Il1l1.l1111l11llll111lIl1l1(waitress, 'serve', l1l11l111111lll1Il1l1)

    def ll1lll1l11lll1llIl1l1(lll11111ll1l11l1Il1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        l1l1l1111111lll1Il1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        l1l1l1111111lll1Il1l1 = l1l1l1111111lll1Il1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(l1l1l1111111lll1Il1l1, cli.__dict__)

    def lll1ll1l1111llllIl1l1(lll11111ll1l11l1Il1l1) -> None:
        super().lll1ll1l1111llllIl1l1()
        import flask.app

        lll11111ll1l11l1Il1l1.l1111ll111l111l1Il1l1 = flask.app.Flask.dispatch_request

        def l1l11l111111lll1Il1l1(*l11lll1llllllll1Il1l1: Any, **l111l11lll11l111Il1l1: Any) -> Any:
            l1111lllll111lllIl1l1 = lll11111ll1l11l1Il1l1.l1111ll111l111l1Il1l1(*l11lll1llllllll1Il1l1, **l111l11lll11l111Il1l1)

            if ( not lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1):
                return l1111lllll111lllIl1l1

            if (isinstance(l1111lllll111lllIl1l1, str)):
                l1l1l11llll1llllIl1l1 = lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1.ll111l1ll1111l1lIl1l1(l1111lllll111lllIl1l1)
                return l1l1l11llll1llllIl1l1
            elif ((isinstance(l1111lllll111lllIl1l1, flask.app.Response) and 'text/html' in l1111lllll111lllIl1l1.content_type)):
                l1111lllll111lllIl1l1.data = lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1.ll111l1ll1111l1lIl1l1(l1111lllll111lllIl1l1.data.decode('utf-8')).encode('utf-8')
                return l1111lllll111lllIl1l1
            else:
                return l1111lllll111lllIl1l1

        flask.app.Flask.dispatch_request = l1l11l111111lll1Il1l1  # type: ignore
