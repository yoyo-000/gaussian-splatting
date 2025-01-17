import os
import subprocess
import sys
import time
import shutil

current_directory = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.dirname(current_directory)


def run_command(command, log_file):
    try:
        print(f"Running command: {command}")
        with open(log_file, "a") as log:
            result = subprocess.run(command, shell=True, check=True, stdout=log, stderr=log)
            return True
    except subprocess.CalledProcessError as e:
        with open(log_file, "a") as log:
            log.write(f"Error occurred while running: {command}\n")
            log.write(f"Error: {e}\n")
        return False


def extract_camera_params(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
        parts = last_line.split()
        params = parts[4:]
        return ','.join(params)


def main(data_dir):
    log_file = os.path.join(data_dir, "logfile.log")

    # Clear the log file at the beginning
    with open(log_file, "w") as log:
        log.write("==== Script Start ====\n")
        log.write(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Change to the specified directory
    os.chdir(data_dir)

    # Run prepareData.py
    with open(log_file, "a") as log:
        log.write("\n")
        log.write(f"Running command: prepareData.py\n")
    if not run_command(f"python {utils_dir}\\2.copyInfoAndRun\\prepareData.py {data_dir}", log_file):
        print("Error occurred in prepareData.py, stopping script.")
        return

    camera_file = os.path.join(data_dir, 'sparse/model/cameras.txt')
    camera_param = extract_camera_params(camera_file)

    # Run colmap feature_extractor
    with open(log_file, "a") as log:
        log.write("\n")
        log.write(f"Running command: colmap feature_extractor\n")
    if not run_command(
        f'colmap feature_extractor --database_path database.db --image_path images --ImageReader.camera_model SIMPLE_PINHOLE --ImageReader.camera_params ""{camera_param}""',
        log_file,
    ):
        print("Error occurred in colmap feature_extractor, stopping script.")
        return

    # Run colmap exhaustive_matcher
    with open(log_file, "a") as log:
        log.write("\n")
        log.write(f"Running command: colmap exhaustive_matcher\n")
    if not run_command("colmap exhaustive_matcher --database_path database.db", log_file):
        print("Error occurred in colmap exhaustive_matcher, stopping script.")
        return

    # Run updateCameraID.py
    with open(log_file, "a") as log:
        log.write("\n")
        log.write(f"Running command: updateCameraID.py\n")
    if not run_command(
        f"python {utils_dir}\\2.copyInfoAndRun\\updateCameraID.py --database_path database.db --new_camera_id 1",
        log_file,
    ):
        print("Error occurred in updateCameraID.py, stopping script.")
        return

    # Run colmap point_triangulator
    with open(log_file, "a") as log:
        log.write("\n")
        log.write(f"Running command: colmap point_triangulator\n")
    if not run_command(
        "colmap point_triangulator --database_path database.db --image_path images --input_path sparse/model --output_path sparse/0",
        log_file,
    ):
        print("Error occurred in colmap point_triangulator, stopping script.")
        return

    # replace images.bin
    with open(log_file, "a") as log:
        log.write("\n")
        log.write(f"Running command: replace images.bin\n")
        cameras_extrinsic_file = utils_dir + r"/1.prepareCameraInfo/images.bin"
        replace_file = os.path.join(data_dir, "sparse/0/images.bin")
        shutil.copy(cameras_extrinsic_file, replace_file)

    # Log script completion
    with open(log_file, "a") as log:
        log.write("\n")
        log.write(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Total time taken: {time.time() - start_time} seconds\n")
        log.write("==== Script End ====\n")

    print("Script completed successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run.py <DATA_DIR>")
        sys.exit(1)

    data_dir = sys.argv[1]

    if not os.path.exists(data_dir):
        print(f"Error: Directory {data_dir} does not exist.")
        sys.exit(1)

    start_time = time.time()
    main(data_dir)
