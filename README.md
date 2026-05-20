# Adversarial Civilization Training

A fully functional multi-agent adversarial civilization simulation built in Python.

## 🎯 Overview

This project implements a minimal but complete MVP of a multi-agent civilization with:

- **Multiple AI Agents**: 5+ agents with individual personalities and state
- **Simple Economy**: Resource trading, stealing, and sharing mechanics
- **Communication System**: Agents can trade promises and lies
- **Trust Mechanics**: Dynamic trust updates based on past interactions
- **Deception System**: Agents can lie with detection mechanisms
- **Reinforcement Learning Layer**: Simple reward system for agent actions
- **Environmental Events**: Random events (abundance, plague, drought, feast) affect the world
- **Visualization**: Real-time console output + matplotlib graphs + network visualization

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Simulation

```bash
python main.py
```

This will:
1. Run 100 ticks of simulation with 5 agents
2. Print real-time action logs to console
3. Generate final summary with rankings
4. Export event log as JSON
5. Generate 4 PNG visualizations (resources, pool, stability, trust network)

## 📊 Output Files

After running, you'll find:

- `simulation_events.json`: Complete replay log of all events
- `resources_over_time.png`: Resource accumulation chart
- `pool_over_time.png`: Shared pool dynamics
- `stability_over_time.png`: Civilization stability score over time
- `trust_network.png`: Network graph of trust relationships

## 🏗️ Architecture

```
├── main.py                  # Entry point & simulation loop
├── agent.py                 # Agent class with personality
├── world.py                 # World simulation & events
├── decision_engine.py       # Rule-based decision making
├── trust_system.py          # Trust updates & deception detection
├── reward_system.py         # RL-style reward computation
├── event_system.py          # Event logging & replay
└── visualizer.py            # Console & matplotlib output
```

### Core Components

**Agent** (`agent.py`):
- State: id, name, resources, trust_map, memory, personality
- Capabilities: trade, steal, cooperate, share, lie, decide_action
- Personality vector: aggressiveness, cooperativeness, deceptiveness, greed, altruism

**World** (`world.py`):
- Shared resource pool with regeneration/decay
- Environmental events (abundance, scarcity, plague, feast, drought)
- Discrete time-step simulation

**Decision Engine** (`decision_engine.py`):
- Rule-based policy evaluating 5+ action options
- Personality-weighted action selection
- Output: structured action dict with target, message, resource intent

**Trust System** (`trust_system.py`):
- Dynamic trust updates: cooperation (+0.15), betrayal (-0.50), detected lies (-0.30)
- Multi-layered deception detection (historical inconsistency, inflation checks, behavior patterns)
- Trust decay over time for fading memories

**Reward System** (`reward_system.py`):
- Per-action rewards: trades (+2.0), cooperation (+1.5), sharing (+1.0)
- Per-action penalties: theft (-2.0), deception (-1.5)
- Survival & wealth accumulation bonuses

**Event System** (`event_system.py`):
- Complete event logging with JSON export
- Event filtering by agent, tick, or action type

**Visualizer** (`visualizer.py`):
- Console output with colored events
- 4 matplotlib plots: resources, pool, stability, trust network
- Network graph using NetworkX

## 🎮 Example Output

```
======================================================================
     ADVERSARIAL CIVILIZATION SIMULATION
======================================================================

Configuration:
  Agents: 5
  Ticks: 100
  Initial resources per agent: 100
  Shared resource pool: 500

[TICK 1]
  🌍 Abundance! +87 resources to pool
  Actions: cooperate(1), trade(2), idle(2)
  Top agents: Agent-2(145), Agent-0(130), Agent-4(115)

[TICK 2]
  🌍 Scarcity! -65 resources from pool
  Actions: steal(1), trade(1), share(1), idle(2)
  Top agents: Agent-1(210), Agent-2(140), Agent-3(95)

...

======================================================================
     SIMULATION SUMMARY
======================================================================

Simulation Duration: 100 ticks
Civilization Stability: 0.68/1.00

💰 Richest Agent: Agent-1
   Resources: 342
   Accumulated Reward: 87.3

🤝 Most Trusted Agent: Agent-3
   Average Trust from Others: 0.52

🎭 Most Deceptive Agent: Agent-2
   Detected Lies: 8

📊 Global Statistics:
   Total Resources in Civilization: 1245
   Average Resources per Agent: 249
   Average Trust Level: 0.12

📋 Event Statistics:
   Total Events: 487
   Success Rate: 72.3%
   Action Breakdown:
     - idle: 234
     - trade: 123
     - steal: 89
     - cooperate: 34
     - share: 7

🏆 Final Rankings:
   1. Agent-1: 87.3 reward
   2. Agent-3: 65.4 reward
   3. Agent-2: 54.1 reward
   4. Agent-4: 45.2 reward
   5. Agent-0: 38.9 reward

======================================================================
```

