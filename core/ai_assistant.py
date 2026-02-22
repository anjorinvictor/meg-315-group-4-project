import google.generativeai as genai
import streamlit as st
import pandas as pd

def init_ai(api_key):
    """Initializes the Gemini AI client"""
    genai.configure(api_key=api_key)
    # Using the latest available fast gemini model from user's debug list
    return genai.GenerativeModel('gemini-2.5-flash')

def get_engineering_context(gas_results, steam_results, htc_results):
    """Translates the raw mathematical arrays into English context for the AI"""
    if gas_results is None:
        sys_state = "The user has not run the Analysis yet. Engage them in conversation, greet them delightfully, and encourage them to click 'ANALYZE SYSTEM' when they are ready to simulate the AD-HTC cycle."
    else:
        sys_state = f"""
        SYSTEM STATE:
        - Brayton Cycle (Gas Turbine) Efficiency: {gas_results.get('efficiency', 0):.1f}%
        - Brayton Net Power Output: {gas_results.get('W_net_kW', 0):.1f} kW
        - Gas Turbine Inlet Temp (TIT): {gas_results['states']['T'][2] - 273.15:.1f} °C
        - Mass Flow Rate: {gas_results.get('w_net_specific', 0):.1f} kg/s
        - Exhaust Temp leaving Turbine: {gas_results.get('T4_C', 0):.1f} °C
        
        - HTC Reactor Heat Demand: {htc_results.get('htc_demand_kW', 0)} kW
        - Usable Exhaust Heat Available: {htc_results.get('Q_available_kW', 0):.1f} kW
        - HTC Feasibility Status: {htc_results.get('status', 'Unknown')}
        
        - Steam Cycle (Rankine) Boiler Pressure: {steam_results['P_bar'][1]:.1f} bar
        - Steam Superheat Temp: {steam_results['T_C'][2]:.1f} °C
        """

    return f"""
    Your name is Aura, an exceptionally intelligent, friendly, and conversational Thermodynamics AI Copilot. 
    You are integrated into an AD-HTC (Anaerobic Digestion - Hydrothermal Carbonization) engineering simulation dashboard.
    
    RULES:
    1. Always warmly acknowledge greetings (e.g., "Hi Aura!", "Hello"). Start with a friendly, welcoming tone.
    2. If the user calls you by your name, respond warmly and professionally.
    3. You are an expert engineer. If the user asks technical questions, provide concise, brilliant insights (2-3 paragraphs max).
    4. Use the SYSTEM STATE below to accurately answer any math or cycle efficiency questions they ask.
    
    {sys_state}
    """

def get_ai_response(model, gas_results, steam_results, htc_results, user_query):
    """Sends the context and query to Gemini"""
    try:
        context = get_engineering_context(gas_results, steam_results, htc_results)
        prompt = f"{context}\n\nUSER QUESTION: {user_query}\n\nYOUR EXPERT ANSWER:"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            return f"Error communicating with AI Assistant: {str(e)}\n\nDebug - Available Models on your API Key:\n" + ", ".join(available_models)
        except Exception as e2:
            return f"Error communicating with AI Assistant: {str(e)}\n(Also failed to list models: {str(e2)})"
    
def display_ai_warning(gas_results, steam_results):
    """Local logic to check for critical engineering threshold breaches"""
    warnings = []
    
    # Check TIT Melt Threshold
    tit_c = gas_results['states']['T'][2] - 273.15
    if tit_c > 1350:
        warnings.append(f"**🚨 TIT LIMIT EXCEEDED ({tit_c:.0f}°C):** Standard turbine blades melt at 1350°C. Advanced active cooling / thermal barrier coatings required.")
        
    # Check Steam Pressure
    p_boiler = steam_results['P_bar'][1]
    if p_boiler > 150:
        warnings.append(f"**⚠️ SUPERCRITICAL WARNING ({p_boiler:.0f} bar):** Pressures over 150 bar mandate supercritical boiler architectures, significantly increasing capital cost.")
        
    # Check Compressor Ratio
    rp = gas_results['states']['P'][1] / gas_results['states']['P'][0]
    if rp > 40:
        warnings.append(f"**⚠️ COMPRESSOR STALL RISK:** Pressure ratio ({rp:.1f}) exceeds standard limits (max ~40). Intercooling required.")
        
    return warnings
