# utils/constants.py
"""
Fixed thermodynamic constants for the AD-HTC Gas Cycle Simulator
All units in SI (kg, K, kJ, kW)
"""

# Gas properties (Air - ideal gas)
CP_AIR = 1.005  # kJ/kg·K (specific heat at constant pressure)
CV_AIR = 0.718  # kJ/kg·K (specific heat at constant volume)
GAMMA_AIR = CP_AIR / CV_AIR  # ≈ 1.4
R_AIR = 0.287  # kJ/kg·K (gas constant)

# Standard conditions
T0 = 298.15  # K (reference temperature for exergy, 25°C)
P0 = 101.325  # kPa (reference pressure, 1 atm)

# Conversion factors
KELVIN_OFFSET = 273.15  # °C to K: T(K) = T(°C) + 273.15

# Cycle limits (reasonable ranges)
PRESSURE_RATIO_MIN = 5
PRESSURE_RATIO_MAX = 25
TIT_MIN = 800  # K
TIT_MAX = 1600  # K
EFFICIENCY_MIN = 0.7
EFFICIENCY_MAX = 0.95

# HTC parameters
STACK_TEMP_MIN = 120  # °C (minimum to avoid condensation)
STACK_TEMP_DEFAULT = 170  # °C (from lecturer's slide)

# File paths
SCHEMATIC_PATH = "assets/schematic.png"