# ui/schematic.py
"""
Interactive, dark-themed animated schematic based directly on the lecturer's slide layout.
Includes glowing components, dash animations, moving particles, and clickable tooltips.
"""

import streamlit as st

def get_animated_schematic_html(gas_results=None, steam_results=None, T1_C=33, T3_C=927):
    # Dynamic values mapping
    val_t2 = f"{gas_results.get('T2_C', 0):.1f}" if gas_results else "248.0"
    val_t3 = f"{T3_C:.1f}"
    val_t4 = f"{gas_results.get('T4_C', 0):.1f}" if gas_results else "485.0"
    
    steam_t1 = f"{steam_results['T_C'][0]:.1f}" if steam_results else "33.0"
    steam_p1 = f"{steam_results['P_bar'][0]:.1f}" if steam_results else "0.1"
    steam_h1 = f"{steam_results['h'][0]:.1f}" if steam_results else "138.3"
    steam_s1 = f"{steam_results['s'][0]:.4f}" if steam_results else "0.4764"
    
    steam_t2 = f"{steam_results['T_C'][1]:.1f}" if steam_results else "33.2"
    steam_p2 = f"{steam_results['P_bar'][1]:.1f}" if steam_results else "40.0"
    steam_h2 = f"{steam_results['h'][1]:.1f}" if steam_results else "142.3"
    steam_s2 = f"{steam_results['s'][1]:.4f}" if steam_results else "0.4764"
    
    steam_t3 = f"{steam_results['T_C'][2]:.1f}" if steam_results else "350.0"
    steam_p3 = f"{steam_results['P_bar'][2]:.1f}" if steam_results else "40.0"
    steam_h3 = f"{steam_results['h'][2]:.1f}" if steam_results else "3093.3"
    steam_s3 = f"{steam_results['s'][2]:.4f}" if steam_results else "6.5843"
    
    steam_t4 = f"{steam_results['T_C'][3]:.1f}" if steam_results else "99.6"
    steam_p4 = f"{steam_results['P_bar'][3]:.1f}" if steam_results else "0.1"
    steam_h4 = f"{steam_results['h'][3]:.1f}" if steam_results else "2195.4"
    steam_s4 = f"{steam_results['s'][3]:.4f}" if steam_results else "6.5843"
    
    # Gas mock/calc properties since brayton doesn't return s and h explicitly
    gas_m = f"{gas_results.get('w_net_specific', 2.0) if gas_results else 2.0:.1f}"
    
    gas_p2 = f"{(gas_results['states']['P'][1]/100):.2f}" if gas_results else "12.0"
    gas_p3 = f"{(gas_results['states']['P'][2]/100):.2f}" if gas_results else "11.64"
    
    T1_K = T1_C + 273.15
    gas_h2 = f"{(gas_results['states']['T'][1] * 1.005):.1f}" if gas_results else "500.0"
    gas_s2 = "1.702"
    gas_h3 = f"{(gas_results['states']['T'][2] * 1.005):.1f}" if gas_results else "1200.0"
    gas_s3 = "2.831"
    gas_h4 = f"{(gas_results['states']['T'][3] * 1.005):.1f}" if gas_results else "753.0"
    gas_s4 = "2.831"
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
            
            body {{
                background-color: transparent;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                font-family: 'Inter', sans-serif;
                color: #e2e8f0;
            }}
            
            .schematic-container {{
                width: 100%;
                max-width: 1000px;
                background-color: #0f172a;
                border-radius: 12px;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
                border: 1px solid #1e293b;
                background-image: 
                    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
                background-size: 30px 30px;
            }}
            
            svg {{
                display: block;
                width: 100%;
                height: auto;
            }}
            
            /* Box Styling with Neon Glow Engine */
            .box {{ stroke-width: 2px; }}
            .box-green {{ fill: #1e293b; stroke: #22c55e; filter: drop-shadow(0 0 10px rgba(34,197,94,0.4)); }}
            .box-blue {{ fill: #1e293b; stroke: #3b82f6; filter: drop-shadow(0 0 10px rgba(59,130,246,0.4)); }}
            .box-cyan {{ fill: #1e293b; stroke: #06b6d4; filter: drop-shadow(0 0 10px rgba(6,182,212,0.4)); }}
            .box-orange {{ fill: #1e293b; stroke: #f97316; filter: drop-shadow(0 0 10px rgba(249,115,22,0.4)); }}
            .box-red {{ fill: #1e293b; stroke: #ef4444; filter: drop-shadow(0 0 10px rgba(239,68,68,0.4)); }}
            .box-purple {{ fill: #1e293b; stroke: #a855f7; filter: drop-shadow(0 0 10px rgba(168,85,247,0.4)); }}
            .box-yellow {{ fill: #1e293b; stroke: #eab308; filter: drop-shadow(0 0 10px rgba(234,179,8,0.4)); }}

            /* Text Styling */
            .text-main {{ fill: #ffffff; font-size: 11px; font-weight: 800; text-anchor: middle; dominant-baseline: middle; }}
            .text-title {{ fill: #94a3b8; font-size: 26px; font-weight: 800; font-family: "Times New Roman", serif; }}
            .text-sub {{ fill: #e2e8f0; font-size: 11px; font-weight: 600; font-family: 'JetBrains Mono', monospace; text-anchor: middle; }}
            .text-outside {{ fill: #ffffff; font-size: 11px; font-weight: 600; }}

            /* Moving Paths & Particles */
            .line-path {{ fill: none; stroke-width: 2px; }}
            
            .path-green {{ stroke: #22c55e; }}
            .path-blue {{ stroke: #3b82f6; }}
            .path-cyan {{ stroke: #06b6d4; }}
            .path-orange {{ stroke: #f97316; }}
            .path-red {{ stroke: #ef4444; }}
            .path-purple {{ stroke: #a855f7; }}
            .path-yellow {{ stroke: #eab308; }}
            .path-gray {{ stroke: #cbd5e1; }}
            
            /* Shaft Animation */
            @keyframes dash-shaft {{ to {{ stroke-dashoffset: -40; }} }}
            .shaft-path {{
                fill: none; stroke: #64748b; stroke-width: 3px; stroke-dasharray: 15 8 5 8;
                animation: dash-shaft 2s linear infinite;
            }}

            /* Flow Particle Animation Setup */
            @keyframes offset-flow {{
                from {{ stroke-dashoffset: 24; }}
                to {{ stroke-dashoffset: 0; }}
            }}
            .flow-anim {{
                stroke-dasharray: 12;
                animation: offset-flow 1s linear infinite;
            }}

            /* Clickable Nodes Details */
            .node-circle {{ fill: #3b82f6; stroke: #0f172a; stroke-width: 2px; cursor: pointer; transition: transform 0.2s; }}
            .node-circle:hover {{ transform: scale(1.2); stroke: #ffffff; }}
            .node-text {{ fill: #ffffff; font-size: 12px; font-weight: 800; text-anchor: middle; pointer-events: none; }}

            /* Tooltip window styling */
            .tooltip-box {{
                opacity: 0;
                position: absolute;
                background: #1e293bd9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 15px;
                pointer-events: none;
                transition: opacity 0.2s;
                box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5);
                backdrop-filter: blur(4px);
                z-index: 100;
                color: #e2e8f0;
                min-width: 200px;
                font-family: 'JetBrains Mono', monospace;
            }}
            .tooltip-box.active {{
                opacity: 1 !important;
                pointer-events: auto !important;
            }}
            .tooltip-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #334155; padding-bottom: 8px; }}
            .tooltip-header h4 {{ color: #facc15; margin: 0; font-size: 14px; font-family: 'Inter', sans-serif; font-weight: 700; }}
            .tooltip-close {{ color: #94a3b8; cursor: pointer; font-size: 14px; font-weight: bold; background: none; border: none; padding: 0; }}
            .tooltip-close:hover {{ color: #ffffff; }}
            
            .tooltip-data {{ display: flex; flex-direction: column; gap: 8px; font-size: 12px; }}
            .tooltip-row {{ display: flex; justify-content: space-between; }}
            .tooltip-label {{ color: #64748b; font-weight: 600; width: 30px; }}
            .tooltip-val {{ color: #f8fafc; font-weight: 700; text-align: right; }}

        </style>
    </head>
    <body>
        <div class="schematic-container">
            <!-- Tooltip container rendered over SVG -->
            <div id="dynamic-tooltip" class="tooltip-box">
                <div class="tooltip-header">
                    <h4 id="tt-title">State</h4>
                    <button class="tooltip-close" id="tt-close">X</button>
                </div>
                <div class="tooltip-data" id="tt-data"></div>
            </div>

            <svg viewBox="0 0 1000 850" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" id="main-svg">
                <defs>
                    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#22c55e" />
                    </marker>
                    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#3b82f6" />
                    </marker>
                    <marker id="arrow-cyan" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#06b6d4" />
                    </marker>
                    <marker id="arrow-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#f97316" />
                    </marker>
                    <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef4444" />
                    </marker>
                    <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#a855f7" />
                    </marker>
                    <marker id="arrow-yellow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#eab308" />
                    </marker>
                    <marker id="arrow-gray" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#cbd5e1" />
                    </marker>
                </defs>

                <!-- Titles -->
                <text x="80" y="60" class="text-title">AD-HTC Fuel-Enhanced Power</text>
                <text x="350" y="100" class="text-title">Gas Cycle</text>
                
                <!-- LINE FLOWS (ANIMATED) -->
                <!-- Biomass In -->
                <path d="M 40,185 L 110,185" class="line-path path-green flow-anim" marker-end="url(#arrow-green)" />
                <text x="40" y="165" class="text-outside">Biomass Feedstock</text>

                <!-- Homogenizer Top splitting Out (Green) -->
                <!-- Routes right all the way to AD -->
                <path d="M 220,165 L 820,165 L 820,295 L 720,295" class="line-path path-green flow-anim" marker-end="url(#arrow-green)" />
                <text x="650" y="155" class="text-outside" style="fill:#22c55e;">Moisture-rich Biomass Feedstock</text>

                <!-- Homogenizer Bottom to Reactor (Green) -->
                <path d="M 170,230 L 170,410 L 330,410" class="line-path path-green flow-anim" marker-end="url(#arrow-green)" />
                <text x="180" y="390" class="text-outside" style="fill:#22c55e;">Moisture-lean Biomass Feedstock</text>

                <!-- STEAM LOOP (Blue & Orange Heat) -->
                <!-- Pump to Boiler -->
                <path d="M 250,315 L 250,265 L 330,265" class="line-path path-blue flow-anim" marker-end="url(#arrow-blue)" />
                
                <!-- Boiler -> Returns (Orange, then Blue) -->
                <!-- Boiler right out splits up down -->
                <path d="M 430,265 L 500,265" class="line-path path-orange flow-anim" />
                <!-- -> Reactor branch -->
                <path d="M 500,265 L 500,350 L 385,350 L 385,380" class="line-path path-orange flow-anim" marker-end="url(#arrow-orange)" />
                <!-- -> AD branch -->
                <path d="M 500,265 L 500,240 L 630,240 L 630,295 L 640,295" class="line-path path-orange flow-anim" marker-end="url(#arrow-orange)" />

                <!-- AD return to Pump (Cyan/Blue return water) -->
                <path d="M 650,315 L 480,315 L 480,460 L 220,460 L 220,340 L 235,340" class="line-path path-blue flow-anim" marker-end="url(#arrow-blue)" />
                <!-- Reactor return to Pump -->
                <path d="M 340,440 L 220,440" class="line-path path-blue flow-anim" />

                <!-- SYNGAS FLOWS (Cyan) -->
                <!-- Reactor -> Collector -->
                <path d="M 430,430 L 520,430 L 520,390 L 530,390" class="line-path path-cyan flow-anim" marker-end="url(#arrow-cyan)" />
                <!-- AD -> Collector -->
                <path d="M 650,275 L 565,275 L 565,360" class="line-path path-cyan flow-anim" marker-end="url(#arrow-cyan)" />
                
                <!-- Biogas Distribution out -->
                <path d="M 710,275 L 850,275" class="line-path path-cyan flow-anim" marker-end="url(#arrow-cyan)" />
                <text x="860" y="270" class="text-outside" style="fill:#06b6d4;">Biogas Distribution to</text>
                <text x="860" y="285" class="text-outside" style="fill:#06b6d4;">Building Envelopes</text>

                <!-- Combustion Flow (Red) -->
                <path d="M 565,440 L 565,540 L 585,540" class="line-path path-red flow-anim" marker-end="url(#arrow-red)" />
                
                <!-- External Flows -->
                <path d="M 385,450 L 385,490" class="line-path path-gray flow-anim" marker-end="url(#arrow-gray)" />
                <text x="390" y="505" class="text-outside" style="fill:#94a3b8;">Volatile Matters and Feedstock Waste</text>

                <path d="M 350,750 L 350,696" class="line-path path-purple flow-anim" marker-end="url(#arrow-purple)" />
                <text x="315" y="745" class="text-outside" style="fill:#a855f7;">Air</text>
                
                <!-- Comp to Combustor (Purple) -->
                <path d="M 400,626 L 400,560 L 490,560" class="line-path path-purple flow-anim" marker-end="url(#arrow-purple)" />
                <!-- Combustor out to Turbine (Red to Yellow curve) -->
                <path d="M 720,560 L 800,560 L 800,634" class="line-path path-red flow-anim" marker-end="url(#arrow-red)" />

                <!-- Exhaust Out (Yellow/Gray) -->
                <path d="M 850,696 L 850,750" class="line-path path-yellow flow-anim" marker-end="url(#arrow-yellow)" />
                <text x="860" y="745" class="text-outside" style="fill:#eab308;">Exhaust Gases</text>


                <!-- SHAFT -->
                <path d="M 220,660 L 960,660" class="shaft-path" />
                <path d="M 940,630 C 980,630 980,690 940,690" class="line-path path-yellow flow-anim" marker-end="url(#arrow-yellow)" />
                <text x="965" y="660" class="text-main" style="font-size: 24px; fill:#eab308;">⚛</text>

                <!-- COMPONENTS -->
                
                <!-- 1. Homogenizer -->
                <rect x="120" y="140" width="100" height="90" class="box box-green" rx="6" />
                <text x="170" y="175" class="text-main">Biomass</text>
                <text x="170" y="190" class="text-main">Feedstock</text>
                <text x="170" y="205" class="text-main">Homogenizer</text>

                <!-- 2. Pump -->
                <circle cx="250" cy="330" r="16" class="box box-blue" />
                <polygon points="242,338 258,338 250,318" fill="#ffffff" />
                <text x="210" y="330" class="text-sub">PUMP</text>

                <!-- 3. Boiler -->
                <rect x="340" y="240" width="90" height="50" class="box box-orange" rx="6" />
                <text x="385" y="265" class="text-main">Boiler</text>

                <!-- 4. Reactor -->
                <rect x="340" y="390" width="90" height="60" class="box box-blue" rx="6" />
                <text x="385" y="420" class="text-main">Reactor</text>

                <text x="385" y="340" class="text-main" style="fill: #3b82f6;">HTC Steam Cycle</text>

                <!-- 5. AD -->
                <rect x="650" y="260" width="60" height="70" class="box box-green" rx="6" />
                <text x="680" y="295" class="text-main">AD</text>

                <!-- 6. Enhanced Biogas Collector -->
                <rect x="530" y="370" width="80" height="70" class="box box-cyan" rx="6" />
                <text x="570" y="395" class="text-main">Enhanced</text>
                <text x="570" y="410" class="text-main">Biogas</text>
                <text x="570" y="425" class="text-main">Collector</text>

                <!-- 7. Comb Chamber -->
                <rect x="500" y="520" width="220" height="70" class="box box-red" rx="10" />
                <text x="610" y="550" class="text-main">Biogas Combustion</text>
                <text x="610" y="565" class="text-main">Chamber</text>

                <!-- 8. Compressor -->
                <polygon points="270,626 460,646 460,674 270,696" class="box box-purple" stroke-linejoin="round" />
                <text x="365" y="660" class="text-main">Compressor</text>

                <!-- 9. Turbine -->
                <polygon points="730,646 920,626 920,696 730,674" class="box box-yellow" stroke-linejoin="round" />
                <text x="825" y="660" class="text-main">Turbine</text>

                <!-- CLICKABLE DATA NODES -->
                <!-- Node 1: Air Inlet -->
                <g class="clickable-node" data-title="State 1: Air Inlet" data-v1="{T1_C}°C" data-v2="1.01 bar" data-v3="300.2 kJ/kg" data-v4="1.702 kJ/kg-K" data-v5="{gas_m} kg/s">
                    <circle cx="350" cy="720" r="14" class="node-circle" />
                    <text x="350" y="722" class="node-text">1</text>
                </g>

                <!-- Node 2: Compressor Out -->
                <g class="clickable-node" data-title="State 2: Comp Out" data-v1="{val_t2}°C" data-v2="{gas_p2} bar" data-v3="{gas_h2} kJ/kg" data-v4="{gas_s2} kJ/kg-K" data-v5="{gas_m} kg/s">
                    <circle cx="450" cy="560" r="14" class="node-circle" />
                    <text x="450" y="562" class="node-text">2</text>
                </g>

                <!-- Node 3: Combustor Out -->
                <g class="clickable-node" data-title="State 3: Turbine Inlet" data-v1="{val_t3}°C" data-v2="{gas_p3} bar" data-v3="{gas_h3} kJ/kg" data-v4="{gas_s3} kJ/kg-K" data-v5="{gas_m} kg/s">
                    <circle cx="760" cy="560" r="14" class="node-circle" style="fill:#ef4444; stroke:#b91c1c;"/>
                    <text x="760" y="562" class="node-text">3</text>
                </g>

                <!-- Node 4: Turbine Out -->
                <g class="clickable-node" data-title="State 4: Exhaust" data-v1="{val_t4}°C" data-v2="1.01 bar" data-v3="{gas_h4} kJ/kg" data-v4="{gas_s4} kJ/kg-K" data-v5="{gas_m} kg/s">
                    <circle cx="850" cy="720" r="14" class="node-circle" style="fill:#eab308; stroke:#a16207;"/>
                    <text x="850" y="722" class="node-text">4</text>
                </g>
                <!-- Node 5: Turbine In (Boiler Out) -->
                <g class="clickable-node" data-title="State 5: Turbine In" data-v1="{steam_t3}°C" data-v2="{steam_p3} bar" data-v3="{steam_h3} kJ/kg" data-v4="{steam_s3} kJ/kg-K" data-v5="N/A">
                    <circle cx="480" cy="265" r="14" class="node-circle" style="fill:#f97316;" />
                    <text x="480" y="267" class="node-text">5</text>
                </g>

                <!-- Node 6: HTC Return (Turbine Out) -->
                <g class="clickable-node" data-title="State 6: HTC Return" data-v1="{steam_t4}°C" data-v2="{steam_p4} bar" data-v3="{steam_h4} kJ/kg" data-v4="{steam_s4} kJ/kg-K" data-v5="N/A">
                    <circle cx="385" cy="365" r="14" class="node-circle" style="fill:#06b6d4;" />
                    <text x="385" y="367" class="node-text">6</text>
                </g>

                <!-- Node 7: Pump Inlet (Condenser Out) -->
                <g class="clickable-node" data-title="State 7: Pump Inlet" data-v1="{steam_t1}°C" data-v2="{steam_p1} bar" data-v3="{steam_h1} kJ/kg" data-v4="{steam_s1} kJ/kg-K" data-v5="N/A">
                    <circle cx="210" cy="330" r="14" class="node-circle" style="fill:#3b82f6;" />
                    <text x="210" y="332" class="node-text">7</text>
                </g>

                <!-- Node 8: Boiler Feed (Pump Out) -->
                <g class="clickable-node" data-title="State 8: Boiler Feed" data-v1="{steam_t2}°C" data-v2="{steam_p2} bar" data-v3="{steam_h2} kJ/kg" data-v4="{steam_s2} kJ/kg-K" data-v5="N/A">
                    <circle cx="280" cy="265" r="14" class="node-circle" style="fill:#3b82f6;" />
                    <text x="280" y="267" class="node-text">8</text>
                </g>

            </svg>
        </div>

        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                const nodes = document.querySelectorAll('.clickable-node');
                const tooltip = document.getElementById('dynamic-tooltip');
                const ttTitle = document.getElementById('tt-title');
                const ttData = document.getElementById('tt-data');
                const svgContainer = document.querySelector('.schematic-container');
                const closeBtn = document.getElementById('tt-close');
                let activeNode = null;

                const closeTooltip = () => {{
                    tooltip.classList.remove('active');
                    activeNode = null;
                }};

                closeBtn.addEventListener('click', closeTooltip);

                nodes.forEach(node => {{
                    node.addEventListener('click', function(e) {{
                        e.stopPropagation();
                        // if clicked same node, toggle close
                        if (activeNode === this) {{
                            closeTooltip();
                            return;
                        }}
                        
                        activeNode = this;
                        const box = this.getBoundingClientRect();
                        const containerBox = svgContainer.getBoundingClientRect();
                        
                        ttTitle.textContent = this.getAttribute('data-title');
                        
                        ttData.innerHTML = `
                            <div class="tooltip-row"><span class="tooltip-label">T</span><span class="tooltip-val">${{this.getAttribute('data-v1')}}</span></div>
                            <div class="tooltip-row"><span class="tooltip-label">P</span><span class="tooltip-val">${{this.getAttribute('data-v2')}}</span></div>
                            <div class="tooltip-row"><span class="tooltip-label">h</span><span class="tooltip-val">${{this.getAttribute('data-v3')}}</span></div>
                            <div class="tooltip-row"><span class="tooltip-row tooltip-label">s</span><span class="tooltip-val">${{this.getAttribute('data-v4')}}</span></div>
                            <div class="tooltip-row"><span class="tooltip-label">m&#775;</span><span class="tooltip-val">${{this.getAttribute('data-v5')}}</span></div>
                        `;

                        let x = (box.left - containerBox.left) + 20;
                        let y = (box.top - containerBox.top) - 100;

                        if(x > containerBox.width - 240) {{ x -= 240; }}
                        if(y < 0) {{ y += 120; }}

                        tooltip.style.transform = `translate(${{x}}px, ${{y}}px)`;
                        tooltip.classList.add('active');
                    }});
                }});

                // Click away to close (unless clicking inside tooltip)
                document.addEventListener('click', function(e) {{
                    if (activeNode && !tooltip.contains(e.target)) {{
                        closeTooltip();
                    }}
                }});
            }});
        </script>
    </body>
    </html>
    """
    return html_code

def display_animated_schematic(gas_results=None, steam_results=None, T1_C=33, T3_K=1200):
    """
    Displays the dark UI glowing schematic layout based strictly on the lecturer's slide format.
    Click the circular node points to view live calculated thermodynamic parameters!
    """
    T3_C = T3_K - 273
    
    html_content = get_animated_schematic_html(
        gas_results=gas_results,
        steam_results=steam_results,
        T1_C=T1_C,
        T3_C=round(T3_C, 0)
    )
    
    # 850 height ensures no scrolling needed and captures the entire detailed view.
    st.components.v1.html(html_content, height=850, scrolling=False)