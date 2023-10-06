import pdb
from pathlib import Path
from render_engine.hookspecs import hook_impl
from render_engine.site import Site
from render_engine.page import Page


class RenderEngineI18n:
    @hook_impl
    def post_render_content(
            page: Page,
            settings: dict[str, any],
            site: Site,
    ):
        """Called after a page is rendered."""
        for lang in settings["RenderEngineI18n"]["languages"]:
            path = (
                Path(settings["RenderEngineI18n"]["languages_path"])
                / Path(lang)
                / Path(page.content_path).name
            )
            if lang == settings["RenderEngineI18n"]["default_language"]:
                path = Path(page.content_path)
            parser = page.Parser
            route = Path(lang)/settings["route"]
            class LangPage(page):
                content_path = path
                Parser = parser

            lang_page = LangPage()
            content = lang_page._render_content(engine=site.engine)
            
            for route in lang_page.routes:
                lang_route = site.output_path/Path(lang)/route/lang_page.path_name
                lang_route.parent.mkdir(parents=True, exist_ok=True)
                lang_route.write_text(content)
