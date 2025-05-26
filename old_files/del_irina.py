import pandas as pd
import sys
import os
import plotly.express as px
import plotly.graph_objects as go


dashboard_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dashboard_path)

from utils.constants import DATA_DIRECTORY


assets_path = "/Users/ira/Documents/DE24/github/the-skool-group5/assets"
sys.path.append(assets_path)

try:
    from swedish_coordinates import swedish_coordinates
    print("Successfully imported swedish_coordinates")
except ImportError:
    print("Warning: Could not import swedish_coordinates, using empty dict")
    swedish_coordinates = {}


def prepare_pie_data(df):

    result_df = df[df['Beslut'] == 'Beviljad']
    area_stats = result_df.groupby('Utbildningsområde')['Antal beviljade platser start 2024'].sum().sort_values(ascending=False)
    return area_stats

def prepare_map_data(df):

    result_df = df[df['Beslut'] == 'Beviljad'].copy()
    result_df['Kommun'] = result_df['Kommun'].replace('Se "Lista flera kommuner"', 'Flera kommuner')
    

    kommun_stats = result_df.groupby('Kommun')['Antal beviljade platser start 2024'].sum().reset_index()
    kommun_stats.columns = ['Kommun', 'Antal_platser']
    
 
    if swedish_coordinates:
        kommun_stats['lat'] = kommun_stats['Kommun'].map(lambda x: swedish_coordinates.get(x, {}).get('lat'))
        kommun_stats['lon'] = kommun_stats['Kommun'].map(lambda x: swedish_coordinates.get(x, {}).get('lon'))
    
    return kommun_stats


def create_pie_chart(df):

    if len(df) == 0:
        return go.Figure().add_trace(go.Pie(labels=['Ingen data'], values=[1]))
    
    fig = px.pie(
        values=df.values, 
        names=df.index,
        title='Fördelning av beviljade platser per utbildningsområde'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(t=50, l=0, r=0, b=0),
        font=dict(size=12)
    )
    return fig

def create_heat_map(df, show_map=True):

    if len(df) == 0:
        return go.Figure().add_trace(go.Bar(x=['Ingen data'], y=[1]))
    
    if show_map and 'lat' in df.columns and 'lon' in df.columns:
      
        df_valid = df.dropna(subset=['lat', 'lon'])
        if len(df_valid) > 0:
            try:
         
                fig = px.scatter_mapbox(
                    df_valid,
                    lat='lat',
                    lon='lon',
                    size='Antal_platser',
                    hover_name='Kommun',
                    hover_data=['Antal_platser'],
                    mapbox_style='open-street-map',
                    zoom=4,
                    title='Geografisk fördelning av YH-program',
                    height=600
                )
                fig.update_layout(
                    margin=dict(t=50, l=0, r=0, b=0),
                )
                return fig
            except Exception as e:
                print(f"Error creating map: {e}")
                pass
    
   
    df_sorted = df.sort_values('Antal_platser', ascending=True).tail(15)
    fig = px.bar(
        df_sorted,
        x='Antal_platser',
        y='Kommun',
        orientation='h',
        title='Top 15 kommuner med flest beviljade platser',
        labels={'Antal_platser': 'Antal platser', 'Kommun': 'Kommun'}
    )
    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(t=50, l=120, r=30, b=50),
        yaxis={'categoryorder': 'total ascending'},
        height=500,
        font=dict(size=12)
    )
    return fig


def get_summary_stats(df):
 
    result_df = df[df['Beslut'] == 'Beviljad']
    
    stats = {
        'total_approved_places': result_df['Antal beviljade platser start 2024'].sum(),
        'total_applications': len(df),
        'approved_applications': len(result_df),
        'approval_rate': len(result_df) / len(df) * 100 if len(df) > 0 else 0,
        'unique_schools': result_df['Anordnare namn'].nunique(),
        'unique_municipalities': result_df['Kommun'].nunique(),
        'unique_areas': result_df['Utbildningsområde'].nunique()
    }
    
    return stats

def create_additional_chart(df, chart_type="bar"):

    if chart_type == "bar" and len(df) > 0:
        # Диаграмма топ школ
        result_df = df[df['Beslut'] == 'Beviljad']
        school_stats = result_df.groupby('Anordnare namn')['Antal beviljade platser start 2024'].sum().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=school_stats.values,
            y=school_stats.index,
            orientation='h',
            title='Top 10 skolor med flest beviljade platser',
            labels={'x': 'Antal platser', 'y': 'Skola'}
        )
        fig.update_layout(
            plot_bgcolor="white",
            margin=dict(t=50, l=150, r=30, b=50),
            yaxis={'categoryorder': 'total ascending'},
            height=400,
            font=dict(size=11)
        )
        return fig
    
    return go.Figure()


def export_filtered_data(df, filename="filtered_data.xlsx"):

    try:
        df.to_excel(filename, index=False)
        print(f"Data exported to {filename}")
        return True
    except Exception as e:
        print(f"Error exporting data: {e}")
        return False


