import short_url_service
from gevent.pywsgi import WSGIServer

if __name__ == "__main__":
    # Flask built-in method
    # short_url_service.app.run(
    #     host='0.0.0.0',
    #     port=short_url_service.port,
    #     threaded=True,
    #     debug=False
    # )

    # gevent method
    http_server = WSGIServer(('localhost', 1234), short_url_service.app)
    http_server.serve_forever()