## ⚙️ Configuration

Edit `main.py` to customize simulation:

```python
NUM_AGENTS = 5              # Number of agents
NUM_TICKS = 100             # Simulation length (ticks)
INITIAL_RESOURCES = 100     # Starting resources per agent
INITIAL_SHARED_RESOURCES = 500  # Shared pool size
MAX_RESOURCES_PER_AGENT = 500   # Resource cap per agent
RANDOM_SEED = 42            # Reproducibility
```

## 📈 Key Metrics

### Civilization Stability Score (0-1)

Computed from:
- **Trust Stability** (25%): Average trust centrality in network
- **Resource Equality** (25%): Inverse of resource inequality
- **Survival Rate** (25%): Percentage of agents alive
- **Cooperation Rate** (25%): Successful cooperations vs conflicts

### Agent Metrics

- **Total Reward**: Cumulative reward from all actions
- **Average Trust**: How much others trust this agent
- **Lie Count**: Number of detected deceptions
- **Resource Accumulation**: Wealth over time

## 🎨 Visualization Examples

### Resources Over Time
Shows each agent's resource trajectory. Look for:
- Wealth inequality growth
- Sudden drops from theft
- Gains from successful trades

### Trust Network
Network graph with:
- **Green edges** = positive trust (cooperation likely)
- **Red dashed edges** = negative trust (conflict likely)
- Arrow thickness = strength of trust

### Stability Over Time
Civilization health metric combining trust, equality, cooperation.

## 🧠 Emergent Behaviors

The simulation naturally produces:

1. **Trust Evolution**: Repeated interactions build or destroy trust
2. **Deception Strategies**: Agents learn when lying is profitable
3. **Cooperation Clusters**: Similar personalities team up
4. **Resource Inequality**: Wealth naturally concentrates
5. **Betrayal Spirals**: Once trust breaks, retaliation escalates
6. **Personality Matching**: Aggressive agents clash, cooperatives align

## 🔬 Advanced Features

- **Personality Vectors**: 5 traits control agent behavior
- **Memory System**: Agents remember past interactions
- **Multi-layer Deception Detection**: Pattern recognition + consistency checks
- **Dynamic Civilization Stability**: Combined health metric
- **Environmental Events**: 5 types of world events
- **Complete Event Replay**: JSON export of all events

## 📊 Performance

- 5 agents, 100 ticks: ~0.5 seconds
- 10 agents, 1000 ticks: ~5 seconds
- Scales linearly O(n*t)

## 🤝 Extensibility

Easy to extend:

```python
# Add new action type in decision_engine.py
def _evaluate_blackmail(self, agent, other_agents):
    return {...}

# Add new agent trait
personality.manipulativeness = random.uniform(0.1, 0.9)

# Add new event type in world.py
EventType.INVASION = "invasion"

# Add custom visualization
visualizer.plot_deception_rate_over_time()
```

## 📚 Files Reference

| File | Purpose | Lines |
|------|---------|-------|
| main.py | Simulation orchestrator + loop | 350 |
| agent.py | Agent class + personality | 200 |
| world.py | World + events + resource management | 180 |
| decision_engine.py | Rule-based decision making | 170 |
| trust_system.py | Trust updates + deception detection | 200 |
| reward_system.py | RL reward computation | 150 |
| event_system.py | Event logging + replay | 120 |
| visualizer.py | Plots + network graphs + console output | 280 |

**Total: ~1,650 lines of production-ready Python**

## ⚡ Key Algorithms

### Trust Update
```
trust[other] += delta (clamped to [-1, 1])
- Successful trade/cooperate: +0.15
- Theft/betrayal: -0.50
- Detected lie: -0.30
- Decay over time: × (1 - 0.02)
```

### Deception Detection
Multi-layer checks:
1. Historical inconsistency (claimed vs actual past resources)
2. Resource inflation (claimed > max_resources * 1.2)
3. Behavior patterns (>40% lie rate = flagged)

### Decision Making
1. Evaluate all possible actions
2. Weight by personality fit
3. 80% pick best, 20% explore
4. Execute with resolution + conflict handling

## 🎓 What You Learn

- Multi-agent system design
- Game theory in distributed systems
- Trust metrics + deception detection
- Event-driven simulation
- Personality-driven behavior
- Network analysis
- Data visualization
- Reinforcement learning basics

## 📝 License

This project is provided as-is for educational and research purposes.

## 🚀 Future Enhancements

- LLM-driven decision making (GPT-4 API integration)
- Coalition formation mechanics
- Governance systems (voting, rules)
- More sophisticated negotiation
- Multi-currency economies
- Spatial/territorial aspects
- Genetic algorithm optimization
