# asko-analyzer
A very specific script made to read a CSV containing daily data for the company ASKO, and create a new CSV file with the monthly sums.

The script is written voluntarily for a group of electro engineering students at NTNU Trondheim to aid their Bachelor thesis.

## Notes about the code
- As mentioned, the code is very specialized, and everything except the toolboxes are mostly irrelevant to other projects
- The code quality isn't great, the focus was to create the program quickly (you may notice inconsistencies in naming conventions and very ineffective code)
- You may notice that the semi-colon separator is used instead of the comma separator; this is because Excel files are separated by semi-colon
- The CSV files used are test files written by me; it does not contain any data from ASKO, it simply follows the same format

## Requirements
For this project, I used
- Python 3.9.2
- NumPy 1.20.1 (only used for the NumPy arrays which is not important at all, you may omit it)
