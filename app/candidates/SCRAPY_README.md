# Updating Candidate Information
The process to update candidate information in the DB (and show on the UI) is manual at this time.  
1. Run the Scrapy commands to get candidate date into the JSON files.
2. Run the `import_candidates.py` python script to load the JSON data to the DB.

# Scrapy Instructions
The easiest way to use Scrapy locally is with the Scrapy Docker Container.

## Running the Scrapy Container
Container info is on the Docker Hub for [aciobanu/scrapy](https://hub.docker.com/r/aciobanu/scrapy/).

### General Usage
For a list of scrapy commands, simply run:

`$ docker run --rm -v $(pwd):/runtime/app -e PYTHONDONTWRITEBYTECODE=1 aciobanu/scrapy`

Since the container doesn't provide any persistence, we can use the volumes (-v) directive to share the current folder with the container.

The `-e` env variable tells Python not to create .pyc files.

## Getting Candidates Data
To run any of these commands below (including the detailed steps) using the Scrapy container, place `$ docker run --rm -v $(pwd):/runtime/app -e PYTHONDONTWRITEBYTECODE=1 aciobanu/scrapy` before it (w/o 'scrapy' again). For example `$ docker run --rm -v $(pwd):/runtime/app -e PYTHONDONTWRITEBYTECODE=1 aciobanu/scrapy list` to list available spiders.

- To run scrapy:
`scrapy crawl <spider name>`

- Use `-o <filename>` to output the parsed data to JSON file.
`scrapy crawl cand -o items.json`
 
- Use `-L` to adjust the logging level 'DEBUG' 'INFO' ...
`scrapy crawl senate2 -L INFO`

- Use the different spiders for following purposes:
	* Spider1: parse out state links
	* Spider2: parse the majority of candidate
	* Spider4: (Senate Only) parse FL, NH as they have different html layout

### Steps
Follow these steps to get candidate data and import to the DB.  
1. Get General Election Senate candidates: `scrapy crawl senate-GeneralElectionCandidatesInfo -o genElect_senate.json`  
2. Get General Election House candidates: `scrapy crawl house-GeneralElectionCandidatesInfo -o genElect_house.json`  
3. Import Senate candidates to the DB: `python import_candidates.py genElect_senate.json`  
4. Import House candidates to the DB: `python import_candidates.py genElect_house.json`  

