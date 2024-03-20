import subprocess
import signal
import os
import time

basepath = os.path.dirname(os.path.abspath(__file__)) + "/"

python_scripts = [
    f"{basepath}order_scheduler.py",
    f"{basepath}callback_scheduler.py",
    f"{basepath}order_management_system.py",
    #f"{basepath}LinkCreation.py",
    f"{basepath}qr_code_website.py",
    f"{basepath}recipe_service.py",
    f"{basepath}simulator.py",
    f"{basepath}shoutout.py",
    f"{basepath}analysing_logs.py",
    f"{basepath}order_store.py",
]

processes = []



# Function to start Python scripts as subprocesses
def start_python_scripts(scripts):
    for script in scripts:
        print(f"Starting {script}")
        # Start the script and store the process object
        process = subprocess.Popen(["python", script])
        processes.append(process)


# Function to kill all the subprocesses
def kill_python_scripts():
    for process in processes:
        print(f"Terminating PID: {process.pid}")
        process.terminate()  # Sends SIGTERM
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(f"Force killing PID: {process.pid}")
            process.kill()  # Force kill if not terminated after timeout


# Register the kill function to SIGINT and SIGTERM
def register_exit_signals():
    signal.signal(signal.SIGINT, lambda signum, frame: kill_python_scripts())
    signal.signal(signal.SIGTERM, lambda signum, frame: kill_python_scripts())


def main():
    # Register the signal handlers
    register_exit_signals()

    # Start the Python scripts
    start_python_scripts(python_scripts)

    # Wait for all subprocesses to finish
    try:
        while True:
            # Check if all subprocesses have finished
            if all(p.poll() is not None for p in processes):
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        # Handle Ctrl+C
        pass
    finally:
        # Ensure all subprocesses are terminated
        kill_python_scripts()


if __name__ == "__main__":
    main()
