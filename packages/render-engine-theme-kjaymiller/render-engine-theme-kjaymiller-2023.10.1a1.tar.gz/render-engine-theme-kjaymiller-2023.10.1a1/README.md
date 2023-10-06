# render-engine-i18n
Plugin that adds internationalization

This is the initial plan
Type: Plugin

MVP: Create a second route under the language with all the pages. Check for pages in the base and raise an error if base_page doesn't exist.

```
site_settings:
    languages: ['en', 'es', ...]
    default_language: 'en'
```

create a page at the same routes if there is an `en` page there. It will ignore routes. If the page doesn't exist, default to the default_language and add a variable `missing_language` eq true.
