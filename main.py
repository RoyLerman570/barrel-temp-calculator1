import streamlit as st
import numpy as np
import pandas as pd
import io

# App title
st.title("🔧 Barrel Temperature Calculator")

# Sidebar inputs for the parameters
st.sidebar.header("Input Parameters")
T_ambient = st.sidebar.number_input("Ambient Temperature (°C)", value=25.0)
thickness = st.sidebar.number_input("Wall Thickness (m)", value=0.0152, format="%0.5f")
time_elapsed = st.sidebar.number_input("Elapsed Time After Firing (s)", value=30.0)
k = st.sidebar.number_input("Thermal Conductivity (W/m·K)", value=46.0)
rho = st.sidebar.number_input("Density (kg/m³)", value=7850.0)
c = st.sidebar.number_input("Specific Heat (J/kg·K)", value=460.0)

# Derived value
alpha = k / (rho * c)  # Thermal diffusivity

# External temperature range
external_temps = np.arange(25, 305, 5)

# Internal temperature calculation
exp_factor = np.exp(-alpha * time_elapsed / (thickness ** 2))
temp_internal = (external_temps - exp_factor * T_ambient) / (1 - exp_factor)

# Create result DataFrame
df = pd.DataFrame({
    'External Temperature (°C)': external_temps,
    'Internal Temperature (°C)': np.round(temp_internal, 2)
})

# Show table with results
st.subheader("Calculated Temperatures")
st.dataframe(df)

# Plot the results
st.subheader("Temperature Profile")
st.line_chart(df.set_index('External Temperature (°C)'))

# Download the results as an Excel file
st.subheader("Download Results")
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Temp Calculation', index=False)
    pd.DataFrame({
        'Description': ['Ambient Temp', 'Thickness', 'Elapsed Time', 'Conductivity', 'Density', 'Specific Heat'],
        'Value': [T_ambient, thickness, time_elapsed, k, rho, c]
    }).to_excel(writer, sheet_name='Input Parameters', index=False)
output.seek(0)

st.download_button(
    label="📥 Download Excel File",
    data=output,
    file_name="Barrel_Temperature_Calculator.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Footer
st.markdown("---")
st.caption("Built with Streamlit ✨")
