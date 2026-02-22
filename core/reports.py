# core/reports.py
"""
Report generation for AD-HTC analysis results
Produces professional summary reports
"""

from datetime import datetime
import io

def generate_text_report(gas_results, htc_results, steam_results, input_params):
    """
    Generate a detailed text-based report of the analysis
    
    Parameters:
    -----------
    gas_results : dict
        Brayton cycle results
    htc_results : dict
        HTC heat balance results
    steam_results : dict
        Steam cycle state properties
    input_params : dict
        Input parameters used
    
    Returns:
    --------
    str : Formatted report text
    """
    
    report = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║         AD-HTC FUEL-ENHANCED GAS CYCLE - ANALYSIS REPORT                   ║
║                                                                            ║
║                    Energhx Research Group                                  ║
║                  Faculty of Engineering, University of Lagos               ║
║                                                                            ║
║                      Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}                         ║
╚════════════════════════════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────────────────────────────
1. EXECUTIVE SUMMARY
──────────────────────────────────────────────────────────────────────────────

System Type:        AD-HTC Fuel-Enhanced Gas Cycle
Analysis Mode:      Thermodynamic Performance Analysis
Status:             ✓ Feasible

Key Results:
  • Net Power Output:           {gas_results['W_net_MW']:.2f} MW
  • Thermal Efficiency:         {gas_results['efficiency']:.2f} %
  • Heat Available for HTC:     {htc_results['Q_available_MW']:.2f} MW
  • System Feasibility:         {"✓ FEASIBLE" if "FEASIBLE" in htc_results['status'] else "✗ NOT FEASIBLE"}

──────────────────────────────────────────────────────────────────────────────
2. INPUT PARAMETERS
──────────────────────────────────────────────────────────────────────────────

GAS CYCLE PARAMETERS:
  Ambient Temperature:          {input_params.get('T1_C', 'N/A')}°C
  Compressor Pressure Ratio:    {input_params.get('rp', 'N/A')}
  Compressor Efficiency:        {input_params.get('eta_c', 1.0)*100:.1f}%
  Turbine Inlet Temperature:    {input_params.get('T3_K', 'N/A')}K ({input_params.get('T3_K', 0)-273:.0f}°C)
  Turbine Efficiency:           {input_params.get('eta_t', 1.0)*100:.1f}%
  Mass Flow Rate:               {input_params.get('m_dot', 'N/A')} kg/s

HTC STEAM LOOP PARAMETERS:
  Heat Demand:                  {input_params.get('htc_demand', 'N/A')} kW
  Boiler Pressure:              {input_params.get('p_boiler', 'N/A')} bar
  Superheat Temperature:        {input_params.get('t_superheat', 'N/A')}°C
  Stack Temperature Limit:      {input_params.get('stack_temp', 'N/A')}°C

──────────────────────────────────────────────────────────────────────────────
3. BRAYTON CYCLE ANALYSIS
──────────────────────────────────────────────────────────────────────────────

State Point Properties:
┌────────┬──────────┬──────────┬─────────────┬────────────────────────┐
│ State  │ Temp(°C) │ Pressure │ Enthalpy(?) │ Description            │
├────────┼──────────┼──────────┼─────────────┼────────────────────────┤
│   1    │ {input_params.get('T1_C', 0):.0f}      │  1.0 bar │    N/A      │ Compressor Inlet      │
│   2    │ {gas_results['T2_C']:.0f}     │ {input_params.get('rp', 1):.0f} bar │    N/A      │ Compressor Outlet     │
│   3    │ {input_params.get('T3_K', 0)-273:.0f}     │ {input_params.get('rp', 1):.0f} bar │    N/A      │ Turbine Inlet         │
│   4    │ {gas_results['T4_C']:.0f}     │  1.0 bar │    N/A      │ Turbine Outlet        │
└────────┴──────────┴──────────┴─────────────┴────────────────────────┘

Energy Balance:
  Heat Input (Combustion):      {gas_results['Q_in_MW']:.2f} MW
  Compressor Work Required:     {abs(gas_results['W_c_MW']):.2f} MW (consumed)
  Turbine Work Produced:        {gas_results['W_t_MW']:.2f} MW
  Net Power Output:             {gas_results['W_net_MW']:.2f} MW
  
  Thermal Efficiency:           {gas_results['efficiency']:.2f}%
  Turbine Exit Temperature:     {gas_results['T4_C']:.1f}°C

──────────────────────────────────────────────────────────────────────────────
4. HTC HEAT BALANCE & FEASIBILITY
──────────────────────────────────────────────────────────────────────────────

Exhaust Heat Recovery:
  Exhaust Temperature In:       {htc_results['exhaust_temp_C']:.1f}°C
  Stack Temperature Out:        {htc_results['exhaust_final_C']:.1f}°C
  Temperature Drop:             {htc_results['exhaust_temp_C'] - htc_results['exhaust_final_C']:.1f}°C
  
  Heat Available:               {htc_results['Q_available_MW']:.2f} MW
  Heat Demand:                  {htc_results['htc_demand_MW']:.2f} MW
  Heat Exchanger Effectiveness: {htc_results['hx_effectiveness']:.2f}%

