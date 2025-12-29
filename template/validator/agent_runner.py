import subprocess
import importlib.util
import tempfile
from pathlib import Path
import bittensor as bt


def run_github_agent(repo_url: str):
    """
    Clone a GitHub repo and load agent.py.
    Returns loaded module or None.
    """
    try:
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(
                ["git", "clone", repo_url, temp],
                check=True,
                timeout=30,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            agent_path = Path(temp) / "agent.py"
            if not agent_path.exists():
                raise FileNotFoundError("agent.py not found")

            spec = importlib.util.spec_from_file_location("agent", agent_path)
            agent = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent)

            bt.logging.info("Agent loaded successfully")
            return agent

    except Exception as e:
        bt.logging.warning(f"Failed to load agent from {repo_url}: {e}")
        return None
