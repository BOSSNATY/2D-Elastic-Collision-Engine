# Web VPython 3.2
from vpython import *
import matplotlib.pyplot as plt

# ==================== SCENE SETUP ====================
scene = canvas(title='2D Elastic Puck Collision', 
               width=900, height=600, background=color.black)
scene.forward = vector(0, -0.2, -1)
scene.range = 12

# ==================== PARAMETERS ====================
dt = 5e-6
k = 5000000
r_base = 1.2          
v_arrow_scale = 0.3
t_max = 6.0
post_collision_grace = 1.5

v1_dir = norm(vector(5.5, 1.2, 0))
v2_dir = norm(vector(-4.5, -0.9, 0))

# ==================== CREATE PUCKS ====================
puck1 = sphere(pos=vector(-6, -1, 0), radius=r_base, color=color.cyan, make_trail=True, retain=50)
puck2 = sphere(pos=vector(6, 1, 0), radius=r_base, color=color.orange, make_trail=True, retain=50)
puck1.m = 2.0
puck2.m = 2.0
puck1.v = v1_dir * 5.6
puck2.v = v2_dir * 5.6

arrow1 = arrow(pos=puck1.pos, axis=puck1.v * v_arrow_scale, color=color.yellow)
arrow2 = arrow(pos=puck2.pos, axis=puck2.v * v_arrow_scale, color=color.yellow)

# ==================== ON-SCREEN LABELS ====================
ke_display = label(pos=vector(0, 9, 0), text='KE: --', height=16, border=4, font='monospace', box=False)
mom_display = label(pos=vector(0, 7.5, 0), text='Momentum: --', height=16, border=4, font='monospace', box=False)

# Final velocity labels (One decimal place)
v1_final_lbl = label(pos=vector(-5, -8, 0), text='V1 Final: --', color=color.cyan, height=14, box=False)
v2_final_lbl = label(pos=vector(5, -8, 0), text='V2 Final: --', color=color.orange, height=14, box=False)

# Simulation State
t = 0
running = True
paused = False
collision_occurred = False
separation_time = None

# ==================== UI FUNCTIONS ====================
def reset_sim():
    global t, running, paused, collision_occurred, separation_time
    t = 0
    running = True
    paused = False
    btn_pause.text = "Pause"
    collision_occurred = False
    separation_time = None
    
    puck1.pos = vector(-6, -1, 0)
    puck2.pos = vector(6, 1, 0)
    
    # Apply new slider values
    puck1.m = sl_m1.value
    puck2.m = sl_m2.value
    puck1.v = v1_dir * sl_v1.value
    puck2.v = v2_dir * sl_v2.value
    
    puck1.clear_trail()
    puck2.clear_trail()
    
    puck1.radius = 0.85 * (puck1.m ** 0.5)
    puck2.radius = 0.85 * (puck2.m ** 0.5)
    
    v1_final_lbl.text = 'V1 Final: --'
    v2_final_lbl.text = 'V2 Final: --'
    update_visual_arrows()

def update_visual_arrows():
    # Hide arrow if velocity is 0
    if mag(puck1.v) > 0.01:
        arrow1.visible = True
        arrow1.pos = puck1.pos
        arrow1.axis = puck1.v * v_arrow_scale
    else:
        arrow1.visible = False

    if mag(puck2.v) > 0.01:
        arrow2.visible = True
        arrow2.pos = puck2.pos
        arrow2.axis = puck2.v * v_arrow_scale
    else:
        arrow2.visible = False

def update_params():
    m1_txt.text = '{:1.1f} kg'.format(sl_m1.value)
    m2_txt.text = '{:1.1f} kg'.format(sl_m2.value)
    v1_txt.text = '{:.1f} m/s'.format(sl_v1.value)
    v2_txt.text = '{:.1f} m/s'.format(sl_v2.value)
    reset_sim()

def toggle_pause():
    global paused
    paused = not paused
    btn_pause.text = "Resume" if paused else "Pause"

def dummy(): 
    m1_txt.text = '{:1.1f} kg'.format(sl_m1.value)
    m2_txt.text = '{:1.1f} kg'.format(sl_m2.value)
    v1_txt.text = '{:.1f} m/s'.format(sl_v1.value)
    v2_txt.text = '{:.1f} m/s'.format(sl_v2.value)

# ==================== SLIDERS & UI ====================
scene.append_to_caption("\nMass 1\n")
sl_m1 = slider(min=0.5, max=10, value=2.0, bind=dummy)
m1_txt = wtext(text='2.0 kg')

scene.append_to_caption("\nMass 2\n")
sl_m2 = slider(min=0.5, max=10, value=2.0, bind=dummy)
m2_txt = wtext(text='2.0 kg')

scene.append_to_caption("\nVelocity 1 (m/s)\n")
sl_v1 = slider(min=0, max=15, value=5.6, bind=dummy) # Min set to 0
v1_txt = wtext(text='5.6 m/s')

scene.append_to_caption("\nVelocity 2 (m/s)\n")
sl_v2 = slider(min=0, max=15, value=5.6, bind=dummy) # Min set to 0
v2_txt = wtext(text='5.6 m/s')

scene.append_to_caption("\n\n")
button(text="Apply & Reset", bind=update_params)
scene.append_to_caption("  ")
btn_pause = button(text="Pause", bind=toggle_pause)

# ==================== SIMULATION LOOP ====================
while True:
    rate(100000)
    
    if running and not paused:
        if t > t_max or (separation_time is not None and t - separation_time > post_collision_grace):
            running = False
            # Update final velocity labels with one decimal place
            v1_final_lbl.text = 'V1 Final: {:.1f} m/s'.format(mag(puck1.v))
            v2_final_lbl.text = 'V2 Final: {:.1f} m/s'.format(mag(puck2.v))

        r_rel = puck2.pos - puck1.pos
        dist = mag(r_rel)
        overlap = max(0, (puck1.radius + puck2.radius) - dist)
        force = vector(0, 0, 0)
        
        if overlap > 0:
            force = k * overlap * (r_rel / dist)
            collision_occurred = True
        elif collision_occurred and separation_time is None:
            separation_time = t
        
        puck1.v += (-force / puck1.m) * dt
        puck2.v += (force / puck2.m) * dt
        puck1.pos += puck1.v * dt
        puck2.pos += puck2.v * dt
        
        update_visual_arrows()
        t += dt
        
        if int(t/dt) % 2000 == 0:
            ke = 0.5 * puck1.m * mag2(puck1.v) + 0.5 * puck2.m * mag2(puck2.v)
            p_vec = puck1.m * puck1.v + puck2.m * puck2.v
            ke_display.text = 'Total KE: {:.2f} J'.format(ke)
            mom_display.text = 'Total Momentum: {:.2f} kg·m/s'.format(mag(p_vec))