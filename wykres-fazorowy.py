import math
import matplotlib.pyplot as plt
import matplotlib.patches as Patches

if __name__ == '__main__':
    # Dane impedancji
    U_volts = 157.5
    I_amps = 0.504
    phi_deg = -57.71
    title = "Trójkąt impedancji dla pomiaru Zx nr y"

    # Konwersja kąta ze stopni na radiany
    phi_rad = phi_deg / 180 * math.pi

    # Oblicz osie X i Y
    os_X = round(U_volts * math.cos(phi_rad), 2)
    os_Y = round(math.fabs(U_volts * math.sin(phi_rad)), 2)

    # Utwórz nowy wykres
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal', adjustable='box')

    # Utwórz siatkę
    ax.grid(which="both", linestyle="-", linewidth=0.5)

    # Narysuj trójkąt impedancji
    ax.plot([0, os_X], [0, 0], 'r')
    ax.plot([0, os_X], [0, os_Y], 'g')
    plt.annotate('', xy=(os_X * 1.015, 0), xytext=(-0.1, -0.1),
                 arrowprops=dict(arrowstyle='->', lw=1.5, color='r'))
    plt.annotate('', xy=(os_X * 1.015, os_Y * 1.015), xytext=(-0.1, -0.1),
                 arrowprops=dict(arrowstyle='->', lw=1.5, color='g'))

    # Dodaj oznaczenie kąta między I oraz U
    style = "Simple, tail_width=0.5, head_width=6, head_length=10"
    kw = dict(arrowstyle=style, color="k")
    gdzie = os_X / 5
    gdzieX = math.cos(phi_rad) * gdzie
    gdzieY = math.fabs((math.sin(phi_rad) * gdzie))
    fancyA = Patches.FancyArrowPatch((gdzie, 0), (gdzieX, gdzieY), connectionstyle=f"Arc3,rad={-0.2 if phi_deg<0 else 0.2}", **kw)
    fancyA.set_zorder(2)
    ax.add_patch(fancyA)

    # Dodaj adnotacje nad przyprostokątnymi
    ax.annotate(f"I = {I_amps} A", (os_X / 2, 0), textcoords="offset points", xytext=(0, 4), ha='center',
                fontsize=12)

    # Dodaj adnotację przy przeciwprostokątnej
    ax.annotate(f"U = {U_volts} V", (os_X / 2, os_Y / 2), textcoords="offset points", xytext=(0, -10), ha='center',
                fontsize=12, rotation=phi_deg)

    # Dodaj adnotację obok oznaczenia kąta
    ax.annotate(f"φ = {(phi_deg)}°", (os_X / 4.5, abs((os_X / 4) * math.tan(phi_rad) / 3)), textcoords="offset points",
                xytext=(0, 0), ha='left', fontsize=12)

    # Ukryj przeciwne osie X i Y
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Ogranicz osie
    if phi_deg < 0:
        ax.set_ylim(os_Y + 5, -5)
    else:
        ax.set_ylim(-5, os_Y + 5)

    # Dostosuj skalę pod osią X
    scaling_factor = I_amps / os_X
    desired_xticks = [0, os_X * 0.25, os_X * 0.5, os_X * 0.75, os_X]
    ax.set_xticks(desired_xticks)
    ax.set_xticklabels([f'{(tick * scaling_factor):.3f}' for tick in desired_xticks])

    # Dodaj tytuł
    ax.set_title(title, fontsize=14, pad=20)

    # Zapisz rysunek do pliku PNG
    file_name = title.replace(" ", "_").lower() + ".png"
    plt.savefig(file_name, dpi=200, bbox_inches='tight')

    # Wyświetl rysunek
    plt.show()
