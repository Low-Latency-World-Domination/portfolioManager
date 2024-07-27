import asyncio
import json
from dataclasses import dataclass


@dataclass
class DeribitConnection:
    queue: asyncio.Queue


async def subscribe_orders(ws):
    subscribe_message = {
        "jsonrpc": "2.0",
        "method": "private/subscribe",
        "params": {
            "channels": [
                "user.orders.BTC-PERPETUAL.raw"
            ]  # Adjust the instrument as needed
        },
        "id": 1,
    }
    await ws.send(json.dumps(subscribe_message))
    print("Subscribed to orders")


    def to_fill():

