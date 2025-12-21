#!/usr/bin/env python3

import os
import re
import shutil
import sys
from dateutil import parser

if "GITHUB_WORKSPACE" in os.environ:
    system_header = os.environ["GITHUB_WORKSPACE"]
else:
    system_header = "/Users/ismailefetop/ismailefe_org"


class NowPageError(Exception):
    """Base exception for now page workflow errors."""
    pass


def extract_date_from_now_page(now_html_path):
    """
    Extract the date from the current now page using regex.
    Returns the date string (e.g., "Nov 20, 2025").
    Raises NowPageError if date cannot be extracted.
    """
    try:
        with open(now_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise NowPageError(f"Now page not found: {now_html_path}")
    except IOError as e:
        raise NowPageError(f"Cannot read now page: {e}")
    
    pattern = r'<h1[^>]*id="when-did-i-last-update-this-page"[^>]*>.*?</h1>\s*<ul>\s*<li>\s*([^<]+?)\s*</li>'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        raise NowPageError(f"Could not find date in 'When did I last update this page' section")
    
    return match.group(1).strip()


def convert_date_to_iso(date_str):
    """
    Convert date string (e.g., "Nov 20, 2025") to ISO format (YYYY-MM-DD).
    Raises NowPageError if date cannot be parsed.
    """
    try:
        date_obj = parser.parse(date_str)
        return date_obj.strftime('%Y-%m-%d')
    except (ValueError, TypeError) as e:
        raise NowPageError(f"Cannot parse date '{date_str}': {e}")


def archive_current_page(now_html_path, archive_dir, date_iso):
    """
    Copy the current now page to the archive with a date-based filename,
    adding a meta description tag with the date.
    Returns the archive filename.
    Raises NowPageError if archiving fails.
    """
    try:
        # Read the current now page
        with open(now_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create the meta description tag
        meta_description = f'    <meta name="description" content="Now page of {date_iso}" />\n'
        
        # Check if a meta description tag already exists
        meta_description_pattern = r'<meta\s+name="description"\s+content="[^"]*"\s*/>'
        if re.search(meta_description_pattern, content, re.IGNORECASE):
            # Replace existing meta description tag
            content = re.sub(meta_description_pattern, meta_description.strip(), content, flags=re.IGNORECASE)
        else:
            # Add meta description tag after the title tag or after the author meta tag
            # Try to find a good insertion point (after title or after author meta)
            title_pattern = r'(<title>.*?</title>)'
            author_pattern = r'(<meta\s+name="author"[^>]*/>)'
            
            if re.search(title_pattern, content, re.IGNORECASE | re.DOTALL):
                # Insert after title tag
                content = re.sub(
                    title_pattern,
                    r'\1\n' + meta_description,
                    content,
                    flags=re.IGNORECASE | re.DOTALL
                )
            elif re.search(author_pattern, content, re.IGNORECASE):
                # Insert after author meta tag
                content = re.sub(
                    author_pattern,
                    r'\1\n' + meta_description,
                    content,
                    flags=re.IGNORECASE
                )
            else:
                # Fallback: insert after the first meta tag
                first_meta_pattern = r'(<meta[^>]*/>)'
                content = re.sub(
                    first_meta_pattern,
                    r'\1\n' + meta_description,
                    content,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        # Ensure archive directory exists
        os.makedirs(archive_dir, exist_ok=True)
        archive_filename = f"{date_iso}.html"
        archive_path = os.path.join(archive_dir, archive_filename)
        
        # Write the modified content to the archive file
        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return archive_filename
    except FileNotFoundError:
        raise NowPageError(f"Now page not found: {now_html_path}")
    except IOError as e:
        raise NowPageError(f"Cannot read now page or write archive file: {e}")
    except OSError as e:
        raise NowPageError(f"Cannot create archive directory: {e}")
    except Exception as e:
        raise NowPageError(f"Unexpected error archiving page: {e}")


def update_archive_index(archive_index_path, archive_filename, date_iso):
    """
    Update the archive index HTML by inserting a new entry at the top of the list.
    Raises NowPageError if update fails.
    """
    try:
        with open(archive_index_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise NowPageError(f"Archive index not found: {archive_index_path}")
    except IOError as e:
        raise NowPageError(f"Cannot read archive index: {e}")
    
    new_entry = f'''      <li>
        <p>
          <a href="/now/archive/indexes/{archive_filename}">{date_iso}</a>
        </p>
      </li>
'''
    
    pattern = r'(<h2[^>]*id="archive"[^>]*>Archive</h2>\s*<ul>\s*)(<li>)'
    match = re.search(pattern, content, re.IGNORECASE)
    
    if not match:
        raise NowPageError("Could not find archive list section in index.html")
    
    new_content = content[:match.end(1)] + new_entry + content[match.end(1):]
    
    try:
        with open(archive_index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except IOError as e:
        raise NowPageError(f"Cannot write to archive index: {e}")


def deploy_new_page(source_html_path, target_html_path):
    """
    Copy the new HTML from src/now/now.html to now/index.html,
    removing the style tag from the head section.
    Raises NowPageError if deployment fails.
    """
    try:
        # Read the source HTML file
        with open(source_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the style tag and its contents from the head section
        # This pattern matches <style>...</style> including multiline content
        style_pattern = r'<style[^>]*>.*?</style>'
        content = re.sub(style_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Ensure target directory exists
        target_dir = os.path.dirname(target_html_path)
        os.makedirs(target_dir, exist_ok=True)
        
        # Write the modified content to the target file
        with open(target_html_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except FileNotFoundError:
        raise NowPageError(f"Source file not found: {source_html_path}")
    except IOError as e:
        raise NowPageError(f"Cannot read source file or write target file: {e}")
    except OSError as e:
        raise NowPageError(f"Cannot create target directory: {e}")
    except Exception as e:
        raise NowPageError(f"Unexpected error deploying page: {e}")


def main():
    """
    Main workflow function that orchestrates all steps.
    """
    now_html_path = os.path.join(system_header, "now/index.html")
    source_html_path = os.path.join(system_header, "src/now/now.html")
    archive_dir = os.path.join(system_header, "now/archive/indexes")
    archive_index_path = os.path.join(system_header, "now/archive/index.html")
    
    try:
        print(f"Checking source file: {source_html_path}")
        if not os.path.exists(source_html_path):
            raise NowPageError(f"Source file not found: {source_html_path}\nPlease export your org file to HTML first.")
        
        if not os.path.exists(now_html_path):
            print("No existing now page found. Deploying initial page...")
            deploy_new_page(source_html_path, now_html_path)
            print("✓ Initial page deployed successfully!")
            return 0
        
        print("Extracting dates from source and current pages...")
        # Extract dates from both files
        source_date_str = extract_date_from_now_page(source_html_path)
        current_date_str = extract_date_from_now_page(now_html_path)
        
        # Convert both to ISO format for comparison
        source_date_iso = convert_date_to_iso(source_date_str)
        current_date_iso = convert_date_to_iso(current_date_str)
        
        print(f"Source date: {source_date_str} ({source_date_iso})")
        print(f"Current date: {current_date_str} ({current_date_iso})")
        
        # If dates match, do nothing
        if source_date_iso == current_date_iso:
            print("✓ Dates match. No update needed.")
            return 0
        
        print(f"Dates differ. Proceeding with archiving and deployment...")
        # Dates are different, proceed with archiving and deployment
        date_iso = current_date_iso
        print(f"Archiving current page as {date_iso}.html...")
        archive_filename = archive_current_page(now_html_path, archive_dir, date_iso)
        print(f"✓ Archived to: {archive_filename}")
        
        print("Updating archive index...")
        update_archive_index(archive_index_path, archive_filename, date_iso)
        print("✓ Archive index updated")
        
        print("Deploying new page...")
        deploy_new_page(source_html_path, now_html_path)
        print("✓ New page deployed successfully!")
        
        return 0
    except NowPageError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())

