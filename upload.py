import os
import time
import shutil
import subprocess

# Configuration
WATCH_FOLDER = "/home/nziza/Pictures/Webcam"  # Folder to monitor for new pictures from my cheese app
UPLOADED_FOLDER = "./uploaded"  # Folder to move uploaded pictures
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
ATTRIBUTE = "imageFile"  # Key attribute for the curl command
UPLOAD_INTERVAL = 30  # Time to wait before uploading each file (in seconds)

# Ensure the uploaded folder exists
os.makedirs(UPLOADED_FOLDER, exist_ok=True)

def upload_image(file_path):
    """Uploads an image using curl and returns the success status."""
    try:
        command = [
            "curl", "-X", "POST",
            "-F", f"{ATTRIBUTE}=@{file_path}",
            UPLOAD_URL
        ]
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)
        # Check if the upload was successful (HTTP status code 200 is assumed success)
        if result.returncode == 0:
            print(f"Successfully uploaded: {file_path}")
            return True
        else:
            print(f"Failed to upload: {file_path}\nError: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")
        return False

def monitor_and_upload():
    """Monitors the folder, uploads pictures, and moves uploaded files."""
    while True:
        # Get a list of all files in the watch folder
        files = [f for f in os.listdir(WATCH_FOLDER) if os.path.isfile(os.path.join(WATCH_FOLDER, f))]

        for file_name in files:
            file_path = os.path.join(WATCH_FOLDER, file_name)

            # Upload the file
            if upload_image(file_path):
                # Move the file to the uploaded folder
                shutil.move(file_path, os.path.join(UPLOADED_FOLDER, file_name))

        # Wait before the next iteration
        time.sleep(UPLOAD_INTERVAL)

if __name__ == "__main__":
    print("Starting folder monitoring...")
    monitor_and_upload()
