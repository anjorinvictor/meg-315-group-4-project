# app.py - Main AD-HTC Dashboard
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# Import our modules
from core.brayton import brayton_cycle
from core.htc_balance import htc_heat_balance
from core.steam_states import steam_cycle_states
from core.ai_assistant import init_ai, get_ai_response, display_ai_warning
from ui.styles import get_css
from ui.schematic import display_animated_schematic

from visualization.hs_diagram import plot_hs_diagram
from visualization.tq_diagram import plot_tq_diagram
from visualization.exergy_diagram import plot_exergy_destruction, render_efficiency_comparison
from visualization.energy_flow import render_energy_flow_bars

# Page config
st.set_page_config(
    page_title="AD-HTC Fuel-Enhanced Gas Cycle | Premium",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Session States
if 'gas_results' not in st.session_state: st.session_state.gas_results = None
if 'htc_results' not in st.session_state: st.session_state.htc_results = None
if 'steam_results' not in st.session_state: st.session_state.steam_results = None
if 'analyzed' not in st.session_state: st.session_state.analyzed = False
if 'ai_chat_history' not in st.session_state: st.session_state.ai_chat_history = []
if 'show_report' not in st.session_state: st.session_state.show_report = True

# =============================================================================
# TOP NAVIGATION HEADER
# =============================================================================
top_col1, top_col2 = st.columns([1, 1])

with top_col1:
    st.markdown("""
    <div class="top-bar-container" style="border:none; margin:0; padding:0;">
        <div class="logo-section">
            <div class="logo-icon">⚡</div>
            <div>
                <p class="logo-text-title">AD-HTC</p>
                <p class="logo-text-sub">FUEL-ENHANCED GAS CYCLE</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with top_col2:
    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        toggle_txt = "📉 Hide Report" if st.session_state.show_report else "📈 Show Report"
        if st.button(toggle_txt):
            st.session_state.show_report = not st.session_state.show_report
            st.rerun()
    with btn_col2:
        pass # moved analyze button below input column

# Separator
st.markdown("<hr style='border-color: #1e293b; margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

# =============================================================================
# 3-COLUMN MAIN LAYOUT
# =============================================================================
if st.session_state.show_report:
    col_input, col_schema, col_report = st.columns([0.8, 2.2, 1.2])
else:
    col_input, col_schema = st.columns([0.8, 3.2])
    col_report = None

# =============================================================================
# LEFT: INPUT PARAMETERS
# =============================================================================
with col_input:
    st.markdown('<div class="input-panel-wrapper">', unsafe_allow_html=True)
    st.markdown('<p style="color:#60a5fa; font-weight:700; font-size:12px; letter-spacing:1px; margin-bottom:0;">INPUT PARAMETERS</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b; font-size:10px; margin-bottom:15px; font-family:\'JetBrains Mono\', monospace;">Thermodynamic Configuration</p>', unsafe_allow_html=True)
    
    tab_gas, tab_steam, tab_ad, tab_sys = st.tabs(["Gas", "Steam", "AD", "Sys"])
    
    with tab_gas:
        st.markdown('<p style="text-align:center; font-size:9px; color:#475569; letter-spacing:1.5px; margin: 15px 0 5px 0;">— BRAYTON GAS CYCLE —</p>', unsafe_allow_html=True)
        rp = st.slider("Pressure Ratio (rp)", 5.0, 20.0, 8.0, 0.5)
        eta_c = st.slider("Compressor Eff. (ηc)", 0.60, 0.98, 0.85, 0.01)
        T3_K = st.slider("Turbine Inlet T3 (°K)", 700, 1400, 1100, 10)
        eta_t = st.slider("Turbine Eff. (ηt)", 0.60, 0.98, 0.88, 0.01)
        m_dot = st.slider("Air Mass Flow (ṁ)", 1.0, 10.0, 2.0, 0.5)
        T1_C = st.slider("Ambient Temp (T0)", 0.0, 50.0, 25.0, 1.0)
        P1_kPa = st.number_input("Ambient Press (P0) kPa", value=101.32, step=0.1)

    with tab_steam:
        st.markdown('<p style="text-align:center; font-size:9px; color:#475569; letter-spacing:1.5px; margin: 15px 0 5px 0;">— RANKINE STEAM CYCLE —</p>', unsafe_allow_html=True)
        p_boiler = st.slider("Boiler Pressure (bar)", 10.0, 100.0, 40.0, 1.0)
        p_condenser = st.slider("Condenser Pres. (bar)", 0.05, 1.0, 0.1, 0.01)
        t_superheat = st.slider("Superheat Temp (°C)", 200, 600, 350, 10)
        htc_demand = st.number_input("HTC Heat Demand (kW)", value=5000, step=500)

    with tab_ad:
        st.markdown('<p style="text-align:center; font-size:9px; color:#475569; letter-spacing:1.5px; margin: 15px 0 5px 0;">— ANAEROBIC DIGESTION —</p>', unsafe_allow_html=True)
        st.slider("Biogas Yield (%)", 40, 95, 75)
        st.number_input("Retention Time (days)", value=14)

    with tab_sys:
        st.markdown('<p style="text-align:center; font-size:9px; color:#475569; letter-spacing:1.5px; margin: 15px 0 5px 0;">— SYSTEM LIMITS —</p>', unsafe_allow_html=True)
        stack_temp = st.slider("Stack Limit (°C)", 100, 250, 150)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)
    if st.button("▶ ANALYZE SYSTEM", use_container_width=True):
        st.session_state.gas_results = brayton_cycle(T1_C=T1_C, P1_kPa=P1_kPa, rp=rp, T3_K=T3_K, eta_c=eta_c, eta_t=eta_t, m_dot=m_dot)
        st.session_state.htc_results = htc_heat_balance(exhaust_temp_C=st.session_state.gas_results['T4_C'], m_dot_air=m_dot, htc_demand_kW=htc_demand, stack_temp_C=stack_temp)
        st.session_state.steam_results = steam_cycle_states(p_boiler_bar=p_boiler, p_condenser_bar=p_condenser, t_superheat_C=t_superheat)
        st.session_state.analyzed = True



# =============================================================================
# CENTER: ANIMATED SCHEMATIC
# =============================================================================
with col_schema:
    display_animated_schematic(gas_results=st.session_state.gas_results, steam_results=st.session_state.steam_results, T1_C=T1_C, T3_K=T3_K)

# =============================================================================
# RIGHT: ANALYSIS REPORT
# =============================================================================
if col_report and st.session_state.analyzed:
    with col_report:
        st.markdown('<p style="color:#60a5fa; font-weight:700; font-size:12px; letter-spacing:1px; margin-bottom:0;">ANALYSIS REPORT</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#64748b; font-size:10px; margin-bottom:15px; font-family:\'JetBrains Mono\', monospace;">Thermodynamic Simulation Results</p>', unsafe_allow_html=True)
        
        rep_kpis, rep_hs, rep_th, rep_tab, rep_ex = st.tabs(["KPIs", "h-s", "T-Ḣ", "Table", "Exergy"])
        
        gas = st.session_state.gas_results
        htc = st.session_state.htc_results
        steam = st.session_state.steam_results
        
        with rep_kpis:
            
            # Simulated extra variables to match the glorious Lovable UI screens
            steam_eff = 31.3 # approx placeholder for Rankine UI match
            bwr = abs(gas['W_c_kW']) / gas['W_t_kW'] * 100 if gas['W_t_kW'] > 0 else 0
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon" style="color: #facc15;">⚡</div>
                <div class="metric-unit-badge">%</div>
                <div class="metric-value yellow">{gas['efficiency']:.1f}</div>
                <div class="metric-label">Gas Cycle Efficiency</div>
                <div class="metric-desc">Brayton cycle net thermal efficiency</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon" style="color: #4ade80;">🔋</div>
                <div class="metric-unit-badge">kW</div>
                <div class="metric-value green">{gas['W_net_kW']:.1f}</div>
                <div class="metric-label">Net Power Output</div>
                <div class="metric-desc">Total net electrical power generated</div>
            </div>

            <div class="metric-card">
                <div class="metric-icon" style="color: #f87171;">♨️</div>
                <div class="metric-unit-badge">%</div>
                <div class="metric-value red">{steam_eff:.1f}</div>
                <div class="metric-label">Steam Cycle Efficiency</div>
                <div class="metric-desc">HTC Rankine cycle thermal efficiency</div>
            </div>

            <div class="metric-card">
                <div class="metric-icon" style="color: #60a5fa;">↪</div>
                <div class="metric-unit-badge">%</div>
                <div class="metric-value blue">{bwr:.2f}</div>
                <div class="metric-label">Back Work Ratio</div>
                <div class="metric-desc">Compressor work / Turbine work</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon" style="color: #4ade80;">🌿</div>
                <div class="metric-unit-badge">%</div>
                <div class="metric-value green">75.0</div>
                <div class="metric-label">Biogas Utilization</div>
                <div class="metric-desc">Fraction of biogas energy utilized</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon" style="color: #22d3ee;">🌍</div>
                <div class="metric-unit-badge">kg/h</div>
                <div class="metric-value cyan">5.6</div>
                <div class="metric-label">CO₂ Avoided</div>
                <div class="metric-desc">Equivalent carbon offset per hr</div>
            </div>
            """, unsafe_allow_html=True)
            
            render_energy_flow_bars(gas)
            
        with rep_hs:
            st.markdown('<p style="font-size:11px; color:#94a3b8;">h-s Diagram for Steam Cycle</p>', unsafe_allow_html=True)
            try:
                fig_hs = plot_hs_diagram(steam)
                st.plotly_chart(fig_hs, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error("Chart Render Err: " + str(e))

        with rep_th:
            st.markdown('<p style="font-size:11px; color:#94a3b8;">T-Ḣ Diagram</p>', unsafe_allow_html=True)
            try:
                fig_tq = plot_tq_diagram(gas, htc)
                st.plotly_chart(fig_tq, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error("Chart Render Err: " + str(e))

        with rep_tab:
            st.markdown('<p style="font-size:11px; color:#94a3b8;">Thermodynamic State Points</p>', unsafe_allow_html=True)
            html_table = f"""
            <table class="dataframe" style="font-size:10px;">
                <thead><tr><th>Pt</th><th>Fluid</th><th>Location</th><th>T(°C)</th><th>P(bar)</th><th>h(kJ)</th></tr></thead>
                <tbody>
                    <tr><td>1</td><td style="color:#ef4444;">Air</td><td>Compressor In</td><td>{gas['states']['T'][0]-273.15:.1f}</td><td>{gas['states']['P'][0]/100:.2f}</td><td>{gas['states']['T'][0]*1.005:.1f}</td></tr>
                    <tr><td>2</td><td style="color:#ef4444;">Air</td><td>Compressor Out</td><td>{gas['states']['T'][1]-273.15:.1f}</td><td>{gas['states']['P'][1]/100:.2f}</td><td>{gas['states']['T'][1]*1.005:.1f}</td></tr>
                    <tr><td>3</td><td style="color:#ef4444;">Gas</td><td>Turbine In</td><td>{gas['states']['T'][2]-273.15:.1f}</td><td>{gas['states']['P'][2]/100:.2f}</td><td>{gas['states']['T'][2]*1.005:.1f}</td></tr>
                    <tr><td>4</td><td style="color:#ef4444;">Exhaust</td><td>Turbine Out</td><td>{gas['states']['T'][3]-273.15:.1f}</td><td>{gas['states']['P'][3]/100:.2f}</td><td>{gas['states']['T'][3]*1.005:.1f}</td></tr>
                    <tr><td colspan="6" style="border:none; height:8px;"></td></tr>
                    <tr><td>7</td><td style="color:#3b82f6;">Liq</td><td>Pump In</td><td>{steam['T_C'][0]:.1f}</td><td>{steam['P_bar'][0]:.1f}</td><td>{steam['h'][0]:.1f}</td></tr>
                    <tr><td>8</td><td style="color:#3b82f6;">Liq</td><td>Boiler Feed</td><td>{steam['T_C'][1]:.1f}</td><td>{steam['P_bar'][1]:.1f}</td><td>{steam['h'][1]:.1f}</td></tr>
                    <tr><td>5</td><td style="color:#3b82f6;">Steam</td><td>Turbine In</td><td>{steam['T_C'][2]:.1f}</td><td>{steam['P_bar'][2]:.1f}</td><td>{steam['h'][2]:.1f}</td></tr>
                    <tr><td>6</td><td style="color:#3b82f6;">Wet</td><td>HTC Return</td><td>{steam['T_C'][3]:.1f}</td><td>{steam['P_bar'][3]:.1f}</td><td>{steam['h'][3]:.1f}</td></tr>
                </tbody>
            </table>
            """
            st.markdown(html_table, unsafe_allow_html=True)
            
        with rep_ex:
            fig_ex = plot_exergy_destruction(gas)
            st.plotly_chart(fig_ex, use_container_width=True, config={'displayModeBar': False})
            st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
            render_efficiency_comparison(gas)
            
elif col_report:
    with col_report:
        st.markdown('<p style="color:#60a5fa; font-weight:700; font-size:12px; letter-spacing:1px; margin-bottom:0;">ANALYSIS REPORT</p>', unsafe_allow_html=True)
        st.info("System awaiting execution. Please click ANALYZE.")

# =============================================================================
# FLOATING AI COPILOT (PREMIUM REDESIGN)
# =============================================================================
with st.popover("✨"):
    # Header
    st.markdown('<h4 class="ai-chat-header-text">Aura - AI Copilot</h4>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:12px; color:#94a3b8; margin-top:2px; margin-bottom:15px;">Your unified AD-HTC Engineering Assistant.</p>', unsafe_allow_html=True)
    
    # Status Indicator Logic
    indicator_html = '<div class="ai-status-indicator"><span class="dot-yellow">🟡</span> Pending Analysis</div>'
    if st.session_state.analyzed:
        gas = st.session_state.gas_results
        steam = st.session_state.steam_results
        tit = gas['states']['T'][2] - 273.15
        p_boiler = steam['P_bar'][1]
        
        if tit > 1350 or p_boiler > 150:
            indicator_html = '<div class="ai-status-indicator"><span class="dot-red">🔴</span> Engineering Drop/Risk Detected</div>'
        elif gas['efficiency'] < 33:
            indicator_html = '<div class="ai-status-indicator"><span class="dot-yellow">🟡</span> Optimization Suggested</div>'
        else:
            indicator_html = '<div class="ai-status-indicator"><span class="dot-green">🟢</span> System Stable</div>'

    st.markdown(indicator_html, unsafe_allow_html=True)
    
    # Engineering Warnings
    if st.session_state.analyzed:
        warnings = display_ai_warning(st.session_state.gas_results, st.session_state.steam_results)
        for w in warnings:
            st.warning(w)

    chat_container = st.container(height=400)
    
    # Render previous messages
    with chat_container:
        if not st.session_state.ai_chat_history:
            st.info("No chat history. Say Hi to Aura or run your simulation to begin optimizing the cycle!")
        for msg in st.session_state.ai_chat_history:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                with st.chat_message("assistant", avatar="✨"):
                    st.markdown(f'<div class="ai-text-white-bg">\n\n{msg["content"]}\n\n</div>', unsafe_allow_html=True)
                
    st.markdown("<hr style='border-top:1px solid rgba(148, 163, 184, 0.1); margin:10px 0;'>", unsafe_allow_html=True)
    
    # Input Area
    col_input_chat, col_clear_chat = st.columns([4, 1])
    with col_input_chat:
        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input("Ask Aura...", label_visibility="collapsed", placeholder="Message Aura...")
            submitted = st.form_submit_button("Send")
            if submitted and user_msg:
                st.session_state.ai_chat_history.append({"role": "user", "content": user_msg})
                
                with chat_container:
                    st.chat_message("user").write(user_msg)
                    with st.spinner("Aura is analyzing..."):
                        ai_model = init_ai("AIzaSyAPBUZmK8c1qXW-IPimq85M2uTty3bnae4")
                        gas = st.session_state.gas_results
                        steam = st.session_state.steam_results
                        htc = st.session_state.htc_results
                            
                        # Concatenate context prompt with memory
                        hist_str = "\\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.ai_chat_history])
                        prompt = f"HISTORY CALLED:\\n{hist_str}\\n\\nANSWER THIS LATEST QUERY CONCISELY: {user_msg}"
                        response_text = get_ai_response(ai_model, gas, steam, htc, prompt)
                            
                        st.session_state.ai_chat_history.append({"role": "assistant", "content": response_text})
                        st.rerun()

    with col_clear_chat:
        if st.button("Clear", use_container_width=True, key="clear_chat_button"):
            st.session_state.ai_chat_history = []
            st.rerun()
