import pandas as pd
from utils.constants import DATA_DIRECTORY


df = pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")

filtered_df = df.copy()  
df_bar_chart=df.copy()


try:
    from assets.swedish_coordinates import swedish_coordinates
    print("Successfully imported swedish_coordinates")
except ImportError:
    print("Warning: Could not import swedish_coordinates, using empty dict")
    swedish_coordinates = {}
   



