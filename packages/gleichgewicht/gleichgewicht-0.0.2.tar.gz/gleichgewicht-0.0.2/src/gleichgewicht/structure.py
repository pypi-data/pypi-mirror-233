import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from .actions import *
from .reactions import *
from IPython.display import display

class System:
    """
    Represents a system of forces and moments to calculate reaction forces and moments at specified points.

    Parameters
    ----------
    actionforces : list of Actionforce, optional
        A list of Actionforce objects representing applied forces. Default is `None`.
    actionmoments : list of Actionmoment, optional
        A list of Actionmoment objects representing applied moments. Default is `None`.
    reactionforces : list of Reactionforce, optional
        A list of Reactionforce objects representing reaction forces. Default is `None`.
    reactionmoments : list of Reactionmoment, optional
        A list of Reactionmoment objects representing reaction moments. Default is `None`.

    Methods
    -------
    calculate_reaction_force():
        Calculates the reaction forces and moments at specified points for the given system.
    """
    
    def __init__(self, actionforces=None, actionmoments=None, reactionforces=None, reactionmoments=None):
        self.actionforces = actionforces
        self.actionmoments = actionmoments
        self.reactionforces = reactionforces
        self.reactionmoments = reactionmoments
        
    def calculate_reaction_force(self):
        """
        Calculates the reaction forces and moments at specified points for the given system.
        
        Returns
        -------
        None
        """
        
        # Zuerst werden alle Einwirkungen in Variablen gespeichert:
        if self.actionforces != None:
            for actionforce in self.actionforces:
                if not isinstance(actionforce, Actionforce):
                    raise ValueError('An error occurred: Wrong input in actionforces')
                
            forces_x = np.array([actionforces.magnitude_x for actionforces in self.actionforces])
            forces_y = np.array([actionforces.magnitude_y for actionforces in self.actionforces])
            distances_x_actionforces = np.array([actionforces.position_x for actionforces in self.actionforces])
            distances_y_actionforces = np.array([actionforces.position_y for actionforces in self.actionforces])

        else:
            forces_x, forces_y, distances_x_actionforces, distances_y_actionforces = 0,0,0,0
                   
            
        # Danach für alle einwirkenden Momente
        if self.actionmoments != None:
            for actionmoment in self.actionmoments:
                if not isinstance(actionmoment, Actionmoment):
                    raise ValueError('An error occurred: Wrong input in actionmoments')
                
            moments = np.array([actionmoments.magnitude for actionmoments in self.actionmoments])
        else:
            moments = 0
            
            
        
        

        
        # Alle Reaktionskräfte in Variablen:
        
        if self.reactionforces != None:
            for reactionforce in self.reactionforces:
                if not isinstance(reactionforce, Reactionforce):
                    raise ValueError('An error occurred: Wrong input in reactionforces')
                
            reactionforces_x = np.array([reactionforces.magnitude_x for reactionforces in self.reactionforces])
            reactionforces_y = np.array([reactionforces.magnitude_y for reactionforces in self.reactionforces])
            distances_x_reaction = np.array([reactionforces.position_x for reactionforces in self.reactionforces])
            distances_y_reaction = np.array([reactionforces.position_y for reactionforces in self.reactionforces])
        
        else: 
            reactionforces_x, reactionforces_y, distances_x_reaction, distances_y_reaction = 0,0,0,0,0

            
        # Alle Reaktionsmomente in Variablen:
        if self.reactionmoments != None:
            for reactionmoment in self.reactionmoments:
                if not isinstance(reactionmoment, Reactionmoment):
                    raise ValueError('An error occurred: Wrong input in reactionmoments')
                
            reactionmoments_symbols = np.array([reactionmoments.magnitude for reactionmoments in self.reactionmoments])

        
        else:
            reactionmoments_symbols = 0


        # Drehpunkte dürfen lediglich nicht mit den Koordinaten der Reaktionskräfte und Momente übereinstimmen, damit diese nicht aus den Gleichungen fallen
        # Erstellen Sie ein Array mit möglichen Einträgen. Falls eine Reaktionskraft an einer der Koordinaten von node_pos erstellt wird, so 
          
        node_pos_x = np.array([1e10, 1e9, 1e8])
        node_pos_y = np.array([-1e8, -1e10, -1e10])
       
        # Gleichgewicht            
        equations_equilibrium = []
        # Es wird die Summe aller Momente um weit entfernte Punkte ermittelt
        for i in range(0,len(node_pos_x)):
            sum_moment = sp.Eq(0,np.sum(-forces_x * (distances_y_actionforces-node_pos_y[i]) + forces_y * (distances_x_actionforces-node_pos_x[i])) + np.sum(-reactionforces_x * (distances_y_reaction-node_pos_y[i]) + reactionforces_y * (distances_x_reaction-node_pos_x[i])) + np.sum(moments) + np.sum(reactionmoments_symbols))
            equations_equilibrium.append(sum_moment)
    
        
        # Das Lösen der Gleichungen ergibt die magnitudes
        sol = sp.solve(equations_equilibrium)
        if len(sol) == 0:
            raise ValueError('An error occurred: The system has no solution, check static determinacy')
        
        for value in sol.values():
            if type(value) != sp.core.numbers.Float:
                raise ValueError('An error occurred: The system has too many unknowns, check static determinacy')
        
        # Die Symbolischen Werte der Reaktionskräfte und der Reaktionsmomente werden mit der Lösung überschrieben       
        if self.reactionforces != None:
            if type(self.reactionforces[0]) == type(Reactionforce(0,0,0)):
                for reactionforces in self.reactionforces:
                    reactionforces.magnitude = np.float64(reactionforces.magnitude.subs(sol))
                    reactionforces.magnitude_x = reactionforces.magnitude * np.cos(np.radians(reactionforces.rotation))
                    reactionforces.magnitude_y = reactionforces.magnitude * np.sin(np.radians(reactionforces.rotation))
        if self.reactionmoments != None:
            if type(self.reactionmoments[0]) == type(Reactionmoment(0,0)):                        
                for reactionmoment in self.reactionmoments:
                        reactionmoment.magnitude = np.float64(reactionmoment.magnitude.subs(sol))
                        
                        
                        
        ## Die Reaktionskräfte werden als Gleichungen dargestellt:
        
        def dict_render(params):
            """renders a dictionary containing the parameters

            Args:
                params (dict): Parameters for substitution
            """
            from sympy import Eq, Symbol
            
            symbols = list(params.keys())
            values = list(params.values())

            for i in range(0,len(symbols)):
                if values[i] <= 0.001 and values[i] >=-0.001:
                    values[i] = sp.Symbol('0')
                
                display(Eq(symbols[i], values[i].evalf(4)))
                
        dict_render(sol)
        return sol
  
