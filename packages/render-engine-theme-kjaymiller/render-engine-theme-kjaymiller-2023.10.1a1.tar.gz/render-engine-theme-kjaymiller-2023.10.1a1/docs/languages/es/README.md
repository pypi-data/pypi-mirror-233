---
title: Readme
---

# Complemento que agrega internacionalización

Este es el plan inicial
Tipo: Complemento

MVP: Crear una segunda ruta debajo del idioma con todas las páginas. Verificar la existencia de páginas en la base y generar un error si no existe la página base.

Configuración del sitio:

```json
languages: ['en', 'es', ...]
default_languages: 'en'
```

Crear una página en las mismas rutas si hay una página en inglés allí. Ignorará las rutas. Si la página no existe, volverá al idioma predeterminado y agregará una variable missing_language igual a true.