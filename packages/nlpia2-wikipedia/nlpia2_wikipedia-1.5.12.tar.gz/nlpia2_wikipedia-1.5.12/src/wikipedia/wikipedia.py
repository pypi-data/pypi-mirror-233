from __future__ import unicode_literals

import logging
import requests
import time
from datetime import datetime, timedelta
from decimal import Decimal

from .exceptions import (
    PageError, DisambiguationError, RedirectError, HTTPTimeoutError,
    WikipediaException, ODD_ERROR_MESSAGE
)
from bs4 import BeautifulSoup
from .util import cache, stdout_encode
from .util import debug  # noqa
import pandas as pd
import re

log = logging.getLogger(__name__)

API_URL = 'http://en.wikipedia.org/w/api.php'
RATE_LIMIT = False
RATE_LIMIT_MIN_WAIT = None
RATE_LIMIT_LAST_CALL = None
USER_AGENT = 'wikipedia (https://github.com/goldsmith/Wikipedia/)'


def set_lang(prefix):
    '''Change the language of the API being requested.

    Set `prefix` to one of the two letter prefixes found on the
    `list of all Wikipedias <http://meta.wikimedia.org/wiki/List_of_Wikipedias>`.

    After setting the language, the cache for `search`, `suggest`, and `summary`
    will be cleared.

    .. note:: Make sure you search for page titles in the language that you have set.
    '''
    global API_URL
    API_URL = 'http://' + prefix.lower() + '.wikipedia.org/w/api.php'

    for cached_func in (search, suggest, summary):
        cached_func.clear_cache()


def set_user_agent(user_agent_string):
    '''
    Set the User-Agent string to be used for all requests.

    Arguments:

    * user_agent_string - (string) a string specifying the User-Agent header
    '''
    global USER_AGENT
    USER_AGENT = user_agent_string


def set_rate_limiting(rate_limit, min_wait=timedelta(milliseconds=50)):
    '''
    Enable or disable rate limiting on requests to the Mediawiki servers.
    If rate limiting is not enabled, under some circumstances (depending on
    load on Wikipedia, the number of requests you and other `wikipedia` users
    are making, and other factors), Wikipedia may return an HTTP timeout error.

    Enabling rate limiting generally prevents that issue, but please note that
    HTTPTimeoutError still might be raised.

    Arguments:

    * rate_limit - (Boolean) whether to enable rate limiting or not

    Keyword arguments:

    * min_wait (timedelta): if rate limiting is enabled, timedelta min time to wait between requests.
        default: timedelta(milliseconds=50)
    '''
    global RATE_LIMIT
    global RATE_LIMIT_MIN_WAIT
    global RATE_LIMIT_LAST_CALL

    RATE_LIMIT = rate_limit
    if not rate_limit:
        RATE_LIMIT_MIN_WAIT = None
    else:
        RATE_LIMIT_MIN_WAIT = min_wait

    RATE_LIMIT_LAST_CALL = None


@cache
def search(query, results=10, suggestion=False):
    '''
    Do a Wikipedia search for `query`.

    Keyword arguments:

    * results - the maxmimum number of results returned
    * suggestion - if True, return results and suggestion (if any) in a tuple
    '''

    search_params = {
        'list': 'search',
        'srprop': '',
        'srlimit': results,
        'limit': results,
        'srsearch': query
    }
    if suggestion:
        search_params['srinfo'] = 'suggestion'

    raw_results = _wiki_request(search_params)

    if 'error' in raw_results:
        if raw_results['error']['info'] in ('HTTP request timed out.', 'Pool queue is full'):
            raise HTTPTimeoutError(query)
        else:
            raise WikipediaException(raw_results['error']['info'])

    search_results = (d['title'] for d in raw_results['query']['search'])

    if suggestion:
        if raw_results['query'].get('searchinfo'):
            return list(search_results), raw_results['query']['searchinfo']['suggestion']
        else:
            return list(search_results), None

    return list(search_results)


