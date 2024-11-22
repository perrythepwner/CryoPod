import time
import os
import argparse
from typing import List, Tuple
from logging import Logger
from web3 import Web3
from web3.contract import Contract
from .EVMBot import EVMBot as Bot
from .utils import is_node_running, setup_logger, load_env, get_contracts_instances, get_bots

FLAG = os.getenv("FLAG", "HTB{pl4c3h0ld3r}") 
USERS_PODS = {
    # TODO: add users secrets (and some memes)
    1: [
        "**Peanut Butter and Pickle Sandwich**: 2 slices of bread (white, whole wheat, or sourdough), 2 tablespoons of Peanut Butter, 4-6 dill pickle slices, a dash of hot sauce, lettuce, or honey (optional). Preparation: 1) Apply peanut butter evenly on one side of each bread slice. 2) Layer the pickle slices on one peanut butter-covered bread slice. 3) Add a sprinkle of salt, hot sauce, or extra layers like lettuce. 4) Place the second bread slice on top, peanut butter side down. Press gently. 5) Cut diagonally for easier handling and enjoy. Description: Embark on an unexpected gastronomic journey with our Peanut Butter & Pickle Symphony, a harmonious fusion of contrasting flavors and textures that redefine the boundaries of contemporary cuisine. This avant-garde creation marries the rich, velvety notes of artisanal creamy peanut butter with the crisp, tangy zest of hand-selected dill pickles, meticulously layered between slices of freshly baked, stone-ground sourdough bread.",
        "",
        "",
        "",
        ""
    ],
    
    2: [
        "https://youtu.be/dQw4w9WgXcQ",
        "https://youtu.be/JxS5E-kZc2s",
        "",
        ""
    ],
    
    3: [
        "",
        "",
        "",
        ""
    ],
    
    4: [
        "",
        "",
        "",
        ""
    ],
    
    5: [
        "",
        "",
        "",
        ""
    ]
}

def start_simulation(w3: Web3, bots: List[Tuple[str, str]], contracts: List[Contract], rpc_url: str,
                     max_retries: int, retry_interval: int, logger: Logger):
    logger.info(f"\nStarting simulation with {len(bots)} bots.")

    for contract_name, contract_instance in contracts.items():
        if contract_name == "CryoPod":
            CryoPod = contract_instance

    for n in range(1, 5):
        for bot_id, bot_info in enumerate(bots, 1):
            logger.info(f"Starting bot-{bot_id} with info {bot_info}.")
            bot_addr, bot_pvk = bot_info
            if (n * bot_id) == 20:
                secret = FLAG
            else: 
                secret = USERS_PODS.get(bot_id).pop()
            Bot(
                bot_id=bot_id, bot_addr=bot_addr,
                w3=w3, target_contract=CryoPod, function_sig="storePod(string)", args=[secret], tx_options={},
                private_key=bot_pvk, rpc_url=rpc_url,
                max_retries=max_retries, retry_interval=retry_interval, logger=logger
            ).start()
            time.sleep(5)
        logger.info("Simulation ended.")

def main():
    if not is_node_running():
        #logger.error("Node is not running. Please start the node before running the simulation.")
        # wait until the node is running
        # TODO
        time.sleep(10)
        main()
    env = load_env()
    w3 = Web3(Web3.HTTPProvider(env["LOCAL_RPC_URL"]))
    logger = setup_logger(env["BOT_LOG_FILE"])
    contract_address_mapping = {"Setup": "setupAddress", "CryoPod": "targetAddress"}
    contracts = get_contracts_instances(w3, "/home/ctf/backend/contracts/compiled", contract_address_mapping, logger)
    bots = get_bots()
    start_simulation(
        w3=w3,
        bots=bots,
        contracts=contracts,
        rpc_url=env["LOCAL_RPC_URL"],
        max_retries=env["BOT_MAX_RETRIES"],
        retry_interval=env["BOT_RETRY_INTERVAL"],
        logger=logger
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TODO")
    # @TODO [...]
    _ = parser.parse_args()
    main()
