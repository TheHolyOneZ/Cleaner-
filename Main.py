import os
import re
import shutil
from bs4 import BeautifulSoup
import subprocess
import multiprocessing

# Configuration options
DEFAULT_CONFIG = {
    "backup_directory": "backup",  # Backup directory for original files
    "clean_format": "compact",  # Options: "compact" or "readable"
    "remove_comments": True,  # Remove all comments
    "remove_empty_lines": True,  # Remove extra empty lines
    "normalize_indentation": True,  # Convert tabs to spaces
    "js_minify": False,  # Minify JS code (optional)
    "optimize_css": False,  # Remove unused CSS (optional)
    "dry_run": False  # Dry run mode (do not modify files)
}

# Log file path
LOG_FILE_PATH = "cleanup_log.txt"

# Watermark message to be added to each file
WATERMARK = """
/* 
    Cleaned by TheZ Cleaning Tool 
    Watermark: 'This file was processed by TheZ's Cleaning Tool'
    For support and feedback, visit: https://discord.gg/zsGTqgnsmK 
    Version: 1.1
*/
"""

def log_message(message):
    """Logs a message to the log file with a timestamp."""
    print(f"[{message}]")
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{message}]\n")

def create_backup(file_path):
    """Creates a backup of the file in the specified backup directory."""
    backup_dir = DEFAULT_CONFIG["backup_directory"]
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, os.path.basename(file_path))
    shutil.copy2(file_path, backup_path)
    log_message(f"Backup created for {file_path} at {backup_path}")

def add_watermark(content):
    """Adds watermark to the top of the content."""
    return WATERMARK + content

def clean_html(file_path):
    """Cleans an HTML file by removing unnecessary whitespace and comments."""
    create_backup(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    if DEFAULT_CONFIG["remove_comments"]:
        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, str) and text.startswith("<!--")):
            comment.extract()

    # Clean the HTML
    cleaned_html = soup.prettify(formatter="html")
    
    # Remove extra empty lines
    if DEFAULT_CONFIG["remove_empty_lines"]:
        cleaned_html = "\n".join([line.strip() for line in cleaned_html.splitlines() if line.strip()])

    # Normalize indentation (optional)
    if DEFAULT_CONFIG["normalize_indentation"]:
        cleaned_html = cleaned_html.replace("\t", "    ")

    # Adjust formatting based on the selected format
    if DEFAULT_CONFIG["clean_format"] == "compact":
        cleaned_html = cleaned_html.replace("\n\n", "")
    elif DEFAULT_CONFIG["clean_format"] == "readable":
        cleaned_html = re.sub(r"(\})", r"\1\n", cleaned_html)

    # Add watermark
    cleaned_html = add_watermark(cleaned_html)
    
    # Dry run: just log changes, don't modify files
    if DEFAULT_CONFIG["dry_run"]:
        log_message(f"Dry run: HTML changes for {file_path}")
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned_html)
    log_message(f"HTML cleaned: {file_path}")

def clean_js(file_path):
    """Cleans a JavaScript file by removing unnecessary whitespace, comments, and optionally minifying."""
    create_backup(file_path)
    
    with open(file_path, "r", encoding="utf-8") as f:
        js_code = f.read()

    if DEFAULT_CONFIG["remove_comments"]:
        # Remove single-line comments (//) and multi-line comments (/* */) safely
        js_code = re.sub(r"//.*?$", "", js_code, flags=re.MULTILINE)  
        js_code = re.sub(r"/\*.*?\*/", "", js_code, flags=re.DOTALL)  

    # Remove extra empty lines
    js_code = "\n".join([line.strip() for line in js_code.splitlines() if line.strip()])

    # Minify JS (if enabled)
    if DEFAULT_CONFIG["js_minify"]:
        js_code = re.sub(r"\s+", " ", js_code)  # Replace multiple spaces with one
        js_code = js_code.replace("\n", "")  # Remove all newlines

    # Handle readable format
    if DEFAULT_CONFIG["clean_format"] == "compact":
        js_code = re.sub(r"\n\s*\n", "\n", js_code)  # Remove excessive newlines
    elif DEFAULT_CONFIG["clean_format"] == "readable":
        # Add an empty line after each closing curly brace for better readability
        js_code = re.sub(r"(\})", r"\1\n", js_code)

    # Add watermark
    js_code = add_watermark(js_code)

    # Dry run: just log changes, don't modify files
    if DEFAULT_CONFIG["dry_run"]:
        log_message(f"Dry run: JS changes for {file_path}")
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(js_code)
    log_message(f"JavaScript cleaned: {file_path}")

