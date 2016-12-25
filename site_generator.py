import os
import json

from jinja2 import Environment, PackageLoader
from markdown import markdown

CONFIG_PATH = 'config.json'
SITE_DIRECTORY = 'site'

def read_config(path):
    with open(path, 'r') as file_with_json:
        config = json.load(file_with_json)
    return config


def create_site_structure(config):
    site_structure = []
    for item in config['topics']:
        topic = item['title']
        site_structure.append((topic, []))
        articles = filter(
            lambda x: x['topic']==item['slug'],
            config['articles']
        )
        for article in articles:
            title = article['title']
            directory, file = os.path.split(article['source'])
            file = file.replace('md', 'html')
            href = os.path.join(directory, file)
            directory_structure = os.path.join(SITE_DIRECTORY, directory)
            full_html_path = os.path.join(directory_structure, file)
            html_path = full_html_path
            site_structure[-1][1].append({
                'source': article['source'],
                'title': title,
                'href': href,
                'html_path': html_path
            })
    return site_structure


def create_articles(site_structure, template):
    for _, articles in site_structure:
        for article in articles:
            directory, file = os.path.split(article['html_path'])
            if not os.path.exists(directory):
                os.makedirs(directory)

            markdown_path = os.path.join('articles',article['source'])
            with open(markdown_path, 'r') as file_with_markdown:
                article_body = markdown(file_with_markdown.read())

            with open(article['html_path'], 'w') as html_file:
                html_file.write(
                    template.render(
                        title=article['title'],
                        article_body=article_body
                    )
                )


def create_index(site_structure, template):
    if not os.path.exists(SITE_DIRECTORY):
        os.makedirs(SITE_DIRECTORY)

    with open(os.path.join(SITE_DIRECTORY, 'index.html'), 'w') as html_file:
        html_file.write(
            template.render(
                title='Статьи',
                site_structure=site_structure
            )
        )
        

def main():
    env = Environment(loader=PackageLoader('site_generator', 'templates'))
    index_template = env.get_template('index.html')
    article_template = env.get_template('article.html')

    config = read_config(CONFIG_PATH)
    site_structure = create_site_structure(config)
    create_articles(site_structure, article_template)
    create_index(site_structure, index_template)


if __name__ == '__main__':
    main()
    