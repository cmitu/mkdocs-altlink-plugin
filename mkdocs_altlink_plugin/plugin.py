import re
from mkdocs.plugins import BasePlugin

class AlternateLinkPlugin(BasePlugin):

    MD_LINK = re.compile(r']\(([^)]*)\)', re.UNICODE)

    def _should_ignore_link(self, link):
        return link.startswith(u"http") or link.startswith(u"#") or link.startswith(u"ftp") or link.startswith(u"www") or link.endswith(u".md")

    def on_page_markdown(self, markdown, page, config, **kwargs):

        links = re.findall(self.MD_LINK, markdown)
        for link in links:
            if self._should_ignore_link(link.lstrip()):
                continue

            # Get any anchors in the URL
            vals = link.lstrip().split("#")

            # Check if it's a valid internal .md page URL
            if vals[0].endswith(".md"):
                continue

            # Append .md to the page name if not found
            vals[0] += ".md"

            # Re-construct the link
            href_new = "#".join(vals)

            # Replace the values in the markdown
            markdown = markdown.replace("({})".format(link), "({})".format(href_new))

        return markdown
