"""
📘 Geothermal Drilling Dashboard – Interactive Data Exploration Tool
Author: Yi Luo
Date: 2025-03-28

This Streamlit-based dashboard is developed to visualize and explore real-world geothermal drilling data
from the Utah FORGE site. The dataset used is publicly available from Kaggle:
https://www.kaggle.com/datasets/gauravan/geothermal-drilling-data-utah-forge-mu-esw1/data

📌 What this tool does:
- Loads and cleans raw drilling sensor data (including depth, temperature, ROP, WOB, torque).
- Applies interactive filters to subset data by depth, ROP, and WOB.
- Generates plots to analyze:
    • Subsurface temperature profiles (Temp In vs. Temp Out)
    • Rate of Penetration (ROP) vs. Depth
    • Weight on Bit (WOB) vs. Depth
    • Surface Torque vs. Depth
    • Temperature Gain (ΔT) vs. Depth

🔍 What we found in analysis:
- The temperature gain (ΔT) between input and output fluids increases with depth, showing strong heat transfer in deeper formations.
- Drilling resistance (inferred from torque and WOB) fluctuates at different depth intervals, indicating variable formation properties.
- ROP decreases at greater depths, which is consistent with harder rock layers encountered during deep drilling.

🧰 Technologies used:
- Python (OOP)
- Streamlit for interactive interface
- pandas for data manipulation
- matplotlib for plotting

This project demonstrates how geothermal drilling data can be turned into actionable visual insights using modern data tools. It aligns closely with real-world needs in geothermal resource assessment and tool development.

"""


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class GeothermalDashboard:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = self.load_and_clean_data()
        self.df_filtered = self.df.copy()

    def load_and_clean_data(self):
        df_raw = pd.read_csv(self.csv_path)
        df_raw.columns = df_raw.iloc[1]
        df = df_raw.drop([0, 1]).reset_index(drop=True)

        numeric_cols = [
            "Depth", "Temp Out( degF)", "Temp In(degF)",
            "ROP(1 ft)", "WOB (k-lbs)", "Surface Torque (psi)"
        ]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    def apply_filters(self):
        st.sidebar.header("Filter")

        depth_min = st.sidebar.slider("Minimum Depth (ft)",
            float(self.df["Depth"].min()), float(self.df["Depth"].max()), float(self.df["Depth"].min()))
        depth_max = st.sidebar.slider("Maximum Depth (ft)",
            float(self.df["Depth"].min()), float(self.df["Depth"].max()), float(self.df["Depth"].max()))

        min_rop = st.sidebar.slider("Min ROP (ft/hr)", float(self.df["ROP(1 ft)"].min()), float(self.df["ROP(1 ft)"].max()), float(self.df["ROP(1 ft)"].min()))
        max_rop = st.sidebar.slider("Max ROP (ft/hr)", float(self.df["ROP(1 ft)"].min()), float(self.df["ROP(1 ft)"].max()), float(self.df["ROP(1 ft)"].max()))

        min_wob = st.sidebar.slider("Min WOB (k-lbs)", float(self.df["WOB (k-lbs)"].min()), float(self.df["WOB (k-lbs)"].max()), float(self.df["WOB (k-lbs)"].min()))
        max_wob = st.sidebar.slider("Max WOB (k-lbs)", float(self.df["WOB (k-lbs)"].min()), float(self.df["WOB (k-lbs)"].max()), float(self.df["WOB (k-lbs)"].max()))

        df = self.df[
            (self.df["Depth"] >= depth_min) & (self.df["Depth"] <= depth_max) &
            (self.df["ROP(1 ft)"] >= min_rop) & (self.df["ROP(1 ft)"] <= max_rop) &
            (self.df["WOB (k-lbs)"] >= min_wob) & (self.df["WOB (k-lbs)"] <= max_wob)
        ]
        df["ΔT (Temp Gain)"] = df["Temp Out( degF)"] - df["Temp In(degF)"]
        self.df_filtered = df

    def plot_curve(self, x, y, xlabel, ylabel, title, color='blue'):
        fig, ax = plt.subplots()
        ax.plot(x, y, color=color)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.invert_yaxis()
        st.pyplot(fig)

    def render(self):
        st.title("🌋 Geothermal Drilling Dashboard")
        self.apply_filters()

        st.subheader("Temperature vs Depth")
        fig, ax = plt.subplots()
        ax.plot(self.df_filtered["Temp Out( degF)"], self.df_filtered["Depth"], label="Temp Out")
        ax.plot(self.df_filtered["Temp In(degF)"], self.df_filtered["Depth"], label="Temp In")
        ax.set_xlabel("Temperature (°F)")
        ax.set_ylabel("Depth (ft)")
        ax.invert_yaxis()
        ax.legend()
        st.pyplot(fig)

        self.plot_curve(self.df_filtered["ROP(1 ft)"], self.df_filtered["Depth"],
                        "ROP (ft/hr)", "Depth (ft)", "Rate of Penetration", color="green")

        self.plot_curve(self.df_filtered["WOB (k-lbs)"], self.df_filtered["Depth"],
                        "WOB (k-lbs)", "Depth (ft)", "Weight on Bit", color="purple")

        self.plot_curve(self.df_filtered["Surface Torque (psi)"], self.df_filtered["Depth"],
                        "Torque (psi)", "Depth (ft)", "Surface Torque", color="red")

        self.plot_curve(self.df_filtered["ΔT (Temp Gain)"], self.df_filtered["Depth"],
                        "ΔT (°F)", "Depth (ft)", "Temperature Gain (ΔT)", color="orange")

        st.subheader("Filtered Data Table")
        show_cols = ["Depth", "Temp Out( degF)", "Temp In(degF)", "ΔT (Temp Gain)", "ROP(1 ft)", "WOB (k-lbs)", "Surface Torque (psi)"]
        st.dataframe(self.df_filtered[show_cols].dropna().reset_index(drop=True))


# === Run the Dashboard ===
if __name__ == "__main__":
    app = GeothermalDashboard("/Users/luoyi/Desktop/10_kaggle/08_geothermal/202503_geothermal.csv")
    app.render()
