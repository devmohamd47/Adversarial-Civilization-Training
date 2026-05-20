"""
World system with environmental events and resource management.
"""

import random
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class EventType(Enum):
    """Types of environmental events"""
    ABUNDANCE = "abundance"
    SCARCITY = "scarcity"
    PLAGUE = "plague"
    FEAST = "feast"
    DROUGHT = "drought"


@dataclass
class Event:
    """Environmental event"""
    event_type: EventType
    description: str
    magnitude: float


class World:
    """Simulated world with resources and events"""
    
    def __init__(self, initial_pool: float = 500):
        self.shared_pool = initial_pool
        self.max_pool = initial_pool * 2
        self.event_tick = 0
        self.regeneration_rate = 5.0  # Resources per tick
        self.decay_rate = 0.02         # Decay percentage
    
    def tick(self) -> Optional[Event]:
        """Execute one world tick and return any events"""
        # Pool decay
        self.shared_pool *= (1 - self.decay_rate)
        
        # Pool regeneration
        self.shared_pool = min(self.max_pool, self.shared_pool + self.regeneration_rate)
        
        # Environmental events (10% per tick)
        if random.random() < 0.1:
            return self._generate_event()
        
        return None
    
    def _generate_event(self) -> Event:
        """Generate random environmental event"""
        event_type = random.choice(list(EventType))
        
        if event_type == EventType.ABUNDANCE:
            magnitude = random.uniform(50, 120)
            self.shared_pool += magnitude
            return Event(
                event_type=EventType.ABUNDANCE,
                description=f"🌾 Abundance! +{magnitude:.0f} resources to pool",
                magnitude=magnitude
            )
        
        elif event_type == EventType.SCARCITY:
            magnitude = random.uniform(30, 80)
            self.shared_pool = max(0, self.shared_pool - magnitude)
            return Event(
                event_type=EventType.SCARCITY,
                description=f"🏜️  Scarcity! -{magnitude:.0f} resources from pool",
                magnitude=-magnitude
            )
        
        elif event_type == EventType.PLAGUE:
            magnitude = random.uniform(20, 60)
            self.shared_pool = max(0, self.shared_pool - magnitude * 0.5)
            return Event(
                event_type=EventType.PLAGUE,
                description=f"💀 Plague! Population affected",
                magnitude=-magnitude
            )
        
        elif event_type == EventType.FEAST:
            magnitude = random.uniform(40, 100)
            self.shared_pool += magnitude
            return Event(
                event_type=EventType.FEAST,
                description=f"🍽️  Feast! +{magnitude:.0f} resources",
                magnitude=magnitude
            )
        
        else:  # DROUGHT
            magnitude = random.uniform(40, 100)
            self.shared_pool = max(0, self.shared_pool - magnitude)
            return Event(
                event_type=EventType.DROUGHT,
                description=f"☠️  Drought! Pool depleted",
                magnitude=-magnitude
            )
    
    def get_pool_status(self) -> str:
        """Get pool status as string"""
        if self.shared_pool > self.max_pool * 0.7:
            return "abundant"
        elif self.shared_pool > self.max_pool * 0.4:
            return "normal"
        else:
            return "scarce"
