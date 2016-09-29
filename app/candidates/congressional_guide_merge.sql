-- Update Incumbent Candidates bioGuideID (from Scrapy) with Sunlight Data
UPDATE candidates
SET source = source || ' sunlight',
    bioguideId = (
		SELECT bioguide_id
        FROM legislators l
        WHERE instr(replace(replace(l.lastname, 'á', 'a'), 'é', 'e'), 
        	candidates.lastName) != 0 -- Match with last names where > 1 words
        AND candidates.state = l.state 
        AND (candidates.district = l.district OR 
        	length(l.district) > 2) 
        AND in_office = '1'-- only select current legislators
       )
 WHERE incumbent = 1;
