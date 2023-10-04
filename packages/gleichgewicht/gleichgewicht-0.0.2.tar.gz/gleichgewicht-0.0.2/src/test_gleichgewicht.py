from gleichgewicht import *


def test_calculate_reaction_force():
    einwirkungen_kraefte = [Actionforce(-15,90, 1.5,0), Actionforce(50, 90, 3,0), Actionforce(-104, 90, 7.4, 0), Actionforce(50, 0,10,0)]
    einwirkungen_momente = [Actionmoment(10, 0,0)]
    reaktionen_kraefte = [Reactionforce(90, 10,0), Reactionforce(0,5,5)]
    reaktionen_momente = [Reactionmoment(0,0)]

    system_1 = System(actionforces=einwirkungen_kraefte, reactionforces=reaktionen_kraefte, actionmoments=einwirkungen_momente, reactionmoments=reaktionen_momente)
    
    solution_system = system_1.calculate_reaction_force()
    solution_expected = '{M_(0, 0): -307.900000000000, R_(10, 0, 90): 69.0000000000000, R_(5, 5, 0): -50.0000000000000}'
    print(solution_system)
    assert str(solution_system) == solution_expected
    
    

    
    einwirkung_vertikal = []
    for einwirkung in einwirkungen_kraefte:
        einwirkung_vertikal.append(einwirkung.magnitude_y)
        
    einwirkung_vertikal_sum = sum(einwirkung_vertikal)
    assert abs(list(solution_system.values())[1]) - abs(einwirkung_vertikal_sum) <= 0.1

def test_calculate_reaction_force_2():

    einwirkungen_kraefte = [Actionforce(4*3*25*0.3, -90, 2,3.5)]
    reaktionen_kraefte = [Reactionforce(90, 0, 0), Reactionforce(-45, 6, 0), Reactionforce(0, 6, 5)]

    system_6 = System(actionforces=einwirkungen_kraefte, reactionforces=reaktionen_kraefte)
    solution = system_6.calculate_reaction_force()
    solution_expected = '{R_(0, 0, 90): -89.9995505050503, R_(6, 0, -45): -254.557805545303, R_(6, 5, 0): 179.999550505050}'
    assert str(solution) == solution_expected
    
    

