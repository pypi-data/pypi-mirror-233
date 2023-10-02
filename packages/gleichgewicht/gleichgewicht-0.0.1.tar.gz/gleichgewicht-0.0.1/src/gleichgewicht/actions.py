import numpy as np
import sympy as sp
class Actionforce:
    """
    Represents a force vector with magnitude, direction, and position.

    Parameters
    ----------
    magnitude : float
        The magnitude (strength) of the force.
    rotation_to_x : float
        The angle (in degrees) of the force vector relative to the positive X-axis.
    position_x : float
        The X-coordinate of the point where the force is applied.
    position_y : float
        The Y-coordinate of the point where the force is applied.

    Attributes
    ----------
    magnitude_x : float
        The X-component of the force vector.
    magnitude_y : float
        The Y-component of the force vector.

    Methods
    -------
    __str__():
        Returns a string representation of the force vector.

    Examples
    --------
    >>> force = Actionforce(10.0, 45.0, 2.0, 3.0)
    >>> print(force)
    Kraft: (F_x = 7.1, F_y = 7.1) | Position: (x = 2.0, y = 3.0)
    """
    
    def __init__(self, magnitude, rotation_to_x, position_x, position_y):
        self.magnitude = magnitude  # Kraftbetrag 
        self.rotation = rotation_to_x # Winkel in Bezug auf die X-Achse
        self.magnitude_x = magnitude * np.round(np.cos(np.radians(rotation_to_x)),90) #the rounding helps with calculationspeed
        self.magnitude_y = magnitude * np.round(np.sin(np.radians(rotation_to_x)),90)
        self.position_x = position_x   # Position des Angriffspunkts in X-Richtung
        self.position_y = position_y    # Position des Angriffspunkts in Y-Richtung

    def __str__(self):
        return f"Kraft: (F_x = {round(self.magnitude_x,1)}, F_y = {round(self.magnitude_y)}) | Position: (x ={self.position_x}, y = {self.position_y})"


class Actionmoment:
    """
    Represents a moment (torque) applied at a specific position.

    Parameters
    ----------
    magnitude : float
        The magnitude (strength) of the moment.
    position_x : float
        The X-coordinate of the point where the moment is applied.
    position_y : float
        The Y-coordinate of the point where the moment is applied.

    Methods
    -------
    __str__():
        Returns a string representation of the moment.

    Examples
    --------
    >>> moment = Actionmoment(15.0, 2.0, 3.0)
    >>> print(moment)
    Moment: (M = 15.0) | Position: (x = 2.0, y = 3.0)
    """
    
    def __init__(self, magnitude, position_x, position_y):
        self.magnitude = magnitude    # Betrag des Moments
        self.position_x = position_x  # Position des Moments in X-Richtung
        self.position_y = position_y  # Position des Moments in Y-Richtung

    def __str__(self):
        return f"Moment: (M = {round(self.magnitude, 1)}) | Position: (x = {self.position_x}, y = {self.position_y})"