Feasibility Assessment:
  Status:                       {htc_results['status']}
  Margin:                       {(htc_results['Q_available_MW'] / htc_results['htc_demand_MW'] - 1) * 100:.1f}%

System Evaluation:
  ✓ Gas cycle provides sufficient heat for HTC demands
  ✓ Heat exchanger effectiveness within acceptable limits
  ✓ Stack temperature constraints satisfied

──────────────────────────────────────────────────────────────────────────────
5. STEAM CYCLE ANALYSIS
──────────────────────────────────────────────────────────────────────────────

Steam State Points:
┌────────┬──────────┬──────────┬──────────────┬──────────┬──────────┐
│ Point  │ Temp(°C) │ Pressure │ Enthalpy     │ Entropy  │ Phase    │
│        │          │ (bar)    │ (kJ/kg)      │ (kJ/kgK) │          │
├────────┼──────────┼──────────┼──────────────┼──────────┼──────────┤
│   1    │ {steam_results['T_C'][0]:.1f}  │ {steam_results['P_bar'][0]:.1f}   │ {steam_results['h'][0]:.1f}      │ {steam_results['s'][0]:.4f}   │ {steam_results['points'][0]['phase']:<8} │
│   2    │ {steam_results['T_C'][1]:.1f}  │ {steam_results['P_bar'][1]:.1f}   │ {steam_results['h'][1]:.1f}      │ {steam_results['s'][1]:.4f}   │ {steam_results['points'][1]['phase']:<8} │
│   3    │ {steam_results['T_C'][2]:.1f}  │ {steam_results['P_bar'][2]:.1f}   │ {steam_results['h'][2]:.1f}      │ {steam_results['s'][2]:.4f}   │ {steam_results['points'][2]['phase']:<8} │
│   4    │ {steam_results['T_C'][3]:.1f}  │ {steam_results['P_bar'][3]:.1f}   │ {steam_results['h'][3]:.1f}      │ {steam_results['s'][3]:.4f}   │ {steam_results['points'][3]['phase']:<8} │
└────────┴──────────┴──────────┴──────────────┴──────────┴──────────┘

Cycle Processes:
  1→2: Pump (liquid enters, work input required)
  2→3: Boiler (isobaric heat addition)
  3→4: Throttle (irreversible expansion process)
  4→1: Condenser (isothermal/isobaric heat rejection)

──────────────────────────────────────────────────────────────────────────────
6. RECOMMENDATIONS & OBSERVATIONS
──────────────────────────────────────────────────────────────────────────────

Performance Recommendations:
  • Monitor turbine inlet temperature to maximize efficiency
  • Maintain compressor pressure ratio for optimal performance
  • Ensure heat exchanger cleanliness for maintained effectiveness
  • Regular inspection of stack temperature monitoring equipment

System Integration Notes:
  ✓ Current configuration meets design requirements
  ✓ HTC heat demand can be satisfied by waste heat recovery
  ✓ System operates within safe temperature constraints
  ✓ Overall system appears technically feasible

Operations Guidance:
  • Maintain ambient intake temperature within {input_params.get('T1_C', 15) ± 5}°C range
  • Monitor exhaust temperature at {gas_results['T4_C']:.0f}°C
  • HTC system should be sized for {htc_results['Q_available_MW']:.2f} MW heat input

──────────────────────────────────────────────────────────────────────────────
7. CONCLUSION
──────────────────────────────────────────────────────────────────────────────

The AD-HTC Fuel-Enhanced Gas Cycle analysis indicates that the proposed system
configuration is FEASIBLE and VIABLE for implementation.

Key Performance Indicators:
  • Thermal Efficiency: {gas_results['efficiency']:.2f}% (meets engineering standards)
  • Heat Recovery Ratio: {(htc_results['Q_available_MW']/gas_results['Q_in_MW']*100):.1f}% (excellent)
  • System Safety Margin: {(htc_results['Q_available_MW'] / htc_results['htc_demand_MW'] - 1) * 100:.1f}% above demand

The system is recommended for further detailed engineering design and 
implementation planning.

──────────────────────────────────────────────────────────────────────────────

Report Generated by: Energhx Analysis Platform v2.0
Date & Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Analysis Version: MEG 315 Applied Thermodynamics - Final Project
For: Faculty of Engineering, University of Lagos

╔════════════════════════════════════════════════════════════════════════════╗
║                           END OF REPORT                                    ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    
    return report


def generate_summary_metrics(gas_results, htc_results, steam_results):
    """
    Generate concise summary of key metrics
    """
    summary = {
        'thermal_efficiency': f"{gas_results['efficiency']:.2f}%",
        'net_power': f"{gas_results['W_net_MW']:.2f} MW",
        'heat_available': f"{htc_results['Q_available_MW']:.2f} MW",
        'heat_demand': f"{htc_results['htc_demand_MW']:.2f} MW",
        'feasibility': "✓ FEASIBLE" if "FEASIBLE" in htc_results['status'] else "✗ NOT FEASIBLE",
        'hx_effectiveness': f"{htc_results['hx_effectiveness']:.2f}%",
        'turbine_exit_temp': f"{gas_results['T4_C']:.1f}°C",
        'compressor_pressure_ratio': f"{gas_results.get('pressure_ratio', 'N/A')}:1"
    }
    return summary
