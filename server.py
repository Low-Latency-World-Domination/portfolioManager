import asyncio
from asyncio import Queue
from concurrent import futures
from dataclasses import dataclass
from datetime import datetime

# import deribit_api
import grpc

import fed_messages_pb2
import portfolio_manager_pb2
import portfolio_manager_pb2_grpc
from ExchangeConnection.deribit import DeribitConnection
from portfolio_manager_pb2 import Fill, StreamFillsRequest
from sp_logger import SpLogger

# Load API keys from environment variables
# DERIBIT_API_KEY = os.getenv("DERIBIT_API_KEY")
# DERIBIT_API_SECRET = os.getenv("DERIBIT_API_SECRET")


@dataclass(slots=True)
class PortfolioManagerServicer(portfolio_manager_pb2_grpc.PortfolioManagerServicer):
    logger: SpLogger

    async def StreamFills(self, request: StreamFillsRequest, context):
        if request.portfolio_name == fed_messages_pb2.PortfolioName.DBT_SP:
            q: asyncio.Queue[Fill] = asyncio.Queue()
            deribit = DeribitConnection(q)
            asyncio.create_task(deribit.subscribe_trades())
            while True:
                fill = await q.get()
                print(f"{fill.symbol} {fill.side} {fill.amount} {fill.price}")
                yield fill


async def serve():
    file_name = f"PM{datetime.now().strftime('%Y%m%d')}.log"
    logger = SpLogger(f"./logs/{file_name}")
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    portfolio_manager_pb2_grpc.add_PortfolioManagerServicer_to_server(
        PortfolioManagerServicer(logger), server
    )
    server.add_insecure_port("[::]:50052")
    await server.start()
    print("Trader server started on port 50052")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
