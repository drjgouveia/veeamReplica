import time
from modules import syncer, logger
import argparse

logger = logger.setup_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Synchronize folders with specified interval and log file path.")

    # Adding arguments
    parser.add_argument('-s', '--source', type=str, required=True, help='Source folder path')
    parser.add_argument('-d', '--destination', type=str, required=True, help='Destination folder path')
    parser.add_argument('-i', '--interval', type=int, required=True, help='Synchronization interval in seconds')
    parser.add_argument('-l', '--logfile', type=str, required=True, help='Path to the log file')

    # Parsing arguments
    args = parser.parse_args()

    # Accessing arguments
    source_folder = args.source
    destination_folder = args.destination
    sync_interval = args.interval
    log_file_path = args.logfile

    logger.info(f"Source Folder: {source_folder}")
    logger.info(f"Destination Folder: {destination_folder}")
    logger.info(f"Synchronization Interval: {sync_interval} seconds")
    logger.info(f"Log File Path: {log_file_path}")

    while True:
        fs = syncer.Syncer(source_folder, destination_folder)
        fs.sync_destination_filesystem()
        time.sleep(sync_interval)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        logger.error(e)
        logger.error("Please check the paths and try again.")
    except Exception as e:
        logger.error(e)
    except KeyboardInterrupt:
        logger.info("Exiting...")
        exit(0)
