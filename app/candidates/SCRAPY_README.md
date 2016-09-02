# Scrapy Instructions
The easiest way to use scrapy locally is with the Scrapy Docker Container.

## Running the Scrapy Container
Container info is on the Docker Hub for [aciobanu/scrapy](https://hub.docker.com/r/aciobanu/scrapy/).

### General Usage
For a list of scrapy commands, simply run:

`$ docker run -v $(pwd):/runtime/app -e PYTHONDONTWRITEBYTECODE=1 aciobanu/scrapy`

Since the container doesn't provide any persistence, we can use the volumes (-v) directive to share the current folder with the container.

The env variable passed tells Python not to create .pyc files.

## Getting Candidates Data
To run any of these commands below using the Scrapy container, place `$ docker run -v $(pwd):/runtime/app -e PYTHONDONTWRITEBYTECODE=1 aciobanu/scrapy` before it. For example `$ docker run -v $(pwd):/runtime/app -e PYTHONDONTWRITEBYTECODE=1 aciobanu/scrapy list` to list available spiders.

- To run scrapy:
`scrapy crawl <spider name>`

- Use `-o <filename>` to output the parsed data to JSON file.
`scrapy crawl cand -o items.json`
 
- Use `-L` to adjust the logging level 'DEBUG' 'INFO' ...
`scrapy crawl senate2 -L INFO`

- Use the different spiders for following purposes:
	* Spider1: parse out state links
	* Spider2: parse the majority of candidate
	* Spider4: parse FL, NH as they have different html layout

### Note:
NY senators can have multiple party affiliations, see the [Ballotpedia page](https://ballotpedia.org/United_States_Senate_election_in_New_York,_2016)
