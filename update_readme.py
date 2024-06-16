import requests
from bs4 import BeautifulSoup
import hashlib

# Medium RSS feed URL
rss_url = "https://medium.com/feed/@mark.friese.meng"

# Fetch the RSS feed
response = requests.get(rss_url)
soup = BeautifulSoup(response.content, 'xml')  # Use 'xml' as the parser

# Extract articles
articles = soup.findAll('item')

# Generate HTML for the articles
articles_html = []
for article in articles[:5]:  # Limiting to the latest 5 articles
    title = article.title.text if article.title else "No title"
    link = article.link.text if article.link else "No link"
    description = BeautifulSoup(article.description.text, 'html.parser').text if article.description else "No description"
    pub_date = article.pubDate.text if article.pubDate else "No date"
    thumbnail = article.find('media:thumbnail')['url'] if article.find('media:thumbnail') else ""

    articles_html.append(f"""
    <div style="margin-bottom: 20px;">
        <a href="{link}" style="text-decoration: none; color: black;">
            <h3>{title}</h3>
            <img src="{thumbnail}" alt="{title}" style="width: 100px; height: 100px; float: left; margin-right: 20px;">
            <p>{description}</p>
            <small>{pub_date}</small>
        </a>
        <div style="clear: both;"></div>
    </div>
    """)

articles_html = "\n".join(articles_html)

# Read the README file
try:
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()
except FileNotFoundError:
    print("README.md not found, creating a new one.")
    readme_content = ""

# Define the start and end markers for the articles section
start_marker = "<!-- START_MEDIUM_ARTICLES -->"
end_marker = "<!-- END_MEDIUM_ARTICLES -->"

# Check if the markers exist in the README content
if start_marker in readme_content and end_marker in readme_content:
    # Extract content before and after the markers
    before_articles = readme_content.split(start_marker)[0]
    after_articles = readme_content.split(end_marker)[1]
else:
    # If markers are not found, create a new structure
    before_articles = readme_content
    after_articles = "\n" + end_marker

# Combine the new content
new_readme_content = f"{before_articles}{start_marker}\n{articles_html}\n{end_marker}{after_articles}"

# Calculate the hash of the new content
new_readme_hash = hashlib.md5(new_readme_content.encode('utf-8')).hexdigest()

# Calculate the hash of the existing content
existing_readme_hash = hashlib.md5(readme_content.encode('utf-8')).hexdigest()

# Only write to the file if the content has changed
if new_readme_hash != existing_readme_hash:
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(new_readme_content)
