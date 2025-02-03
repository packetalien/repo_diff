# RepoDiff Tool

A Python script for comparing two Git repositories, detailing files that have been modified, added, removed, or renamed between them.

## Features

- **File Comparison**: Compares files between two Git repositories.
- **Markdown Output**: Generates comparison results in Markdown format for easy reading.
- **Logging**: Logs all operations for debugging and tracking.
- **Software Bill of Materials (SBOM)**: Provides an SBOM for transparency on what software components are used in the comparison.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/packetalien/repo_diff.git
   cd repo_diff
2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt

## Required Packages
- **gitpython**: This script relies on the GitPython package to interact with Git repositories. It must be installed for the script to function correctly.

## Usage
Run the script from the command line:
    ```sh
     python repo_diff.py --repo1 /path/to/repo1 --repo2 /path/to/repo2 [--output output_file.md]

- --repo1: Path to the first repository.
- --repo2: Path to the second repository.
- --output: Optional. Specifies the output file name. Default is repo_diff_results.md.

## Example
    ```sh
    python repo_diff.py --repo1 ./my-first-repo --repo2 ./my-second-repo --output comparison.md

## Output
- Comparison Results: Saved to the specified output file (or default) in Markdown format.
- Log File: repo_diff.log is created in the same directory where the script runs, logging all operations.
- SBOM: sbom.txt detailing the software components involved in the comparison.

## ontributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License
[Creative Commons Legal Code]

## Contact
@packetmonk on X

## Project Link
https://github.com/packetalien/repo_diff