import numpy as np
from typing import List, Optional
import bittensor as bt
from template.protocol import Dummy


def reward(response: Optional[Dummy]) -> float:
    """
    Reward a miner based on whether it returned a valid github_url.
    """

    if response is None:
        bt.logging.info("Reward: response is None")
        return 0.0

    github_url = getattr(response, "github_url", None)

    if github_url and isinstance(github_url, str) and github_url.startswith("https://github.com"):
        bt.logging.info(f"Reward: valid github_url received: {github_url}")
        return 1.0

    bt.logging.info(f"Reward: invalid or missing github_url: {github_url}")
    return 0.0


def get_rewards(
    self,
    responses: List[Optional[Dummy]],
) -> np.ndarray:
    """
    Compute rewards for all miner responses.
    """
    return np.array([reward(response) for response in responses], dtype=np.float32)
