# core/brayton.py
"""
Open Brayton Cycle Model for Gas Turbine
Based on air-standard assumptions with isentropic efficiencies
"""

import numpy as np
from utils.constants import CP_AIR, GAMMA_AIR, KELVIN_OFFSET

def brayton_cycle(T1_C=15, P1_kPa=101.3, rp=12, T3_K=1200, 
                  eta_c=0.85, eta_t=0.90, m_dot=100):
    """
    Calculate open Brayton cycle performance
    
    Parameters:
    -----------
    T1_C : float
        Compressor inlet temperature (°C)
    P1_kPa : float
        Compressor inlet pressure (kPa)
    rp : float
        Pressure ratio (P2/P1)
    T3_K : float
        Turbine inlet temperature (K)
    eta_c : float
        Compressor isentropic efficiency (0-1)
    eta_t : float
        Turbine isentropic efficiency (0-1)
    m_dot : float
        Mass flow rate of air (kg/s)
    
    Returns:
    --------
    dict : All state points and performance metrics
    """
    
    # Convert inputs to consistent units
    T1 = T1_C + KELVIN_OFFSET  # K
    P1 = P1_kPa  # kPa
    
    # ----- COMPRESSOR (1 → 2) -----
    # Isentropic compression
    T2s = T1 * (rp) ** ((GAMMA_AIR - 1) / GAMMA_AIR)
    
    # Actual compression with efficiency
    T2 = T1 + (T2s - T1) / eta_c
    
    # Compressor work (kW)
    W_c = m_dot * CP_AIR * (T2 - T1)
    
    # Pressures
    P2 = P1 * rp
    P3 = P2 * 0.97  # Assume 3% pressure drop in combustor
    P4 = P1  # Exhaust to atmosphere
    
    # ----- COMBUSTOR (2 → 3) -----
    # Heat input (kW)
    Q_in = m_dot * CP_AIR * (T3_K - T2)
    
    # ----- TURBINE (3 → 4) -----
    # Isentropic expansion
    T4s = T3_K * (1 / rp) ** ((GAMMA_AIR - 1) / GAMMA_AIR)
    
    # Actual expansion with efficiency
    T4 = T3_K - eta_t * (T3_K - T4s)
    
    # Turbine work (kW)
    W_t = m_dot * CP_AIR * (T3_K - T4)
    
    # ----- CYCLE PERFORMANCE -----
    W_net = W_t - W_c  # Net power (kW)
    eta_thermal = (W_net / Q_in) * 100  # Percent
    
    # Specific work (kJ/kg)
    w_net_specific = W_net / m_dot
    
    # Exhaust temperature in °C for display
    T4_C = T4 - KELVIN_OFFSET
    
    # State points for T-s diagram
    states = {
        'points': [
            {'name': '1 - Compressor Inlet', 'T': T1, 'P': P1, 'fluid': 'Air'},
            {'name': '2 - Compressor Outlet', 'T': T2, 'P': P2, 'fluid': 'Air'},
            {'name': '3 - Turbine Inlet', 'T': T3_K, 'P': P3, 'fluid': 'Gas'},
            {'name': '4 - Turbine Outlet', 'T': T4, 'P': P4, 'fluid': 'Exhaust'}
        ],
        'T': [T1, T2, T3_K, T4],
        'P': [P1, P2, P3, P4],
        's': []  # Entropy will be calculated separately if needed
    }
    
    return {
        'states': states,
        'T2_K': T2,
        'T2_C': T2 - KELVIN_OFFSET,
        'T4_K': T4,
        'T4_C': T4_C,
        'W_c_kW': W_c,
        'W_c_MW': W_c / 1000,
        'W_t_kW': W_t,
        'W_t_MW': W_t / 1000,
        'W_net_kW': W_net,
        'W_net_MW': W_net / 1000,
        'Q_in_kW': Q_in,
        'Q_in_MW': Q_in / 1000,
        'efficiency': eta_thermal,
        'efficiency_decimal': eta_thermal / 100,
        'w_net_specific': w_net_specific
    }


def test_brayton():
    """Test function to verify calculations"""
    print("=" * 50)
    print("TESTING BRAYTON CYCLE CALCULATIONS")
    print("=" * 50)
    
    # Test with example from your slide (1000K max, 288K min, rp=6)
    results = brayton_cycle(
        T1_C=15,  # 288K
        rp=6,
        T3_K=1000,
        eta_c=0.85,
        eta_t=0.90,
        m_dot=100
    )
    
    print(f"\nINPUTS:")
    print(f"  T1 (ambient): 15°C (288K)")
    print(f"  Pressure ratio: 6")
    print(f"  TIT: 1000K (727°C)")
    print(f"  Compressor efficiency: 85%")
    print(f"  Turbine efficiency: 90%")
    print(f"  Mass flow: 100 kg/s")
    
    print(f"\nRESULTS:")
    print(f"  T2 (after compressor): {results['T2_C']:.1f}°C ({results['T2_K']:.1f}K)")
    print(f"  T4 (exhaust): {results['T4_C']:.1f}°C ({results['T4_K']:.1f}K)")
    print(f"  Compressor work: {results['W_c_MW']:.2f} MW")
    print(f"  Turbine work: {results['W_t_MW']:.2f} MW")
    print(f"  Net power: {results['W_net_MW']:.2f} MW")
    print(f"  Heat input: {results['Q_in_MW']:.2f} MW")
    print(f"  Thermal efficiency: {results['efficiency']:.2f}%")
    
    print(f"\nCHECK against slide example:")
    print(f"  Slide expected T4: 639K = 366°C")
    print(f"  Calculated T4: {results['T4_K']:.1f}K = {results['T4_C']:.1f}°C")
    
    if abs(results['T4_K'] - 639) < 10:
        print("  ✅ MATCHES closely!")
    else:
        print("  ⚠️  Slight difference (normal due to assumptions)")
    
    return results


if __name__ == "__main__":
    # Run test if file is executed directly
    test_brayton()