def clean_css(file_path):
    """Cleans a CSS file by removing unnecessary whitespace and comments."""
    create_backup(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        css_code = f.read()

    if DEFAULT_CONFIG["remove_comments"]:
        # Remove comments
        css_code = re.sub(r"/\*.*?\*/", "", css_code, flags=re.DOTALL)

    # Remove unused CSS selectors (optional)
    if DEFAULT_CONFIG["optimize_css"]:
        # Placeholder: Actual optimization logic like purify-css can be added here.
        pass
    
    # Clean up extra whitespace between rules
    css_code = "\n".join([line.strip() for line in css_code.splitlines() if line.strip()])

    if DEFAULT_CONFIG["clean_format"] == "compact":
        css_code = css_code.replace("\n\n", "")
    elif DEFAULT_CONFIG["clean_format"] == "readable":
        css_code = re.sub(r"(\})", r"\1\n", css_code)

    # Add watermark
    css_code = add_watermark(css_code)

    # Dry run: just log changes, don't modify files
    if DEFAULT_CONFIG["dry_run"]:
        log_message(f"Dry run: CSS changes for {file_path}")
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(css_code)
    log_message(f"CSS cleaned: {file_path}")

def clean_directory(directory, clean_format="compact"):
    """Cleans all HTML, JS, and CSS files in the specified directory."""
    DEFAULT_CONFIG["clean_format"] = clean_format
    if not os.path.exists(directory):
        log_message(f"Directory {directory} does not exist!")
        return
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".html"):
                clean_html(file_path)
            elif file.endswith(".js"):
                clean_js(file_path)
            elif file.endswith(".css"):
                clean_css(file_path)

def setup_backup_directory():
    """Sets up the backup directory."""
    backup_dir = DEFAULT_CONFIG["backup_directory"]
    os.makedirs(backup_dir, exist_ok=True)

def main():
    print("Welcome to the Enhanced Code Cleaner Tool for HTML, JS, and CSS")

    # Gather user preferences for cleaning
    action = input("Choose an action: 1) Clean files in current folder 2) Clean custom folder: ").strip()
    
    if action == "1":
        directory = os.path.join(os.getcwd(), "scripts")  # Default folder
    elif action == "2":
        directory = input("Enter the full path of the directory: ").strip()
    else:
        print("Invalid action!")
        return
    
    format_option = input("Choose cleaning format: 1) Compact (no empty lines) 2) Readable (with empty lines between functions): ").strip()
    if format_option == "1":
        clean_format = "compact"
    elif format_option == "2":
        clean_format = "readable"
    else:
        print("Invalid format choice!")
        return

    # Additional configuration options for cleaning
    remove_comments = input("Remove comments? (yes/no): ").strip().lower() == "yes"
    remove_empty_lines = input("Remove empty lines? (yes/no): ").strip().lower() == "yes"
    normalize_indentation = input("Normalize indentation (convert tabs to spaces)? (yes/no): ").strip().lower() == "yes"
    js_minify = input("Minify JavaScript? (yes/no): ").strip().lower() == "yes"
    optimize_css = input("Optimize CSS (remove unused selectors)? (yes/no): ").strip().lower() == "yes"
    dry_run = input("Dry run mode (no actual changes made)? (yes/no): ").strip().lower() == "yes"

    # Update configuration
    DEFAULT_CONFIG["remove_comments"] = remove_comments
    DEFAULT_CONFIG["remove_empty_lines"] = remove_empty_lines
    DEFAULT_CONFIG["normalize_indentation"] = normalize_indentation
    DEFAULT_CONFIG["js_minify"] = js_minify
    DEFAULT_CONFIG["optimize_css"] = optimize_css
    DEFAULT_CONFIG["dry_run"] = dry_run

    # Run the cleaning process
    setup_backup_directory()
    clean_directory(directory, clean_format)
    if dry_run:
        print("Dry run mode: No files were modified.")
    else:
        print("Code cleanup complete.")

if __name__ == "__main__":
    main()
