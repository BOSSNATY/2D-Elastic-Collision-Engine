from vpython import *
import matplotlib.pyplot as plt

# ==================== SCENE SETUP ====================
scene = canvas(title='2D Elastic Puck Collision – Euler Method',
               width=900, height=700, background=color.black)
scene.forward = vector(0, -0.2, -1)
scene.range = 12
scene.autoscale = False

# ==================== PARAMETERS ====================
dt = 5e-4          # small time step for stability
k = 2500           # stiff spring constant
r = 1.2            # puck radius
m1 = m2 = 2.0      # masses
damping = 0.0      # optional damping

# ==================== CREATE PUCKS ====================
puck1 = sphere(pos=vector(-5, -2, 0), radius=r, color=color.cyan,
               make_trail=True, trail_type="points", interval=5, retain=200)
puck1.m = m1
puck1.v = vector(4.0, 2.0, 0)  # velocity in x and y

puck2 = sphere(pos=vector(5, 2, 0), radius=r, color=color.orange,
               make_trail=True, trail_type="points", interval=5, retain=200)
puck2.m = m2
puck2.v = vector(-3.0, -1.5, 0)  # velocity in x and y

# ==================== LABELS ====================
ke_label = wtext(text='\nKinetic Energy: calculating...')
mom_label = wtext(text='\nMomentum magnitude: calculating...')

# ==================== DATA LISTS ====================
time_list = []
KE_list = []
momentum_list = []

# ==================== SIMULATION LOOP ====================
t = 0
t_last = 0
t_max = 5.0  # simulate 5 seconds

while t < t_max:
    rate(500)  # controls simulation speed

    # Compute relative position and overlap
    r_rel = puck2.pos - puck1.pos
    dist = mag(r_rel)
    overlap = max(0, 2*r - dist)
    overlap = min(overlap, 0.5*r)  # cap extreme overlap

    a1 = vector(0,0,0)
    a2 = vector(0,0,0)

    if overlap > 0:
        # Force along the line connecting puck centers
        unit = r_rel / dist
        F_mag = k * overlap
        F_on2 = F_mag * unit
        F_on1 = -F_on2

        # Damping (optional)
        v_rel = puck2.v - puck1.v
        F_damp = damping * dot(v_rel, unit) * unit
        F_on2 += F_damp
        F_on1 -= F_damp

        # Acceleration
        a1 = F_on1 / puck1.m
        a2 = F_on2 / puck2.m

    # Euler integration (velocity then position)
    puck1.v += a1 * dt
    puck2.v += a2 * dt

    puck1.pos += puck1.v * dt
    puck2.pos += puck2.v * dt

    t += dt
    if t - t_last > 0.02:  # record every 0.02s
        KE = 0.5*puck1.m*mag2(puck1.v) + 0.5*puck2.m*mag2(puck2.v)
        mom_mag = mag(puck1.m*puck1.v + puck2.m*puck2.v)

        ke_label.text = f'\nKinetic Energy: {KE:>9.3f} J'
        mom_label.text = f'\nMomentum magnitude: {mom_mag:>9.3f} kg·m/s'

        time_list.append(t)
        KE_list.append(KE)
        momentum_list.append(mom_mag)

        t_last = t

# ==================== FINAL PRINT ====================
print(f"Final KE: {KE_list[-1]:.3f} J")
print(f"Final Momentum magnitude: {momentum_list[-1]:.3f} kg·m/s")

# ==================== PLOTTING ====================
'''
plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.plot(time_list, KE_list, color='blue')
plt.title("Kinetic Energy vs Time")
plt.xlabel("Time (s)")
plt.ylabel("KE (J)")
plt.ylim(min(KE_list)*0.95, max(KE_list)*1.05)

plt.subplot(1,2,2)
plt.plot(time_list, momentum_list, color='red')
plt.title("Momentum Magnitude vs Time")
plt.xlabel("Time (s)")
plt.ylabel("|p| (kg·m/s)")
plt.ylim(min(momentum_list)*0.95, max(momentum_list)*1.05)

plt.tight_layout()
plt.show()
'''
