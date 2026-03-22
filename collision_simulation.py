from vpython import *
import matplotlib.pyplot as plt

scene = canvas(title='2D Elastic Puck Collision – Using Euler Method ',
               width=900, height=700, background=color.black)
scene.forward = vector(0, -0.2, -1)
scene.range = 12
scene.autoscale = False

# ==================== PARAMETERS ====================
dt = 2e-5          
k = 60000          
r = 1.2
m1 = m2 = 2.0
damping = 0.0

# ==================== CREATE PUCKS ====================
puck1 = sphere(pos=vector(-6, -1, 0), radius=r, color=color.cyan,
               make_trail=True, trail_type="points", interval=15, retain=150)
puck1.m = m1
puck1.v = vector(5.5, 1.2, 0)

puck2 = sphere(pos=vector(6, 1, 0), radius=r, color=color.orange,
               make_trail=True, trail_type="points", interval=15, retain=150)
puck2.m = m2
puck2.v = vector(-4.5, -0.9, 0)

# ==================== VELOCITY ARROWS ====================
vel_arrow1 = arrow(pos=puck1.pos, axis=puck1.v * 0.15, color=color.yellow,
                   shaftwidth=0.08, headwidth=0.18, headlength=0.25)
vel_arrow2 = arrow(pos=puck2.pos, axis=puck2.v * 0.15, color=color.yellow,
                   shaftwidth=0.08, headwidth=0.18, headlength=0.25)

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
t_max = 5.0

while t < t_max:
    rate(3000)  

    # Compute forces
    r_rel = puck2.pos - puck1.pos
    dist = mag(r_rel)
    overlap = max(0, 2*r - dist)

    a1 = vector(0,0,0)
    a2 = vector(0,0,0)

    if overlap > 0:
        unit = r_rel / dist
        F_mag = k * overlap
        F_on2 = F_mag * unit
        F_on1 = -F_on2

        v_rel = puck2.v - puck1.v
        F_damp = damping * dot(v_rel, unit) * unit
        F_on2 += F_damp
        F_on1 -= F_damp

        a1 = F_on1 / puck1.m
        a2 = F_on2 / puck2.m

    # Euler integration
    puck1.v += a1 * dt
    puck2.v += a2 * dt

    puck1.pos += puck1.v * dt
    puck2.pos += puck2.v * dt

    # Update velocity arrows
    vel_arrow1.pos = puck1.pos
    vel_arrow1.axis = puck1.v * 0.15   
    vel_arrow2.pos = puck2.pos
    vel_arrow2.axis = puck2.v * 0.15

    t += dt
    if t - t_last > 0.05:
        KE = 0.5*puck1.m*mag2(puck1.v) + 0.5*puck2.m*mag2(puck2.v)
        mom_mag = mag(puck1.m*puck1.v + puck2.m*puck2.v)

        ke_label.text = f'\nKinetic Energy: {KE:>9.3f} J'
        mom_label.text = f'\nMomentum magnitude: {mom_mag:>9.3f} kg·m/s'

        time_list.append(t)
        KE_list.append(KE)
        momentum_list.append(mom_mag)

        t_last = t

# ==================== FINAL PRINT ====================
initial_KE = 0.5*m1*mag2(vector(5.5, 1.2, 0)) + 0.5*m2*mag2(vector(-4.5, -0.9, 0))
initial_mom = mag(m1*vector(5.5, 1.2, 0) + m2*vector(-4.5, -0.9, 0))
print(f"Initial KE: {initial_KE:.3f} J")
print(f"Final KE: {KE_list[-1]:.3f} J  (change: {(KE_list[-1]/initial_KE - 1)*100:.2f}%)")
print(f"Initial Momentum magnitude: {initial_mom:.3f} kg·m/s")
print(f"Final Momentum magnitude: {momentum_list[-1]:.3f} kg·m/s")

# ==================== PLOTTING ====================
# ==================== MATPLOTLIB # ================
plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.plot(time_list, KE_list, color='blue')
plt.title("Kinetic Energy vs Time")
plt.xlabel("Time (s)")
plt.ylabel("KE (J)")
plt.ylim(min(KE_list)*0.9, max(KE_list)*1.1)

plt.subplot(1,2,2)
plt.plot(time_list, momentum_list, color='red')
plt.title("Momentum Magnitude vs Time")
plt.xlabel("Time (s)")
plt.ylabel("|p| (kg·m/s)")
plt.ylim(min(momentum_list)*0.95, max(momentum_list)*1.05)

plt.tight_layout()
plt.show()