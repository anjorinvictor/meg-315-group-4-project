# core/steam_states.py
"""
HTC Steam Loop States using CoolProp
Calculates enthalpy and entropy for water/steam at different states
"""

import CoolProp.CoolProp as CP
from utils.constants import KELVIN_OFFSET

def steam_cycle_states(p_boiler_bar=40, p_condenser_bar=0.1, t_superheat_C=350):
    """
    Calculate steam states for h-s diagram
    
    Parameters:
    -----------
    p_boiler_bar : float
        Boiler pressure (bar)
    p_condenser_bar : float
        Condenser pressure (bar) - for return line
    t_superheat_C : float
        Superheat temperature (°C)
    
    Returns:
    --------
    dict : State points with h, s, T, P
    """
    
    # Convert bar to Pa for CoolProp (1 bar = 100,000 Pa)
    p_boiler_Pa = p_boiler_bar * 1e5
    p_condenser_Pa = p_condenser_bar * 1e5
    
    # ----- STATE 1: Pump inlet (saturated liquid at condenser pressure) -----
    h1 = CP.PropsSI('H', 'P', p_condenser_Pa, 'Q', 0, 'Water')  # J/kg
    s1 = CP.PropsSI('S', 'P', p_condenser_Pa, 'Q', 0, 'Water')  # J/kg·K
    T1 = CP.PropsSI('T', 'P', p_condenser_Pa, 'Q', 0, 'Water')  # K
    
    # ----- STATE 2: Pump outlet (compressed liquid) -----
    # For simplicity, assume pump work is negligible
    # In real cycle, h2 = h1 + v*(P2-P1), but we'll approximate
    h2 = h1
    s2 = s1
    T2 = T1
    
    # ----- STATE 3: Boiler outlet (superheated steam) -----
    T3_K = t_superheat_C + KELVIN_OFFSET
    h3 = CP.PropsSI('H', 'P', p_boiler_Pa, 'T', T3_K, 'Water')
    s3 = CP.PropsSI('S', 'P', p_boiler_Pa, 'T', T3_K, 'Water')
    T3 = T3_K
    
    # ----- STATE 4: After HTC reactor (throttle to condenser pressure) -----
    # Throttling is isenthalpic: h4 = h3
    h4 = h3
    
    # Find quality and temperature at condenser pressure
    h_f = CP.PropsSI('H', 'P', p_condenser_Pa, 'Q', 0, 'Water')
    h_g = CP.PropsSI('H', 'P', p_condenser_Pa, 'Q', 1, 'Water')
    
    # Quality (vapor fraction)
    if h4 <= h_f:
        x4 = 0  # Subcooled liquid
    elif h4 >= h_g:
        x4 = 1  # Superheated vapor
    else:
        x4 = (h4 - h_f) / (h_g - h_f)  # Two-phase mixture
    
    # Entropy at state 4
    if x4 <= 0:
        s4 = CP.PropsSI('S', 'P', p_condenser_Pa, 'Q', 0, 'Water')
    elif x4 >= 1:
        s4 = CP.PropsSI('S', 'P', p_condenser_Pa, 'Q', 1, 'Water')
    else:
        s_f = CP.PropsSI('S', 'P', p_condenser_Pa, 'Q', 0, 'Water')
        s_g = CP.PropsSI('S', 'P', p_condenser_Pa, 'Q', 1, 'Water')
        s4 = s_f + x4 * (s_g - s_f)
    
    # Temperature at state 4 (saturation temp at condenser pressure)
    T4 = CP.PropsSI('T', 'P', p_condenser_Pa, 'Q', 0, 'Water')
    
    # Convert units for readability (kJ/kg and kJ/kg·K)
    h1_kJ = h1 / 1000
    h2_kJ = h2 / 1000
    h3_kJ = h3 / 1000
    h4_kJ = h4 / 1000
    
    s1_kJ = s1 / 1000
    s2_kJ = s2 / 1000
    s3_kJ = s3 / 1000
    s4_kJ = s4 / 1000
    
    # Convert temperatures to °C for display
    T1_C = T1 - KELVIN_OFFSET
    T2_C = T2 - KELVIN_OFFSET
    T3_C = T3 - KELVIN_OFFSET
    T4_C = T4 - KELVIN_OFFSET
    
    # Phase descriptions
    phases = [
        'Saturated Liquid',
        'Compressed Liquid',
        'Superheated Steam',
        'Two-phase' if 0 < x4 < 1 else ('Liquid' if x4 <= 0 else 'Steam')
    ]
    
    return {
        'points': [
            {'name': '1 - Pump Inlet', 'T_C': T1_C, 'T_K': T1, 'P_bar': p_condenser_bar, 
             'h_kJ': h1_kJ, 's_kJ': s1_kJ, 'phase': phases[0]},
            {'name': '2 - Pump Outlet', 'T_C': T2_C, 'T_K': T2, 'P_bar': p_boiler_bar,
             'h_kJ': h2_kJ, 's_kJ': s2_kJ, 'phase': phases[1]},
            {'name': '3 - Boiler Outlet', 'T_C': T3_C, 'T_K': T3, 'P_bar': p_boiler_bar,
             'h_kJ': h3_kJ, 's_kJ': s3_kJ, 'phase': phases[2]},
            {'name': '4 - HTC Return', 'T_C': T4_C, 'T_K': T4, 'P_bar': p_condenser_bar,
             'h_kJ': h4_kJ, 's_kJ': s4_kJ, 'phase': phases[3]}
        ],
        'h': [h1_kJ, h2_kJ, h3_kJ, h4_kJ],
        's': [s1_kJ, s2_kJ, s3_kJ, s4_kJ],
        'T_C': [T1_C, T2_C, T3_C, T4_C],
        'T_K': [T1, T2, T3, T4],
        'P_bar': [p_condenser_bar, p_boiler_bar, p_boiler_bar, p_condenser_bar],
        'quality': [0, 0, 1, x4],
        'labels': ['1', '2', '3', '4']
    }


def test_steam_states():
    """Test function for steam cycle states"""
    print("=" * 50)
    print("TESTING HTC STEAM CYCLE STATES (CoolProp)")
    print("=" * 50)
    
    # Test with typical values
    results = steam_cycle_states(
        p_boiler_bar=40,
        p_condenser_bar=0.1,
        t_superheat_C=350
    )
    
    print(f"\nINPUTS:")
    print(f"  Boiler pressure: 40 bar")
    print(f"  Condenser pressure: 0.1 bar")
    print(f"  Superheat temperature: 350°C")
    
    print(f"\nSTATE POINTS:")
    print(f"  {'Point':<5} {'T(°C)':<8} {'P(bar)':<8} {'h(kJ/kg)':<10} {'s(kJ/kgK)':<12} {'Phase':<20}")
    print(f"  {'-'*60}")
    
    for i, point in enumerate(results['points']):
        print(f"  {i+1:<5} {point['T_C']:<8.1f} {point['P_bar']:<8.1f} "
              f"{point['h_kJ']:<10.1f} {point['s_kJ']:<12.4f} {point['phase']:<20}")
    
    return results


if __name__ == "__main__":
    test_steam_states()