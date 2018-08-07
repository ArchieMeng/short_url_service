from flask import Flask, request, redirect, abort, Response
from short_url_manager import ShortUrlManager

app = Flask(__name__)
host_name = 'localhost'
port = 1234
url_manager = None
valid_host = {"127.0.0.1", "localhost"}


@app.route('/')
def hello_world():
    return 'Simple short url service'


@app.route('/<string:key>')
def redirect_to_url(key):
    global url_manager

    # initialize url_manager with configured port number
    if not url_manager:
        url_manager = ShortUrlManager(host_name, port)

    url = url_manager.get_url(key)
    # Todo fix bug: somehow a char "%0A" is added to the tail of url when redirect
    if url:
        return redirect(url, 301)
    else:
        abort(404)


@app.route('/shorten/')
def shorten_url():
    global url_manager
    if request.remote_addr in valid_host:
        if request.args:
            url = request.args.get('url', None)
            if url:
                for key in request.args:
                   if key != 'url':
                       url += '&{}={}'.format(key, request.args[key])

                # initialize url_manager with configured port number
                if not url_manager:
                    url_manager = ShortUrlManager(host_name, port)

                return url_manager.get_short_url(url)
        abort(403, "argument url is needed")
    else:
        # hide this page to invalid remote host
        abort(404)


if __name__ == '__main__':
    app.run(port=port, threaded=True, debug=True)
