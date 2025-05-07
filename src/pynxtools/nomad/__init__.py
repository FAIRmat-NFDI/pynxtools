import multiprocessing
import uvicorn
import atexit
import os
import sys

server_process = None

def start_ontology_service():
    """Start the superclasses FastAPI server."""
    uvicorn.run("pynxtools.nomad.ontology_service:app", host="0.0.0.0", port=8089, reload=False)

def stop_ontology_service():
    """Stop the superclasses FastAPI server."""
    global server_process
    if server_process is not None and server_process.is_alive():
        print("Superclasses server shutdown requested.")
        server_process.terminate()  # Terminate the process
        server_process.join()       # Wait for the process to finish
    server_process = None
        

def run_ontology_service():
    """Run the superclasses FastAPI server in a separate process."""
    global server_process
    if server_process is None or not server_process.is_alive():
        server_process = multiprocessing.Process(target=start_ontology_service)
        server_process.start()
        atexit.register(stop_ontology_service) 
         
# Ensure the server stops when the main program exits
if os.getenv("LAUNCH_CONTEXT") == "app":
    run_ontology_service()
else:
    print("Ontology service not started: LAUNCH_CONTEXT is not 'app'.")