import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def read_customers() -> pd.DataFrame:
    return pd.read_csv("../data/output/olist_customers_dataset.csv", dtype={'zip_code': str})

def read_sellers() -> pd.DataFrame:
    return pd.read_csv("../data/output/olist_sellers_dataset.csv", dtype={'zip_code': str})

def read_orders() -> pd.DataFrame:
    df = pd.read_csv("../data/raw/olist_orders_dataset.csv", parse_dates=[
                         'order_purchase_timestamp', 
                         'order_approved_at',
                         'order_delivered_carrier_date',
                         'order_delivered_customer_date',
                         'order_estimated_delivery_date'])
    return df

def read_seller_delivery() -> pd.DataFrame:
    df = pd.read_csv("../data/output/sellers_shipping_time_dataset.csv" , 
                       dtype={'zip_code': str}, 
                       parse_dates=[
                           'shipping_limit_date',
                           'order_purchase_timestamp']
                    )
    df['delivered_carrier_time'] = pd.to_timedelta(df['delivered_carrier_time'])    
    return df

def _read_geojson(file_name) -> gpd.GeoDataFrame:
    df = gpd.read_file(f"../data/others/geojson/data/{file_name}.json")
    return df

def add_brazil_geometry(df: pd.DataFrame, on: str) -> gpd.GeoDataFrame:
    #read Brasil geojson
    geo = _read_geojson('Brasil')
    
    df = pd.merge(geo[["UF", "geometry"]], df, left_on='UF', right_on=on, how='left')

    # original df might not have value for every states
    df = df.drop(on, axis = 1)
    df = df.fillna(0)
    
    # Create a copy of the geometry using EPSG:3857 
    geometry_3857 = df.geometry.to_crs(epsg = 3857)

    # Find the center point for Markers/PopUps
    df['center'] = geometry_3857.centroid.to_crs(epsg = 4236)

    return df

#Show Bad, and Good
def plot_changes(gdf: gpd.GeoDataFrame, column: str, title: str):
    # 1. Setup the figure
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    
    # 2. Define the color range to be symmetrical around zero
    # This ensures that '0' is exactly in the middle (usually yellow/white)
    vmin, vmax = -gdf[column].abs().max(), gdf[column].abs().max()

    # 3. Plot
    ax = gdf.plot(
        column=column,
        cmap='RdBu',      # Red-Yellow-Green colormap
        linewidth=0.8,
        ax=ax,
        edgecolor='0.8',    # Light gray borders
        legend=True,
        vmin=vmin,          # Force the scale start
        vmax=vmax,          # Force the scale end
        legend_kwds={'label': "Change"}
    )
    
    texts = []
    for x, y, label in zip(gdf.center.x, gdf.center.y, gdf['UF']):
        t = ax.text(x, y, label, fontsize=8) # Use ax.text for adjustText compatibility
        texts.append(t)
        
    ax.set_title(title, fontsize=15)
    ax.axis('off') # Hide latitude/longitude lines
    plt.show()

# Show Which area is performing better
def plot_performance(gdf: gpd.GeoDataFrame, column: str, title: str):
    ax = gdf.plot(column = column, cmap = 'Greens', edgecolor= 'grey', legend = True, figsize=(14, 8))

    texts = []
    for x, y, label in zip(gdf.center.x, gdf.center.y, gdf['UF']):
        t = ax.text(x, y, label, fontsize=8) # Use ax.text for adjustText compatibility
        texts.append(t)
        
    plt.title(title)
    plt.show();