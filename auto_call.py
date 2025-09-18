import subprocess
import time
import threading
import sys

# Global event to signal threads to stop
stop_event = threading.Event()

def run_adb_command(device_serial, command):
    """Executes an ADB command for a specific device."""
    full_command = f"adb -s {device_serial} {command}"
    try:
        # Add a timeout to subprocess calls to prevent indefinite blocking
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True, check=True, timeout=60) 
        print(f"Device {device_serial}: {command} -> {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error on device {device_serial} with command '{command}': {e.stderr.strip()}")
        return None
    except subprocess.TimeoutExpired:
        print(f"Command timed out for device {device_serial}: '{command}'")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for device {device_serial} with command '{command}': {e}")
        return None

def get_connected_devices():
    """Lists all connected ADB devices and returns their serials."""
    output = run_adb_command(None, "devices")
    if not output:
        return []
    
    devices = []
    lines = output.splitlines()
    for line in lines:
        if "\tdevice" in line:
            serial = line.split("\t")[0]
            devices.append(serial)
    return devices

def make_call(device_serial, phone_number, call_duration, wait_time_after_hangup, num_calls):
    """Performs a series of calls on a single device."""
    print(f"Starting call sequence on device: {device_serial}")
    for i in range(num_calls):
        if stop_event.is_set():
            print(f"Device {device_serial}: Interruption signal received. Stopping call sequence.")
            break

        print(f"Device {device_serial}: Call {i+1}/{num_calls}")
        
        # Dial the number
        dial_command = f"shell am start -a android.intent.action.CALL -d tel:{phone_number}"
        if run_adb_command(device_serial, dial_command) is None:
            print(f"Device {device_serial}: Failed to initiate call. Skipping to next call attempt.")
            continue
        
        print(f"Device {device_serial}: Calling {phone_number} for {call_duration} seconds...")
        # Use stop_event.wait() for interruptible sleep
        if stop_event.wait(call_duration):
            print(f"Device {device_serial}: Interruption signal received during call. Hanging up and stopping.")
            run_adb_command(device_serial, "shell input keyevent KEYCODE_ENDCALL") # Attempt to hang up
            break
        
        # Hang up
        hangup_command = "shell input keyevent KEYCODE_ENDCALL"
        if run_adb_command(device_serial, hangup_command) is None:
            print(f"Device {device_serial}: Failed to hang up call. Proceeding to next call attempt.")
            # Even if hangup fails, we still wait to avoid rapid redialing
        
        print(f"Device {device_serial}: Call sequence step completed. Waiting for {wait_time_after_hangup} seconds before next call.")
        if i < num_calls - 1: # Don't wait after the last call
            if stop_event.wait(wait_time_after_hangup):
                print(f"Device {device_serial}: Interruption signal received during wait. Stopping.")
                break
    print(f"Finished call sequence on device: {device_serial}")

def main():
    # --- User-defined parameters ---
    PHONE_NUMBER = "922"  # The phone number to dial
    CALL_DURATION = 50          # Duration of each call in seconds
    WAIT_TIME_AFTER_HANGUP = 5  # Wait time after hanging up before redialing in seconds
    NUM_CALLS = 300               # Number of calls to make per device
    
    # List of specific device serials (names) to use.
    # If this list is empty, the script will attempt to use all currently connected devices.
    # You can specify up to 8 devices as requested.
    SPECIFIC_DEVICES = [
        "BS88523AA1430400069", # Replace with your actual device serial
        "BS88532AA1533100678", 
    ] 

    all_connected_devices = get_connected_devices()
    if not all_connected_devices:
        print("No ADB devices found. Please ensure devices are connected and ADB is authorized.")
        return

    devices_to_use = []
    if SPECIFIC_DEVICES:
        for dev in SPECIFIC_DEVICES:
            if dev in all_connected_devices:
                devices_to_use.append(dev)
            else:
                print(f"Warning: Specified device '{dev}' not found among connected devices.")
    else:
        # If SPECIFIC_DEVICES is empty, use all connected devices
        devices_to_use = all_connected_devices

    if not devices_to_use:
        print("No valid devices selected for dialing. Exiting.")
        return

    print(f"Selected devices for dialing: {devices_to_use}")

    threads = []
    for device_serial in devices_to_use:
        thread = threading.Thread(target=make_call, args=(device_serial, PHONE_NUMBER, CALL_DURATION, WAIT_TIME_AFTER_HANGUP, NUM_CALLS))
        threads.append(thread)
        thread.start()

    try:
        while any(thread.is_alive() for thread in threads):
            time.sleep(1) # Keep main thread alive to catch KeyboardInterrupt
    except KeyboardInterrupt:
        print("\nMain thread: KeyboardInterrupt received. Signaling all threads to stop.")
        stop_event.set() # Signal all threads to stop
    finally:
        for thread in threads:
            thread.join() # Wait for all threads to finish
        print("All parallel dialing tasks completed or interrupted gracefully.")

if __name__ == "__main__":
    main()
