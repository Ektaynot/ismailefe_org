from datetime import datetime
from bs4 import BeautifulSoup

system_header = "/Users/ismailefetop/ismailefe_org"
website_header= "https://ismailefe.org"
blog_posts = ["/blog/my_org_pandoc_workflow/index.html",
            "/blog/arc_and_firefox/index.html",
            "/blog/org-awk-anki/index.html",
            "/blog/rotring500/index.html",
            "/blog/emacs_functions/index.html",
            "/blog/plain_text/index.html",
            "/blog/my_edc/index.html",
            "/blog/eye_candy/index.html",
            "/blog/best_albums_2023/index.html",
            "/blog/favorite_themes/index.html",
            "/blog/rss/index.html",
            "/blog/uni_file_structure/index.html",
            "/blog/good_presentations/index.html"]

update_time = str(datetime.now().strftime('%a, %d %b %Y %H:%M:%S'))+' +0300'

feed_output = system_header + "/feed.xml"
xml_file = open(feed_output, "w")

xml_file.write(
f'''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>İsmail Efe's Blog Site</title>
<link>https://ismailefe.org/</link>
<description>İsmail Efe's Second Brain.</description>
<language>en</language>
<atom:link href="https://ismailefe.org/feed.xml" rel="self" type="application/rss+xml"/>
<lastBuildDate>{update_time}</lastBuildDate>'''
)

xml_file.close()

# Below function is partially written by ChatGPT.
def parse_html(filename_arg):
    # Read the HTML file
    with open(filename_arg, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title
    title_tag = soup.find('title')
    title = title_tag.text if title_tag else None

    # Extract date (assuming date is in an element with class="date")
    date_tag = soup.find(class_='date')
    date = date_tag.text if date_tag else None

    # Extract body content as HTML
    body_tag = soup.body
    body_html = str(body_tag) if body_tag else None

    post_dict = {"title":title,"date":date,"body_html":body_html}

    return post_dict

# Below function is written by ChatGPT.
def format_date(input_date):
    # Convert input date string to a datetime object
    input_datetime = datetime.strptime(input_date, '%Y-%m-%d')

    # Format the datetime object to the desired string format
    formatted_date = input_datetime.strftime('%a, %d %b %Y')

    return formatted_date

for post in blog_posts:
    post_dictionary = parse_html(system_header+post)
    xml_file = open(feed_output, "a")
    xml_file.write(f'''
<item>
  <title>{post_dictionary["title"]}</title>
  <description><![CDATA[<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">{post_dictionary["body_html"]}</html>]]></description>
  <author>ismailefetop@gmail.com (İsmail Efe Top)</author>
  <link>{website_header+post}</link>
  <guid>{website_header+post}</guid>
  <pubDate>{format_date(post_dictionary["date"])} 00:00:00 +0300</pubDate>
</item>
''')
    xml_file.close()

xml_file = open(feed_output, "a")
xml_file.write('''
</channel>
</rss>''')
xml_file.close()
