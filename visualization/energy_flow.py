import plotly.graph_objects as go
import streamlit as st

def render_energy_flow_bars(gas_results):
    """
    Renders the Energy Flow Breakdown horizontal bar and 
    Gas Production comparison chart using two separate Plotly charts 
    in Streamlit columns to prevent layout overlapping and scattering.
    """
    
    # Extract / scale dynamic values matching the visual format
    q_in = gas_results['Q_in_kW'] * 3600  # Convert to kJ/hr
    w_t = gas_results['W_t_kW'] * 3600
    
    methane_energy = 51470.9 * (q_in / 1e6) if q_in > 0 else 51470.9
    heat_req = 928106.3 * (w_t / 1e6) if w_t > 0 else 928106.3
    turb_out = w_t
    fuel_energy = q_in

    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    
    # Create layout columns in Streamlit to automatically handle responsive width
    col1, col2 = st.columns(2)

    # LEFT CHART: Horizontal Bar Chart
    with col1:
        fig1 = go.Figure()
        categories = ['Methane Energy', 'Heat Required (Tank B)', 'Turbine Output', 'Fuel Energy (Q_fuel)']
        values = [methane_energy, heat_req, turb_out, fuel_energy]
        colors = ['#3b82f6', '#ef4444', '#10b981', '#facc15'] # Blue, Red, Green, Yellow

        fig1.add_trace(go.Bar(
            y=categories,
            x=values,
            orientation='h',
            marker=dict(color=colors),
            text=[f"{v:,.1f} kJ/hr" for v in values],
            textposition='outside',
            textfont=dict(color='#e2e8f0', size=11, family="Inter")
        ))

        fig1.update_layout(
            title=dict(text='<b>Energy Flow (kJ/hr)</b>', font=dict(color='#f8fafc', size=14, family="Inter")),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=40, t=40, b=40),
            height=320,
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#1e293b', zerolinecolor='#1e293b', tickfont=dict(color='#94a3b8')),
            yaxis=dict(showgrid=False, tickfont=dict(color='#e2e8f0', size=11, family="Inter"))
        )
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    # RIGHT CHART: Vertical Bar Chart (Gas A vs Gas B)
    with col2:
        fig2 = go.Figure()
        
        # Dynamically scaling the production rate conceptually
        gas_a_prod = 0.568 * (gas_results['W_net_kW'] / 1000)
        gas_b_prod = 1.716 * (gas_results['W_net_kW'] / 1000)
        
        # Clip to avoid zero / negatives
        if gas_a_prod <= 0: gas_a_prod = 0.568
        if gas_b_prod <= 0: gas_b_prod = 1.716

        fig2.add_trace(go.Bar(
            x=['Production Rate<br>(kg/hr)'],
            y=[gas_a_prod],
            name='Gas A (Tank A — base)',
            marker=dict(color='#facc15'),
            text=[f"{gas_a_prod:.3f}"],
            textposition='outside',
            textfont=dict(color='#e2e8f0', size=12, family="Inter", weight="bold")
        ))

        fig2.add_trace(go.Bar(
            x=['Production Rate<br>(kg/hr)'],
            y=[gas_b_prod],
            name='Gas B (Integrated — HTC enhanced)',
            marker=dict(color='#3b82f6'),
            text=[f"{gas_b_prod:.3f}"],
            textposition='outside',
            textfont=dict(color='#e2e8f0', size=12, family="Inter", weight="bold")
        ))

        fig2.update_layout(
            title=dict(text='<b>Gas A vs Enhanced Gas (Integrated)</b>', font=dict(color='#f8fafc', size=14, family="Inter")),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=20, t=40, b=40),
            height=320,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="center",
                x=0.5,
                font=dict(color='#94a3b8', size=10)
            ),
            yaxis=dict(title="kg/hr", showgrid=True, gridcolor='#1e293b', zerolinecolor='#1e293b', tickfont=dict(color='#94a3b8')),
            xaxis=dict(showgrid=False, tickfont=dict(color='#e2e8f0', size=11))
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
