# Cleaner-
Cleans HTML,CSS and .js files effective
# TheZ Cleaning Tool

## Overview
The **TheZ Cleaning Tool** is a Python-based script that allows you to clean and optimize your HTML, JavaScript, and CSS files. It can remove unnecessary comments, empty lines, and whitespace, normalize indentation, and even minify JavaScript code if desired. Additionally, it adds a watermark to each processed file to keep track of the tool's usage. It also supports dry-run mode where no changes are made to files, only logs are generated.

This tool is designed to help clean up and organize your project files quickly and efficiently.

## Features
- **HTML, JS, CSS cleaning**: Clean up unnecessary comments, whitespace, and indentation in HTML, JavaScript, and CSS files.
- **File minification**: Optionally minify JavaScript code.
- **Watermark**: Adds a custom watermark to each file processed by the tool.
- **Backup**: Automatically creates backups of files before modifying them.
- **Dry-run mode**: Allows you to simulate the cleaning process without making any changes.
- **Customizable settings**: Choose the level of cleanup (compact or readable) and whether or not to remove comments, empty lines, and normalize indentation.

## Installation
To use this tool, make sure you have Python 3.x installed on your system. You will also need to install `beautifulsoup4` for HTML parsing.

### Dependencies
You can install the necessary dependencies with the following command:
```bash
pip install beautifulsoup4
