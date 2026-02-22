import plotly.graph_objects as go
import numpy as np

def plot_tq_diagram(gas_results, htc_results=None):
    """
    Generate T-Ḣ Diagram mapping Cumulative Heat Transfer to Temperature,
    reproducing the curve in the requested Image 5 reference.
    """
    T1_C = gas_results['states']['T'][0] - 273.15
    T2_C = gas_results['T2_C']
    T3_C = gas_results['states']['T'][2] - 273.15
    T4_C = gas_results['T4_C']
    
    W_c = gas_results['W_c_kW']
    Q_in = gas_results['Q_in_kW']
    W_t = gas_results['W_t_kW']
    # If htc_results has 'Q_available_kW', plot that for recovery, else 0
    Q_rec = htc_results['htc_demand_kW'] if htc_results else 0
    T_stack = htc_results['exhaust_final_C'] if htc_results else T4_C
    
    gap_x = max(200, W_c * 0.3)
    
    points_x = []
    points_y = []
    current_x = 0
    
    def add_curve(start_T, end_T, delta_x):
        nonlocal current_x
        if delta_x <= 0: return
        xs = np.linspace(current_x, current_x + delta_x, 30)
        # Smooth S-curve transition
        norm_x = (xs - current_x) / delta_x
        ys = start_T + (end_T - start_T) * (3 * norm_x**2 - 2 * norm_x**3)
        points_x.extend(xs)
        points_y.extend(ys)
        current_x += delta_x

    def add_flat():
        nonlocal current_x
        xs = np.linspace(current_x, current_x + gap_x, 10)
        ys = np.full(10, points_y[-1] if points_y else 0)
        points_x.extend(xs)
        points_y.extend(ys)
        current_x += gap_x

    # 1. Compression Work
    add_curve(T1_C, T2_C, W_c)
    add_flat()
    
    # 2. Combustion Heat
    add_curve(T2_C, T3_C, Q_in)
    add_flat()
    
    # 3. Turbine Work (expansion drops T)
    add_curve(T3_C, T4_C, W_t)
    add_flat()
    
    # 4. Heat Recovery
    if Q_rec > 0 and T4_C > T_stack:
        add_curve(T4_C, T_stack, Q_rec)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=points_x, y=points_y,
        mode='lines',
        name='Gas Cycle Temp',
        line=dict(color='#f59e0b', width=3),
        fill='tozeroy',
        fillcolor='rgba(245, 158, 11, 0.1)',
        hovertemplate='Q: %{x:.1f} kW<br>T: %{y:.1f} °C<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text='<b>T-Ḣ DIAGRAM — GAS CYCLE PROCESSES</b>', font=dict(color='#94a3b8', size=13, family='JetBrains Mono')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Cumulative Heat Transfer (kW)', color='#94a3b8', showgrid=True, gridcolor='#1e293b', griddash='dash', zeroline=False),
        yaxis=dict(title='Temperature (°C)', color='#94a3b8', showgrid=True, gridcolor='#1e293b', griddash='dash', zeroline=False, dtick=300),
        margin=dict(l=60, r=40, t=50, b=50),
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5,
            font=dict(color='#f59e0b', family='JetBrains Mono')
        ),
        hovermode="x unified"
    )
    
    return fig