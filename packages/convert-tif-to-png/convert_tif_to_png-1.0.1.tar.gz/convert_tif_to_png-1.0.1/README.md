# TIF to PNG Image Converter

## Introduction

This Python script converts TIF images to PNG format. It allows for resizing the images to various predefined sizes (Original, 4K, 2K) and works either on a directory or individual files. It also allows for renaming the converted files based on a regex pattern extracted from the original file name.

## Requirements

- Python 3.5+
- PIL (Pillow) library

## Installation

Install the convert-tif-to-png tool via pip:

```bash
pip install convert-tif-to-png
```

Also, ensure you have the required Pillow library:

```bash
pip install Pillow
```

## Usage

### Command Line Options

| Option | Description |
| --- | --- |
| `--dir` | Path to directory containing TIF files to convert. |
| `--file` | Path to individual TIF file(s) to convert. |
| `--pattern` | Regex pattern to name converted files, extracted from the original file name.
| `--size` | Resize images to one of the following sizes: `original`, `4k`, `2k`. |
| `--log` | Log output to file. Defaults to `./.log.txt` |

### Examples

To process a directory:

```bash
convert-tif-to-png --dir /path/to/directory --pattern 'some-regex-pattern' --size 4k
```

To process individual files:

```bash
convert-tif-to-png --file /path/to/file1.tif /path/to/file2.tif --pattern 'some-regex-pattern' --size 4k
```

### Integration: MacOS Automator

#### Prerequisites

Before integrating this script into MacOS Automator, make sure you have the following prerequisites installed and configured:

1. `pyenv`: A Python version management tool, used to set the Python version for the script.
    - Installation: Use Homebrew by running `brew install pyenv` in your terminal.
    - Setting up: Add `pyenv init` to your shell to enable shims and autocompletion. [See official documentation for more details](https://github.com/pyenv/pyenv#installation).

2. Python Path: You'll need the full path to your Python interpreter.
    - Finding Python Path: Run `which python` or `which python3` in your terminal to get the full path.

#### Integration

To integrate this script into macOS Automator for automated file processing:

1. Open Automator and create a new "Folder Action."
2. Set the "Folder Action receives files and folders added to" to your desired directory.
3. Set "Pass input" to "as arguments."
4. Add a "Run Shell Script" action.
5. Enter the full path to your Python interpreter and script, along with any command line arguments, like so:

```bash
/full/path/to/python3 -m convert-tif-to-png --size 4k --pattern 'some-regex-pattern' --file "$@"
```

Make sure you replace `/full/path/to/python3` with the actual path on your system.

Any new TIF files added to the specified folder will automatically be converted to PNG.
