from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

# openssl req -x509 -newkey rsa:4096 -sha256 \\n-nodes -keyout server.key -out server.crt \\n-subj "/CN=example.com" -days 3650
# 上のコマンドを実施する


def run(host, port, ctx, handler):
    server = HTTPServer((host, port), handler)
    server.socket = ctx.wrap_socket(server.socket)
    print('Server Starts - %s:%s' % (host, port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print('Server Stops - %s:%s' % (host, port))


if __name__ == '__main__':
    host = 'localhost'
    port = 8000

    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain('server.crt', keyfile='server.key')
    ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    handler = SimpleHTTPRequestHandler

    run(host, port, ctx, handler)