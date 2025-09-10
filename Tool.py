import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import joblib
import numpy as np
from PIL import Image, ImageTk

class YieldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌽 Corn Yield Prediction App")

        # File holders
        self.ivs_df = None
        self.weather_df = None
        self.predictions = None

        # --- Heading ---
        tk.Label(root, text="Corn Yield Prediction Tool", font=("Helvetica", 16, "bold")).pack(pady=10)

        # --- Instruction ---
        tk.Label(root, text="Upload IVS & Weather files, clean data, select year, and predict yield.", font=("Helvetica", 10)).pack(pady=5)

        # --- Functional Buttons ---
        self.upload_ivs_button = tk.Button(root, text="📁 Upload IVS File", width=30, command=self.load_ivs)
        self.upload_weather_button = tk.Button(root, text="📁 Upload Weather File", width=30, command=self.load_weather)
        self.clean_button = tk.Button(root, text="🧹 Clean IVS", width=30, command=self.clean_ivs)
        self.year_label = tk.Label(root, text="Select Year:")
        self.year_dropdown = ttk.Combobox(root, state="readonly", width=28)
        self.predict_button = tk.Button(root, text="🤖 Predict Yield", width=30, command=self.predict_yield)
        self.summary_button = tk.Button(root, text="📊 Show Summary", width=30, command=self.show_summary)
        self.export_button = tk.Button(root, text="💾 Export CSV", width=30, command=self.export_csv)

        # Pack UI
        for widget in [
            self.upload_ivs_button,
            self.upload_weather_button,
            self.clean_button,
            self.year_label,
            self.year_dropdown,
            self.predict_button,
            self.summary_button,
            self.export_button
        ]:
            widget.pack(pady=4)

        # --- Logos Section at Bottom ---
        self.logo_frame = tk.Frame(root)
        self.logo_frame.pack(pady=20)

        try:
            logo1 = Image.open("C:/Users/araza/Desktop/Model_base_files/PAC.png").resize((150, 100))
            logo2 = Image.open("C:/Users/araza/Desktop/Model_base_files/USDA.png").resize((120, 100))
            logo3 = Image.open("C:/Users/araza/Desktop/Model_base_files/NASA.png").resize((120, 100))

            self.logo1_img = ImageTk.PhotoImage(logo1)
            self.logo2_img = ImageTk.PhotoImage(logo2)
            self.logo3_img = ImageTk.PhotoImage(logo3)

            tk.Label(self.logo_frame, image=self.logo1_img).pack(side=tk.LEFT, padx=10)
            tk.Label(self.logo_frame, image=self.logo2_img).pack(side=tk.LEFT, padx=10)
            tk.Label(self.logo_frame, image=self.logo3_img).pack(side=tk.LEFT, padx=10)

        except Exception as e:
            messagebox.showwarning("Logo Load Error", f"Could not load one or more logos:\n{str(e)}")

    # --- Functional Methods ---
    def load_ivs(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.ivs_df = pd.read_csv(file_path)
            messagebox.showinfo("Success", "IVS file loaded successfully!")

    def load_weather(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.weather_df = pd.read_csv(file_path)
            self.weather_df['DATE'] = pd.to_datetime(self.weather_df['DATE'])
            years = sorted(self.weather_df['DATE'].dt.year.unique())
            self.year_dropdown['values'] = years
            if years:
                self.year_dropdown.current(0)
            messagebox.showinfo("Success", "Weather file loaded and years populated!")

    def clean_ivs(self):
        if self.ivs_df is not None:
            original_rows = len(self.ivs_df)
            self.ivs_df.dropna(inplace=True)
            removed = original_rows - len(self.ivs_df)
            messagebox.showinfo("Cleaned", f"Removed {removed} rows with missing data.")
        else:
            messagebox.showerror("Error", "Please upload IVS file first!")

    def process_weather(self, year):
        df = self.weather_df
        mask = (df['DATE'].dt.year == year) & (df['DATE'].dt.month >= 5) & (df['DATE'].dt.month <= 9)
        season = df[mask]
        return pd.DataFrame([{
            'CHU': season['CHU'].sum(),
            'GDD': season['GDD'].sum(),
            'AWDR': season['AWDR'].mean(),
            'SPI': season['SPI'].mean(),
            'PRECIPITATION': season['PRECIPITATION'].sum(),
            'TM': season['TM'].mean(),
            'TM_MAX': season['TM_MAX'].mean(),
            'TM_MIN': season['TM_MIN'].mean(),
            'SW_DWN': season['SW_DWN'].sum(),
            'PAR_TOT': season['PAR_TOT'].sum()
        }])

    def predict_yield(self):
        try:
            import numpy as np
            np.foo = "dummy"  
            year = int(self.year_dropdown.get())
            if self.ivs_df is None or self.weather_df is None:
                messagebox.showerror("Error", "Upload both IVS and weather files!")
                return

            input_df = self.ivs_df.copy()
            input_df['Year'] = year

            weather_agg = self.process_weather(year)
            for col in weather_agg.columns:
                input_df[col] = weather_agg[col].values[0]

            model = joblib.load('C:/Users/araza/Desktop/Model_base_files/stacking_model.pkl')
            scaler = joblib.load('C:/Users/araza/Desktop/Model_base_files/scaler.pkl')
            imputer = joblib.load("C:/Users/araza/Desktop/Model_base_files/imputer.pkl")

            required_features = [
                'MNDWI', 'TVI', 'EVI', 'NDWI', 'ELAI', 'NCMI', 'SR', 'GCI', 'CVI',
                'GCVI', 'WDRVI', 'GNDVI', 'NDVI', 'ARVI', 'Sand_%', 'Clay_%',
                'Silt_%', 'OM_%', 'pH', 'BD_g/cm3', 'Ksat_cm/hr', 'PSDI',
                'HB_Kpa', 'MPSD', 'SPIPMPD', 'RSWC', 'SSWC','TWI', 'Curvature', 'Slope',
                'Relative_Elevation', 'Aspect', 'CHU', 'GDD', 'AWDR', 'SPI',
                'PRECIPITATION', 'TM', 'TM_MAX', 'TM_MIN', 'SW_DWN', 'PAR_TOT'
            ]

            missing = set(required_features) - set(input_df.columns)
            if missing:
                messagebox.showerror("Error", f"Missing columns: {missing}")
                return

            X = input_df[required_features]
            X_scaled = scaler.transform(imputer.transform(X))
            predictions = model.predict(X_scaled)

            self.predictions = input_df[['Lat', 'Lon']].copy()
            self.predictions['Year'] = year
            self.predictions['Predicted_Yield_kg/ha'] = predictions

            messagebox.showinfo("Success", "Prediction completed!")

        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

    def show_summary(self):
        if self.predictions is not None:
            stats = self.predictions['Predicted_Yield_kg/ha'].describe()
            messagebox.showinfo("Summary Stats", stats.to_string())
        else:
            messagebox.showerror("Error", "Please run prediction first!")

    def export_csv(self):
        if self.predictions is not None:
            export_path = filedialog.asksaveasfilename(defaultextension=".csv")
            if export_path:
                self.predictions.to_csv(export_path, index=False)
                messagebox.showinfo("Exported", f"Predictions exported to {export_path}")
        else:
            messagebox.showerror("Error", "No predictions to export!")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = YieldApp(root)
    root.mainloop()