class Plot:
    
    def __init__(self, system=None):
        self.system = system
    
    def plot_forces_and_moments(self):
        
        """Plot des Systems
        """
        fig, ax = plt.subplots(figsize=(15, 15))        
        
        
        def moment_symbol(moment, color):
            """Symbol of Moments

            Args:
                moment (Moment): Moment-class
                color (string): matplotlib color
                label (string): label for the legend
            """
            ax.annotate(f'M = {round(moment.magnitude,1)}', xy=(moment.position_x,moment.position_y), xytext = (30,30), textcoords="offset pixels", color=color)
            ax.plot(moment.position_x, moment.position_y, marker=r'$\circlearrowleft$',ms=40, color=color)
            
            
            
        def force_symbol(force, color):
            """Symbol of Forces / Forcevectors

            Args:
                force (_type_): _description_
                color (_type_): _description_
                label (_type_): _description_
            """
            scaler = max([force.magnitude for force in self.system.actionforces])   
             
            quiver_style = {
                'angles':'xy',
                'scale_units':'xy',
                'scale':scaler
            }
            
            # Die Position der Vektoren wird durch die länge des Vektors subtrahiert, dies gewährleistet, dass die Pfeilspitze am definierten Punkt zu liegen kommt.
            ax.annotate(f'$F$ = {abs(round(force.magnitude,1))}', xy=(force.position_x - force.magnitude_x/scaler,force.position_y - force.magnitude_y/scaler), xytext = (7,7), textcoords="offset pixels", color=color)
            ax.quiver(force.position_x- force.magnitude_x/scaler, force.position_y - force.magnitude_y/scaler, force.magnitude_x, force.magnitude_y, color=color, **quiver_style)
            # ax.quiver(force.position_x- force.magnitude_x/scaler, force.position_y - force.magnitude_y/scaler, force.magnitude_x, 0, color=color, **quiver_style, alpha=0.08)
            # ax.quiver(force.position_x- force.magnitude_x/scaler, force.position_y - force.magnitude_y/scaler, 0, force.magnitude_y, color=color, **quiver_style, alpha=0.08)
            
            
            
        if self.system.actionforces != None:
            for actionforce in self.system.actionforces:
                # Symboldarstellung
                force_symbol(actionforce, 'red')
            for reactionforce in self.system.reactionforces:
                force_symbol(reactionforce, 'green', )
                force_symbol(reactionforce, 'green', )
                
                
        if self.system.actionmoments != None:    
            for actionmoment in self.system.actionmoments:
                # Symboldarstellung
                moment_symbol(actionmoment, 'red', )
        if self.system.reactionmoments != None:
            for reactionmoment in self.system.reactionmoments:
                moment_symbol(reactionmoment, 'green', )            
            
        
        # Berechnen Sie die Begrenzungen basierend auf den Kräften und Momenten
        max_magnitude = max(actionforce.magnitude for actionforce in self.system.actionforces)
        ax.set_xlim(-max_magnitude, max_magnitude)
        ax.set_ylim(-max_magnitude, max_magnitude)

        # Optional: Beschriften Sie die Achsen
        ax.set_xlabel('X-Achse')
        ax.set_ylabel('Y-Achse')
        ax.set_aspect('equal')
        ax.axis('equal')
        # ax.legend(ncol=2)
        ax.grid()

        plt.show()
