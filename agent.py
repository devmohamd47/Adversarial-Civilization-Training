"""
Agent class with personality, state, and capabilities.
"""

from enum import Enum
from typing import Dict, List
from dataclasses import dataclass, field
import random


class ActionType(Enum):
    """Available agent actions"""
    IDLE = "idle"
    TRADE = "trade"
    STEAL = "steal"
    COOPERATE = "cooperate"
    SHARE = "share"


@dataclass
class Personality:
    """Agent personality vector"""
    aggressiveness: float      # 0-1: tendency to steal/conflict
    cooperativeness: float     # 0-1: tendency to cooperate/share
    deceptiveness: float       # 0-1: tendency to lie
    greed: float              # 0-1: resource accumulation drive
    altruism: float           # 0-1: tendency to help others


class Agent:
    """Individual agent in the civilization"""
    
    def __init__(
        self,
        id: str,
        name: str,
        resources: float,
        personality: Personality = None
    ):
        self.id = id
        self.name = name
        self.resources = resources
        self.alive = True
        
        # Personality
        self.personality = personality or Personality(
            aggressiveness=random.uniform(0.3, 0.7),
            cooperativeness=random.uniform(0.3, 0.7),
            deceptiveness=random.uniform(0.2, 0.6),
            greed=random.uniform(0.3, 0.7),
            altruism=random.uniform(0.2, 0.6)
        )
        
        # State
        self.trust_map: Dict[str, float] = {}      # agent_id -> trust (-1 to 1)
        self.memory: List[Dict] = []               # Past events
        
        # Tracking
        self.trade_count = 0
        self.steal_count = 0
        self.cooperation_count = 0
        self.lie_count = 0
        self.total_reward = 0.0
        self.last_action = None
    
    def update_trust(self, other_id: str, delta: float):
        """Update trust toward another agent"""
        if other_id not in self.trust_map:
            self.trust_map[other_id] = 0.0
        
        self.trust_map[other_id] = max(-1.0, min(1.0, self.trust_map[other_id] + delta))
    
    def get_average_trust(self) -> float:
        """Get average trust level"""
        if not self.trust_map:
            return 0.0
        return sum(self.trust_map.values()) / len(self.trust_map)
    
    def add_memory(self, event: Dict):
        """Add event to memory"""
        self.memory.append(event)
        # Keep only recent 50 memories
        if len(self.memory) > 50:
            self.memory.pop(0)
    
    def get_trust_toward(self, other_id: str) -> float:
        """Get trust value toward specific agent"""
        return self.trust_map.get(other_id, 0.0)
    
    def set_trust_toward(self, other_id: str, value: float):
        """Set trust value toward specific agent"""
        self.trust_map[other_id] = max(-1.0, min(1.0, value))
