import math
import matplotlib.pyplot as plt
import matplotlib.patches as Patches

import js
import io, base64

if __name__ == '__main__':
    # Dane impedancji
    Z_ohms = float(js.document.getElementById("tr-impedance").value)
    phi_deg = float(js.document.getElementById("tr-angle").value)
    title = js.document.getElementById("tr-title").value

    # Konwersja kąta ze stopni na radiany
    phi_rad = phi_deg / 180 * math.pi

    # Oblicz boki R i X
    R_ohms = round(Z_ohms * math.cos(phi_rad), 2)
    X_ohms = round(math.fabs(Z_ohms * math.sin(phi_rad)), 2)

    # Utwórz nowy wykres
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal', adjustable='box')

    # Utwórz siatkę
    ax.grid(which="both", linestyle="-", linewidth=0.5)

    # Narysuj trójkąt impedancji
    ax.plot([0, R_ohms], [0, 0], 'r')
    ax.plot([R_ohms, R_ohms], [X_ohms, 0], 'b')
    ax.plot([0, R_ohms], [0, X_ohms], 'g')

    # Dodaj oznaczenie kąta między R i Z

    style = "Simple, tail_width=0.5, head_width=6, head_length=10"
    kw = dict(arrowstyle=style, color="k")
    gdzie = R_ohms / 6
    gdzieX = math.cos(phi_rad) * gdzie
    gdzieY = math.fabs((math.sin(phi_rad) * gdzie))
    fancyA = Patches.FancyArrowPatch((gdzie, 0), (gdzieX, gdzieY), connectionstyle=f"Arc3,rad={-0.2 if phi_deg<0 else 0.2}", **kw)
    fancyA.set_zorder(2)
    ax.add_patch(fancyA)

    # Dodaj adnotacje nad przyprostokątnymi
    ax.annotate(f"R = {R_ohms} Ω", (R_ohms / 2, 0), textcoords="offset points", xytext=(0, 4), ha='center',
                fontsize=12)
    ax.annotate(f"X = {X_ohms} Ω", (R_ohms, X_ohms / 2), textcoords="offset points", xytext=(4, 0), va='center',
                fontsize=12, rotation=90)

    # Dodaj adnotację przy przeciwprostokątnej
    ax.annotate(f"Z = {Z_ohms} Ω", (R_ohms / 2, X_ohms / 2), textcoords="offset points", xytext=(0, -10), ha='center',
                    fontsize=12, rotation=phi_deg)

    # Dodaj adnotację obok oznaczenia kąta
    ax.annotate(f"φ = {(phi_deg)}°", (R_ohms / 5, abs((R_ohms / 4) * math.tan(phi_rad) / 3)), textcoords="offset points",
                xytext=(0, 0), ha='left', fontsize=12)

    # Ukryj przeciwne osie X i Y
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Ogranicz osie
    if phi_deg < 0:
        ax.set_ylim(X_ohms + 5, -5)
    else:
        ax.set_ylim(-5, X_ohms + 5)

    # Dodaj tytuł
    ax.set_title(title, fontsize=14, pad=20)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=200, bbox_inches='tight')
    buf.seek(0)
    tr_img = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('UTF-8')
