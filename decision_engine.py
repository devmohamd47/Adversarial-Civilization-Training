"""
Decision engine for agent action selection.
"""

import random
import math
from typing import List, Dict
from agent import Agent, ActionType, Personality


class DecisionEngine:
    """Rule-based decision making engine"""
    
    def __init__(self, exploration_rate: float = 0.2):
        self.exploration_rate = exploration_rate
    
    def decide(
        self,
        agent: Agent,
        other_agents: List[Agent],
        pool_status: str,
        pool_amount: float
    ) -> Dict:
        """
        Make a decision for an agent.
        
        Returns:
        {
            "action": "trade|steal|cooperate|share|idle",
            "target": "agent_id or None",
            "message": "string",
            "resource_change_intent": int,
            "is_lying": bool
        }
        """
        
        if not other_agents:
            return self._idle_action()
        
        # Evaluate all actions
        actions = []
        
        # TRADE
        if agent.resources > 20:
            for target in other_agents:
                if target.resources > 20:
                    score = self._evaluate_trade(agent, target, pool_status)
                    actions.append(("trade", target, score))
        
        # STEAL
        for target in other_agents:
            if target.resources > 20 and agent.personality.aggressiveness > 0.3:
                score = self._evaluate_steal(agent, target, pool_status)
                actions.append(("steal", target, score))
        
        # COOPERATE
        if agent.resources > 15:
            for target in other_agents:
                if target.resources > 10:
                    score = self._evaluate_cooperate(agent, target, pool_status)
                    actions.append(("cooperate", target, score))
        
        # SHARE
        if agent.resources > 20 and agent.personality.altruism > 0.3:
            for target in other_agents:
                if target.resources < 30:  # Help the needy
                    score = self._evaluate_share(agent, target, pool_status)
                    actions.append(("share", target, score))
        
        # IDLE (always available)
        actions.append(("idle", None, 0.5))
        
        # Choose action: 80% best, 20% explore
        if random.random() < self.exploration_rate and len(actions) > 1:
            action, target, score = random.choice(actions)
        else:
            action, target, score = max(actions, key=lambda x: x[2])
        
        # Build decision
        is_lying = (
            action in ["trade", "cooperate"] and
            random.random() < agent.personality.deceptiveness
        )
        
        return {
            "action": action,
            "target": target.id if target else None,
            "message": self._get_message(action, agent, target),
            "resource_change_intent": self._estimate_resource_change(action, agent, target),
            "is_lying": is_lying
        }
    
    def _evaluate_trade(self, agent: Agent, target: Agent, pool_status: str) -> float:
        """Evaluate trade opportunity"""
        base_score = 0.6
        
        # Personality factors
        base_score += agent.personality.cooperativeness * 0.2
        base_score -= agent.personality.greed * 0.1  # Greedy agents less interested in fair trade
        
        # Trust factor
        trust = agent.get_trust_toward(target.id)
        base_score += trust * 0.2  # More trusting = more likely to trade
        
        # Pool status (high resources = more willing to trade)
        if pool_status == "abundant":
            base_score += 0.1
        elif pool_status == "scarce":
            base_score -= 0.1
        
        return min(1.0, base_score)
    
    def _evaluate_steal(self, agent: Agent, target: Agent, pool_status: str) -> float:
        """Evaluate stealing opportunity"""
        base_score = 0.3
        
        # Personality factors
        base_score += agent.personality.aggressiveness * 0.3
        base_score += agent.personality.greed * 0.2
        
        # Risk based on target strength (approximated by resources)
        if target.resources > agent.resources:
            base_score -= 0.1
        
        # Trust factor (low/negative trust makes stealing more likely)
        trust = agent.get_trust_toward(target.id)
        if trust < -0.3:  # Distrustful
            base_score += 0.15
        elif trust > 0.3:  # Trusting
            base_score -= 0.2
        
        # Scarcity drives theft
        if pool_status == "scarce":
            base_score += 0.2
        
        return min(1.0, max(0.0, base_score))
    
    def _evaluate_cooperate(self, agent: Agent, target: Agent, pool_status: str) -> float:
        """Evaluate cooperation opportunity"""
        base_score = 0.5
        
        # Personality factors
        base_score += agent.personality.cooperativeness * 0.3
        base_score -= agent.personality.aggressiveness * 0.1
        
        # Trust factor
        trust = agent.get_trust_toward(target.id)
        base_score += max(0.0, trust * 0.3)
        
        # Pool status
        if pool_status == "abundant":
            base_score += 0.1
        elif pool_status == "scarce":
            base_score -= 0.2
        
        return min(1.0, base_score)
    
    def _evaluate_share(self, agent: Agent, target: Agent, pool_status: str) -> float:
        """Evaluate sharing opportunity"""
        base_score = 0.3
        
        # Personality factors
        base_score += agent.personality.altruism * 0.4
        base_score -= agent.personality.greed * 0.2
        
        # Target need
        if target.resources < 20:
            base_score += 0.2
        
        # Trust factor
        trust = agent.get_trust_toward(target.id)
        if trust > 0:
            base_score += 0.1
        
        return min(1.0, base_score)
    
    def _estimate_resource_change(self, action: str, agent: Agent, target: Agent = None) -> int:
        """Estimate resource change from action"""
        if action == "idle":
            return 0
        elif action == "trade":
            return -20  # Cost to initiate
        elif action == "steal":
            return 30   # Potential gain
        elif action == "cooperate":
            return -15  # Investment
        elif action == "share":
            return -20  # Gift
        return 0
    
    def _get_message(self, action: str, agent: Agent, target: Agent = None) -> str:
        """Generate appropriate message for action"""
        messages = {
            "idle": "Observing...",
            "trade": f"Trade with {target.name if target else 'someone'}" if target else "Trade",
            "steal": f"Steal from {target.name if target else 'someone'}" if target else "Steal",
            "cooperate": f"Cooperate with {target.name if target else 'someone'}" if target else "Cooperate",
            "share": f"Share with {target.name if target else 'someone'}" if target else "Share"
        }
        return messages.get(action, "Unknown action")
    
    def _idle_action(self) -> Dict:
        """Return idle action"""
        return {
            "action": "idle",
            "target": None,
            "message": "Idle",
            "resource_change_intent": 0,
            "is_lying": False
        }