@cache
def geosearch(latitude, longitude, title=None, results=10, radius=1000):
    '''
    Do a wikipedia geo search for `latitude` and `longitude`
    using HTTP API described in http://www.mediawiki.org/wiki/Extension:GeoData

    Arguments:

    * latitude (float or decimal.Decimal)
    * longitude (float or decimal.Decimal)

    Keyword arguments:

    * title - The title of an article to search for
    * results - the maximum number of results returned
    * radius - Search radius in meters. The value must be between 10 and 10000
    '''

    search_params = {
        'list': 'geosearch',
        'gsradius': radius,
        'gscoord': '{0}|{1}'.format(latitude, longitude),
        'gslimit': results
    }
    if title:
        search_params['titles'] = title

    raw_results = _wiki_request(search_params)

    if 'error' in raw_results:
        if raw_results['error']['info'] in ('HTTP request timed out.', 'Pool queue is full'):
            raise HTTPTimeoutError('{0}|{1}'.format(latitude, longitude))
        else:
            raise WikipediaException(raw_results['error']['info'])

    search_pages = raw_results['query'].get('pages', None)
    if search_pages:
        search_results = (v['title'] for k, v in search_pages.items() if k != '-1')
    else:
        search_results = (d['title'] for d in raw_results['query']['geosearch'])

    return list(search_results)


@cache
def suggest(query):
    '''
    Get a Wikipedia search suggestion for `query`.
    Returns a string or None if no suggestion was found.
    '''

    search_params = {
        'list': 'search',
        'srinfo': 'suggestion',
        'srprop': '',
    }
    search_params['srsearch'] = query

    raw_result = _wiki_request(search_params)

    if raw_result['query'].get('searchinfo'):
        return raw_result['query']['searchinfo']['suggestion']

    return None


def random(pages=1):
    '''
    Get a list of random Wikipedia article titles.

    .. note:: Random only gets articles from namespace 0, meaning no Category, User talk, or other meta-Wikipedia pages.

    Keyword arguments:

    * pages - the number of random pages returned (max of 10)
    '''
    # http://en.wikipedia.org/w/api.php?action=query&list=random&rnlimit=5000&format=jsonfm
    query_params = {
        'list': 'random',
        'rnnamespace': 0,
        'rnlimit': pages,
    }

    response = _wiki_request(query_params)
    titles = [page['title'] for page in response['query']['random']]

    if len(titles) == 1:
        return titles[0]

    return titles


@cache
def summary(article, sentences=0, chars=0, auto_suggest=True, redirect=True):
    '''
    Plain text summary of the page.

    .. note:: This is a convenience wrapper - auto_suggest and redirect are enabled by default

    Keyword arguments:

    * sentences - if set, return the first `sentences` sentences (can be no greater than 10).
    * chars - if set, return only the first `chars` characters (actual text returned may be slightly longer).
    * auto_suggest - let Wikipedia find a valid page title for the query
    * redirect - allow redirection without raising RedirectError
    '''

    # use auto_suggest and redirect to get the correct article
    # also, use page's error checking to raise DisambiguationError if necessary
    article = get_page(article, auto_suggest=auto_suggest, redirect=redirect)

    title = article.title
    pageid = article.pageid

    query_params = {
        'prop': 'extracts',
        'explaintext': '',
        'titles': title
    }

    if sentences:
        query_params['exsentences'] = sentences
    elif chars:
        query_params['exchars'] = chars
    else:
        query_params['exintro'] = ''

    response = _wiki_request(query_params)
    summary = response['query']['pages'][pageid]['extract']

    return dict(summary=summary, response=response)


