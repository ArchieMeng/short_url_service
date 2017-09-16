import short_url_service

if __name__ == "__main__":
    short_url_service.app.run(
        host='0.0.0.0',
        port=short_url_service.port,
        threaded=True,
        debug=False
    )