import logging
import math

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from model import Aave

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

RAY = 10 ** 27
SECONDS_PER_YEAR = 31536000

API = '272d79f68cfe32ee4c3b91a5165054b5'
subgraph = {
    "Ethereum": f"https://gateway-arbitrum.network.thegraph.com/api/{API}/subgraphs/id/Cd2gEDVeqnjBn1hSeqFMitw8Q1iiyV9FYUZkLNRcL87g",
    "Base": "https://api.goldsky.com/api/public/project_clk74pd7lueg738tw9sjh79d6/subgraphs/aave-v3-base/1.0.0/gn",
    "Arbitrum": f"https://gateway-arbitrum.network.thegraph.com/api/{API}/subgraphs/id/DLuE98kEb5pQNXAcKFQGQgfSQ57Xdou4jnVbAEqMfy3B",
    "Avalanche": f"https://gateway-arbitrum.network.thegraph.com/api/{API}/subgraphs/id/2h9woxy8RTjHu1HJsCEnmzpPHFArU33avmUh4f71JpVn",
    "Fantom": f"https://gateway-arbitrum.network.thegraph.com/api/{API}/subgraphs/id/6L1vPqyE3xvkzkWjh6wUKc1ABWYYps5HJahoxhrv2PJn",
    "Harmony": f"https://gateway-arbitrum.network.thegraph.com/api/{API}/subgraphs/id/FifJapBdCqT9vgNqJ5axmr6eNyUpUSaRAbbZTfsViNsT",
    "Optimism": f"https://gateway-arbitrum.network.thegraph.com/api/{API}/subgraphs/id/DSfLz8oQBUeU5atALgUFQKMTSYV9mZAVYp4noLSXAfvb",
    "Polygon": f"https://gateway-arbitrum.network.thegraph.com/api/{API}/subgraphs/id/Co2URyXjnxaw8WqxKyVHdirq9Ahhm5vcTs4dMedAq211",
    "Metis": "https://metisapi.0xgraph.xyz/subgraphs/name/aave/protocol-v3-metis",
    "Gnosis": f"https://gateway-arbitrum.network.thegraph.com/api/{API}/subgraphs/id/HtcDaL8L8iZ2KQNNS44EBVmLruzxuNAz1RkBYdui1QUT",
    "BNB Chain": f"https://gateway-arbitrum.network.thegraph.com/api/{API}/subgraphs/id/7Jk85XgkV1MQ7u56hD8rr65rfASbayJXopugWkUoBMnZ",
    "Scroll": f"https://gateway-arbitrum.network.thegraph.com/api/{API}/subgraphs/id/74JwenoHZb2aAYVGCCSdPWzi9mm745dyHyQQVoZ7Sbub",
}


def to_per(num):
    if num < 0.0001:
        return math.trunc(num * 10000) / 100
    return round(num * 100, 2)


def fetch_apy(network):
    reserves = []

    query = gql(
        """
        {
          reserves {
            name
            symbol
            underlyingAsset

            liquidityRate 
            stableBorrowRate
            variableBorrowRate
          }
        }
    """
    )

    try:
        response = Client(
            transport=RequestsHTTPTransport(subgraph[network]),
            fetch_schema_from_transport=True,
        ).execute(query)

        for reserve in response["reserves"]:
            liquidity_rate = int(reserve["liquidityRate"])
            variable_borrow_rate = int(reserve["variableBorrowRate"])

            deposit_apr = liquidity_rate / RAY
            variable_borrow_apr = variable_borrow_rate / RAY
            stable_borrow_apr = variable_borrow_apr / RAY

            deposit_apy = (
                                  (1 + (deposit_apr / SECONDS_PER_YEAR)) ** SECONDS_PER_YEAR
                          ) - 1
            variable_borrow_apy = (
                                          (1 + (variable_borrow_apr / SECONDS_PER_YEAR)) ** SECONDS_PER_YEAR
                                  ) - 1
            stable_borrow_apy = (
                                        (1 + (stable_borrow_apr / SECONDS_PER_YEAR)) ** SECONDS_PER_YEAR
                                ) - 1

            reserves.append(
                Aave(
                    reserve["name"],
                    reserve["symbol"],
                    network,
                    to_per(deposit_apr),
                    to_per(variable_borrow_apr),
                    to_per(stable_borrow_apr),
                    to_per(deposit_apy),
                    to_per(variable_borrow_apy),
                    to_per(stable_borrow_apy),
                )
            )
    except Exception as e:
        logging.info(
            f"Catch exception while fetching data from {network}: {e}", exc_info=True
        )

    return reserves
