# Alternate Link

*An MkDocs plugin that simplifies internal links*

Alternate Links is a very simple [mkdocs plugin](http://www.mkdocs.org/user-guide/plugins/) to enable an
alternate syntax for internal links, removing the need to add the `.md` suffix for the target page.
 
## Quick start

Download this repo and (eventually) unzip it in a folder, or simply clone it via `git`:
``` bash
git clone https://github.com/cmitu/mkdocs-altlink-plugin
```

Enable the plugin in your `mkdocs.yml`:

```yaml
plugins:
    - search
    - alternate-link
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins]


## Usage
When creating an internal Markdown link, you can omit the `.md` extension for the target page:

* `[My Page](source-page.md)` can be written as `[My Page](source-page)`
* `[My Page](source-page.md#Point)` can be written as `[My Page](source-page#Point)`

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
