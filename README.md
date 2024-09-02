# portfolioManager
Used to manage various portfoilo infomation. Stream, order data and account risk metrics



debug
Traceback (most recent call last):
  File "/home/steve/LLWD/sloppyPipe/portfolioManager/tests/test_deribit_connection.py", l
ine 17, in <module>
    asyncio.run(test_get_test_message())
  File "/home/steve/anaconda3/envs/py3.12/lib/python3.12/asyncio/runners.py", line 194, i
n run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/home/steve/anaconda3/envs/py3.12/lib/python3.12/asyncio/runners.py", line 118, i
n run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/steve/anaconda3/envs/py3.12/lib/python3.12/asyncio/base_events.py", line 68
7, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/home/steve/LLWD/sloppyPipe/portfolioManager/tests/test_deribit_connection.py", l
ine 13, in test_get_test_message
    await deribit.subscribe_trades()
  File "/home/steve/LLWD/sloppyPipe/portfolioManager/ExchangeConnection/deribit.py", line
 39, in subscribe_trades
    resp = await ws.recv()
           ^^^^^^^^^^^^^^^
  File "/home/steve/.cache/pypoetry/virtualenvs/portfoliomanager-hHDjDttp-py3.12/lib/pyth
on3.12/site-packages/websockets/legacy/protocol.py", line 568, in recv
    await self.ensure_open()
  File "/home/steve/.cache/pypoetry/virtualenvs/portfoliomanager-hHDjDttp-py3.12/lib/pyth
on3.12/site-packages/websockets/legacy/protocol.py", line 939, in ensure_open
    raise self.connection_closed_exc()
websockets.exceptions.ConnectionClosedError: received 4000 (private use) heartbeat close;
 then sent 4000 (private use) heartbeat close
(base) steve@DESKTOP-9SUIJJ8:~/LLWD/sloppyPipe/portfolioManager$
