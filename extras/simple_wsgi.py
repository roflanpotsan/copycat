def request_logger(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    query_string = environ['QUERY_STRING']
    content_length = int(environ.get('CONTENT_LENGTH', '0'))
    post_data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''

    log_message = f'{method} {path}?{query_string} {post_data.decode()}'
    print(log_message)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    response_body = b'OK\n'

    start_response(status, headers)
    return [response_body]
