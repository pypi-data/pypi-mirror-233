import sys
import threading
import time
import uuid
from enum import Enum
from typing import Dict

import zmq

from isyntax_backend.isyntax_reader import IsyntaxSlide
from isyntax_backend.timed_cache import TimedCache


class LogIssuer(str, Enum):
    MASTER = "Master"
    WORKER = "Worker"
    CACHE = "Cache"


def tprint(issuer: LogIssuer, msg: str, verbose_logging: bool = True):
    """like print, but won't get newlines confused with multiple threads"""
    if verbose_logging:
        sys.stdout.write(f"{issuer} | {msg}\n")
        sys.stdout.flush()


class BackendServer(threading.Thread):
    """BackendServer"""

    port = 5556

    def __init__(self):
        tprint(LogIssuer.MASTER, "Initializing backend parent worker...")
        threading.Thread.__init__(self)

    def run(self):
        # Initialization
        context: zmq.Context = zmq.Context()
        incoming_router_socket: zmq.Socket = context.socket(zmq.ROUTER)
        incoming_router_socket.bind(f"tcp://*:{self.port}")
        tprint(LogIssuer.MASTER, f"Zeromq server binding to 'tcp://*:{self.port}'")

        broker_socket: zmq.Socket = context.socket(zmq.ROUTER)
        broker_socket.identity = f"broker_%{uuid.uuid4()}".encode("ascii")
        broker_socket.bind("inproc://backend")

        def callback_kill_proc(worker_socket: zmq.Socket):
            tprint(
                LogIssuer.CACHE, f"Dispatching kill signal to {worker_socket.identity}"
            )
            broker_socket.send(worker_socket.identity, zmq.SNDMORE)
            broker_socket.send_string("SIGNAL", zmq.SNDMORE)
            broker_socket.send_json({"req": "KILL_PROC"})

        worker_socket_cache = TimedCache(
            timeout_seconds=600, callback_kill_proc=callback_kill_proc
        )

        while True:
            client_id = incoming_router_socket.recv_string()
            req_msg = incoming_router_socket.recv_json()
            # tprint(LogIssuer.WORK_DISPATCHER, f"Received request [{req_msg}] from client {client_id}")

            mapped_filepath = f"/data{req_msg['filepath']}"
            worker_socket: zmq.Socket = worker_socket_cache.get(
                key=mapped_filepath, default=None
            )
            if worker_socket is None:
                tprint(
                    LogIssuer.MASTER,
                    f"Cache miss. Creating new thread and socket for filepath {mapped_filepath}",
                )
                worker_socket: zmq.Socket = context.socket(zmq.DEALER)
                worker_socket.identity = f"{mapped_filepath}_%{uuid.uuid4()}".encode(
                    "ascii"
                )
                worker_socket.connect("inproc://backend")

                slide_worker = SlideWorker(
                    mapped_filepath=mapped_filepath, socket=worker_socket
                )
                slide_worker.start()
                worker_socket_cache.set(key=mapped_filepath, value=worker_socket)

            broker_socket.send(worker_socket.identity, zmq.SNDMORE)
            broker_socket.send_string(client_id, zmq.SNDMORE)
            broker_socket.send_json(req_msg)

            # route response to frontend
            response = broker_socket.recv_multipart()
            response.pop(0)

            tprint(
                LogIssuer.MASTER,
                f"Forwarding message to {response[0]}: {response[1][:100]}...",
            )

            incoming_router_socket.send_multipart(response)


class SlideWorker(threading.Thread):
    """SlideWorker"""

    def __init__(self, mapped_filepath: str, socket: zmq.Socket):
        threading.Thread.__init__(self)
        self.mapped_filepath = mapped_filepath
        self.slide_instance = IsyntaxSlide(self.mapped_filepath)
        self.socket = socket
        tprint(LogIssuer.WORKER, f"Initialized worker for slide {mapped_filepath}")

    def run(self):
        tprint(LogIssuer.WORKER, f"Start listening on socket {self.socket}")
        while True:
            client_id = self.socket.recv_string()
            req_msg = self.socket.recv_json()
            tprint(LogIssuer.WORKER, f"Received request from {client_id}: {req_msg}")
            if client_id == "SIGNAL" and req_msg["req"] == "KILL_PROC":
                tprint(
                    LogIssuer.WORKER,
                    f"Received kill signal. Closing socket connection for {self.mapped_filepath}...",
                )
                self.socket.close()
                break
            elif req_msg["req"] == "verification":
                self.__send_json(
                    worker=self.socket,
                    client_id=client_id,
                    rep_msg=self.slide_instance.result,
                )
            elif req_msg["req"] == "get_info":
                self.__send_json(
                    worker=self.socket,
                    client_id=client_id,
                    rep_msg=self.slide_instance.get_info(),
                )
            elif req_msg["req"] == "LABEL":
                self.__send(
                    worker=self.socket,
                    client_id=client_id,
                    rep_msg=self.slide_instance.get_label(),
                )
            elif req_msg["req"] == "MACRO":
                self.__send(
                    worker=self.socket,
                    client_id=client_id,
                    rep_msg=self.slide_instance.get_macro(),
                )
            elif req_msg["req"] == "get_region":
                resp, image_array, width, height = self.slide_instance.get_region(
                    req_msg["level"],
                    req_msg["start_x"],
                    req_msg["start_y"],
                    req_msg["size_x"],
                    req_msg["size_y"],
                )
                self.__send_array_response(
                    worker=self.socket,
                    client_id=client_id,
                    resp=resp,
                    image_array=image_array,
                    width=width,
                    height=height,
                )
            elif req_msg["req"] == "get_tile":
                resp, image_array, width, height = self.slide_instance.get_tile(
                    req_msg["level"], req_msg["tile_x"], req_msg["tile_y"]
                )
                self.__send_array_response(
                    worker=self.socket,
                    client_id=client_id,
                    resp=resp,
                    image_array=image_array,
                    width=width,
                    height=height,
                )
            elif req_msg["req"] == "get_thumbnail":
                resp, image_array, width, height = self.slide_instance.get_thumbnail(
                    req_msg["max_x"], req_msg["max_y"]
                )
                self.__send_array_response(
                    worker=self.socket,
                    client_id=client_id,
                    resp=resp,
                    image_array=image_array,
                    width=width,
                    height=height,
                )
            else:
                req = req_msg["req"]
                self.__send_json(
                    worker=self.socket,
                    client_id=client_id,
                    rep_msg={
                        "rep": "error",
                        "status_code": 422,
                        "detail": f"Invalid request ({req})",
                    },
                )

        self.slide_instance.close()

    def __send_json(self, worker: zmq.Socket, client_id: str, rep_msg: Dict):
        worker.send_string(client_id, zmq.SNDMORE)
        worker.send_json(rep_msg)

    def __send(self, worker: zmq.Socket, client_id: str, rep_msg):
        worker.send_string(client_id, zmq.SNDMORE)
        worker.send(rep_msg)

    def __send_array_response(
        self, worker: zmq.Socket, client_id: str, resp: Dict, image_array, width, height
    ):
        if resp["rep"] == "success":
            rep_msg = {
                "rep": "success",
                "status_code": 200,
                "detail": "",
                "width": width,
                "height": height,
            }
            rep_payload = image_array
        else:
            rep_msg = resp
            rep_payload = b""

        worker.send_string(client_id, zmq.SNDMORE)
        worker.send_json(rep_msg, zmq.SNDMORE)
        worker.send(rep_payload)


if __name__ == "__main__":
    server = BackendServer()
    server.start()
    time.sleep(1)

    server.join()
