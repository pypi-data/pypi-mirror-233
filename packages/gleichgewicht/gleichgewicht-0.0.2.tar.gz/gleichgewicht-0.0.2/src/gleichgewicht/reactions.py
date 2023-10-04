import numpy as np
import sympy as sp

class Reactionforce:
    
    """
    Represents a reaction force vector with magnitude, direction, and position.

    Parameters
    ----------
    rotation_to_x : float
        The angle (in degrees) of the reaction force vector relative to the positive X-axis.
    position_x : float
        The X-coordinate of the point where the reaction force is applied.
    position_y : float
        The Y-coordinate of the point where the reaction force is applied.

    Attributes
    ----------
    magnitude : sympy.Symbol
        The magnitude (strength) of the reaction force, represented as a symbolic variable for solving.
    magnitude_x : float
        The X-component of the reaction force vector.
    magnitude_y : float
        The Y-component of the reaction force vector.
    rotation : float
        The angle (in degrees) of the reaction force vector relative to the positive X-axis.
    position_x : float
        The X-coordinate of the point where the reaction force is applied.
    position_y : float
        The Y-coordinate of the point where the reaction force is applied.

    Methods
    -------
    __str__():
        Returns a string representation of the reaction force.

    Examples
    --------
    >>> reaction = Reactionforce(45.0, 2.0, 3.0)
    >>> print(reaction)
    Reaktionskraft: | Winkel zur Horizontalen: 45.0 | Position: (x = 2.0, y = 3.0)
    """
    
    
    def __init__(self, rotation_to_x, position_x, position_y):
        self.magnitude = sp.Symbol(f'R_{position_x, position_y, rotation_to_x}', real=True, rational=True) #Die Stärke wird als Symbol eingeführt um nach diesen zu solven
        self.magnitude_x = sp.nsimplify(self.magnitude *sp.cos(sp.rad(rotation_to_x)),tolerance= 1e-7).evalf(90) #the rounding helps with calculation speed
        self.magnitude_y = sp.nsimplify(self.magnitude *sp.sin(sp.rad(rotation_to_x)),tolerance= 1e-7).evalf(90)
        self.rotation = rotation_to_x  # Winkel in Bezug auf die X-Achse
        self.position_x = position_x   # Position des Angriffspunkts in X-Richtung
        self.position_y = position_y    # Position des Angriffspunkts in Y-Richtung

    def __str__(self):
        return f"Reaktionskraft: | Winkel zur Horizontalen: {self.rotation} | Position: (x ={self.position_x}, y = {self.position_y})"


class Reactionmoment:
    """
    Represents a reaction moment applied at a specific position.

    Parameters
    ----------
    position_x : float
        The X-coordinate of the point where the reaction moment is applied.
    position_y : float
        The Y-coordinate of the point where the reaction moment is applied.

    Attributes
    ----------
    magnitude : sympy.Symbol
        The magnitude (strength) of the reaction moment, represented as a symbolic variable for solving.
    position_x : float
        The X-coordinate of the point where the reaction moment is applied.
    position_y : float
        The Y-coordinate of the point where the reaction moment is applied.

    Methods
    -------
    __str__():
        Returns a string representation of the reaction moment.

    Examples
    --------
    >>> moment = Reactionmoment(2.0, 3.0)
    >>> print(moment)
    Reaktionsmoment: | Position: (x = 2.0, y = 3.0)
    """
    
    def __init__(self, position_x, position_y):
        self.magnitude = sp.Symbol(f'M_{position_x, position_y}')
        self.position_x = position_x  # Position des Moments in X-Richtung
        self.position_y = position_y  # Position des Moments in Y-Richtung

    def __str__(self):
        return f"Reaktionsmoment: | Position: (x = {self.position_x}, y = {self.position_y})"
  