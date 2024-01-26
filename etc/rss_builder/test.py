from bs4 import BeautifulSoup

# Read the HTML file
with open('/Users/ismailefetop/projects/org-blog/ismailefe_org/blog/eye_candy/index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract title
title_tag = soup.find('title')
title = title_tag.text if title_tag else None

# Extract date (assuming date is in an element with class="date")
date_tag = soup.find(class_='date')
date = date_tag.text if date_tag else None

# Extract author (assuming author is in a <meta> tag with name="author")
author_tag = soup.find('meta', {'name': 'author'})
author = author_tag['content'] if author_tag and 'content' in author_tag.attrs else None

# Extract body content as HTML
body_tag = soup.body
body_html = str(body_tag) if body_tag else None

# Print or use the extracted information as needed
print(f'Title: {title}')
print(f'Date: {date}')
print(f'Author: {author}')
print(f"Body Html: {body_html}")
