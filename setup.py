from setuptools import setup

setup(
    name='mkdocs-altlink-plugin',
    version='1.0.0',
    packages=['mkdocs_altlink_plugin'],
    url='https://github.com/cmitu/mkdocs-altlink-plugin',
    license='MIT',
    author='mitu',
    keywords='markdown wiki mkdocs internal links',
    description='Alternate Link is a very simple mkdocs plugin to rewrite the Markdown links source',
    install_requires=['mkdocs'],
    entry_points={
        'mkdocs.plugins': [
            'alternate-link = mkdocs_altlink_plugin.plugin:AlternateLinkPlugin',
        ]
    },
)
