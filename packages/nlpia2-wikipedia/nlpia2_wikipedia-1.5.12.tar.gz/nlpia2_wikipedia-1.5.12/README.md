# Wikipedia

[![image](https://travis-ci.org/goldsmith/Wikipedia.png?branch=master)](https://travis-ci.org/goldsmith/Wikipedia)

[![image](https://pypip.in/d/wikipedia/badge.png)](https://crate.io/packages/wikipedia)

[![image](https://pypip.in/v/wikipedia/badge.png)](https://crate.io/packages/wikipedia)

[![License](https://pypip.in/license/wikipedia/badge.png)](https://pypi.python.org/pypi/wikipedia/)

**Wikipedia** is a Python library that makes it easy to access and parse
data from Wikipedia.

Search Wikipedia, get article summaries, get data like links and images
from a page, and more. Wikipedia wraps the [MediaWiki
API](https://www.mediawiki.org/wiki/API) so you can focus on using
Wikipedia data, not getting it.

``` {.python}
>>> from wikipedia import wikipedia as wiki
>>> print wiki.summary("Wikipedia")
Wikipedia (/ˌwɪkɨˈpiːdiə/ or /ˌwɪkiˈpiːdiə/ WIK-i-PEE-dee-ə) is a collaboratively edited, multilingual, free Internet encyclopedia supported by the non-profit Wikimedia Foundation...

>>> wiki.search("Barack")
['Barak (given name)', 'Barack Obama', ... 'Presidential transition of Barack Obama']
>>> titles = wiki.search("New York")
>>> page = wiki.page(titles[1])
>>> page.title
'New York (State)'
>>> page.url
'http://en.wikipedia.org/wiki/New_York_(state)'
>>> page.content
'New York, sometimes called New York State...'
>>> page.summary
'New York, sometimes called New York State...'
>>> page.links[0]
'10 Hudson Yards'

>>> wiki.set_lang("fr")
>>> wiki.summary("Facebook", sentences=1)
Facebook est un service de réseautage social en ligne sur Internet permettant d'y publier des informations (photographies, liens, textes, etc.) en contrôlant leur visibilité par différentes catégories de personnes.
```

Note: this library was designed for ease of use and simplicity, not for
advanced use. If you plan on doing serious scraping or automated
requests, please use
[Pywikipediabot](http://www.mediawiki.org/wiki/Manual:Pywikipediabot)
(or one of the other more advanced [Python MediaWiki API
wrappers](http://en.wikipedia.org/wiki/Wikipedia:Creating_a_bot#Python)),
which has a larger API, rate limiting, and other features so we can be
considerate of the MediaWiki infrastructure.

## Installation

To install Wikipedia, simply run:

    $ pip install nlpia2-wikipedia

Wikipedia is compatible with Python 2.6+ (2.7+ to run unittest discover)
and Python 3.3+.

## Documentation

Read the docs at <https://wikipedia.readthedocs.org/en/latest/>.

-   [Quickstart](https://wikipedia.readthedocs.org/en/latest/quickstart.html)
-   [Full API](https://wikipedia.readthedocs.org/en/latest/code.html)

To run tests, clone the [repository on
GitHub](https://github.com/goldsmith/Wikipedia), then run:

    $ pip install -r requirements.txt
    $ bash runtests  # will run tests for python and python3
    $ python -m unittest discover tests/ '*test.py'  # manual style

in the root project directory.

To build the documentation yourself, after installing requirements.txt,
run:

    $ pip install sphinx
    $ cd docs/
    $ make html

## License

MIT licensed. See the [LICENSE
file](https://github.com/goldsmith/Wikipedia/blob/master/LICENSE) for
full details.

## Credits

-   [wiki-api](https://github.com/richardasaurus/wiki-api) by
    \@richardasaurus for inspiration
-   \@nmoroze and \@themichaelyang for feedback and suggestions
-   The [Wikimedia Foundation](http://wikimediafoundation.org/wiki/Home)
    for giving the world free access to data

[![Bitdeli badge](https://d2weczhvl823v0.cloudfront.net/goldsmith/wikipedia/trend.png)](https://bitdeli.com/free)
