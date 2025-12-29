import time
import bittensor as bt
from template.protocol import Dummy
from template.validator.reward import get_rewards
from template.utils.uids import get_random_uids
from template.validator.agent_runner import wrun_github_agent


async def forward(self):
    """
    Validator forward loop:
    - Query miners
    - Receive github_url
    - Score miners
    """

    miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)

    # 1️⃣ Query miners
    responses = await self.dendrite(
        axons=[self.metagraph.axons[uid] for uid in miner_uids],
        synapse=Dummy(ping="Send me your agent code"),
        deserialize=True,
    )

    bt.logging.info(f"Received responses: {responses}")
    for response in responses:
        if response is not None:
            agent = wrun_github_agent(response, "task.json", "output.json")
            if agent is not None:
                bt.logging.info(f"Successfully loaded agent from {response}")
            else:
                bt.logging.warning(f"Failed to load agent from {response}")
    # 2️⃣ Score responses
    rewards = get_rewards(self, responses=responses)

    bt.logging.info(f"Scored rewards: {rewards}")

    # 3️⃣ Update miner scores
    self.update_scores(rewards, miner_uids)

    time.sleep(5)
    return responses