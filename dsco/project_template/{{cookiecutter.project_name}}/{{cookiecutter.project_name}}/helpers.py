import sqlparse

from pygments import highlight
from pygments.lexers.sql import SqlLexer
from pygments.formatters.html import HtmlFormatter
import sqlparse

import IPython.display as dis


def fsql(sql_, reindent=False):
    """Format text as an SQL statement"""
    return sqlparse.format(sql_, reindent=reindent, keyword_case="upper")


def printsql(sql_string):
    """Prints an SQL statement with syntax highlighting"""
    style_string = """
    <style>
    {pygments_css}
    </style>
    """

    dis.display(
        dis.HTML(
            style_string.format(
                pygments_css=HtmlFormatter().get_style_defs(".highlight")
            )
        )
    )

    dis.display(dis.HTML(data=highlight(sql_string, SqlLexer(), HtmlFormatter())))


