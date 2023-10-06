import sys

__RELOADIUM__ = True


def l1ll1l1l1l1l11llIl1l1(lll1l111ll1l111lIl1l1, ll1ll1l1l11l1l1lIl1l1):
    from reloadium.lib.environ import env
    from pathlib import Path
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    import io
    import os

    env.sub_process += 1
    env.save_to_os_environ()

    def l11111111l1lll11Il1l1(*ll11ll1l11l11111Il1l1):

        for l1llll1l1ll1ll1lIl1l1 in ll11ll1l11l11111Il1l1:
            os.close(l1llll1l1ll1ll1lIl1l1)

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
    else:
        from multiprocessing import semaphore_tracker as tracker 

    l1lllll1ll1ll1llIl1l1 = tracker.getfd()
    lll1l111ll1l111lIl1l1._fds.append(l1lllll1ll1ll1llIl1l1)
    ll111llllllllll1Il1l1 = spawn.get_preparation_data(ll1ll1l1l11l1l1lIl1l1._name)
    ll1ll1lllll111l1Il1l1 = io.BytesIO()
    set_spawning_popen(lll1l111ll1l111lIl1l1)

    try:
        reduction.dump(ll111llllllllll1Il1l1, ll1ll1lllll111l1Il1l1)
        reduction.dump(ll1ll1l1l11l1l1lIl1l1, ll1ll1lllll111l1Il1l1)
    finally:
        set_spawning_popen(None)

    lll111111ll1l1l1Il1l1l1ll1111l11l1lllIl1l1l111llllll1l111lIl1l1l1ll11l1l1111111Il1l1 = None
    try:
        (lll111111ll1l1l1Il1l1, l1ll1111l11l1lllIl1l1, ) = os.pipe()
        (l111llllll1l111lIl1l1, l1ll11l1l1111111Il1l1, ) = os.pipe()
        ll111l1ll11llll1Il1l1 = spawn.get_command_line(tracker_fd=l1lllll1ll1ll1llIl1l1, pipe_handle=l111llllll1l111lIl1l1)


        l1111ll1l1l1l1l1Il1l1 = str(Path(ll111llllllllll1Il1l1['sys_argv'][0]).absolute())
        ll111l1ll11llll1Il1l1 = [ll111l1ll11llll1Il1l1[0], '-B', '-m', 'reloadium_launcher', 'spawn_process', str(l1lllll1ll1ll1llIl1l1), 
str(l111llllll1l111lIl1l1), l1111ll1l1l1l1l1Il1l1]
        lll1l111ll1l111lIl1l1._fds.extend([l111llllll1l111lIl1l1, l1ll1111l11l1lllIl1l1])
        lll1l111ll1l111lIl1l1.pid = util.spawnv_passfds(spawn.get_executable(), 
ll111l1ll11llll1Il1l1, lll1l111ll1l111lIl1l1._fds)
        lll1l111ll1l111lIl1l1.sentinel = lll111111ll1l1l1Il1l1
        with open(l1ll11l1l1111111Il1l1, 'wb', closefd=False) as llll11l1l1111l11Il1l1:
            llll11l1l1111l11Il1l1.write(ll1ll1lllll111l1Il1l1.getbuffer())
    finally:
        ll11lllll111l11lIl1l1 = []
        for l1llll1l1ll1ll1lIl1l1 in (lll111111ll1l1l1Il1l1, l1ll11l1l1111111Il1l1, ):
            if (l1llll1l1ll1ll1lIl1l1 is not None):
                ll11lllll111l11lIl1l1.append(l1llll1l1ll1ll1lIl1l1)
        lll1l111ll1l111lIl1l1.finalizer = util.Finalize(lll1l111ll1l111lIl1l1, l11111111l1lll11Il1l1, ll11lllll111l11lIl1l1)

        for l1llll1l1ll1ll1lIl1l1 in (l111llllll1l111lIl1l1, l1ll1111l11l1lllIl1l1, ):
            if (l1llll1l1ll1ll1lIl1l1 is not None):
                os.close(l1llll1l1ll1ll1lIl1l1)