def get_page(article=None, pageid=None, auto_suggest=True, redirect=True, preload=False):
    '''
    Get a WikipediaPage object for the page with title `title` or the pageid
    `pageid` (mutually exclusive).

    Keyword arguments:

    * title - the title of the page to load
    * pageid - the numeric pageid of the page to load
    * auto_suggest - let Wikipedia find a valid page title for the query
    * redirect - allow redirection without raising RedirectError
    * preload - load content, summary, images, references, and links during initialization
    '''
    if isinstance(article, WikipediaPage):
        return article
    if article and not pageid and isinstance(article, int):
        pageid = article
        try:
            return WikipediaPage(pageid=pageid, preload=preload)
        except (PageError, DisambiguationError) as e:
            log.exception()
            raise e
    if article:
        article = article.strip().replace(' ', '_').title()
        if auto_suggest:
            results, suggestion = search(
                article, results=1, suggestion=True)
            try:
                suggestion = suggestion or results[0]
            except IndexError:
                log.info('Unable to automatically suggest a title')
                # FIXME: If the suggestion or search results, does the page really not exist?
                # raise PageError(title)
        try:
            # search for exact match first, even if alternative suggestions found
            return WikipediaPage(
                article,
                redirect=redirect, preload=preload
            )
        except (PageError, DisambiguationError):
            try:
                return WikipediaPage(suggestion, redirect=redirect, preload=preload)
            except (PageError, DisambiguationError) as e:
                log.error(f'BAD SUGGESTION: {e}')
                log.error(f'BAD SUGGESTION: {__name__}.suggest({article}) => {suggestion}')
                if suggestion != article:
                    return WikipediaPage(article, redirect=redirect, preload=preload)
                raise e
    raise ValueError("Either a title, pageid, or WikipediaPage must be specified")


page = get_page


