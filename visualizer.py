"""
Visualization system for console output, plots, and network graphs.
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Dict
from agent import Agent
from world import World
from event_system import EventLog
from trust_system import TrustSystem


class Visualizer:
    """Visualization and output system"""
    
    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"
    
    @staticmethod
    def print_header(text: str):
        """Print a styled header"""
        print("\n" + "=" * 70)
        print(f"{Visualizer.BOLD}{Visualizer.CYAN}{text}{Visualizer.RESET}")
        print("=" * 70 + "\n")
    
    @staticmethod
    def print_tick_header(tick: int):
        """Print tick header"""
        print(f"{Visualizer.BOLD}{Visualizer.BLUE}[TICK {tick}]{Visualizer.RESET}")
    
    @staticmethod
    def print_action(action: str, actor: str, target: str = None, result: str = ""):
        """Print an action in color"""
        action_icons = {
            "trade": "💱",
            "steal": "🔪",
            "cooperate": "🤝",
            "share": "💝",
            "idle": "😴"
        }
        
        icon = action_icons.get(action, "•")
        
        target_str = f" → {Visualizer.YELLOW}{target}{Visualizer.RESET}" if target else ""
        result_str = f" ({Visualizer.GREEN}{result}{Visualizer.RESET})" if result else ""
        
        print(
            f"  {icon} {Visualizer.CYAN}{actor}{Visualizer.RESET} "
            f"{Visualizer.BOLD}{action}{Visualizer.RESET}{target_str}{result_str}"
        )
    
    @staticmethod
    def print_summary(
        agents: List[Agent],
        world: World,
        event_log: EventLog,
        num_ticks: int,
        stability: float
    ):
        """Print final simulation summary"""
        
        Visualizer.print_header("SIMULATION SUMMARY")
        
        # Basic stats
        alive_count = sum(1 for a in agents if a.alive)
        total_resources = sum(a.resources for a in agents)
        avg_resources = total_resources / alive_count if alive_count > 0 else 0
        
        print(f"Simulation Duration: {num_ticks} ticks")
        print(f"Civilization Stability: {Visualizer.BOLD}{stability:.2f}/1.00{Visualizer.RESET}")
        print()
        
        # Agent rankings
        sorted_agents = sorted(agents, key=lambda a: a.total_reward, reverse=True)
        
        richest = sorted_agents[0]
        print(
            f"{Visualizer.GREEN}💰 Richest Agent: {Visualizer.BOLD}{richest.name}{Visualizer.RESET} "
            f"({richest.resources:.0f} resources, +{richest.total_reward:.1f} reward)"
        )
        
        trusted_agents = sorted(agents, key=lambda a: a.get_average_trust(), reverse=True)
        most_trusted = trusted_agents[0]
        print(
            f"{Visualizer.CYAN}🤝 Most Trusted Agent: {Visualizer.BOLD}{most_trusted.name}{Visualizer.RESET} "
            f"(avg trust: {most_trusted.get_average_trust():.2f})"
        )
        
        deceptive_agents = sorted(agents, key=lambda a: a.lie_count, reverse=True)
        most_deceptive = deceptive_agents[0]
        print(
            f"{Visualizer.RED}🎭 Most Deceptive Agent: {Visualizer.BOLD}{most_deceptive.name}{Visualizer.RESET} "
            f"(detected lies: {most_deceptive.lie_count})"
        )
        print()
        
        # Global stats
        print("Global Statistics:")
        print(f"  Total Resources: {total_resources:.0f}")
        print(f"  Average Resources: {avg_resources:.0f}")
        print(f"  Shared Pool: {world.shared_pool:.0f}")
        print(f"  Agents Alive: {alive_count}/{len(agents)}")
        print()
        
        # Event stats
        stats = event_log.get_summary_stats()
        print("Event Statistics:")
        print(f"  Total Events: {stats['total_events']}")
        print(f"  Total Actions: {stats['total_actions']}")
        print(f"  Success Rate: {stats['action_success_rate']*100:.1f}%")
        print()
        
        # Action breakdown
        print("Action Breakdown:")
        for action, count in sorted(stats['action_counts'].items(), key=lambda x: x[1], reverse=True):
            print(f"  - {action}: {count}")
        print()
        
        # Final rankings
        print(f"{Visualizer.BOLD}Final Rankings (by reward):{Visualizer.RESET}")
        for i, agent in enumerate(sorted_agents[:5], 1):
            print(f"  {i}. {agent.name}: {agent.total_reward:.1f} reward")
    
    @staticmethod
    def plot_resources_over_time(resource_history: Dict[str, List[float]]):
        """Plot resource accumulation over time"""
        plt.figure(figsize=(12, 6))
        
        for agent_id, history in resource_history.items():
            plt.plot(history, label=agent_id, linewidth=2)
        
        plt.xlabel("Tick", fontsize=12)
        plt.ylabel("Resources", fontsize=12)
        plt.title("Agent Resource Accumulation Over Time", fontsize=14, fontweight='bold')
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("resources_over_time.png", dpi=100)
        plt.close()
        
        print("✓ Saved: resources_over_time.png")
    
    @staticmethod
    def plot_pool_over_time(pool_history: List[float]):
        """Plot shared pool over time"""
        plt.figure(figsize=(12, 6))
        
        plt.plot(pool_history, color='steelblue', linewidth=2.5)
        plt.fill_between(range(len(pool_history)), pool_history, alpha=0.3, color='steelblue')
        
        plt.xlabel("Tick", fontsize=12)
        plt.ylabel("Resources in Pool", fontsize=12)
        plt.title("Shared Resource Pool Over Time", fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("pool_over_time.png", dpi=100)
        plt.close()
        
        print("✓ Saved: pool_over_time.png")
    
    @staticmethod
    def plot_stability_over_time(stability_history: List[float]):
        """Plot civilization stability metric"""
        plt.figure(figsize=(12, 6))
        
        plt.plot(stability_history, color='forestgreen', linewidth=2.5)
        plt.fill_between(range(len(stability_history)), stability_history, alpha=0.3, color='forestgreen')
        
        plt.axhline(y=0.5, color='orange', linestyle='--', label='Neutral')
        plt.axhline(y=0.7, color='green', linestyle='--', label='Healthy')
        
        plt.xlabel("Tick", fontsize=12)
        plt.ylabel("Stability Score (0-1)", fontsize=12)
        plt.title("Civilization Stability Over Time", fontsize=14, fontweight='bold')
        plt.legend(loc='best')
        plt.ylim(0, 1)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("stability_over_time.png", dpi=100)
        plt.close()
        
        print("✓ Saved: stability_over_time.png")
    
    @staticmethod
    def plot_trust_network(agents: List[Agent]):
        """Plot trust network graph using NetworkX"""
        G = nx.DiGraph()
        
        # Add nodes
        for agent in agents:
            G.add_node(agent.id)
        
        # Add edges with trust values
        for agent in agents:
            for target_id, trust in agent.trust_map.items():
                if trust != 0:  # Only show non-zero trust
                    G.add_edge(agent.id, target_id, weight=trust)
        
        # Draw
        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Draw positive trust edges (green)
        positive_edges = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] > 0.2]
        nx.draw_networkx_edges(
            G, pos,
            edgelist=positive_edges,
            edge_color='green',
            width=2,
            alpha=0.6,
            arrowsize=20,
            connectionstyle="arc3,rad=0.1"
        )
        
        # Draw negative trust edges (red, dashed)
        negative_edges = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] < -0.2]
        nx.draw_networkx_edges(
            G, pos,
            edgelist=negative_edges,
            edge_color='red',
            width=2,
            alpha=0.6,
            style='dashed',
            arrowsize=20,
            connectionstyle="arc3,rad=0.1"
        )
        
        # Draw nodes
        node_colors = []
        for agent in agents:
            avg_trust = agent.get_average_trust()
            if avg_trust > 0.2:
                node_colors.append('lightgreen')
            elif avg_trust < -0.2:
                node_colors.append('lightcoral')
            else:
                node_colors.append('lightgray')
        
        nx.draw_networkx_nodes(
            G, pos,
            node_color=node_colors,
            node_size=2000,
            alpha=0.9
        )
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        plt.title("Trust Network (Green=Positive, Red=Negative)", fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig("trust_network.png", dpi=100, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved: trust_network.png")
