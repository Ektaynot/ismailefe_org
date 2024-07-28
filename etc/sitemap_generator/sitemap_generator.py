import glob
import os

home_dir = os.path.expanduser("~")
project_dir = "ismailefe_org/"

website_url = "https://ismailefe.org/"

sitemap_list = []
excluded = ["etc/","src/"]

# included: *.html, feed.xml
for name in glob.glob('/Users/ismailefetop/ismailefe_org/**/*.html', recursive = True): 
    name = name.replace(f'{home_dir}/{project_dir}',website_url)
    if f"{website_url}etc/" not in name and f"{website_url}src/" not in name and "index.html" in name:
        sitemap_list.append(name[0:name.rindex("/")+1])

sitemap_list.append(website_url+"feed.xml")        

with open(f"{home_dir}/{project_dir}sitemap.txt", "w") as file:
    for i in sitemap_list:
        file.write(i+"\n")

print(sitemap_list)