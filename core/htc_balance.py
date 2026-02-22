# core/htc_balance.py
"""
HTC Heat Balance Model
Calculates if turbine exhaust can meet HTC reactor heat demand
"""

from utils.constants import CP_AIR, KELVIN_OFFSET

def htc_heat_balance(exhaust_temp_C, m_dot_air=100, htc_demand_kW=5000, stack_temp_C=170):
    """
    Check if exhaust can meet HTC heat demand
    
    Parameters:
    -----------
    exhaust_temp_C : float
        Temperature of exhaust from turbine (°C)
    m_dot_air : float
        Mass flow rate of air (kg/s)
    htc_demand_kW : float
        Heat required by HTC reactor (kW)
    stack_temp_C : float
        Minimum stack temperature to avoid corrosion (°C)
    
    Returns:
    --------
    dict : Heat availability and feasibility status
    """
    
    # Convert to Kelvin for calculations
    exhaust_temp_K = exhaust_temp_C + KELVIN_OFFSET
    stack_temp_K = stack_temp_C + KELVIN_OFFSET
    
    # Heat available in exhaust (cooling to stack temp)
    # Q = m_dot * cp * (T_exhaust - T_stack)
    Q_available_kW = m_dot_air * CP_AIR * (exhaust_temp_K - stack_temp_K)
    
    # Convert to MW for display
    Q_available_MW = Q_available_kW / 1000
    htc_demand_MW = htc_demand_kW / 1000
    
    # Feasibility check
    if Q_available_kW >= htc_demand_kW:
        status = "✅ FEASIBLE"
        excess_kW = Q_available_kW - htc_demand_kW
        excess_MW = excess_kW / 1000
        
        # Final exhaust temperature after supplying HTC demand
        # T_final = T_exhaust - (Q_demand)/(m_dot * cp)
        temp_drop = htc_demand_kW / (m_dot_air * CP_AIR)
        exhaust_final_K = exhaust_temp_K - temp_drop
        exhaust_final_C = exhaust_final_K - KELVIN_OFFSET
        
        message = f"Exhaust can supply HTC demand with {excess_MW:.2f} MW excess"
    else:
        status = "⚠️ NOT FEASIBLE"
        excess_kW = 0
        excess_MW = 0
        deficit_kW = htc_demand_kW - Q_available_kW
        deficit_MW = deficit_kW / 1000
        
        # Can't meet demand, exhaust goes to stack temp
        exhaust_final_C = stack_temp_C
        
        message = f"Insufficient heat - need {deficit_MW:.2f} MW more"
    
    # Calculate heat exchanger effectiveness
    if htc_demand_kW > 0:
        if Q_available_kW > 0:
            hx_effectiveness = (htc_demand_kW / Q_available_kW) * 100
            if hx_effectiveness > 100:
                hx_effectiveness = 100
        else:
            hx_effectiveness = 0
    else:
        hx_effectiveness = 0
    
    return {
        'Q_available_kW': Q_available_kW,
        'Q_available_MW': Q_available_MW,
        'htc_demand_kW': htc_demand_kW,
        'htc_demand_MW': htc_demand_MW,
        'status': status,
        'message': message,
        'excess_kW': excess_kW,
        'excess_MW': excess_MW,
        'exhaust_final_C': exhaust_final_C,
        'hx_effectiveness': hx_effectiveness,
        'temp_drop_C': temp_drop if 'temp_drop' in locals() else 0
    }


def test_htc_balance():
    """Test function for HTC heat balance"""
    print("=" * 50)
    print("TESTING HTC HEAT BALANCE")
    print("=" * 50)
    
    # Test with typical values
    results = htc_heat_balance(
        exhaust_temp_C=366,  # From our Brayton example
        m_dot_air=100,
        htc_demand_kW=5000,  # 5 MW demand
        stack_temp_C=170
    )
    
    print(f"\nINPUTS:")
    print(f"  Exhaust temperature: 366°C")
    print(f"  Mass flow: 100 kg/s")
    print(f"  HTC demand: 5000 kW (5 MW)")
    print(f"  Stack limit: 170°C")
    
    print(f"\nRESULTS:")
    print(f"  Heat available in exhaust: {results['Q_available_MW']:.2f} MW")
    print(f"  Status: {results['status']}")
    print(f"  {results['message']}")
    print(f"  Heat exchanger effectiveness: {results['hx_effectiveness']:.1f}%")
    print(f"  Final exhaust temperature: {results['exhaust_final_C']:.1f}°C")
    
    # Test with impossible demand
    print(f"\n\nTEST 2 - High demand (20 MW):")
    results2 = htc_heat_balance(
        exhaust_temp_C=366,
        m_dot_air=100,
        htc_demand_kW=20000,  # 20 MW demand
        stack_temp_C=170
    )
    print(f"  Status: {results2['status']}")
    print(f"  {results2['message']}")
    
    return results


if __name__ == "__main__":
    test_htc_balance()