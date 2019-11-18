from views import index, pickTrace, health, websocket_handler, getTrace, websocket_bytes

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/health', health)
    app.router.add_post('/pickTrace', pickTrace)
    app.router.add_get('/ws', websocket_handler)
    app.router.add_get('/getTrace', getTrace)
    app.router.add_get('/websocketbytes', websocket_bytes)


