""" Parsers for wikitext (page content) downloaded using Wikipedia's API with the nlpia2_wikipedia package """
import re
import pandas as pd

RE_HEADING = r'^\s*[=]+ [^=]+ [=]+\s*'



