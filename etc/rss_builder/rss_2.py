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
f'''<rss version="2.0">
<channel>
<title>İsmail Efe's Blog Site</title>
<description>İsmail Efe's Blog Site</description>
<link>https://ismailefe.org</link>
<atom:link href="http://ismailefe.org/feed.xml" rel="self" type="application/rss+xml"/>
<lastBuildDate>{update_time}</lastBuildDate>'''
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
<item>
  <title>{post_dictionary["title"]}</title>
  <author><name>{post_dictionary["author"]}</name></author>
  <description>{post_dictionary["body_html"]}</description>
  <link>{website_header+post}</link>
  <pubDate>{post_dictionary["date"]}T00:00:00+03:00</pubDate>
</item>
''')
    xml_file.close()

xml_file = open(feed_output, "a")
xml_file.write('''
</channel>
</feed>''')
xml_file.close()
