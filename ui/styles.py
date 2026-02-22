# ui/styles.py
"""
Premium Lovable Dark Theme
"""

def get_css():
    """Return completely overhauled dark theme CSS for Streamlit app"""
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
        
        /* Disable default Streamlit header */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Global Page Background */
        .stApp {
            background-color: #0b1120 !important;
            color: #cbd5e1 !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Target the main block to remove excessive padding */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }

        /* ===== TITLES ===== */
        h1, h2, h3, h4, .stMarkdown p strong {
            color: #f8fafc !important;
            font-family: 'Inter', sans-serif !important;
            letter-spacing: 0.5px;
        }
        
        h1 { font-size: 24px !important; font-weight: 800 !important; padding-bottom: 0px !important; margin-bottom: 0px !important;}
        h2 { font-size: 14px !important; font-weight: 700 !important; color: #60a5fa !important; text-transform: uppercase; margin-top:10px !important;}
        
        /* Dark Theme Markdown Text */
        .stMarkdown p {
            color: #94a3b8;
            font-size: 11px;
        }

        /* ===== BUTTONS ===== */
        .stButton button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            border: 1px solid #3b82f6 !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            font-weight: 700 !important;
            font-size: 11px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4) !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.6) !important;
        }

        /* Subtle secondary button (like Hide Report) */
        button[kind="secondary"] {
            background: transparent !important;
            border: 1px solid #334155 !important;
            color: #94a3b8 !important;
            box-shadow: none !important;
        }
        button[kind="secondary"]:hover {
            border-color: #475569 !important;
            color: #f8fafc !important;
        }
        
        /* ===== SLIDERS ===== */
        /* Range Slider Track */
        .stSlider > div > div > div > div {
            background-color: #1e293b !important;
        }
        /* Slider Fill */
        .stSlider > div > div > div > div > div {
            background-color: #3b82f6 !important;
        }
        /* Slider Thumb */
        .stSlider > div > div > div > div:nth-child(2) > div {
            background-color: #60a5fa !important;
            box-shadow: 0 0 10px rgba(96, 165, 250, 0.6) !important;
            border: none !important;
        }
        
        .stSlider label, .stNumberInput label {
            color: #94a3b8 !important;
            font-size: 11px !important;
            font-weight: 500 !important;
        }
        
        /* Slider Value Text (the red number in screenshot) */
        .stSlider [data-testid="stThumbValue"] {
            color: #f87171 !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 10px !important;
            font-weight: 700 !important;
            background: transparent !important;
        }
        
        /* Hide slider min/max */
        .stSlider [data-testid="stTickBar"] {
            display: none !important;
        }
        
        /* ===== NUMBER INPUTS ===== */
        .stNumberInput input {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border: 1px solid #334155 !important;
            border-radius: 4px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 11px !important;
        }
        
        .stNumberInput input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
        }
        
        /* Button controls in NumberInput */
        .stNumberInput button {
            background-color: #1e293b !important;
            color: #94a3b8 !important;
            border-color: #334155 !important;
        }

        /* ===== METRIC CARDS (lovable dark UI style) ===== */
        /* Create a grid-like card layout for metrics */
        .metric-card {
            background-color: #111827;
            border: 1px solid #1f2937;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: inset 0 2px 4px 0 rgba(255, 255, 255, 0.05);
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: inset 0 2px 4px 0 rgba(255, 255, 255, 0.05), 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            border-color: #374151;
        }
        
        .metric-icon {
            position: absolute;
            top: 15px;
            left: 15px;
            font-size: 16px;
        }
        
        .metric-unit-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            color: #60a5fa;
            font-size: 10px;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            text-transform: uppercase;
        }

        .metric-value {
            color: #f8fafc;
            font-size: 26px;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            margin: 25px 0 5px 0;
            letter-spacing: -0.5px;
        }
        
        .metric-value.yellow { color: #facc15; }
        .metric-value.red { color: #f87171; }
        .metric-value.green { color: #4ade80; }
        .metric-value.blue { color: #60a5fa; }
        .metric-value.cyan { color: #22d3ee; }
        
        .metric-label {
            color: #cbd5e1;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        
        .metric-desc {
            color: #64748b;
            font-size: 9px;
            font-family: 'Inter', sans-serif;
            line-height: 1.3;
        }

        /* ===== TABS (Dark theme Segments) ===== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background-color: #1e293b;
            padding: 4px;
            border: 1px solid #334155;
            border-radius: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 10px;
            font-weight: 600;
            color: #94a3b8;
            background-color: transparent;
            border: 1px solid transparent;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s ease;
            height: auto;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #3b82f6 !important;
            color: #ffffff !important;
            border-color: #2563eb !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        }

        /* Dataframes & Tables */
        .dataframe { font-size: 10px; font-family: 'JetBrains Mono', monospace; color: #cbd5e1; width: 100%; border-collapse: collapse; }
        .dataframe th { background-color: #1e293b; color: #94a3b8; font-weight: 700; border: 1px solid #334155; padding: 8px; text-transform: uppercase; }
        .dataframe td { border: 1px solid #334155; padding: 8px; background-color: #0f172a; }

        /* Left Sidebar Container aesthetic wrapper */
        .input-panel-wrapper {
            background-color: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 16px;
        }

        /* ===== AI FLOATING COPILOT UI (PREMIUM REDESIGN) ===== */
        button[data-testid="stPopoverButton"] {
            position: fixed !important;
            bottom: 30px !important;
            right: 30px !important;
            width: 65px !important;
            height: 65px !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 0 15px rgba(14, 165, 233, 0.5), 0 0 30px rgba(99, 102, 241, 0.3) !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 999999 !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            animation: floatingPulse 3s infinite ease-in-out;
        }

        @keyframes floatingPulse {
            0% { transform: scale(1); box-shadow: 0 0 15px rgba(14, 165, 233, 0.5); }
            50% { transform: scale(1.05); box-shadow: 0 0 25px rgba(14, 165, 233, 0.8), 0 0 40px rgba(99, 102, 241, 0.5); }
            100% { transform: scale(1); box-shadow: 0 0 15px rgba(14, 165, 233, 0.5); }
        }

        button[data-testid="stPopoverButton"]:hover {
            transform: scale(1.1) !important;
            animation: none !important;
        }

        button[data-testid="stPopoverButton"] p {
            font-size: 28px !important;
            margin: 0 !important;
        }

        /* Slide-in Top-to-Bottom Drawer logic using Popover Body */
        div[data-testid="stPopoverBody"] {
            position: fixed !important;
            top: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            height: 100vh !important;
            width: 400px !important;
            max-width: 90vw !important;
            background: rgba(11, 17, 32, 0.75) !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border-left: 1px solid rgba(14, 165, 233, 0.2) !important;
            border-top: none !important;
            border-bottom: none !important;
            border-right: none !important;
            border-radius: 0 !important;
            box-shadow: -15px 0 50px rgba(0, 0, 0, 0.7) !important;
            z-index: 999998 !important;
            padding: 30px 20px !important;
            animation: smoothSlideRight 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
            transform: translateX(100%);
            overflow-y: auto !important;
        }

        @keyframes smoothSlideRight {
            0% { transform: translateX(100%); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }

        /* Status Indicator */
        .ai-status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.5px;
            font-family: 'Inter', sans-serif;
            margin-bottom: 20px;
            color: #e2e8f0;
        }
        
        .ai-chat-header-text {
            background: linear-gradient(135deg, #0ea5e9, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 20px;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.5px;
        }
        
        .system-stable {
            border: 1px solid #22c55e;
            color: #4ade80;
            background: rgba(34, 197, 94, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 9px;
            display: inline-block;
            font-weight: 700;
        }

        /* Top Bar Wrapper */
        .top-bar-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 16px;
            margin-bottom: 20px;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .logo-icon {
            background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 28px;
            font-weight: 800;
        }
        .logo-text-title {
            color: #f8fafc;
            font-size: 16px;
            font-weight: 800;
            margin: 0;
            letter-spacing: 0.5px;
        }
        .logo-text-sub {
            color: #64748b;
            font-size: 9px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin:0;
        }
        
        .actions-section {
            display: flex;
            gap: 12px;
        }

        /* ===== CHAT BUBBLE OVERRIDES (Left/Right) ===== */
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) {
            flex-direction: row-reverse;
            text-align: right;
            background: transparent !important;
        }
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="chatAvatarIcon-user"] {
            margin-left: 1rem;
            margin-right: 0;
        }
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) div[data-testid="stMarkdownContainer"] {
            background-color: rgba(14, 165, 233, 0.15) !important;
            border-radius: 15px 15px 0 15px;
            padding: 10px 15px;
            display: inline-block;
            border: 1px solid rgba(14, 165, 233, 0.3);
            animation: slideInBottom 0.3s ease-out;
        }

        /* AI Custom Div Class explicitly forcing colors and borders inner to standard avatars */
        .ai-text-white-bg {
            background-color: #f8fafc;
            border-radius: 15px 15px 15px 0;
            padding: 12px 16px;
            border: 1px solid rgba(148, 163, 184, 0.4);
            color: #000000 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            display: inline-block;
            max-width: 95%;
            animation: slideInBottom 0.3s ease-out;
            font-size: 13px;
            line-height: 1.5;
        }
        
        .ai-text-white-bg *, 
        .ai-text-white-bg p, 
        .ai-text-white-bg span, 
        .ai-text-white-bg li, 
        .ai-text-white-bg strong {
            color: #000000 !important;
        }


        .stSpinner {
            animation: typingBounce 1s infinite alternate cubic-bezier(0.5, 0, 0.5, 1);
        }

        @keyframes slideInBottom {
            from { transform: translateY(10px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes typingBounce {
            0% { transform: translateY(0); opacity: 0.6; }
            100% { transform: translateY(-3px); opacity: 1; }
        }
        
    </style>
    """