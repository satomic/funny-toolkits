from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

host = ('0.0.0.0', 8888)

global tps_counter,tps
tps_counter = 0
tps = 0

# global tps

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # global tps
        tps_contents = "hello from tps!"
        self.wfile.write(tps_contents.encode())
        global tps_counter
        tps_counter += 1

class ThreadGetCount(threading.Thread):
    def __init__(self, threadID, name, period):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.period = period

    def run(self):
        print("count thread start：" + self.name)
        global tps_counter
        while True:
            tps_counter = 0
            time.sleep(self.period)
            tps = tps_counter
            tps_str = "request_tps=%s" % tps
            print (tps_str)
            with open("/tmp/metric", "w") as f:
                f.write(tps_str)


class ThreadHttp(threading.Thread):
    def __init__(self, threadID, name,):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("http thread start：" + self.name)
        server = HTTPServer(host, Resquest)
        print("Starting server, listen at: %s:%s" % host)
        server.serve_forever()


if __name__ == '__main__':
    thread_tps_counter = ThreadGetCount(1, "tps_counter", 1)
    thread_http = ThreadHttp(1, "http")
    thread_tps_counter.start()
    thread_http.start()
    thread_tps_counter.join()
    thread_http.join()

    # server = HTTPServer(host, Resquest)
    # print("Starting server, listen at: %s:%s" % host)
    # server.serve_forever()

