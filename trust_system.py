"""
Trust system with dynamic updates and deception detection.
"""

from typing import List, Dict, Tuple
from agent import Agent, ActionType


class TrustSystem:
    """Manages trust relationships and deception detection"""
    
    # Trust update constants
    COOPERATION_BONUS = 0.15
    BETRAYAL_PENALTY = -0.50
    LIE_PENALTY = -0.30
    SHARE_BONUS = 0.10
    TRUST_DECAY = 0.98  # Multiply by this each tick
    
    @staticmethod
    def update_trust_from_action(
        agent: Agent,
        target: Agent,
        action: str,
        is_lying: bool = False,
        was_detected: bool = False
    ):
        """Update trust based on action outcome"""
        
        if action == ActionType.TRADE.value:
            if is_lying and was_detected:
                agent.update_trust(target.id, TrustSystem.LIE_PENALTY)
            else:
                agent.update_trust(target.id, TrustSystem.COOPERATION_BONUS)
            target.update_trust(agent.id, TrustSystem.COOPERATION_BONUS)
        
        elif action == ActionType.STEAL.value:
            agent.update_trust(target.id, TrustSystem.BETRAYAL_PENALTY)
            target.update_trust(agent.id, TrustSystem.BETRAYAL_PENALTY)
        
        elif action == ActionType.COOPERATE.value:
            agent.update_trust(target.id, TrustSystem.COOPERATION_BONUS * 1.2)
            target.update_trust(agent.id, TrustSystem.COOPERATION_BONUS * 1.2)
        
        elif action == ActionType.SHARE.value:
            agent.update_trust(target.id, TrustSystem.SHARE_BONUS)
            target.update_trust(agent.id, TrustSystem.COOPERATION_BONUS)
    
    @staticmethod
    def detect_deception(
        actor: Agent,
        target: Agent,
        claimed_amount: float,
        actual_amount: float,
        past_claims: List[float]
    ) -> bool:
        """
        Multi-layer deception detection.
        
        Returns True if deception detected.
        """
        
        # Layer 1: Inflation check
        # If claimed is significantly more than actual, likely lying
        if claimed_amount > actual_amount * 1.5:
            return True
        
        # Layer 2: Resource ceiling check
        # Can't claim more than physically possible
        max_possible = actual_amount * 2.0
        if claimed_amount > max_possible:
            return True
        
        # Layer 3: Historical inconsistency
        # Check against past claims
        if past_claims:
            avg_past = sum(past_claims[-5:]) / min(5, len(past_claims))
            if claimed_amount > avg_past * 2.5:  # Huge jump
                return True
        
        # Layer 4: Behavior pattern
        # If actor has high lie count, increase suspicion
        if actor.lie_count > 5:
            # Increase detection rate for repeat liars
            if actor.lie_count / max(1, actor.trade_count + actor.cooperation_count) > 0.4:
                return True  # >40% lie rate = flagged
        
        return False
    
    @staticmethod
    def apply_trust_decay(agents: List[Agent]):
        """Apply trust decay over time (fading memories)"""
        for agent in agents:
            for other_id in agent.trust_map:
                # Decay all trust toward center (0.0)
                agent.trust_map[other_id] *= TrustSystem.TRUST_DECAY
    
    @staticmethod
    def get_trust_network_stats(agents: List[Agent]) -> Dict:
        """Get statistics about the trust network"""
        if not agents:
            return {}
        
        all_trusts = []
        positive_count = 0
        negative_count = 0
        
        for agent in agents:
            for trust_val in agent.trust_map.values():
                all_trusts.append(trust_val)
                if trust_val > 0.2:
                    positive_count += 1
                elif trust_val < -0.2:
                    negative_count += 1
        
        if not all_trusts:
            return {
                'average_trust': 0.0,
                'network_health': 0.5,
                'positive_edges': 0,
                'negative_edges': 0
            }
        
        avg_trust = sum(all_trusts) / len(all_trusts)
        health = (positive_count - negative_count) / max(1, positive_count + negative_count)
        health = (health + 1.0) / 2.0  # Normalize to 0-1
        
        return {
            'average_trust': avg_trust,
            'network_health': health,
            'positive_edges': positive_count,
            'negative_edges': negative_count
        }
