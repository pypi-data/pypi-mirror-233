from reloadium.corium.vendored import logging
from pathlib import Path
from threading import Thread
import time
from typing import TYPE_CHECKING, List, Optional

from reloadium.corium import l1l1ll1lll1111l1Il1l1
from reloadium.corium.l1l1ll1lll1111l1Il1l1.l1lll1l1llll1111Il1l1 import llll1l11111l11llIl1l1
from reloadium.lib.l1lllll1111l1l1lIl1l1.l11111l1l111lll1Il1l1 import l1l1l11l11l11111Il1l1
from reloadium.corium.ll1l111ll11lllllIl1l1 import l11l11llll111l11Il1l1
from reloadium.corium.ll1ll1l11lllllllIl1l1 import ll1llll1l1lll1llIl1l1
from reloadium.corium.ll11111llll11ll1Il1l1 import l1l111lll11llll1Il1l1
from reloadium.corium.lll11ll11l1lllllIl1l1 import lll11ll11l1lllllIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.vendored.websocket_server import WebsocketServer


__RELOADIUM__ = True

__all__ = ['ll1ll1llll1lll1lIl1l1']



l1111ll111l1l11lIl1l1 = '\n<!--{info}-->\n<script type="text/javascript">\n   // <![CDATA[  <-- For SVG support\n     function refreshCSS() {\n        var sheets = [].slice.call(document.getElementsByTagName("link"));\n        var head = document.getElementsByTagName("head")[0];\n        for (var i = 0; i < sheets.length; ++i) {\n           var elem = sheets[i];\n           var parent = elem.parentElement || head;\n           parent.removeChild(elem);\n           var rel = elem.rel;\n           if (elem.href && typeof rel != "string" || rel.length === 0 || rel.toLowerCase() === "stylesheet") {\n              var url = elem.href.replace(/(&|\\?)_cacheOverride=\\d+/, \'\');\n              elem.href = url + (url.indexOf(\'?\') >= 0 ? \'&\' : \'?\') + \'_cacheOverride=\' + (new Date().valueOf());\n           }\n           parent.appendChild(elem);\n        }\n     }\n     let protocol = window.location.protocol === \'http:\' ? \'ws://\' : \'wss://\';\n     let address = protocol + "{address}:{port}";\n     let socket = undefined;\n     let lost_connection = false;\n\n     function connect() {\n        socket = new WebSocket(address);\n         socket.onmessage = function (msg) {\n            if (msg.data === \'reload\') window.location.href = window.location.href;\n            else if (msg.data === \'refreshcss\') refreshCSS();\n         };\n     }\n\n     function checkConnection() {\n        if ( socket.readyState === socket.CLOSED ) {\n            lost_connection = true;\n            connect();\n        }\n     }\n\n     connect();\n     setInterval(checkConnection, 500)\n\n   // ]]>\n</script>\n'














































