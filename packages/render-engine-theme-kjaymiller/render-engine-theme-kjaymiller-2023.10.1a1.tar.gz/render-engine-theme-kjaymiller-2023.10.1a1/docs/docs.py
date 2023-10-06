from render_engine.site import Site
from render_engine.page import Page
from render_engine.collection import Collection
from render_engine_i18n.render_engine_i18n import RenderEngineI18n
from render_engine.parsers.markdown import MarkdownPageParser

class docSite(Site):
    template_path: str = "docs/templates"


docs = docSite()

docs.site_settings.update(
    {
        "SITE_TITLE": "Render Engine Internationlization (i18n)",
        "SITE_DESCRIPTION": "A Render Engine plugin for internationalization.",
    }
)


docs.register_plugins(RenderEngineI18n)
plugin_settings = {"RenderEngineI18n":
                   { 
                    "languages": ["en", "es"],
                    "languages_path": "docs/languages",
                    "default_language": "en",
                }
}
docs.site_settings["plugins"].update(plugin_settings)

@docs.page
class Index(Page):
    content_path = "docs/pages/README.md"
    template = "page.html"
    Parser = MarkdownPageParser
