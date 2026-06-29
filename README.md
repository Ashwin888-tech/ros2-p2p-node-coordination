# ROS 2 Peer-to-Peer Node Coordination (Core Scripts)

A lightweight repository containing the core Python execution logic for direct, multi-device node communication and state synchronization using ROS 2 Humble.

## 📌 Project Overview
This repository serves as a code showcase for a 3rd Year BTech Electronics and Communication Engineering (ECE) project milestone. It isolates the algorithmic logic required to achieve peer-to-peer telemetry sharing and spatial state-switching without the overhead of complete ROS 2 workspace directory structures.

### Core Scripts
- `luv_node.py`: Logic for Node 1 (ID: 1). Tracks relative coordinates and handles dynamic role switching.
- `kush_node.py`: Logic for Node 2 (ID: 2). Tracks relative coordinates and mirrors the state machine behaviors.

---

## ⚙️ Algorithmic State Machine

The two nodes exchange telemetry data over a shared network fabric via the `/swarm_status` topic matrix. They compare their local coordinates against a hardcoded target point $(50.0, 50.0)$ to dynamically negotiate active and passive roles.



### Behavioral Rules:
1. **Role Election:** The node calculated to be physically closer to the destination target automatically self-elects as the `LEADER`. The remaining node transitions into a `FOLLOWER` state.
2. **Dynamic Velocity Control:** The `LEADER` node moves at full execution speed, while the `FOLLOWER` throttles down to half-speed to preserve formation metrics.
3. **Mission Lock:** Once initial roles are assigned and movement begins, a logic lock prevents the nodes from constantly flickering roles back and forth.
4. **Automated Termination:** When the threshold distance to the target drops below 1.0 unit, the nodes broadcast a termination flag, exit the operational loop, and stop automatically.

---

## 🛠️ Network and Communication Fabric

To run these scripts across two independent physical devices (e.g., separate laptops) on a common Wi-Fi local area network, the underlying ROS 2 Data Distribution Service (DDS) layer must be segmented.



### Custom Message Dependencies
Both nodes utilize a custom message structure (`RobotState`) broadcasting on the `/swarm_status` topic with a standard Quality of Service (QoS) history depth queue of `10`. The data frames transfer the following fields:
* `int32 id` (Unique node identifier)
* `float64 x` (Current X-axis coordinate)
* `float64 y` (Current Y-axis coordinate)
* `string status` (Current operational state: `SEARCHING`, `LEADER`, `FOLLOWER`, or `TASK_COMPLETE`)

### Port Isolation Commands
To prevent cross-talk with outside ROS 2 devices sharing the same Wi-Fi access point subnet, both execution terminals must map to a matching domain ID before launch:

```bash
export ROS_DOMAIN_ID=30
