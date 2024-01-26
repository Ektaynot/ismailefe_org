from datetime import datetime
from bs4 import BeautifulSoup

system_header = "/Users/ismailefetop/projects/org-blog/ismailefe_org"
website_header= "https://ismailefe.org"
blog_posts = ["/blog/my_edc/index.html", 
              "/blog/eye_candy/index.html", 
              "/blog/best_albums_2023/index.html", 
              "/blog/favorite_themes/index.html"
              ]

update_time = str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'))+'+03:00'

feed_output = "/Users/ismailefetop/projects/org-blog/ismailefe_org/feed.xml"
xml_file = open(feed_output, "w")

xml_file.write(
f'''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>İsmail Efe's Blog Site</title>
<generator>Custom Generator</generator>
<link href="https://ismailefe.org/"/>
<link href="https://ismailefe.org/feed.xml" rel="self"/>
<id>https://ismailefe.org/feed.xml</id>
<updated>{update_time}</updated>'''
)

xml_file.close()

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

    # Extract author (assuming author is in a <meta> tag with name="author")
    author_tag = soup.find('meta', {'name': 'author'})
    author = author_tag['content'] if author_tag and 'content' in author_tag.attrs else None

    # Extract body content as HTML
    body_tag = soup.body
    body_html = str(body_tag) if body_tag else None

    post_dict = {"title":title,"date":date,"author":author,"body_html":body_html}

    return post_dict

for post in blog_posts:
    post_dictionary = parse_html(system_header+post)
    xml_file = open(feed_output, "a")
    xml_file.write(f'''
<entry>
  <title>{post_dictionary["title"]}</title>
  <author><name>{post_dictionary["author"]}</name></author>
  <description type="html"><![CDATA[{post_dictionary["body_html"]}]]></description>
  <link href="{website_header+post}"/>
  <id>{website_header+post}</id>
  <updated>{post_dictionary["date"]}T00:00:00+03:00</updated>
</entry>
''')
    xml_file.close()

xml_file = open(feed_output, "a")
xml_file.write("</feed>")
xml_file.close()
