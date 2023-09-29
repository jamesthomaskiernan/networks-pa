## How to run with ZMQ + Flatbuffers

1. Open zmq_flatbuffers directory.
2. Inside serialize.py, update the path to your flatbuffers python module. It will be located wherever you built flatbuffers. By default, it will be assumed to be in `/home/user/Apps/flatbuffers/python`.
3. If the flatbuffer data for python are not already generated and inside the `PA` directory, run `flatc -p schema.fbs` to generate them.
4. Start the grocery server with `python3 grocery_server.py`. You may specify interface with `-i` (default *), and port with `-p` (default 4444 for Grocery Server)
5. Start the health server with `python3 health_status_server.py`. You may specify interface with `-i` (default *), and port with `-p` (default 5555 for Health Status Server)
6. Start the fridge client with `python3 refrigerator.py`. You may specify address with `-a` (default `127.0.0.1`), ports to connect to with with `-p` (defaults are 5555 and 4444), and number of iterations to run with `-i` (default 10).

## Teamwork (who did what)

### Milestone 1
- James: grocery_server.py, health_status_server.py, refrigerator.py, most serialization/deserialization
- Jovian: schema.fbs, helped with serialization/deserialization, reformatted classes to be better, added args to use when running

## Plots of results

