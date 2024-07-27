import asyncio
import json
import os
from dataclasses import dataclass

# from websockets import ClientProtocol
import websockets

from fed_messages_pb2 import Exchange
from portfolio_manager_pb2 import Fill


@dataclass
class DeribitConnection:
    queue: asyncio.Queue
    key = ""
    secret = ""

    def __post_init__(self):
        self.key, self.secret = self.get_key()

    async def subscribe_trades(self):
        subscribe_message = self.get_trades_subscribe_message()
        heartbeat_message = self.get_set_heartbeat_message()
        test_message = self.get_test_message()
        auth_message = self.get_auth_message()
        async with websockets.connect("wss://www.deribit.com/ws/api/v2") as ws:
            await ws.send(auth_message)
            resp = await ws.recv()

            await ws.send(heartbeat_message)
            resp = await ws.recv()

            await ws.send(subscribe_message)
            resp = await ws.recv()

            while True:
                resp = await ws.recv()
                data = json.loads(resp)
                print(f"Received: {data}")
                if "params" in data:
                    if "data" in data["params"]:
                        fills = self.to_fills(data)
                        for fill in fills:
                            await self.queue.put(fill)
                    elif "type" in data["params"]:
                        if data["params"]["type"] == "heartbeat":
                            print("Heartbeat received")
                            await ws.send(test_message)
                        else:
                            print("Unknown message type")

    def get_test_message(self) -> str:
        dict_msg = {
            "jsonrpc": "2.0",
            "method": "public/test",
            "id": 42,
        }
        return json.dumps(dict_msg)

    def get_trades_subscribe_message(self) -> str:
        dict_msg = {
            "jsonrpc": "2.0",
            "method": "private/subscribe",
            "params": {
                "channels": [
                    f"user.trades.any.any.raw"
                ]  # Adjust the instrument as needed
            },
            "id": 1,
        }
        return json.dumps(dict_msg)

    def get_set_heartbeat_message(self) -> str:
        msg = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "public/set_heartbeat",
            "params": {"interval": 10},
        }
        return json.dumps(msg)

    def to_fills(self, data: dict):
        fills: list[Fill] = []
        for i in range(len(data["params"]["data"])):
            fill = Fill()
            fill.exchange = Exchange.DBT
            fill.price = float(data["params"]["data"][i]["price"])
            fill.amount = float(data["params"]["data"][i]["amount"])
            fill.symbol = data["params"]["data"][i]["instrument_name"]
            fill.ts = data["params"]["data"][i]["timestamp"]
            fills.append(fill)
        return fills

    def get_auth_message(self):
        msg = {
            "jsonrpc": "2.0",
            "id": 9929,
            "method": "public/auth",
            "params": {
                "grant_type": "client_credentials",
                "client_id": self.key,
                "client_secret": self.secret,
            },
        }
        return json.dumps(msg)

    def get_key(self):
        key = os.getenv("EX_SP_KEY")
        secret = os.getenv("EX_SP_SECRET")

        assert key is not None, "API key not found"
        assert secret is not None, "API secret not found"

        return key, secret