class WikipediaPage(object):
    ''' Wikipedia article content, title, pageid, sections, and summary.

    Uses property methods to filter data from the raw HTML.
    '''

    def __init__(self, title=None, pageid=None, redirect=True, preload=False,
                 original_title='', format='wikitext', version=1):
        """ Retrieve a wikipedia article (page) or raise exception (PageError, DisambiguationError, ...)

        `format` and `version` ignored but will reflect package version major version
        so bump default version when improved parsers available"""
        # TODO: parse page.content into markdown (headings with ## instead of ==)
        self.title = None
        self.pageid = None
        self._sections = None

        if title is not None:
            self.title = title
            self.original_title = original_title or title
        elif pageid is not None:
            self.pageid = pageid
        else:
            raise ValueError("Either a title or a pageid must be specified")
        self.__load(redirect=redirect, preload=preload)

        if preload:
            for prop in ('content', 'summary', 'images', 'references', 'links', 'sections'):
                getattr(self, prop)

    def __repr__(self):
        return stdout_encode(u'<WikipediaPage \'{}\'>'.format(self.title))

    def __eq__(self, other):
        try:
            return (
                (self.pageid or other.pageid) == other.pageid
                and (self.title or other.title) == other.title
                and self.url == other.url
            )
        except Exception:
            return False

    def __load(self, redirect=True, preload=False):
        '''
        Load basic information from Wikipedia.
        Confirm that page exists and is not a disambiguation/redirect.

        Does not need to be called manually, should be called automatically during __init__.
        '''
        query_params = {
            'prop': 'info|pageprops',
            'inprop': 'url',
            'ppprop': 'disambiguation',
            'redirects': '',
        }
        if self.pageid:
            query_params['pageid'] = self.pageid
        else:
            query_params['titles'] = self.title

        response = _wiki_request(query_params)

        query = response['query']
        pageid = list(query['pages'].keys())[0]
        article = query['pages'][pageid]

        # missing is present if the page is missing
        if 'missing' in str(article).lower():
            if hasattr(self, 'title'):
                raise PageError(self.title)
            else:
                raise PageError(pageid=self.pageid)

        # same thing for redirect, except it shows up in query instead of page for
        # whatever silly reason
        elif 'redirects' in query:
            if redirect:
                redirects = query['redirects'][0]

                if 'normalized' in query:
                    normalized = query['normalized'][0]
                    assert normalized['from'] == self.title, ODD_ERROR_MESSAGE

                    from_title = normalized['to']

                else:
                    from_title = self.title

                assert redirects['from'] == from_title, ODD_ERROR_MESSAGE

                # change the title and reload the whole object
                self.__init__(redirects['to'], redirect=redirect, preload=preload)

            else:
                raise RedirectError(getattr(self, 'title', article['title']))

        # since we only asked for disambiguation in ppprop,
        # if a pageprop is returned,
        # then the page must be a disambiguation page
        elif 'pageprops' in article:
            query_params = {
                'prop': 'revisions',
                'rvprop': 'content',
                'rvparse': '',
                'rvlimit': 1
            }
            if hasattr(self, 'pageid'):
                query_params['pageids'] = self.pageid
            else:
                query_params['titles'] = self.title
            response = _wiki_request(query_params)
            html = response['query']['pages'][pageid]['revisions'][0]['*']

            lis = BeautifulSoup(html, 'html.parser').find_all('li')
            filtered_lis = [li for li in lis if 'tocsection' not in ''.join(li.get('class', []))]
            may_refer_to = [li.a.get_text() for li in filtered_lis if li.a]

            raise DisambiguationError(getattr(self, 'title', article['title']), may_refer_to)

        else:
            self.pageid = pageid
            self.title = article['title']
            self.url = article['fullurl']

    def __continued_query(self, query_params):
        '''
        Based on https://www.mediawiki.org/wiki/API:Query#Continuing_queries
        '''
        query_params.update(self.__title_query_param)

        last_continue = {}
        prop = query_params.get('prop', None)

        while True:
            params = query_params.copy()
            params.update(last_continue)

            response = _wiki_request(params)

            if 'query' not in response:
                break

            pages = response['query']['pages']
            if 'generator' in query_params:
                for datum in pages.values():  # in python 3.3+: "yield from pages.values()"
                    yield datum
            else:
                for datum in pages[self.pageid][prop]:
                    yield datum

            if 'continue' not in response:
                break

            last_continue = response['continue']

    @property
    def __title_query_param(self):
        if getattr(self, 'title', None) is not None:
            return {'titles': self.title}
        else:
            return {'pageids': self.pageid}

    def html(self):
        ''' Get full page HTML.

        WARNING: This is slow for long pages.
        '''

        if not getattr(self, '_html', False):
            query_params = {
                'prop': 'revisions',
                'rvprop': 'content',
                'rvlimit': 1,
                'rvparse': '',
                'titles': self.title
            }

            response = _wiki_request(query_params)
            self._html = response['query']['pages'][self.pageid]['revisions'][0]['*']

        return self._html

    @property
    def content(self):
        '''Plain text content of the page, excluding images, tables, and other data.'''

        if not getattr(self, '_content', False):
            query_params = {
                'prop': 'extracts|revisions',
                'explaintext': '',
                'rvprop': 'ids'
            }
            if not getattr(self, 'title', None) is None:
                query_params['titles'] = self.title
            else:
                query_params['pageids'] = self.pageid
            response = _wiki_request(query_params)
            self._content = response['query']['pages'][self.pageid]['extract']
            self._revision_id = response['query']['pages'][self.pageid]['revisions'][0]['revid']
            self._parent_id = response['query']['pages'][self.pageid]['revisions'][0]['parentid']

        return self._content

    def get_content(self):
        """ Stub to allow improved parsing (sentence separating whitespace in HTML is deleted)

        TODO:
          - [ ] wiki.get_content() with improved parsing of sentence separators in HTML
          - [ ] improved parsing to create .json()
          - [ ] improved @property .json used within .content and .get_content
            - .content utilizes __init__ setting that defaults to old parsing
            - .get_content defaults to new parsing always (ignoring .__init__ setting
          - [ ] with options in Wikipedia.__init__
          - [ ] @property for md/markdown
          - [ ] @property for adoc
          - [ ] @property .rst/restructured_text
          - [ ] @property .rtf/rich_text
          - [ ] @property .wiki/wikitext
          - [ ] get_content defaults to markdown instead of RST or wikitext
          - [ ] __init__ options to control HTML parsing for json and default content format
        """

        return self.content

    def get_html_paragraphs(self, html=None):
        html = html or self.html()
        soup = BeautifulSoup(html, 'html.parser')
        self.paragraphs = [p.text for p in soup.select("p")]
        soup_filtered = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])
        self.paragraphs_with_headings = [x.text for x in soup_filtered]
        return self.paragraphs_with_headings

    @property
    def revision_id(self):
        '''
        Revision ID of the page.

        The revision ID is a number that uniquely identifies the current
        version of the page. It can be used to create the permalink or for
        other direct API calls. See `Help:Page history
        <http://en.wikipedia.org/wiki/Wikipedia:Revision>`_ for more
        information.
        '''

        if not getattr(self, '_revid', False):
            # fetch the content (side effect is loading the revid)
            self.content

        return self._revision_id

    @property
    def parent_id(self):
        '''
        Revision ID of the parent version of the current revision of this
        page. See ``revision_id`` for more information.
        '''

        if not getattr(self, '_parentid', False):
            # fetch the content (side effect is loading the revid)
            self.content

        return self._parent_id

    def summary_sentences(self, **kwargs):
        """List sentences in summary section of wikipedia page"""
        summary(self.title, **kwargs)

    @property
    def summary(self):
        '''Plain text summary of the page.'''

        if not getattr(self, '_summary', False):
            query_params = {
                'prop': 'extracts',
                'explaintext': '',
                'exintro': '',
            }
            if self.title:
                query_params['titles'] = self.title
            else:
                query_params['pageid'] = self.pageid

            # FIXME: insert spaces at end of sentences (or don't strip them)
            # FIXME: add double newlines between paragraphs
            response = _wiki_request(query_params)
            self._summary = response['query']['pages'][self.pageid]['extract']

        return self._summary

    @property
    def images(self):
        '''
        List of URLs of images on the page.
        '''

        if not getattr(self, '_images', False):
            self._images = [
                p['imageinfo'][0]['url']
                for p in self.__continued_query({
                    'generator': 'images',
                    'gimlimit': 'max',
                    'prop': 'imageinfo',
                    'iiprop': 'url',
                })
                if 'imageinfo' in p
            ]

        return self._images

    @property
    def coordinates(self):
        '''
        Tuple of Decimals in the form of (lat, lon) or None
        '''
        if not getattr(self, '_coordinates', False):
            query_params = {
                'prop': 'coordinates',
                'colimit': 'max',
                'titles': self.title,
            }

            response = _wiki_request(query_params)

            if 'query' in response:
                coordinates = response['query']['pages'][self.pageid]['coordinates']
                self._coordinates = (Decimal(coordinates[0]['lat']), Decimal(coordinates[0]['lon']))
            else:
                self._coordinates = None

        return self._coordinates

    @property
    def references(self):
        ''' List of URLs of external references (links) on a page.

        May include external links within page that aren't technically cited anywhere.
        '''

        if not getattr(self, '_references', False):
            def add_protocol(url):
                return url if url.startswith('http') else 'http:' + url

            self._references = [
                add_protocol(link['*'])
                for link in self.__continued_query({
                    'prop': 'extlinks',
                    'ellimit': 'max'
                })
            ]

        return self._references

    @property
    def links(self):
        """List of titles of Wikipedia page links on a page.

        Only includes articles from namespace 0,
        meaning no Category, User talk, or other meta-Wikipedia pages.
        """

        if not getattr(self, '_links', False):
            self._links = [
                link['title']
                for link in self.__continued_query({
                    'prop': 'links',
                    'plnamespace': 0,
                    'pllimit': 'max'
                })
            ]

        return self._links

    @property
    def categories(self):
        """List of categories of a page."""

        if not getattr(self, '_categories', False):
            self._categories = [re.sub(r'^Category:', '', x) for x in
                                [link['title']
                                 for link in self.__continued_query({
                                     'prop': 'categories',
                                     'cllimit': 'max'
                                 })
                                 ]]

        return self._categories

    @property
    def sections(self):
        '''List of section titles from the table of contents on the page.'''

        if self._sections:
            return self._sections
        query_params = {
            'action': 'parse',
            'prop': 'sections',
        }
        if self.pageid:
            query_params['pageid'] = self.pageid
        elif self.title:
            query_params['title'] = self.title
            # query_params['titles'] = self.title  # {'warnings': {'main': {'*': 'Unrecognized parameter: titles.'}}
        response = _wiki_request(query_params)
        self._section_headings = [section['line'] for section in response['parse']['sections']]

        self._sections = dict(zip(self._section_headings, list(response['parse']['sections'])))
        for i, (k, v) in enumerate(self._sections.items()):
            v['section_num'] = i
            v['heading'] = k
            v['text'] = self.section(k)

        return self._sections

    def section(self, section_title):
        '''Get the plain text content of a section from `self.sections`.

        Return None if `section_title` isn't found, otherwise returns a whitespace stripped string.

        This is a convenience method that wraps self.content.

        .. warning:: Calling `section` on a section that has subheadings will NOT return
               the full text of all of the subsections. It only gets the text between
               `section_title` and the next subheading, which is often empty.
        '''
        if isinstance(section_title, int):
            section_title = list(self.sections)[section_title]

        section = f"== {section_title} =="
        try:
            index = self.content.index(section) + len(section)
        except ValueError:
            return None

        try:
            next_index = self.content.index("==", index)
        except ValueError:
            next_index = len(self.content)

        return self.content[index:next_index].lstrip("=").strip()

    def to_dataframe(self, re_heading=r'^\s*[=]+ [^=]+ [=]+\s*'):
        """ Split wikitext into paragraphs and return a dataframe with columns for headings (title, h1, h2, h3, ...)

        TODO: create a method or property within a wikipedia.Page class with this function

        >>> from nlpia2_wikipedia.wikipedia import wikipedia as wiki
        >>> page = wiki.get_page('Large language model')
        >>> df = paragraphs_dataframe(page)
        >>> df.head(2)

        """
        paragraphs = [p for p in self.content.split('\n\n')]
        headings = [self.title]
        df_paragraphs = []
        for p in paragraphs:
            p = p.strip()
            p_headings = re.findall(re_heading, p)
            # TODO strip headings from front of p
            # TODO use match instead of findall (only need 1)
            while p_headings:
                h = p_headings[0]
                p = p[len(h):].strip()
                h = h.strip()
                level = len([c for c in h if c == '=']) + 1
                h = h.strip('=').strip()
                headings = headings[:level]
                if len(headings) <= level:
                    headings = headings + [''] * (level - len(headings))
                    headings[level - 1] = h
                p_headings = re.findall(re_heading, p)
            if p:
                p_record = dict(text=p, title=self.title)
                p_record.update({f'h{i}': h for (i, h) in enumerate(headings)})
                df_paragraphs.append(p_record)

        df = pd.DataFrame(df_paragraphs).fillna('')
        df['h_all'] = [
            ': '.join(h for h in row.loc['h0':] if h) for i, row in df.iterrows()]
        return df


