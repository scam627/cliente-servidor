import zmq
import hashlib

CHUNK_SIZE = 35000000

ctx = zmq.Context()

router = ctx.socket(zmq.ROUTER)
router.bind("tcp://*:6000")

def download():
    h = hashlib.sha256()
    size = 0        
    total = 0
    segments = 0
    for name_segment in list_segment_file:
        file = open(name_segment, "rb")
        data = file.read()
        h.update(data)
        segments += 1
        size = len(data)
        total += size
        print("%i segments send, %i bytes" % (segments, total))
        router.send_multipart([identity, data, h.digest()])
    router.send_multipart([identity, b"", h.digest()])
    print("Complete process")

def upload():
    chunks = 0
    total = 0
    check = hashlib.sha256()
    while True:
        try:
            identity, chunk, h = router.recv_multipart()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                print(e.errno)   # shutting down, quit
            else:
                raise
        chunks += 1
        size = len(chunk)
        total += size
        if size == 0:
            print("Download complete")
            break
        else:
            check.update(chunk)
            if check.digest() != h:
                break
            filename =  "storage-server/" + check.hexdigest()
            list_segment_file.append(filename)
            outfile = open(filename, "wb")
            outfile.write(chunk)
    print("%i chunks received, %i bytes" % (chunks, total))

print("Listening on port 6000")

list_segment_file = []

while True:
    try:
        identity, command = router.recv_multipart()
    except zmq.ZMQError as e:
        if e.errno == zmq.ETERM:
            print(e.errno)
        else:
            raise
    print("Client connected")
    assert command == b"download" or command == b"upload"
    if command == b"download":
        download()
    else:
        list_segment_file = []
        upload()
