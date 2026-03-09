from vpython import *

# Scene setup
scene = canvas(title='2D Elastic Puck Collision – Stiff Spring + Euler',
               width=900, height=700, background=color.black)
scene.forward = vector(0, -0.1, -1)   # slight tilt
scene.range = 12
scene.autoscale = False

# ==================== PARAMETERS ====================
dt       = 0.0001          # small enough for stability
k        = 50000           # stiff but manageable
damping  = 0.0             # 0 = perfectly elastic
r        = 1.2             # puck radius
m1 = m2  = 2.0             # equal masses (can change)
wall     = 10              # box half-size

# ==================== CREATE PUCKS ====================
puck1 = sphere(pos=vector(-8, 1, 0), radius=r, color=color.cyan,
               make_trail=True, trail_type="points", interval=8, retain=400)
puck1.m = m1
puck1.v = vector(5.0, 1.8, 0)

puck2 = sphere(pos=vector(8, -2, 0), radius=r, color=color.orange,
               make_trail=True, trail_type="points", interval=8, retain=400)
puck2.m = m2
puck2.v = vector(-3.5, -0.8, 0)

# Labels
ke_label = wtext(text='\nKinetic Energy: calculating...')
mom_label = wtext(text='\nMomentum magnitude: calculating...')

# Print initial momentum once
init_mom_vec = puck1.m * puck1.v + puck2.m * puck2.v
init_mom_mag = mag(init_mom_vec)
print("Initial momentum vector:", init_mom_vec)
print("Initial momentum magnitude:", init_mom_mag)

t = 0
t_last = 0

while True:
    rate(8000)  # fast but not overwhelming

    # ==================== COMPUTE FORCES ====================
    r_rel = puck2.pos - puck1.pos
    dist = mag(r_rel)
    overlap = 2 * r - dist

    a1 = vector(0, 0, 0)
    a2 = vector(0, 0, 0)

    if overlap > 0:
        unit = r_rel / dist
        F_mag = k * overlap
        F_on2 = F_mag * unit
        F_on1 = -F_on2

        # Optional damping (usually 0 for elastic)
        v_rel = puck2.v - puck1.v
        F_damp = damping * dot(v_rel, unit) * unit
        F_on2 += F_damp
        F_on1 -= F_damp

        a1 = F_on1 / puck1.m
        a2 = F_on2 / puck2.m

    # ==================== SEMI-IMPLICIT EULER ====================
    puck1.v += a1 * dt
    puck2.v += a2 * dt

    puck1.pos += puck1.v * dt
    puck2.pos += puck2.v * dt

    # ==================== WALL COLLISIONS – FIXED VERSION ====================
    for puck in [puck1, puck2]:
        if puck.pos.x > wall:
            puck.v.x = -puck.v.x
            puck.pos.x = wall
            # print("Wall hit (right):", puck.pos, puck.v)   # uncomment for debug
        elif puck.pos.x < -wall:
            puck.v.x = -puck.v.x
            puck.pos.x = -wall
            # print("Wall hit (left):", puck.pos, puck.v)

        if puck.pos.y > wall:
            puck.v.y = -puck.v.y
            puck.pos.y = wall
            # print("Wall hit (top):", puck.pos, puck.v)
        elif puck.pos.y < -wall:
            puck.v.y = -puck.v.y
            puck.pos.y = -wall
            # print("Wall hit (bottom):", puck.pos, puck.v)

    # ==================== UPDATE DISPLAY ====================
    t += dt
    if t - t_last > 0.2:
        KE = 0.5 * puck1.m * mag2(puck1.v) + 0.5 * puck2.m * mag2(puck2.v)
        mom_vec = puck1.m * puck1.v + puck2.m * puck2.v
        mom_mag = mag(mom_vec)

        ke_label.text = f'\nKinetic Energy: {KE:>9.3f} J   (should stay nearly constant)'
        mom_label.text = f'\nMomentum magnitude: {mom_mag:>9.3f}   (should stay constant)'

        # Optional: print full vector for checking
        # print(f"Momentum vector: {mom_vec.x:.1f} {mom_vec.y:.1f} mag: {mom_mag}")

        t_last = t