def __init__(lll1l111ll1l111lIl1l1, ll1ll1l1l11l1l1lIl1l1):
    from reloadium.lib.environ import env
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    from multiprocessing.popen_spawn_win32 import TERMINATE, WINEXE, WINSERVICE, WINENV, _path_eq
    from pathlib import Path
    import os
    import msvcrt
    import sys
    import _winapi

    env.sub_process += 1
    env.save_to_os_environ()

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
        from multiprocessing.popen_spawn_win32 import _close_handles
    else:
        from multiprocessing import semaphore_tracker as tracker 
        _close_handles = _winapi.CloseHandle

    ll111llllllllll1Il1l1 = spawn.get_preparation_data(ll1ll1l1l11l1l1lIl1l1._name)







    (ll1111lll111l1l1Il1l1, ll11l1ll111111l1Il1l1, ) = _winapi.CreatePipe(None, 0)
    ll1l1l1111l11ll1Il1l1 = msvcrt.open_osfhandle(ll11l1ll111111l1Il1l1, 0)
    l11llll11ll1ll1lIl1l1 = spawn.get_executable()
    l1111ll1l1l1l1l1Il1l1 = str(Path(ll111llllllllll1Il1l1['sys_argv'][0]).absolute())
    ll111l1ll11llll1Il1l1 = ' '.join([l11llll11ll1ll1lIl1l1, '-B', '-m', 'reloadium_launcher', 'spawn_process', str(os.getpid()), 
str(ll1111lll111l1l1Il1l1), l1111ll1l1l1l1l1Il1l1])



    if ((WINENV and _path_eq(l11llll11ll1ll1lIl1l1, sys.executable))):
        l11llll11ll1ll1lIl1l1 = sys._base_executable
        env = os.environ.copy()
        env['__PYVENV_LAUNCHER__'] = sys.executable
    else:
        env = None

    with open(ll1l1l1111l11ll1Il1l1, 'wb', closefd=True) as l11lll1llll11l1lIl1l1:

        try:
            (lll1l11l11l11l11Il1l1, l1l1111ll1l11l11Il1l1, l11l11l11l1l111lIl1l1, llll11lllll111l1Il1l1, ) = _winapi.CreateProcess(l11llll11ll1ll1lIl1l1, ll111l1ll11llll1Il1l1, None, None, False, 0, env, None, None)


            _winapi.CloseHandle(l1l1111ll1l11l11Il1l1)
        except :
            _winapi.CloseHandle(ll1111lll111l1l1Il1l1)
            raise 


        lll1l111ll1l111lIl1l1.pid = l11l11l11l1l111lIl1l1
        lll1l111ll1l111lIl1l1.returncode = None
        lll1l111ll1l111lIl1l1._handle = lll1l11l11l11l11Il1l1
        lll1l111ll1l111lIl1l1.sentinel = int(lll1l11l11l11l11Il1l1)
        if (sys.version_info > (3, 8, )):
            lll1l111ll1l111lIl1l1.finalizer = util.Finalize(lll1l111ll1l111lIl1l1, _close_handles, (lll1l111ll1l111lIl1l1.sentinel, int(ll1111lll111l1l1Il1l1), 
))
        else:
            lll1l111ll1l111lIl1l1.finalizer = util.Finalize(lll1l111ll1l111lIl1l1, _close_handles, (lll1l111ll1l111lIl1l1.sentinel, ))



        set_spawning_popen(lll1l111ll1l111lIl1l1)
        try:
            reduction.dump(ll111llllllllll1Il1l1, l11lll1llll11l1lIl1l1)
            reduction.dump(ll1ll1l1l11l1l1lIl1l1, l11lll1llll11l1lIl1l1)
        finally:
            set_spawning_popen(None)
