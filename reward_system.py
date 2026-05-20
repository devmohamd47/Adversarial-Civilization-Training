"""
Reward system for light reinforcement learning layer.
"""

from agent import Agent


class RewardSystem:
    """Computes and manages rewards for agents"""
    
    # Reward constants
    TRADE_REWARD = 2.0
    COOPERATION_REWARD = 1.5
    SHARE_REWARD = 1.0
    STEAL_REWARD = 2.5
    DECEPTION_REWARD = 1.5
    
    BETRAYAL_PENALTY = -2.0
    DECEPTION_PENALTY = -1.5
    DEATH_PENALTY = -10.0
    
    SURVIVAL_BONUS = 0.1
    WEALTH_BONUS_PER_100 = 0.5
    
    @staticmethod
    def compute_action_reward(agent: Agent, action: str, success: bool) -> float:
        """Compute reward from a specific action"""
        
        if not success:
            return -1.0
        
        if action == "trade":
            return RewardSystem.TRADE_REWARD
        elif action == "cooperate":
            return RewardSystem.COOPERATION_REWARD
        elif action == "share":
            return RewardSystem.SHARE_REWARD
        elif action == "steal":
            return RewardSystem.STEAL_REWARD
        elif action == "idle":
            return 0.0
        
        return 0.0
    
    @staticmethod
    def compute_wealth_reward(agent: Agent) -> float:
        """Reward for maintaining/growing wealth"""
        if agent.alive:
            wealth_bonus = (agent.resources / 100.0) * RewardSystem.WEALTH_BONUS_PER_100
            return RewardSystem.SURVIVAL_BONUS + min(wealth_bonus, 2.0)
        else:
            return RewardSystem.DEATH_PENALTY
    
    @staticmethod
    def compute_survival_reward(agent: Agent) -> float:
        """Reward for survival"""
        if agent.alive:
            return RewardSystem.SURVIVAL_BONUS
        else:
            return RewardSystem.DEATH_PENALTY
    
    @staticmethod
    def update_agent_reward(agent: Agent, action: str, reward: float):
        """Update agent's cumulative reward"""
        agent.total_reward += reward
