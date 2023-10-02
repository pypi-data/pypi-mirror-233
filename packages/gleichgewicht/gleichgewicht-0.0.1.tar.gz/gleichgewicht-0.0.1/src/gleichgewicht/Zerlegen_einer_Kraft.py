import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ploterstellung
    

# Eingabewerte der gegebenen Kraft


F = 3  # [Krafteinheit]
phi_F = 134  # in Grad von Richtung x aus positiv zur Richtung y

# Gewünschte Richtungswinkel zur Richtung a und b der zerlegten Kraft
phi_a = 23  # in Grad von Richtung x aus positiv zur Richtung y
phi_b = 44  # in Grad von Richtung x aus positiv zur Richtung y



# Berechnete Komponenten F_a und F_b der zerlegten Kraft
F_a = F / (np.cos(np.radians(phi_a)) * np.sin(np.radians(phi_b)) - np.cos(np.radians(phi_b)) * np.sin(np.radians(phi_a))) * (
            np.sin(np.radians(phi_b)) * np.cos(np.radians(phi_F)) - np.cos(np.radians(phi_b)) * np.sin(
        np.radians(phi_F)))

F_b = F / (np.cos(np.radians(phi_a)) * np.sin(np.radians(phi_b)) - np.cos(np.radians(phi_b)) * np.sin(np.radians(phi_a))) * (
            -np.sin(np.radians(phi_a)) * np.cos(np.radians(phi_F)) + np.cos(np.radians(phi_a)) * np.sin(
        np.radians(phi_F)))




fig, ax = plt.subplots(figsize=(15, 15))
arrow_style = {
    'headlength':5,
    'headaxislength':5,
    'width':0.005,
    'scale':1,
    'angles':'xy',
    'scale_units':'xy',
}


# Kraft F
F_x = F * np.cos(np.radians(phi_F))
F_y = F * np.sin(np.radians(phi_F))

color_F = 'red'

# Vektor
ax.quiver(0, 0, F_x, F_y, color=color_F, label=f'$F = {round(F, 1)}$ [Krafteinheit]', **arrow_style)

# Richtungslinie
ax.plot(np.array([-F_x * .5, F_x]) * 1.5, np.array([-F_y * .5, F_y]) * 1.5,  color=color_F,
        linewidth=0.8)

# Text für Vektor F am Endpunkt hinzufügen
ax.text(F_x*1.05, F_y*1.05, 'F', fontsize=12, color=color_F, verticalalignment='bottom', horizontalalignment='right')



# Zerlegte Kraft a
F_a_x = F_a * np.cos(np.radians(phi_a))
F_a_y = F_a * np.sin(np.radians(phi_a))

color_a = '0.2'

# Vektor
ax.quiver(0, 0, F_a_x, F_a_y, color=color_a,
        label=f'$F_a = {round(abs(F_a), 1)}$ [Krafteinheit]', **arrow_style)

# Richtungslinie
ax.plot(np.array([-F_a_x * .5, F_a_x]) * 1.5, np.array([-F_a_y * .5, F_a_y]) * 1.5, linestyle='dashed', color='red',
        linewidth=0.8)

# Text für Vektor F_a am Endpunkt hinzufügen
ax.text(F_a_x*1.05, F_a_y*1.05, '$F_a$', fontsize=12, color=color_a, verticalalignment='bottom', horizontalalignment='right')



# Zerlegte Kraft b
F_b_x = F_b * np.cos(np.radians(phi_b))
F_b_y = F_b * np.sin(np.radians(phi_b))

color_b = '0.5'

# Vektor
ax.quiver(0, 0, F_b_x, F_b_y, color=color_b,
        label=f'$F_b = {round(abs(F_b), 1)}$ [Krafteinheit]', **arrow_style)

# Richtungslinie
ax.plot(np.array([-F_b_x * .5, F_b_x]) * 1.5, np.array([-F_b_y * .5, F_b_y]) * 1.5, linestyle='dashed', color='red',
        linewidth=0.8)

# Text für Vektor F_b am Endpunkt hinzufügen
ax.text(F_b_x*1.05, F_b_y*1.05, '$F_b$', fontsize=12, color=color_b, verticalalignment='bottom', horizontalalignment='right')

# Versetzt an Endpunkt F_a
ax.quiver(F_a_x, F_a_y, F_b_x, F_b_y, color='0.8', label='$F_b$ verschoben ins Kräftepolygon',**arrow_style)



# Darstellung des Winkels
circle_radius = 0.2 * min(max(F_x, F_a_x, F_b_x), max(F_y, F_a_y, F_b_y))

winkel_styles = {
    'facecolor':'none',
    'alpha':1,
    'theta1':0,
    'center':(0,0)
}




if F_b >=0:
    ax.add_patch(
        patches.Wedge(r = circle_radius,theta2=phi_b, edgecolor='0.5', **winkel_styles))
if F_b <0:
    ax.add_patch(
        patches.Wedge(r = circle_radius,theta2=phi_b+180, edgecolor='0.5', **winkel_styles))

if F_a >= 0:    
    ax.add_patch(
        patches.Wedge(r = circle_radius*1.4,theta2=phi_a, edgecolor='0.2', **winkel_styles))
if F_a < 0:    
    ax.add_patch(
        patches.Wedge(r = circle_radius*1.4,theta2=phi_a+180, edgecolor='0.2', **winkel_styles))
    
if F >= 0:    
    ax.add_patch(
        patches.Wedge(r = circle_radius*1.8,theta2=phi_F, edgecolor=color_F, **winkel_styles))
if F < 0:    
    ax.add_patch(
        patches.Wedge(r = circle_radius*1.8,theta2=phi_F+180, edgecolor=color_F,**winkel_styles))

# Optional: Beschriften Sie die Achsen
ax.set_xlabel('X-Achse [Krafteinheit]')
ax.set_ylabel('Y-Achse [Krafteinheit]')
ax.set_aspect('equal')
ax.axis('equal')
ax.legend(ncol=2)
ax.grid()
ax.set_facecolor('none')

plt.show()

    
