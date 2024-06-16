import requests
from bs4 import BeautifulSoup

# Medium RSS feed URL
rss_url = "https://medium.com/feed/@mark.friese.meng"

# Fetch the RSS feed
response = requests.get(rss_url)
soup = BeautifulSoup(response.content, 'xml')  # Use 'xml' as the parser

# Extract articles
articles = soup.findAll('item')

# Generate Markdown for the articles
articles_md = []
for article in articles[:5]:  # Limiting to the latest 5 articles
    title = article.title.text if article.title else "No title"
    link = article.link.text if article.link else "No link"
    description = article.description.text if article.description else "No description"
    articles_md.append(f"### [{title}]({link})\n- {description}\n")

articles_md = "\n".join(articles_md)

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
