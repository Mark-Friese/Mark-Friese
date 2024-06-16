# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 15:25:23 2024

@author: Mark Friese
"""

import requests
from bs4 import BeautifulSoup

# Medium RSS feed URL
rss_url = "https://medium.com/feed/@mark.friese.meng"

# Fetch the RSS feed
response = requests.get(rss_url)
soup = BeautifulSoup(response.content, features='xml')

# Extract articles
articles = soup.findAll('item')

# Generate Markdown for the articles
articles_md = "\n".join([
    f"### [{article.title.text}]({
        article.link.text})\n- {article.description.text}\n"
    for article in articles[:5]  # Limiting to the latest 5 articles
])

# Read the README file
with open("README.md", "r") as file:
    readme_content = file.read()

# Define the start and end markers for the articles section
start_marker = "<!-- START_MEDIUM_ARTICLES -->"
end_marker = "<!-- END_MEDIUM_ARTICLES -->"

# Extract content before and after the markers
before_articles = readme_content.split(start_marker)[0]
after_articles = readme_content.split(end_marker)[1]

# Combine the new content
new_readme_content = f"{before_articles}{start_marker}\n{
    articles_md}\n{end_marker}{after_articles}"

# Write the updated content to the README file
with open("README.md", "w") as file:
    file.write(new_readme_content)
