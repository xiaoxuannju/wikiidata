# wikidata

First Method: SPARQL query

presenting the information in the Wikidata Query service.
[please check the result.](https://query.wikidata.org/embed.html#%23Timeline%20of%20the%20past%205%20US%20presidents%0A%23defaultView%3ATimeline%0ASELECT%20%3Fpresident%20%3FpresidentLabel%20%3FpresidentDescription%20%3Fstart%20%3Fend%20%3Fimage%20%0AWHERE%20%7B%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%20%20%3Fpresident%20p%3AP39%20%3Fposition%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20wdt%3AP27%20wd%3AQ30%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20wdt%3AP31%20wd%3AQ5.%0A%20%20%3Fposition%20ps%3AP39%20wd%3AQ11696%3B%20%0A%20%20%20%20%20%20%20%20%20%20%20%20pq%3AP580%20%3Fstart%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20pq%3AP582%20%3Fend.%0A%20%20OPTIONAL%7B%3Fpresident%20wdt%3AP18%20%3Fimage%7D%0A%7D%0AORDER%20BY%20DESC(%3Fstart)%0ALIMIT%20)

Second Method: Web data crawling by BeautifulSoup, re and data visualization by bokeh in Python

the screenshot for the result of the second method

<img width="1437" alt="image" src="https://user-images.githubusercontent.com/78805359/162636484-d4811082-3a94-479a-b3bc-bd7e8b2f54f4.png">

