#!/usr/bin/env python3

import glob
import os

if "GITHUB_WORKSPACE" in os.environ:
    full_project_dir = os.environ["GITHUB_WORKSPACE"]
else:
    full_project_dir = os.path.expanduser("~/ismailefe_org/")

website_url = "https://ismailefe.org/"

sitemap_list = []

for name in glob.glob(full_project_dir + "**/index.html", recursive=True):

    name = name.replace(full_project_dir, website_url)

    if (website_url + "etc/") not in name and (website_url + "src/") not in name:
        sitemap_list.append(name[0 : name.rindex("/") + 1])


sitemap_list.append(website_url + "feed.xml")

with open(full_project_dir + "sitemap.txt", "w") as file:
    for i in sitemap_list:
        file.write(i + "\n")