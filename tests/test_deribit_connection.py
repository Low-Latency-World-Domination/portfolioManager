import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ExchangeConnection.deribit import DeribitConnection


async def test_get_test_message():
    q = asyncio.Queue()
    deribit = DeribitConnection(q)
    await deribit.subscribe_trades()


if __name__ == "__main__":
    asyncio.run(test_get_test_message())
