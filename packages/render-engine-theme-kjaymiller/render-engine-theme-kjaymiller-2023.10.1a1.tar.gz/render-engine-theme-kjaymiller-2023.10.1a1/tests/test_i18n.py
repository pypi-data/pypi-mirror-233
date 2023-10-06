import pytest
import pathlib
from render_engine_i18n.render_engine_i18n import RenderEngineI18n
from render_engine.page import Page
from render_engine.site import Site

@pytest.fixture(scope="session")
def site(tmp_path_factory):
    class TestSite(Site):
        output_path: pathlib.Path = tmp_path_factory.getbasetemp() / "output"

    test_site = TestSite()
    test_site.register_plugins(RenderEngineI18n)
    plugin_settings = {
        "RenderEngineI18n":
                    { 
                        "languages": ["es"],
                        "default_language": "en",
                        "languages_path": tmp_path_factory.getbasetemp() / "languages",
                    }
    }
    test_site.site_settings["plugins"].update(plugin_settings)
    return test_site


def test_render_engine_i18n(site, tmp_path_factory):
    """When the site is rendered the output path should contain the rendered pages"""

    en_path = tmp_path_factory.getbasetemp() / "pages" / "hello.txt"
    en_path.parent.mkdir(parents=True, exist_ok=True)
    en_path.write_text("Hello World!")

    es_path = tmp_path_factory.getbasetemp() / "languages" / "es" / "hello.txt"
    es_path.parent.mkdir(parents=True, exist_ok=True)
    es_path.write_text("Hola Mundo!")

    @site.page
    class TestPage(Page):
        content_path = en_path
        title = "Test Page"

    site.render()

    assert (site.output_path / "test-page.html").exists()
    assert (site.output_path /  "es" / "test-page.html").exists()


def test_render_engine_i18n_generates_in_pages(site, tmp_path_factory):
    """Pages are generated in the pages folder"""

   
    en_path = tmp_path_factory.getbasetemp() / "pages" / "hello.txt"
    en_path.parent.mkdir(parents=True, exist_ok=True)
    en_path.write_text("Hello World!")

    es_path = tmp_path_factory.getbasetemp() / "languages" / "es" / "hello.txt"
    es_path.parent.mkdir(parents=True, exist_ok=True)
    es_path.write_text("Hola Mundo!")

    @site.page
    class TestPage(Page):
        content_path = en_path
        title = "Test Page"
        routes = ['pages']

    site.render()

    assert (site.output_path / "pages" /"test-page.html").exists()
    assert (site.output_path /  "es" / "pages" / "test-page.html").exists()
 