# VEEAM Replicator

## Description

This is a simple script that will replicate the contents of a folder (source) to a replica (destination).

## Usage

```bash
python3 main.py --source /path/to/source --destination /path/to/destination --interval 60 --logfile /path/to/logfile
```

## Arguments

- `--source`: The source folder to replicate
- `--destination`: The destination folder to replicate to
- `--interval`: The interval in seconds to check for changes in the source folder
- `--logfile`: The path to the log file
- `--help`: Show the help message

## Requirements

- Python 3.6 or higher

## Installation

1. Clone the repository
2. Install the requirements with `pip install -r requirements.txt`
3. Run the script with the usage command
4. Enjoy!

## Testing

To run the tests, run the following command:

```bash
pytest
```