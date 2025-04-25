import multiprocessing
import uvicorn
import atexit
import os

server_process = None

def start_superclasses_server():
    """Start the superclasses FastAPI server."""
    uvicorn.run("pynxtools.nomad.superclasses_server:app", host="0.0.0.0", port=8089, reload=False)

def stop_superclasses_server():
    """Stop the superclasses FastAPI server."""
    global server_process
    if server_process is not None and server_process.is_alive():
        print("Superclasses server shutdown requested.")
    server_process = None
        

def run_superclasses_server():
    """Run the superclasses FastAPI server in a separate process."""
    global server_process
    if server_process is None or not server_process.is_alive():
        server_process = multiprocessing.Process(target=start_superclasses_server)
        server_process.start()
        atexit.register(stop_superclasses_server)  # Ensure the server stops when the main program exits

# Ensure the server is started when the module is imported
run_superclasses_server()