if __name__ == "__main__":
    print("Testing del_irina functions...")
    
  
    df = pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")
    
   
    print("\n--- Testing create_pie_chart() ---")
    pie_data = prepare_pie_data(df)
    pie_fig = create_pie_chart(pie_data)
    if pie_fig:
        print("Pie chart created successfully!")

    print("\n--- Testing create_heat_map() ---")
    map_data = prepare_map_data(df)
    heat_fig = create_heat_map(map_data)
    if heat_fig:
        print("Heat map created successfully!")

    print("\n--- Testing get_summary_stats() ---")
    stats = get_summary_stats(df)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\nAll functions tested successfully!")





# prepare_map_data
# map_data = prepare_map_data(filtered_df)

# def prepare_map_data(filtered_df):

#     result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad'].copy()
#     result_df['Kommun'] = result_df['Kommun'].replace('Se "Lista flera kommuner"', 'Flera kommuner')
#     kommun_stats = result_df.groupby('Kommun')['Beviljade platser totalt'].sum().reset_index()
#     kommun_stats.columns = ['Kommun', 'Antal_platser']
#     if swedish_coordinates:
#         kommun_stats['lat'] = kommun_stats['Kommun'].map(lambda x: swedish_coordinates.get(x, {}).get('lat'))
#         kommun_stats['lon'] = kommun_stats['Kommun'].map(lambda x: swedish_coordinates.get(x, {}).get('lon')) 

#     return kommun_stats


# def prepare_pie_data(filtered_df):

#     result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad']
#     area_stats = result_df.groupby('Utbildningsområde')['Antal beviljade platser start 2024'].sum().sort_values(ascending=False)
    
#     return area_stats

# def create_additional_chart(fitered_df, chart_type="bar"):

#     if chart_type == "bar" and len(filtered_df) > 0:
#         result_df = filtered_df[filtered_df['Beslut'] == 'Beviljad']
#         school_stats = result_df.groupby('Utbildningsanordnare administrativ enhet')['Beviljade platser totalt'].sum().sort_values(ascending=False).head(10)
        
#         fig = px.bar(
#             x=school_stats.values,
#             y=school_stats.index,
#             orientation='h',
#             title='Top 10 skolor med flest beviljade platser',
#             labels={'x': 'Antal platser', 'y': 'Skola'}
#         )
#         fig.update_layout(
#             plot_bgcolor="white",
#             margin=dict(t=50, l=150, r=30, b=50),
#             yaxis={'categoryorder': 'total ascending'},
#             height=400,
#             font=dict(size=11)
#         )
#         return fig
    
#     return go.Figure()

# def kpi(filtered_df):

#     import duckdb
    
#     total_ans = duckdb.query(
#         """--sql
#     SELECT 
#         "Anordnare namn" AS Anordnare,
#         COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljad,
#         COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag,
#         COUNT(*) AS Totalt
#     FROM filtered_df 
#     GROUP BY Anordnare
#     ORDER BY Totalt DESC
#     """
#     ).df()

#     bevil_platser = duckdb.query(
#         """--sql
#         SELECT
#             "Anordnare namn" AS Anordnare,
#             COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljad
#         FROM filtered_df
#         GROUP BY Anordnare
#     """
#     ).df()

#     anordnare = duckdb.query(
#         """--sql
#         SELECT
#             "Anordnare namn" AS Anordnare,
#             COUNT(*) AS Totalt
#         FROM filtered_df
#         GROUP BY Anordnare
#         ORDER BY Totalt DESC
#     """
#     ).df()

#     bevil_procent = duckdb.query(
#         """--sql
#         SELECT 
#             "Anordnare namn" AS Anordnare,
#             COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljad,
#             COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag,
#             COUNT(*) AS Totalt,
#             CAST(COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS FLOAT) / COUNT(*) * 100 AS Procent
#         FROM filtered_df 
#         GROUP BY Anordnare
#         ORDER BY Totalt DESC
#     """
#     ).df()
    
#     total_applications = len(filtered_df)
#     approved_applications = len(filtered_df[filtered_df['Beslut'] == 'Beviljad'])
#     total_approved_places = filtered_df[filtered_df['Beslut'] == 'Beviljad']['Antal beviljade platser start 2024'].sum()
#     approval_rate = approved_applications / total_applications * 100 if total_applications > 0 else 0
#     unique_schools = filtered_df['Anordnare namn'].nunique()
#     unique_municipalities = filtered_df['Kommun'].nunique()
#     unique_areas = filtered_df['Utbildningsområde'].nunique()

#     avg_places = total_approved_places / approved_applications if approved_applications > 0 else 0
    
#     kpi_dict = {
#         'total_ans': total_ans,
#         'bevil_platser': bevil_platser,
#         'anordnare': anordnare,
#         'bevil_procent': bevil_procent,
#         'total_applications': total_applications,
#         'approved_applications': approved_applications,
#         'total_approved_places': total_approved_places,
#         'approval_rate': approval_rate,
#         'unique_schools': unique_schools,
#         'unique_municipalities': unique_municipalities,
#         'unique_areas': unique_areas,
#         'avg_places': avg_places
#     }
    
#     return kpi_dict