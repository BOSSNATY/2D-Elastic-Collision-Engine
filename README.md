# 2D Elastic Puck Collision Simulation

## Project Overview

This project simulates a **two–dimensional elastic collision between two pucks** using Python and VPython. The objective is to model the motion of two circular objects moving on a frictionless surface and verify the **conservation of momentum and kinetic energy** during their collision.

The simulation demonstrates how physical systems can be modeled using **numerical methods and vector mechanics**, rather than relying on pre-solved algebraic formulas.

The program visualizes the collision in real time and records the system's **total kinetic energy and momentum** to confirm that these quantities remain constant during an elastic interaction.

---

## Objectives

The goals of this project are to:

- Simulate a **2D elastic collision** between two pucks.
- Implement **numerical time integration** to update motion.
- Apply **conservation of momentum** in two dimensions.
- Verify **conservation of kinetic energy** in an elastic system.
- Visualize the system using **VPython**.
- Plot system properties using **Matplotlib**.

---

## Physics Concepts

### Elastic Collision

An elastic collision is a collision in which **both momentum and kinetic energy are conserved**.

For two objects with masses (m_1) and (m_2) and velocities (v_1) and (v_2):

**Momentum conservation**

p = m_1*v_1 + m_2*v_2 = m_1*v_1' + m_2*v_2'

**Kinetic energy conservation**

KE = 1/2*m_1*(v_1)^2 + 1/2*m_2*(v_2)^2 =1/2*m_1*(v_1')^2 + 1/2*m_2*(v_2')^2

Because the system is **two-dimensional**, velocities are treated as **vectors** and collisions occur along the **line connecting the centers of the pucks**.

---

## Computational Approach

The simulation uses **step-by-step numerical integration**.

At each time step:

1. Update puck positions using their current velocities.
2. Check the distance between the two puck centers.
3. If the distance is less than the sum of their radii, a collision occurs.
4. Compute the **collision normal vector**.
5. Apply the **2D elastic collision equations** to update velocities.
6. Record kinetic energy and momentum values.

The process repeats until the simulation time is complete.

---

## Software and Tools

This project uses the following technologies:

- **Python**
- **VPython** – real-time physics visualization
- **Matplotlib** – plotting physical quantities
- **GitHub** – version control and project hosting

---

## Repository Structure

```
project-folder
│
├── collision_simulation.py   # Main VPython simulation script
├── README.md                 # Project documentation

```

---

## Simulation Features

The program includes:

- Real-time **2D visualization of puck motion**
- **Collision detection and resolution**
- **Momentum and kinetic energy calculations**
- **Trajectory trails** for each puck
- Graphs showing:
  - Kinetic Energy vs Time
  - Momentum Magnitude vs Time

---

## Expected Results

Because the collision is **elastic**, the following should occur:

- **Total momentum remains constant**
- **Total kinetic energy remains constant**
- Pucks change direction after collision according to conservation laws

Small fluctuations may occur due to **numerical time stepping**, but the overall quantities remain nearly constant.

---

## How to Run the Simulation

1. Install required libraries:

```bash
pip install vpython matplotlib
```

2. Run the script:

```bash
python collision_simulation.py
```

3. A VPython window will open showing the puck collision.

After the simulation finishes, graphs of **kinetic energy** and **momentum** will be displayed.

**Note that if you don't have enough time to install the above modules, you can directly go to this website to run the program of the simulation:https://www.glowscript.org/#/user/bossnaty/folder/MyPrograms/program/2D-Elastic-Collision-Engine**

## Conclusion

This project demonstrates how **computational physics techniques** can simulate real physical systems. By applying vector mechanics and conservation laws, the program successfully models a **2D elastic collision** and verifies the expected physical behavior through numerical results and visualization.

---

## Authors

Project completed by students as part of a **physics assignment** involving numerical simulation and visualization.