@dataclass
class ll1ll1llll1lll1lIl1l1:
    ll11l11llll1l111Il1l1: str
    lll11111llllllllIl1l1: int
    l1l111llllll11l1Il1l1: ll1llll1l1lll1llIl1l1

    l1ll1l11l1ll11l1Il1l1: Optional["WebsocketServer"] = field(init=False, default=None)
    llll1111ll1ll1l1Il1l1: str = field(init=False, default='')

    ll11llllll1l11llIl1l1 = 'Reloadium page reloader'

    def ll1ll1111l1l11l1Il1l1(lll11111ll1l11l1Il1l1) -> None:
        from reloadium.vendored.websocket_server import WebsocketServer

        lll11111ll1l11l1Il1l1.l1l111llllll11l1Il1l1.ll11llllll1l11llIl1l1(''.join(['Starting reload websocket server on port ', '{:{}}'.format(lll11111ll1l11l1Il1l1.lll11111llllllllIl1l1, '')]))

        lll11111ll1l11l1Il1l1.l1ll1l11l1ll11l1Il1l1 = WebsocketServer(host=lll11111ll1l11l1Il1l1.ll11l11llll1l111Il1l1, port=lll11111ll1l11l1Il1l1.lll11111llllllllIl1l1, loglevel=logging.CRITICAL)
        lll11111ll1l11l1Il1l1.l1ll1l11l1ll11l1Il1l1.run_forever(threaded=True)

        lll11111ll1l11l1Il1l1.llll1111ll1ll1l1Il1l1 = l1111ll111l1l11lIl1l1

        lll11111ll1l11l1Il1l1.llll1111ll1ll1l1Il1l1 = lll11111ll1l11l1Il1l1.llll1111ll1ll1l1Il1l1.replace('{info}', str(lll11111ll1l11l1Il1l1.ll11llllll1l11llIl1l1))
        lll11111ll1l11l1Il1l1.llll1111ll1ll1l1Il1l1 = lll11111ll1l11l1Il1l1.llll1111ll1ll1l1Il1l1.replace('{port}', str(lll11111ll1l11l1Il1l1.lll11111llllllllIl1l1))
        lll11111ll1l11l1Il1l1.llll1111ll1ll1l1Il1l1 = lll11111ll1l11l1Il1l1.llll1111ll1ll1l1Il1l1.replace('{address}', lll11111ll1l11l1Il1l1.ll11l11llll1l111Il1l1)

    def ll111l1ll1111l1lIl1l1(lll11111ll1l11l1Il1l1, ll11ll11lll1l111Il1l1: str) -> str:
        l11l1lll1111111lIl1l1 = ll11ll11lll1l111Il1l1.find('<head>')
        if (l11l1lll1111111lIl1l1 ==  - 1):
            l11l1lll1111111lIl1l1 = 0
        l1l1l11llll1llllIl1l1 = ((ll11ll11lll1l111Il1l1[:l11l1lll1111111lIl1l1] + lll11111ll1l11l1Il1l1.llll1111ll1ll1l1Il1l1) + ll11ll11lll1l111Il1l1[l11l1lll1111111lIl1l1:])
        return l1l1l11llll1llllIl1l1

    def l1l11l11ll1111l1Il1l1(lll11111ll1l11l1Il1l1) -> None:
        try:
            lll11111ll1l11l1Il1l1.ll1ll1111l1l11l1Il1l1()
        except Exception as l1ll1l1l11ll1ll1Il1l1:
            lll11111ll1l11l1Il1l1.l1l111llllll11l1Il1l1.l1l11l1l11ll11l1Il1l1('Could not start server')

    def ll11ll1l1ll11lllIl1l1(lll11111ll1l11l1Il1l1) -> None:
        if ( not lll11111ll1l11l1Il1l1.l1ll1l11l1ll11l1Il1l1):
            return 

        lll11111ll1l11l1Il1l1.l1l111llllll11l1Il1l1.ll11llllll1l11llIl1l1('Reloading page')
        lll11111ll1l11l1Il1l1.l1ll1l11l1ll11l1Il1l1.send_message_to_all('reload')
        lll11ll11l1lllllIl1l1.l11ll1l111l1111lIl1l1()

    def l111llllll11l111Il1l1(lll11111ll1l11l1Il1l1) -> None:
        if ( not lll11111ll1l11l1Il1l1.l1ll1l11l1ll11l1Il1l1):
            return 

        lll11111ll1l11l1Il1l1.l1l111llllll11l1Il1l1.ll11llllll1l11llIl1l1('Stopping reload server')
        lll11111ll1l11l1Il1l1.l1ll1l11l1ll11l1Il1l1.shutdown()

    def l1ll111l1lll11llIl1l1(lll11111ll1l11l1Il1l1, l111ll1l1l11lll1Il1l1: float) -> None:
        def l1111ll111l11lllIl1l1() -> None:
            time.sleep(l111ll1l1l11lll1Il1l1)
            lll11111ll1l11l1Il1l1.ll11ll1l1ll11lllIl1l1()

        llll1l11111l11llIl1l1(l1l1l1111ll11lllIl1l1=l1111ll111l11lllIl1l1, ll11ll1l111111llIl1l1='page-reloader').start()


