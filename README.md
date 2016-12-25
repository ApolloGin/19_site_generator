# 19_site_generator

## Synopsis

Script creates simple static site from articles are written on markdown. It convert markdown to html and collect them to the static site.

## Quick start

 - First of all install requirements from file `pip3 install -r requirements.txt`
 - make sure there is config.json near the main script site_generator.py. This config must contain the structure of markdown articles.
 - run site_generator.py `python3.5 site_generator.py`

After that you will receive static site in default directory "site". Site has main page - index.html. That page collect all articles with reference to these.

## Extra usage

If you want to automate site generating, you will copy pre-commit file to .git/hooks. And before you commit some changes script automatically generate new site with all changes and adds it to commit.