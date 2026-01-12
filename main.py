from src.extract.scrapers.scraper import TableScraper
from src.transform.population_transformer import PopulationStatesTransformer, PopulationCitiesTransformer
from src.transform.state_name_lookup_transformer import StateNameTransformer
from src.transform.order_transformer import OrderTransformer
from src.transform.geolocation_transformer import GeolocationTransformer

# Define your sources
sources = [
    {
        "url": "https://en.wikipedia.org/wiki/List_of_municipalities_in_Brazil_by_population",
        "index": 1,
        "file": "population_cities_2022.csv"
    },
    {
        "url": "https://en.wikipedia.org/wiki/2022_Brazilian_census",
        "index": 2,
        "file": "population_states_2022.csv"
    },
    {
        "url": "https://brazil-help.com/brazilian_states.htm",
        "index": 27,
        "file": "state_name_lookup.csv"
    }
]

def run_extraction():
    for source in sources:
        # Pass the URL and Filename to the constructor
        scraper = TableScraper(
            url=source["url"], 
            file_name=source["file"]
        )
        
        # This will either load from disk or scrape if it's the first time
        scraper.scrape_table(index=source["index"])

def run_transformation():
    StateNameTransformer(file_name='state_name_lookup.csv').run_all()
    PopulationCitiesTransformer(file_name='population_cities_2022.csv').run_all()
    PopulationStatesTransformer(file_name='population_states_2022.csv').run_all()
    OrderTransformer(file_name='olist_orders_dataset.csv').run_all()
    GeolocationTransformer(file_name='olist_geolocation_dataset.csv').run_all()

    

if __name__ == "__main__":
    run_extraction()
    run_transformation()