@dataclass
class l1111l11l1ll11l1Il1l1(l1l1l11l11l11111Il1l1):
    l1111ll111l1l11lIl1l1: Optional[ll1ll1llll1lll1lIl1l1] = field(init=False, default=None)

    ll1ll1l1l1lll111Il1l1 = '127.0.0.1'
    l1ll11l11ll1l1llIl1l1 = 4512

    def l1ll1l1ll11111l1Il1l1(lll11111ll1l11l1Il1l1) -> None:
        l11l11llll111l11Il1l1.l1l11l111l1ll1llIl1l1.llllll1111l111l1Il1l1.l11l1l1l1ll1l11lIl1l1('html')

    def llll111111llll1lIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path, ll1l11l1ll11l11lIl1l1: List[l1l111lll11llll1Il1l1]) -> None:
        if ( not lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1):
            return 

        from reloadium.corium.l1ll1111lll1l1llIl1l1.l1l11llll11ll111Il1l1 import l11lll1l111lllllIl1l1

        if ( not any((isinstance(lll1l11l1l1lll1lIl1l1, l11lll1l111lllllIl1l1) for lll1l11l1l1lll1lIl1l1 in ll1l11l1ll11l11lIl1l1))):
            if (lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1):
                lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1.ll11ll1l1ll11lllIl1l1()

    def l1l1l1lll1lll1llIl1l1(lll11111ll1l11l1Il1l1, l1lllll1111l11l1Il1l1: Path) -> None:
        if ( not lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1):
            return 
        lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1.ll11ll1l1ll11lllIl1l1()

    def lll1ll11111l1111Il1l1(lll11111ll1l11l1Il1l1, lll11111llllllllIl1l1: int) -> ll1ll1llll1lll1lIl1l1:
        while True:
            l1l1llll111ll1l1Il1l1 = (lll11111llllllllIl1l1 + lll11111ll1l11l1Il1l1.l1ll11l11ll1l1llIl1l1)
            try:
                l1l1l11llll1llllIl1l1 = ll1ll1llll1lll1lIl1l1(ll11l11llll1l111Il1l1=lll11111ll1l11l1Il1l1.ll1ll1l1l1lll111Il1l1, lll11111llllllllIl1l1=l1l1llll111ll1l1Il1l1, l1l111llllll11l1Il1l1=lll11111ll1l11l1Il1l1.ll1l1l11l1ll11l1Il1l1)
                l1l1l11llll1llllIl1l1.l1l11l11ll1111l1Il1l1()
                lll11111ll1l11l1Il1l1.lll1ll1l1111llllIl1l1()
                break
            except OSError:
                lll11111ll1l11l1Il1l1.ll1l1l11l1ll11l1Il1l1.ll11llllll1l11llIl1l1(''.join(["Couldn't create page reloader on ", '{:{}}'.format(l1l1llll111ll1l1Il1l1, ''), ' port']))
                lll11111ll1l11l1Il1l1.l1ll11l11ll1l1llIl1l1 += 1

        return l1l1l11llll1llllIl1l1

    def lll1ll1l1111llllIl1l1(lll11111ll1l11l1Il1l1) -> None:
        lll11111ll1l11l1Il1l1.ll1l1l11l1ll11l1Il1l1.ll11llllll1l11llIl1l1('Injecting page reloader')

    def ll1l1llll111l11lIl1l1(lll11111ll1l11l1Il1l1) -> None:
        super().ll1l1llll111l11lIl1l1()

        if (lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1):
            lll11111ll1l11l1Il1l1.l1111ll111l1l11lIl1l1.l111llllll11l111Il1l1()
