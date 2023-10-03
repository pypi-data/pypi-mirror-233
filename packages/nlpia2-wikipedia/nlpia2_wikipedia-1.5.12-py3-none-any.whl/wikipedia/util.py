from __future__ import print_function, unicode_literals

import sys
import functools

import re
import pandas as pd

RE_HEADING = r'^\s*[=]+ [^=]+ [=]+\s*'


def debug(fn):
    def wrapper(*args, **kwargs):
        print(fn.__name__, 'called!')
        print(sorted(args), tuple(sorted(kwargs.items())))
        res = fn(*args, **kwargs)
        print(res)
        return res
    return wrapper


class cache(object):
    """ Decorator to memoize a Python function """

    def __init__(self, fn):
        self.fn = fn
        self._cache = {}
        functools.update_wrapper(self, fn)

    def __call__(self, *args, **kwargs):
        key = str(args) + str(kwargs)
        if key in self._cache:
            ret = self._cache[key]
        else:
            ret = self._cache[key] = self.fn(*args, **kwargs)

        return ret

    def clear_cache(self):
        self._cache = {}


# from http://stackoverflow.com/questions/3627793/best-output-type-and-encoding-practices-for-repr-functions
def stdout_encode(u, default='UTF8'):
    encoding = sys.stdout.encoding or default
    if sys.version_info > (3, 0):
        return u.encode(encoding).decode(encoding)
    return u.encode(encoding)


""" Parsers for wikitext (page content) downloaded using Wikipedia's API with the nlpia2_wikipedia package """


def page_to_dataframe(page):
    """ Split wikitext into paragraphs and return a dataframe with columns for headings (title, h1, h2, h3, ...)

    TODO: create a method or property within a wikipedia.Page class with this function

    >>> from nlpia2_wikipedia.wikipedia import wikipedia as wiki
    >>> page = wiki.page('Large language model')
    >>> df = page_to_dataframe(page)
    >>> df.head(2)

    """
    paragraphs = [p for p in page.content.split('\n\n')]
    headings = [page.title]
    df_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        p_headings = re.findall(RE_HEADING, p)
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
                p_headings = re.findall(RE_HEADING, p)
        if p:
            p_record = dict(text=p, title=page.title)
            p_record.update({f'h{i}': h for (i, h) in enumerate(headings)}) 
            df_paragraphs.append(p_record)
    
    df = pd.DataFrame(df_paragraphs).fillna('')
    df['h_all'] = [
        ': '.join(h for h in row.loc['h0':] if h) for i, row in df.iterrows()]
    return df
    