@ cache
def languages():
    '''
    List all the currently supported language prefixes (usually ISO language code).

    Can be inputted to `set_lang` to change the Mediawiki that `wikipedia` requests
    results from.

    Returns: dict of <prefix>: <local_lang_name> pairs. To get just a list of prefixes,
    use `wikipedia.languages().keys()`.
    '''
    response = _wiki_request({
        'meta': 'siteinfo',
        'siprop': 'languages'
    })

    languages = response['query']['languages']

    return {
        lang['code']: lang['*']
        for lang in languages
    }


def donate():
    '''
    Open up the Wikimedia donate page in your favorite browser.
    '''
    import webbrowser

    webbrowser.open('https://donate.wikimedia.org/w/index.php?title=Special:FundraiserLandingPage', new=2)


def _wiki_request(params):
    '''
    Make a request to the Wikipedia API using the given search parameters.
    Returns a parsed dict of the JSON response.
    '''
    global RATE_LIMIT_LAST_CALL
    global USER_AGENT

    params['format'] = 'json'
    if 'action' not in params:
        params['action'] = 'query'

    headers = {
        'User-Agent': USER_AGENT
    }

    if RATE_LIMIT and RATE_LIMIT_LAST_CALL and \
            RATE_LIMIT_LAST_CALL + RATE_LIMIT_MIN_WAIT > datetime.now():

        # it hasn't been long enough since the last API call
        # so wait until we're in the clear to make the request

        wait_time = (RATE_LIMIT_LAST_CALL + RATE_LIMIT_MIN_WAIT) - datetime.now()
        time.sleep(int(wait_time.total_seconds()))

    r = requests.get(API_URL, params=params, headers=headers)

    if RATE_LIMIT:
        RATE_LIMIT_LAST_CALL = datetime.now()

    # TODO: find out if json contains spaces at end of sentences or some other sentence separator
    return r.json()
