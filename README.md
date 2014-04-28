### NYS Department of State Division of Corporations Entity Information Scraper

A scraper to pull in data from [http://www.dos.ny.gov/corps/bus_entity_search.html](http://www.dos.ny.gov/corps/bus_entity_search.html).


#### Usage

```
pip install -r requirements.txt
python scrape.py <entity_start_number> <entity_end_number>
```

This will save a huge number of raw HTML files into a zip archive called
`archive.zip`.  Processing to come!

#### TODO

Fix corrupt archive: `zip -FF archive.zip --out uncorrupt.zip`

Processing the raw data.
