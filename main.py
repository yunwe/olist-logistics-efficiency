from src.extract.scrapers.scraper import TableScraper

# Define your sources
sources = [
    {
        "url": "https://en.wikipedia.org/wiki/List_of_municipalities_in_Brazil_by_population",
        "index": 1,
        "file": "population_cities_2022.csv"
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
        

if __name__ == "__main__":
    run_extraction()
