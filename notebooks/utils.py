import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def read_customers() -> pd.DataFrame:
    return pd.read_csv("../data/raw/olist_customers_dataset.csv", dtype={'customer_zip_code_prefix': str})

def read_sellers() -> pd.DataFrame:
    return pd.read_csv("../data/raw/olist_sellers_dataset.csv", dtype={'seller_zip_code_prefix': str})

def read_orders() -> pd.DataFrame:
    df = pd.read_csv("../data/output/olist_orders_dataset.csv", parse_dates=[
                         'order_purchase_timestamp', 
                         'order_approved_at',
                         'order_delivered_carrier_date',
                         'order_delivered_customer_date',
                         'order_estimated_delivery_date'])
    df['total_delivery_time'] = pd.to_timedelta(df['total_delivery_time'])
    df['estimated_delivery_time'] = pd.to_timedelta(df['estimated_delivery_time'])
    df['wait_approve_time'] = pd.to_timedelta(df['wait_approve_time'])
    df['seller_to_logistic_time'] = pd.to_timedelta(df['seller_to_logistic_time'])    
    df['logistic_to_customer_time'] = pd.to_timedelta(df['logistic_to_customer_time'])    
    return df

def read_geojson(file_name) -> pd.DataFrame:
    df = gpd.read_file(f"../data/others/geojson/data/{file_name}.json")
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
    ax = gdf.plot(column = column, cmap = 'YlOrRd', edgecolor= 'grey', legend = True, figsize=(14, 8))

    texts = []
    for x, y, label in zip(gdf.center.x, gdf.center.y, gdf['UF']):
        t = ax.text(x, y, label, fontsize=8) # Use ax.text for adjustText compatibility
        texts.append(t)
        
    plt.title(title)
    plt.show();