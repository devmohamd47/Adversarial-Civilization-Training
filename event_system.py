"""
Event logging system with JSON export and replay.
"""

import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ActionEvent:
    """Single action event record"""
    tick: int
    actor_id: str
    actor_name: str
    action: str
    target_id: Optional[str]
    target_name: Optional[str]
    description: str
    resource_delta: float
    success: bool
    reward: float


class EventLog:
    """Complete event logging system"""
    
    def __init__(self):
        self.events: List[Dict] = []
        self.action_events: List[ActionEvent] = []
        self.environmental_events: List[Dict] = []
    
    def log_action(
        self,
        tick: int,
        actor_id: str,
        actor_name: str,
        action: str,
        target_id: Optional[str],
        target_name: Optional[str],
        description: str,
        resource_delta: float,
        success: bool,
        reward: float
    ):
        """Log an action event"""
        event = ActionEvent(
            tick=tick,
            actor_id=actor_id,
            actor_name=actor_name,
            action=action,
            target_id=target_id,
            target_name=target_name,
            description=description,
            resource_delta=resource_delta,
            success=success,
            reward=reward
        )
        self.action_events.append(event)
        self.events.append(asdict(event))
    
    def log_event(
        self,
        tick: int,
        event_type: str,
        description: str,
        magnitude: float
    ):
        """Log an environmental event"""
        event = {
            "tick": tick,
            "type": "environmental",
            "event_type": event_type,
            "description": description,
            "magnitude": magnitude
        }
        self.environmental_events.append(event)
        self.events.append(event)
    
    def get_events_by_agent(self, agent_id: str) -> List[Dict]:
        """Get all events involving a specific agent"""
        return [
            e for e in self.events
            if e.get("actor_id") == agent_id or e.get("target_id") == agent_id
        ]
    
    def get_events_by_action(self, action: str) -> List[Dict]:
        """Get all events of a specific action type"""
        return [e for e in self.events if e.get("action") == action]
    
    def get_events_by_tick(self, tick: int) -> List[Dict]:
        """Get all events in a specific tick"""
        return [e for e in self.events if e.get("tick") == tick]
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics"""
        action_count = len(self.action_events)
        success_count = sum(1 for e in self.action_events if e.success)
        
        action_counts = {}
        for event in self.action_events:
            action_counts[event.action] = action_counts.get(event.action, 0) + 1
        
        success_rate = success_count / action_count if action_count > 0 else 0
        
        return {
            "total_events": len(self.events),
            "total_actions": action_count,
            "action_counts": action_counts,
            "action_success_rate": success_rate
        }
    
    def export_to_json(self, filename: str = "simulation_events.json"):
        """Export all events to JSON file"""
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "total_events": len(self.events),
            "action_events": [asdict(e) for e in self.action_events],
            "environmental_events": self.environmental_events,
            "summary_stats": self.get_summary_stats()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
