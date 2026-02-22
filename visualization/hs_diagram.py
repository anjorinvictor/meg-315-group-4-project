import plotly.graph_objects as go
import numpy as np

def plot_hs_diagram(steam_results):
    s = steam_results['s']  
    h = steam_results['h']  

    fig = go.Figure()

    # Generate a generic saturation dome
    s_liq = np.linspace(0.1, 4.3, 50)
    h_liq = 0 + (2800 / 4.2**2) * (s_liq - 0.1)**2
    s_vap = np.linspace(4.3, 9.0, 50)
    h_vap = 2800 - 300 * ((s_vap - 4.3) / 4.7)**2
    s_dome = np.concatenate((s_liq, s_vap))
    h_dome = np.concatenate((h_liq, h_vap))

    # Plot saturation dome
    fig.add_trace(go.Scatter(
        x=s_dome, y=h_dome,
        mode='lines',
        name='Saturation Dome',
        line=dict(color='#64748b', width=4, dash='solid'),
        opacity=0.5
    ))
    
    # Optional generic constant pressure dashed lines 
    fig.add_trace(go.Scatter(
        x=[0.1, 8.5], y=[300, 3300],
        mode='lines',
        line=dict(color='#64748b', width=1, dash='dash'),
        opacity=0.3,
        showlegend=False
    ))

    # Connect the dots 7 -> 8 -> 5 -> 6 -> 7
    # s[0]=PumpIn(7), s[1]=PumpOut(8), s[2]=BoilerOut(5), s[3]=TurbineOut(6)
    cycle_s = [s[0], s[1], s[2], s[3], s[0]]
    cycle_h = [h[0], h[1], h[2], h[3], h[0]]

    fig.add_trace(go.Scatter(
        x=cycle_s, y=cycle_h,
        mode='lines+markers+text',
        name='Steam Cycle',
        text=['7', '8', '5', '6', ''],
        textposition='top center',
        textfont=dict(color='#38bdf8', size=13, family='Inter', weight='bold'),
        line=dict(color='#0ea5e9', width=2),
        marker=dict(size=9, color='#38bdf8'),
        hovertemplate='<b>Point %{text}</b><br>s: %{x:.2f}<br>h: %{y:.1f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text='<b>h-s DIAGRAM — HTC STEAM CYCLE</b>', font=dict(color='#94a3b8', size=13, family='JetBrains Mono')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='s (kJ/kg·K)', color='#94a3b8', showgrid=True, gridcolor='#1e293b', griddash='dash', zeroline=False, dtick=3),
        yaxis=dict(title='h (kJ/kg)', color='#94a3b8', showgrid=True, gridcolor='#1e293b', griddash='dash', zeroline=False, dtick=800),
        margin=dict(l=60, r=40, t=50, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color='#94a3b8')
        )
    )

    return fig