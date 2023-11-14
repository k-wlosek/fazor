import math

import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np

import js
import io, base64

# Dane impedancji
U_volts = float(js.document.getElementById("ph-voltage").value)
I_amps = float(js.document.getElementById("ph-current").value)
alpha_deg = float(js.document.getElementById("ph-angle").value)
negative = js.document.getElementById("ph-negative").checked
title = js.document.getElementById("ph-title").value

# Oblicz ucięte U
U_volts_cut = round(math.sqrt(U_volts ** 2 - I_amps ** 2), 2)

# Oblicz wysokość diagramu
alpha_rad = np.deg2rad(alpha_deg)
plot_height = math.sqrt((I_amps / math.cos(alpha_rad)) ** 2 - I_amps ** 2)

# Konwersja kąta ze stopni na radiany
phi_rad = np.deg2rad(alpha_deg)

# Utwórz nowy wykres
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal', adjustable='box')

# Utwórz siatkę
ax.grid(which="both", linestyle="-", linewidth=0.5)

# Narysuj trójkąt impedancji
ax.plot([0, I_amps], [0, 0], 'r')
ax.plot([0, I_amps], [0, plot_height], 'g')

# Dodaj kąt między R i Z
angle = Wedge(center=(0, 0), r=(I_amps / 4), theta1=0, theta2=alpha_deg, color='black', alpha=0.2)
ax.add_patch(angle)

# Dodaj adnotacje nad przyprostokątnymi
ax.annotate(f"I = {I_amps} A", (I_amps / 2, 0), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=12)

if negative:
    ax.annotate(f"U = {U_volts} V", (I_amps / 2, plot_height / 2), textcoords="offset points", xytext=(0, 0), ha='center', fontsize=12, rotation=-alpha_deg)
    ax.annotate(f"φ = -{alpha_deg}°", (I_amps / 5, 0.01), textcoords="offset points", xytext=(I_amps / 15, -U_volts_cut / 10), ha='center', fontsize=12)
else:
    ax.annotate(f"U = {U_volts} V", (I_amps / 2, plot_height / 2), textcoords="offset points", xytext=(0, 0), ha='center', fontsize=12, rotation=alpha_deg)
    ax.annotate(f"φ = {alpha_deg}°", (I_amps / 5, 0), textcoords="offset points", xytext=(I_amps / 15, U_volts_cut / 15), ha='center', fontsize=12)

# Dodaj groty
plt.annotate('', xy=(I_amps * 1.01, plot_height * 1.01), xytext=(I_amps * 0.95, plot_height * 0.95), arrowprops=dict(arrowstyle='->', lw=1.5, color='g'))
plt.annotate('', xy=(I_amps*1.01, 0), xytext=(I_amps*0.95, 0), arrowprops=dict(arrowstyle='->', lw=1.5, color='r'))

# Ukryj przeciwne osie X i Y
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Ogranicz osie
if negative:
    ax.set_ylim(plot_height * 1.05, -plot_height * 0.05)

# Dodaj etykiety osi
ax.set_title(title, fontsize=14, pad=20)

buf = io.BytesIO()
fig.savefig(buf, format='png', dpi=200, bbox_inches='tight')
buf.seek(0)
ph_img = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('UTF-8')
