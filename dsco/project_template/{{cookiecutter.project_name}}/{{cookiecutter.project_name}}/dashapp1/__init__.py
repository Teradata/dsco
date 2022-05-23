"""Integrate Dash into a Flask server

In the section dash_app.config.update we are setting the requests_pathname_prefix
to match the mount point of our webapp + url_base_pathname. To run this manually
with uwsgi you can use:

uwsgi --socket 0.0.0.0:5000 --protocol=http --mount /webapp=wsgi:app --manage-script-name
"""
from dash import Dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html


def add_dash(server):
    """Populates page with previews of datasets."""
    dash_app = Dash(
        server=server, 
        requests_pathname_prefix="/webapp/dash/",
        routes_pathname_prefix="/dash/",
    )

    # Create layout
    dash_app.layout = html.Div(
        children=[
            html.H1(children="Hello Dash"),
            html.Div(
                children="""
        Dash: A web application framework for Python.
    """
            ),
            dcc.Graph(
                id="example-graph",
                figure={
                    "data": [
                        {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
                        {
                            "x": [1, 2, 3],
                            "y": [2, 4, 5],
                            "type": "bar",
                            "name": u"Montréal",
                        },
                    ],
                    "layout": {"title": "Dash Data Visualization"},
                },
            ),
        ]
    )

    return dash_app.server
