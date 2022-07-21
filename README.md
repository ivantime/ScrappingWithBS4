# http-localhost-8888-notebooks-Desktop-ScrappingWithBS4

<br>
<br>
<i>Wikipedia.org</i> Progress:
<br> 
<ul>
<li>Scrapped URLs from Search Page (eg. https://en.wikipedia.org/w/index.php?search=how+to+build+computers)</li>
<li>Scrapped Main Title and Content from Wiki Page (eg. https://en.wikipedia.org/wiki/Computer)</li>
<li>Combined 20 Keywords into Combinations of up to 20 Keywords into a Search Query (to get Webpage as Wiki Page or Wiki Search Result)</li>
</ul>
<br>
<br>
<br>

<b>How to Run Script</b>
<br>
<ul>
<li>Run the Jupyter Notebook</li>
<i>OR</i>
<li>Run via cmd, eg. Command: "python wikiProgram.py"</li>
<i>Might need to pip install the libraries accordingly (install code via python shell below):<br>
<li>pip install beautifulsoup4</li>
<li>pip install requests</li>
</ul>

<br>
<br>
<b><u>Crawler Flow:</u></b>
<br>

<br>
Go through List of keywords>get URL from Wiki Search> EITHER: 
<br>
<br>

<b>(1):</b> 
<i>[Start for (1)]</i>
    [[Depth 1]]
    Wiki Search Returns Wiki Page (Not Search Page):
    Crawl Wiki Page for Title and Content>

        [[Depth 2]]
        Get newly Discovered Links in Wiki Page (known as '2nd Deep Layer')>
        Crawl Wiki Page of newly Discovered Links (in '2nd Deep Layer') for Title and Content>
<i>[[END for (1)]]</i>
<br>
<br>

<b>OR</b>
<br>

<b>(2):</b> 
<i>[Start for (2)]</i>
    Wiki Search Returns Wiki Search Page
    [[Depth 1]]
    Wiki Search Returns Wiki Page (Not Search Page):
    Crawl Wiki Page for Title and Content>

        [[Depth 2]]
        Get newly Discovered Links in Wiki Page (known as '2nd Deep Layer')>
        Crawl Wiki Page of newly Discovered Links (in '2nd Deep Layer') for Title and Content>
<i>[[END for (2)]]</i>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


<br>
<i>OpenLibrary.org</i> Progress:
<br> 
<ul>
<li>Scrapped Search Page</li>
<li>Scrapped Books URLs from Search Page</li>
<li>Scrapped Book Details from Book's Page (Details)</li>
<li> Saved Book Details into json File (File Naming Convention based on URL's Unique AlphaNumeric Code- eg. 'OL6729940W.json' after URL's <i>https://openlibrary.org/works/</i>)
</ul>
<br>
<h3> 4 Json Files included for Reference (Some Books have Missing Key/Values due to Missing Data From OpenLibrary Site)