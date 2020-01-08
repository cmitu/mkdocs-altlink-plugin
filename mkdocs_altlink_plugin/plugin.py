import re
from mkdocs.plugins import BasePlugin

class AlternateLinkPlugin(BasePlugin):

    MD_LINK = re.compile(r''']\(([^)]*)\)''', re.UNICODE)

    def _should_ignore_link(self, link):
        return link.startswith("http") or link.startswith("#") or link.startswith("ftp") or link.startswith("www") or link.endswith(".md")

    def on_page_markdown(self, markdown, page, config, **kwargs):

        print "Page: " + page.title

        links = re.findall(self.MD_LINK, markdown)
        for link in links:
            if self._should_ignore_link(link.strip()):
                continue

            # Get any anchors in the URL
            vals = link.split("#")

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
