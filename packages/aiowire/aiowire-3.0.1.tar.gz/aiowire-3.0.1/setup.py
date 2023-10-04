# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiowire']

package_data = \
{'': ['*']}

install_requires = \
['pyzmq>=23.2.0']

setup_kwargs = {
    'name': 'aiowire',
    'version': '3.0.1',
    'description': 'A simple event loop using asyncio',
    'long_description': 'aiowire - A simple event loop using asyncio\n============================================\n\n.. image:: https://github.com/frobnitzem/aiowire/actions/workflows/python-package.yml/badge.svg\n   :target: https://github.com/frobnitzem/aiowire/actions\n   :alt: CI\n.. image:: https://codecov.io/github/frobnitzem/aiowire/branch/main/graph/badge.svg\n   :target: https://app.codecov.io/gh/frobnitzem/aiowire\n   :alt: Coverage\n\nThis package implements a ``EventLoop`` class\nthat manages concurrent coroutines.\n\nIt is based on the principles of functional\nreactive programming and draws inspiration\nfrom Haskell\'s `Control.Wire <https://hackage.haskell.org/package/netwire-4.0.7/docs/Control-Wire.html>`_ library.\n\nIn particular, every co-routine started by the event loop is a ``Wire``.\n\n``Wire``-s either return ``None``, indicating they\'re done, or another\n``Wire``.\n\nAn example helps explain the idea::\n\n    from aiowire import EventLoop\n\n    event = 0\n    async def show_event(ev) -> Optional[Wire]:\n        print("Running...")\n        event += 1\n        await asyncio.sleep(event*0.15)\n        print(f"Event {event}")\n        if event < 5:\n            return Wire(show_event)\n        return None\n\n    async with EventLoop(timeout=1) as event:\n        event.start(show_event)\n        event.start(show_event)\n\n\nWe start up an event loop and drop in two wires.\nEach runs, then returns the ``show_event`` function.\nThe event loop runs those functions next... and so on.\n\nBut since this isn\'t functional programming.  The wires\nhave access to the event loop, and can start more\ntasks.  Easy, right?\n\n\nWhat can I do with it?\n^^^^^^^^^^^^^^^^^^^^^^\n\nWhat if you have a server that\'s spawning programs,\nworking with sockets, and managing timeouts?  Drop\nin one wire for each program, one polling on socket I/O,\nand another acting as a timer (as above).\n\nSome canonical task types that do these include::\n\n    asyncio.create_subprocess_exec # run a program\n\n    asyncio.sleep # awake the loop after a given time lapse\n\n    zmq.asyncio.Poller.poll # awake the loop after I/O on socket/file\n\n    aiowire.Poller # Wire-y interface to zmq.asyncio.Poller\n\n\nThink about each wire as a finite state machine.\nFor example,\n\n.. code::\n\n    flowchart LR\n        R[Ready] --> N{New Task?};\n        N -- Yes --> W[Working];\n        W --> C{Complete?};\n        C -- Yes --> R;\n\ncan be implemented like so::\n\n    async def ready(ev : EventLoop, info : X) -> Optional[Wire]:\n        if info.new_task():\n            do_working_action()\n            return Wire(working, info) # move to working state\n\n        # Return a sequence of 2 wires:\n        return Call(asyncio.sleep, 1.0) >> Wire(ready, info)\n\n    async def working(ev : EventLoop, info : X) -> Wire:\n        if info.complete():\n            do_complete_action()\n            return Wire(ready, info)\n        await asyncio.sleep(0.5) # directly sleep a bit\n        return Wire(working, info)\n\nNote how your sockets can launch programs, and your program\nresults can start/stop sockets, and everyone can start\nbackground tasks.\n\n\nPoller?\n^^^^^^^\n\nThe ``Poller`` class lets you schedule callbacks in response\nto socket or file-descriptor activity.  Of course, the callbacks\nare wires, and run concurrently.\n\nPoller is also a Wire, created as,\n`Poller(dictionary mapping sockets / fd-s to callback wires)`.\n\nYou add it to your event loop as usual::\n\n    # ... create sock from zmq.asyncio.Context\n\n    async def echo(ev):\n        await sock.send( await sock.recv() )\n\n    todo = { 0:  Call(print, "received input on sys.stdin"),\n             sock: Wire(echo)\n           }\n    async with EventLoop() as ev:\n        ev.start( Poller(todo) )\n\n\nTell me more\n^^^^^^^^^^^^\n\nYes, you *could* just send async functions taking one\nargument to ``EventLoop.start``, but where\'s the fun in\nwriting closures everywhere?\n\nTo take it to the next level, aiowire comes with a\n``Wire`` convenience class that lets you write ``Wire``-s expressively.\nThe following class extensions help you make Wire-s out of common \nprogramming idioms:\n\n* `Wire(w)`: acts like an identity over "async func(ev):" functions\n* `Repeat(w, n)`: repeat wire ``w`` n times in a row\n* `Forever(w)`: repeat forever -- like `Repeat(w) * infinity`\n* `Call(fn, *args, **kargs)`: call fn (normal or async),\n  ignore the return, and exit\n\nConsider, for example, printing 4 alarms separated by some time interval::\n\n    from aiowire import EventLoop, Call\n\n    prog = ( Call(asyncio.sleep, 0.1) >> Call(print, \'beep\\a\') ) * 4\n\n    async with EventLoop() as ev:\n        ev.start(prog)\n\nReferences\n==========\n\n* https://pyzmq.readthedocs.io/en/latest/api/zmq.html#poller\n* https://pythontic.com/modules/select/poll\n* https://blog.tomecek.net/post/non-blocking-stdin-in-python/\n',
    'author': 'David M. Rogers',
    'author_email': 'predictivestatmech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frobnitzem/aiowire',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
