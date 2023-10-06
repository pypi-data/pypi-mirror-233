import textwrap
from wsgiref.types import StartResponse
from wsgiref.types import WSGIEnvironment

html = textwrap.dedent('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8"/>
    <title>Hello, World!</title>
    </head>
    <body>
    <h1>Congratulations</h1>
    <p>Your site is configured correctly.</p>
    <p>Time to edit the entries in the [wsgi] section of the
    config.toml file to point to your Python application.</p>
    </body>
    </html>
''')[1:-1]


def app_hello_world(
        _environ: WSGIEnvironment,
        start_response: StartResponse,
) -> list[bytes]:
    html_as_bytes = html.encode('utf-8')
    start_response(
        '200 OK',
        [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html_as_bytes))),
        ],
    )
    return [html_as_bytes]
