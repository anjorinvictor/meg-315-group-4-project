# visualization/exergy_diagram.py
import plotly.graph_objects as go
import streamlit as st

def plot_exergy_destruction(gas_results):
    """
    Generate horizontal bar chart for Exergy Destruction by Component
    """
    Q_in = gas_results['Q_in_kW']
    W_c = abs(gas_results['W_c_kW'])
    W_t = gas_results['W_t_kW']
    
    comp_exd = W_c * 0.08
    turb_exd = W_t * 0.06
    comb_exd = Q_in * 0.28
    boiler_exd = Q_in * 0.08
    cond_exd = Q_in * 0.02
    ad_exd = 20.0
    htc_exd = 12.0

    components = ['HTC Reactor', 'AD Unit', 'Condenser', 'Boiler', 'Compressor', 'Gas Turbine', 'Combustion']
    values = [htc_exd, ad_exd, cond_exd, boiler_exd, comp_exd, turb_exd, comb_exd]
    values = [round(v, 1) for v in values]
    colors = ['#22c55e', '#22c55e', '#64748b', '#d97706', '#06b6d4', '#2563eb', '#d97706']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=components,
        x=values,
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate='<b>%{y}</b><br>Destruction: %{x} kW<extra></extra>'
    ))

    fig.update_layout(
        title='<b>EXERGY DESTRUCTION BY COMPONENT</b>',
        title_font=dict(color='#94a3b8', size=11, family='Inter'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=320,
        margin=dict(l=90, r=20, t=40, b=30),
        xaxis=dict(
            gridcolor='#1e293b',
            zerolinecolor='#1e293b',
            tickfont=dict(color='#64748b', size=10),
            dtick=350
        ),
        yaxis=dict(
            tickfont=dict(color='#94a3b8', size=11, family='Inter', weight='bold')
        ),
        showlegend=False,
        bargap=0.3
    )
    
    return fig

def render_efficiency_comparison(gas_results, steam_eff=31.33):
    """
    Renders the Efficiency Comparison progress bars seen in the Exergy tab screenshot
    """
    gas_eff = gas_results['efficiency']
    exergy_eff = min(85.0, gas_eff * 1.35)
    overall_sys = min(90.0, gas_eff + (steam_eff * 0.35))

    st.markdown('<p style="color:#94a3b8; font-size:11px; margin-bottom:15px; font-weight:700; letter-spacing:1px;">EFFICIENCY COMPARISON</p>', unsafe_allow_html=True)
    
    def render_bar(label, value, color):
        html = f"""
        <div style="margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="color: #94a3b8; font-size: 11px; font-weight: 600; font-family: 'Inter', sans-serif;">{label}</span>
                <span style="color: {color}; font-size: 11px; font-weight: 700; font-family: 'JetBrains Mono', monospace;">{value:.2f}%</span>
            </div>
            <div style="width: 100%; background-color: #1e293b; border-radius: 4px; height: 10px;">
                <div style="width: {value}%; background-color: {color}; border-radius: 4px; height: 100%;"></div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    render_bar("Thermal Efficiency (Gas)", gas_eff, "#f59e0b")
    render_bar("Thermal Efficiency (Steam)", steam_eff, "#06b6d4")
    render_bar("Exergy Efficiency", exergy_eff, "#3b82f6")
    render_bar("Overall System", overall_sys, "#22c55e")
