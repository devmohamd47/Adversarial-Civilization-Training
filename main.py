"""
Main simulation orchestrator and entry point.

This module runs the complete adversarial civilization simulation with:
- 8-phase tick system
- Agent decision making and action resolution
- Trust updates and reward computation
- Environmental events and resource management
- Complete visualization and logging
"""

import random
import math
from typing import List, Dict, Tuple, Optional
from agent import Agent, Personality, ActionType
from world import World, EventType
from decision_engine import DecisionEngine
from trust_system import TrustSystem
from reward_system import RewardSystem
from event_system import EventLog
from visualizer import Visualizer


# ============ CONFIGURATION ============

NUM_AGENTS = 5
NUM_TICKS = 100
INITIAL_RESOURCES = 100
INITIAL_SHARED_RESOURCES = 500
MAX_RESOURCES_PER_AGENT = 500
RANDOM_SEED = 42


class CivilizationSimulation:
    """Main simulation engine"""
    
    def __init__(
        self,
        num_agents: int = 5,
        num_ticks: int = 100,
        initial_resources: float = 100,
        initial_pool: float = 500,
        random_seed: int = 42
    ):
        random.seed(random_seed)
        
        self.num_agents = num_agents
        self.num_ticks = num_ticks
        self.current_tick = 0
        
        # Initialize world and agents
        self.world = World(initial_pool=initial_pool)
        self.agents = self._create_agents(num_agents, initial_resources)
        self.decision_engine = DecisionEngine(exploration_rate=0.2)
        self.event_log = EventLog()
        
        # Tracking
        self.resource_history: Dict[str, List[float]] = {
            agent.id: [] for agent in self.agents
        }
        self.pool_history: List[float] = []
        self.stability_history: List[float] = []
        self.rewards_history: Dict[str, List[float]] = {
            agent.id: [] for agent in self.agents
        }
    
    def _create_agents(self, count: int, initial_resources: float) -> List[Agent]:
        """Create agents with random personalities"""
        agents = []
        for i in range(count):
            agent = Agent(
                id=f"Agent-{i}",
                name=f"Agent-{i}",
                resources=initial_resources,
                personality=Personality(
                    aggressiveness=random.uniform(0.2, 0.8),
                    cooperativeness=random.uniform(0.2, 0.8),
                    deceptiveness=random.uniform(0.1, 0.6),
                    greed=random.uniform(0.3, 0.9),
                    altruism=random.uniform(0.1, 0.7)
                )
            )
            agents.append(agent)
        
        # Initialize trust between all agents (neutral)
        for agent in agents:
            for other in agents:
                if agent.id != other.id:
                    agent.trust_map[other.id] = 0.0
        
        return agents
    
    def run(self):
        """Run the complete simulation"""
        Visualizer.print_header("ADVERSARIAL CIVILIZATION SIMULATION")
        
        print(f"Configuration:")
        print(f"  Agents: {self.num_agents}")
        print(f"  Ticks: {self.num_ticks}")
        print(f"  Initial resources per agent: {INITIAL_RESOURCES}")
        print(f"  Shared resource pool: {INITIAL_SHARED_RESOURCES}")
        print()
        
        # Main simulation loop
        for tick in range(self.num_ticks):
            self.current_tick = tick
            self._tick()
            
            # Print progress every 10 ticks
            if (tick + 1) % 10 == 0:
                print(f"✓ Completed tick {tick + 1}/{self.num_ticks}")
        
        # Generate summary and visualizations
        self._finalize()
    
    def _tick(self):
        """Execute one simulation tick with 8-phase system"""
        Visualizer.print_tick_header(self.current_tick)
        
        # PHASE 1: Agent decision making
        decisions = self._phase_decision_making()
        
        # PHASE 2: Action resolution
        self._phase_resolve_actions(decisions)
        
        # PHASE 3: Resource decay (metabolism)
        self._phase_resource_decay()
        
        # PHASE 4: Pool regeneration
        self._phase_pool_regeneration()
        
        # PHASE 5: Environmental events
        self._phase_environmental_events()
        
        # PHASE 6: Trust decay
        self._phase_trust_decay()
        
        # PHASE 7: Reward computation
        self._phase_reward_computation()
        
        # PHASE 8: History recording
        self._phase_history_recording()
    
    def _phase_decision_making(self) -> Dict:
        """PHASE 1: All agents make decisions"""
        decisions = {}
        
        for agent in self.agents:
            if not agent.alive:
                continue
            
            decision = self.decision_engine.decide(
                agent,
                [a for a in self.agents if a.id != agent.id and a.alive],
                self.world.get_pool_status(),
                self.world.shared_pool
            )
            
            decisions[agent.id] = decision
        
        return decisions
    
    def _phase_resolve_actions(self, decisions: Dict):
        """PHASE 2: Resolve all actions"""
        for agent_id, decision in decisions.items():
            agent = next(a for a in self.agents if a.id == agent_id)
            action = decision['action']
            target_id = decision.get('target')
            
            if action == ActionType.IDLE.value:
                self._execute_idle(agent)
            
            elif action == ActionType.TRADE.value:
                self._execute_trade(agent, target_id, decision)
            
            elif action == ActionType.STEAL.value:
                self._execute_steal(agent, target_id)
            
            elif action == ActionType.COOPERATE.value:
                self._execute_cooperate(agent, target_id)
            
            elif action == ActionType.SHARE.value:
                self._execute_share(agent, target_id)
    
    def _execute_idle(self, agent: Agent):
        """Execute idle action"""
        pass  # No effect
    
    def _execute_trade(self, agent: Agent, target_id: str, decision: Dict):
        """Execute trade action"""
        if not target_id:
            return
        
        target = next((a for a in self.agents if a.id == target_id), None)
        if not target or not target.alive:
            return
        
        trade_amount = min(20, agent.resources * 0.3)
        is_lying = decision.get('is_lying', False)
        
        if agent.resources >= trade_amount and target.resources >= trade_amount * 0.8:
            agent.resources -= trade_amount
            target.resources += trade_amount * 0.8
            agent.trade_count += 1
            
            if is_lying:
                agent.lie_count += 1
                was_detected = TrustSystem.detect_deception(agent, target, trade_amount * 1.2, trade_amount, [])
                if was_detected:
                    TrustSystem.update_trust_from_action(agent, target, ActionType.TRADE.value, is_lying, True)
                    self.event_log.log_action(
                        self.current_tick, agent.id, agent.name,
                        ActionType.TRADE.value, target_id, target.name,
                        f"Trade (lied, caught)", -trade_amount, False, -1.5
                    )
                else:
                    TrustSystem.update_trust_from_action(agent, target, ActionType.TRADE.value, is_lying, False)
                    self.event_log.log_action(
                        self.current_tick, agent.id, agent.name,
                        ActionType.TRADE.value, target_id, target.name,
                        f"Trade (lied, not caught)", -trade_amount, True, 1.5
                    )
            else:
                TrustSystem.update_trust_from_action(agent, target, ActionType.TRADE.value, False, False)
                self.event_log.log_action(
                    self.current_tick, agent.id, agent.name,
                    ActionType.TRADE.value, target_id, target.name,
                    f"Fair trade", -trade_amount, True, 2.0
                )
    
    def _execute_steal(self, agent: Agent, target_id: str):
        """Execute steal action"""
        if not target_id:
            return
        
        target = next((a for a in self.agents if a.id == target_id), None)
        if not target or not target.alive:
            return
        
        steal_amount = min(random.randint(10, 40), target.resources * 0.4)
        
        if steal_amount > 0:
            agent.resources += steal_amount
            target.resources -= steal_amount
            agent.steal_count += 1
            
            TrustSystem.update_trust_from_action(agent, target, ActionType.STEAL.value)
            
            self.event_log.log_action(
                self.current_tick, agent.id, agent.name,
                ActionType.STEAL.value, target_id, target.name,
                f"Stole {steal_amount:.0f}", steal_amount, True, -2.0
            )
    
    def _execute_cooperate(self, agent: Agent, target_id: str):
        """Execute cooperate action"""
        if not target_id:
            return
        
        target = next((a for a in self.agents if a.id == target_id), None)
        if not target or not target.alive:
            return
        
        investment = min(15, agent.resources * 0.15)
        
        if agent.resources >= investment:
            # Both benefit
            agent.resources -= investment
            agent.resources += investment * 1.2
            target.resources += investment * 0.8
            agent.cooperation_count += 1
            
            TrustSystem.update_trust_from_action(agent, target, ActionType.COOPERATE.value)
            
            self.event_log.log_action(
                self.current_tick, agent.id, agent.name,
                ActionType.COOPERATE.value, target_id, target.name,
                "Cooperation", -investment, True, 1.5
            )
    
    def _execute_share(self, agent: Agent, target_id: str):
        """Execute share action"""
        if not target_id:
            return
        
        target = next((a for a in self.agents if a.id == target_id), None)
        if not target or not target.alive:
            return
        
        share_amount = min(20, agent.resources * 0.2)
        
        if agent.resources >= share_amount:
            agent.resources -= share_amount
            target.resources += share_amount
            
            TrustSystem.update_trust_from_action(agent, target, ActionType.SHARE.value)
            
            self.event_log.log_action(
                self.current_tick, agent.id, agent.name,
                ActionType.SHARE.value, target_id, target.name,
                f"Shared {share_amount:.0f}", -share_amount, True, 1.0
            )
    
    def _phase_resource_decay(self):
        """PHASE 3: Resource decay (metabolism/upkeep)"""
        for agent in self.agents:
            if agent.alive:
                # Each agent "costs" 2-5 resources per tick to stay alive
                decay = random.uniform(2, 5)
                agent.resources = max(0, agent.resources - decay)
                
                # Death check
                if agent.resources <= 0:
                    agent.alive = False
    
    def _phase_pool_regeneration(self):
        """PHASE 4: Pool regeneration"""
        self.world.tick()
    
    def _phase_environmental_events(self):
        """PHASE 5: Environmental events"""
        event = self.world.tick()
        
        if event:
            print(f"  🌍 {event.description}")
            self.event_log.log_event(
                self.current_tick,
                event.event_type.value,
                event.description,
                event.magnitude
            )
            
            # Apply effects
            if event.event_type == EventType.FEAST:
                for agent in self.agents:
                    if agent.alive:
                        agent.resources += random.uniform(20, 40)
            
            elif event.event_type == EventType.PLAGUE:
                for agent in self.agents:
                    if agent.alive:
                        agent.resources -= random.uniform(20, 40)
    
    def _phase_trust_decay(self):
        """PHASE 6: Trust decay over time"""
        TrustSystem.apply_trust_decay(self.agents)
    
    def _phase_reward_computation(self):
        """PHASE 7: Reward computation"""
        for agent in self.agents:
            if agent.alive:
                action_reward = RewardSystem.compute_wealth_reward(agent)
                action_reward += RewardSystem.compute_survival_reward(agent)
                RewardSystem.update_agent_reward(agent, "", action_reward)
    
    def _phase_history_recording(self):
        """PHASE 8: Record history"""
        for agent in self.agents:
            self.resource_history[agent.id].append(agent.resources)
            self.rewards_history[agent.id].append(agent.total_reward)
        
        self.pool_history.append(self.world.shared_pool)
        
        # Compute stability
        stability = self._compute_stability()
        self.stability_history.append(stability)
    
    def _compute_stability(self) -> float:
        """
        Compute civilization stability score (0-1)
        Based on: trust, equality, cooperation, survival
        """
        # Trust metric (20%)
        trust_stats = TrustSystem.get_trust_network_stats(self.agents)
        trust_score = trust_stats.get('network_health', 0.5)
        
        # Equality metric (20%)
        resources = [a.resources for a in self.agents if a.alive]
        if resources:
            avg_resources = sum(resources) / len(resources)
            variance = sum((r - avg_resources) ** 2 for r in resources) / len(resources)
            equality_score = 1.0 / (1.0 + variance / 1000)
        else:
            equality_score = 0.0
        
        # Cooperation metric (20%)
        total_coop = sum(a.cooperation_count for a in self.agents)
        total_steal = sum(a.steal_count for a in self.agents)
        if total_coop + total_steal > 0:
            coop_score = total_coop / (total_coop + total_steal)
        else:
            coop_score = 0.5
        
        # Survival metric (20%)
        alive_count = sum(1 for a in self.agents if a.alive)
        survival_score = alive_count / self.num_agents
        
        # Wealth metric (20%)
        wealth = sum(a.resources for a in self.agents)
        wealth_score = min(1.0, wealth / (self.num_agents * INITIAL_RESOURCES))
        
        stability = (
            trust_score * 0.2 +
            equality_score * 0.2 +
            coop_score * 0.2 +
            survival_score * 0.2 +
            wealth_score * 0.2
        )
        
        return stability
    
    def _finalize(self):
        """Generate final summary and visualizations"""
        print("\n")
        
        # Print summary
        final_stability = self._compute_stability()
        Visualizer.print_summary(
            self.agents,
            self.world,
            self.event_log,
            self.num_ticks,
            final_stability
        )
        
        # Export event log
        self.event_log.export_to_json("simulation_events.json")
        print("\n✅ Exported: simulation_events.json")
        
        # Generate visualizations
        print("\n📊 Generating visualizations...")
        Visualizer.plot_resources_over_time(self.resource_history)
        Visualizer.plot_pool_over_time(self.pool_history)
        Visualizer.plot_stability_over_time(self.stability_history)
        Visualizer.plot_trust_network(self.agents)
        
        print("\n" + "=" * 70)
        print("✨ Simulation complete!")
        print("=" * 70)


def main():
    """Main entry point"""
    sim = CivilizationSimulation(
        num_agents=NUM_AGENTS,
        num_ticks=NUM_TICKS,
        initial_resources=INITIAL_RESOURCES,
        initial_pool=INITIAL_SHARED_RESOURCES,
        random_seed=RANDOM_SEED
    )
    
    sim.run()


if __name__ == "__main__":
    main()
