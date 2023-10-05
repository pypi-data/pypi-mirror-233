# pyreq-merger

Minimal tool used for merging 2 requirement files into a single one by either upgrading or downgrading the package versions.

#### Installation

Using pip inside the project directory: `pip install .`
Using pip: `pip install pyreq-merger` 

#### Usage Example

`pyreq file1 file2 --method downgrade --output mynewreq.txt` 

Output is a new requirement file with the specified name in the current working directory.

#### Notes 

For a full list of available parameters use `pyreq -h` 

```pyreq -h
usage: pyreq [-h] [-v] [-m {upgrade,downgrade}] [-o OUTPUT] first_req_file second_req_file

Merge 2 requirement files into a single file, using the specified method.

positional arguments:
  first_req_file        First file containing requirements
  second_req_file       Second file containing requirements

options:
  -h, --help            show this help message and exit
  -v, --version         Displays version then quit
  -m {upgrade,downgrade}, --method {upgrade,downgrade}
                        Merge method, choose from: 'upgrade' or 'downgrade. (default: upgrade)
  -o OUTPUT, --output OUTPUT
                        Output file containing merged requirements. (default: merged_requirements.txt)

Made by https://github.com/mhristodor.```