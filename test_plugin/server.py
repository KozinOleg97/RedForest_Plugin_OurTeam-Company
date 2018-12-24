import asyncio


def run(self, host: str = "localhost", port: int = 8000, debug: bool = False):
    """
    start the http server
    :param host: The listening host
    :param port: The listening port
    :param debug: whether it is in debug mod or not
    """
    if debug:
        print("Nougat is listening on http://{}:{}\n".format(host, port))
    self.debug = debug
    loop = asyncio.new_event_loop()
    loop.run_until_complete(self.start_server(host, port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()


run()
