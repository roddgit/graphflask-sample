""" app.py """
from flask import Flask, Response
from flask_graphql import GraphQLView

from database import client
from schema import schema
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})



app = Flask(__name__)


def index():
    with open("sample.txt", "r") as file:
        content = file.read()
    
    return Response(content, mimetype='text/plain')

app.add_url_rule('/', 'index', index)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

