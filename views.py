from aiohttp import web
from aiohttp import WSMsgType
import segyio
import numpy as np
import json
import msgpack

f = segyio.open('C:\\Users\\wades\\workspace\\segy\\CSDS28_1.SGY', ignore_geometry = True)

async def index(request):
    return web.FileResponse('./index.html')

async def health(request):
    return web.Response(text = "is heathy")

async def pickTrace(request):
    enc_data = await request.read()
    print(enc_data)
    print(type(enc_data))
    print(bytearray(enc_data))
    data = msgpack.unpackb(bytearray(enc_data),encoding='utf-8')
    print(data)
    index = int( data['index'] )
    samples = int( data['samples'] )
    offset = int( data['offset'] )
    threshold = int( data['threshold'] )

    sample = np.random.choice(f.trace[index], samples)
    a = []
    
    i = 0
    for x in sample:
        if x > threshold or x < -(threshold):
            x2 = 0
        else:
            x2 = x
        x2 = (x2 / threshold) + offset
        y = i
        a.append({"x": x2,"y": y})
        i += 1

    return web.Response(body = msgpack.packb(a))

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.BINARY:
            print("got some good stuff")
            data = msgpack.unpackb(msg.data,encoding='utf-8')
            print(type(data))
            await ws.send_bytes(msgpack.packb({'temp' : 1}))
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

async def websocket_bytes(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.BINARY:
            data = msgpack.unpackb(msg.data,encoding='utf-8')
            index = int( data['index'] )
            samples = int( data['samples'] )
            offset = int( data['offset'] )
            threshold = int( data['threshold'] )

            a = []
            
            i = 0
            for x in f.trace[index]:
                if x > threshold or x < -(threshold):
                    x2 = 0
                else:
                    x2 = x
                x2 = (x2 / threshold) + offset
                y = i
                a.append({"x": x2,"y": y})
                i += 1
            await ws.send_bytes(msgpack.packb(a))

    return ws

async def getTrace(request):
    ws = web.WebSocketResponse()

    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()

            else:    
                print(msg)

                data = json.loads(str(msg.data))
                index = int( data['index'] )
                samples = int( data['samples'] )
                offset = int( data['offset'] )
                threshold = int( data['threshold'] )

                a = []
                i = 0
                for x in f.trace[index]:
                    if x > threshold or x < -(threshold):
                        x2 = 0
                    else:
                        x2 = x
                    x2 = (x2 / threshold) + offset
                    y = i
                    a.append({"x": x2,"y": y})
                    i += 1
                await ws.send_str(json.dumps(a))

        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
     
    return ws

