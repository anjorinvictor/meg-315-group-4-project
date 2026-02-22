# test_integration.py
"""
Test all three core modules together
"""

from core.brayton import brayton_cycle
from core.htc_balance import htc_heat_balance
from core.steam_states import steam_cycle_states

print("=" * 60)
print("AD-HTC FUEL-ENHANCED GAS CYCLE - INTEGRATION TEST")
print("=" * 60)

# Step 1: Run gas cycle
print("\n📌 GAS CYCLE (Brayton)")
print("-" * 40)
gas = brayton_cycle(T1_C=15, rp=6, T3_K=1000, eta_c=0.85, eta_t=0.90, m_dot=100)
print(f"T2: {gas['T2_C']:.1f}°C")
print(f"T4: {gas['T4_C']:.1f}°C")
print(f"Net Power: {gas['W_net_MW']:.2f} MW")
print(f"Efficiency: {gas['efficiency']:.2f}%")

# Step 2: Check HTC heat integration
print("\n📌 HTC HEAT INTEGRATION")
print("-" * 40)
htc = htc_heat_balance(exhaust_temp_C=gas['T4_C'], m_dot_air=100, htc_demand_kW=5000)
print(f"Heat available: {htc['Q_available_MW']:.2f} MW")
print(f"Status: {htc['status']}")
print(htc['message'])

# Step 3: Steam cycle states
print("\n📌 HTC STEAM CYCLE STATES")
print("-" * 40)
steam = steam_cycle_states(p_boiler_bar=40, p_condenser_bar=0.1, t_superheat_C=350)
print(f"Boiler outlet: {steam['points'][2]['T_C']:.1f}°C, {steam['h'][2]:.1f} kJ/kg")
print(f"HTC return: {steam['points'][3]['phase']}, {steam['h'][3]:.1f} kJ/kg")

print("\n✅ All modules working together!")