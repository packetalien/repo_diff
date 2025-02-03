#!/usr/bin/env python3

"""
RepoDiff - Compare Two Git Repositories

This script compares two Git repositories, detailing files that have been modified, 
added, removed, or renamed between them. It outputs results in Markdown format, logs 
all operations, and creates a Software Bill of Materials (SBOM).

Usage:
    repo_diff.py --repo1 PATH_TO_REPO1 --repo2 PATH_TO_REPO2 [--output OUTPUT_FILE]

Arguments:
    --repo1 PATH    Path to the first repository.
    --repo2 PATH    Path to the second repository.
    --output FILE   Path to save the output file (default: 'repo_diff_results.md').

Dependencies:
    - gitpython (install with: pip install gitpython)

Example:
    python repo_diff.py --repo1 ./repo1 --repo2 ./repo2 --output comparison.md
"""

import argparse
import logging
import os
from git import Repo
import git

# Set up logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repo_diff.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file,
    filemode='w'
)
logger = logging.getLogger(__name__)

def read_file(repo, path):
    """
    Read the content of a file from the repository's HEAD.

    :param repo: GitPython Repo object
    :param path: Path to the file
    :return: Content of the file as string
    """
    logger.debug(f"Reading file: {path}")
    return repo.git.show(f'HEAD:{path}')

def compare_repos(repo1_path, repo2_path, output_file):
    """
    Compare two Git repositories, log operations, and write results to a file.

    :param repo1_path: Path to the first repository
    :param repo2_path: Path to the second repository
    :param output_file: Path to the output file for results
    """
    logger.info(f"Starting comparison of {repo1_path} and {repo2_path}")
    
    repo1 = Repo(repo1_path)
    repo2 = Repo(repo2_path)

    logger.debug(f"Checking out 'main' branch for {repo1_path}")
    repo1.git.checkout('main')
    logger.debug(f"Checking out 'main' branch for {repo2_path}")
    repo2.git.checkout('main')

    # Extract file paths from both repos
    files1 = [entry[0] for entry in repo1.index.entries.items()]
    files2 = [entry[0] for entry in repo2.index.entries.items()]

    diffs = {
        'modified': [],
        'added': [],
        'removed': [],
        'renamed': []
    }

    # Compare files
    for file in set(files1 + files2):
        if file in files1 and file in files2:
            try:
                content1 = read_file(repo1, file)
                content2 = read_file(repo2, file)
                if content1 != content2:
                    diffs['modified'].append(file)
            except git.exc.GitCommandError:
                logger.warning(f"File {file} not found in HEAD for comparison")
                continue
        elif file in files1:
            diffs['removed'].append(file)
        else:
            diffs['added'].append(file)

    # Check for renames
    for file in diffs['removed']:
        for added_file in diffs['added']:
            try:
                content1 = read_file(repo1, file)
                content2 = read_file(repo2, added_file)
                if content1 == content2:
                    diffs['renamed'].append((file, added_file))
                    diffs['added'].remove(added_file)
                    diffs['removed'].remove(file)
                    break
            except git.exc.GitCommandError:
                logger.warning(f"File {file} or {added_file} not found in HEAD for rename detection")
                continue

    # Write results to file in Markdown format
    logger.info(f"Writing results to {output_file}")
    with open(output_file, 'w') as f:
        f.write("# Repository Comparison Results\n\n")

        f.write("## Modified Files\n")
        for file in diffs['modified']:
            f.write(f"- {file}\n")

        f.write("\n## Added Files\n")
        for file in diffs['added']:
            f.write(f"- {file}\n")

        f.write("\n## Removed Files\n")
        for file in diffs['removed']:
            f.write(f"- {file}\n")

        f.write("\n## Renamed Files\n")
        for old, new in diffs['renamed']:
            f.write(f"- {old} -> {new}\n")

    print(f"Comparison results saved to {output_file}")
    logger.info("Comparison completed")

    # Software Bill of Materials
    sbom_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sbom.txt')
    with open(sbom_file, 'w') as sbom:
        sbom.write("Software Bill of Materials:\n")
        sbom.write(f"- Python: {'.'.join(map(str, sys.version_info[:3]))}\n")
        sbom.write(f"- GitPython: {git.__version__}\n")
        sbom.write(f"- Script: {os.path.basename(__file__)}\n")
        sbom.write(f"- Repositories compared: {repo1_path}, {repo2_path}\n")
        sbom.write(f"- Output file: {output_file}\n")
        sbom.write(f"- Log file: {log_file}\n")
    
    logger.info(f"SBOM written to {sbom_file}")

if __name__ == "__main__":
    import sys
    
    parser = argparse.ArgumentParser(description="Compare two Git repositories.")
    parser.add_argument("--repo1", required=True, help="Path to the first repository")
    parser.add_argument("--repo2", required=True, help="Path to the second repository")
    parser.add_argument("--output", default="repo_diff_results.md", help="Path to save the output file")

    args = parser.parse_args()
    
    compare_repos(args.repo1, args.repo2, args.output)