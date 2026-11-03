# Cómo publicar artículos en VivaVoltia

La web se genera automáticamente: tú solo editas `content/` (textos) y `static/`
(imágenes y archivos fijos). Las páginas HTML finales ya **no se guardan en el
repositorio**: GitHub las crea y las publica en cada cambio, así que no hay copias
duplicadas que puedan confundirse.

## Publicar un artículo nuevo

1. En GitHub, entra en la carpeta `content/articles/` y pulsa **Add file → Create new file**.
2. Llama al archivo con la URL que quieras, en minúsculas y con guiones:
   por ejemplo `solar-panels-for-rv.html`. Esa será la dirección:
   `vivavoltia.com/articles/solar-panels-for-rv.html`.
3. Copia el contenido de `content/templates/article-template.txt` y rellénalo.
4. Pulsa **Commit changes**.

En 1–2 minutos GitHub regenera la web (pestaña **Actions**, flujo "Build and deploy site"):
- el artículo aparece en **Latest Guides** de la portada (los 6 más recientes,
  según `published`) y en el índice **All Solar Guides**;
- se añade a la página de su categoría y al `sitemap.xml`;
- aparece en "Related Guides" de otros artículos de la misma categoría.

## Campos de la ficha (front matter)

| Campo | Obligatorio | Qué es |
|---|---|---|
| `title` | sí | Título del artículo |
| `description` | sí | Meta descripción para Google y tarjetas: 110–160 caracteres |
| `category` | sí | `costs`, `panels`, `batteries`, `inverters` o `installation` |
| `published` | sí | Fecha de publicación `AAAA-MM-DD` (ordena "Latest Guides") |
| `updated` | no | Fecha de la última revisión |
| `seo_title` | recomendado | Título para Google: máx. ~52 caracteres (se añade " | VivaVoltia") |
| `keyword` | recomendado | Palabra clave principal. Debe aparecer en `seo_title`, `description`, el primer párrafo (`lede`) y algún `<h2>` |
| `dek` | no | Subtítulo visible más largo; si falta se usa `description` |
| `image`, `image_alt` | no | Nombre del archivo de `static/images/articles/` (solo el nombre, sin carpeta). Sin foto se usa el icono de la categoría |
| `takeaway` | no | Puntos clave (repite la línea para cada uno) |
| `source` | no | Fuente: `Nombre | URL` (repite la línea) |
| `related` | no | Artículos relacionados (slug, repite la línea) |
| `featured` | no | `yes` para destacarlo en la portada |
| `order` | no | Número para ordenar artículos publicados el mismo día |

## Comprobaciones automáticas

Cada publicación ejecuta una auditoría SEO: avisa si el título o la descripción
son demasiado largos o si la palabra clave falta en el título, la descripción,
el primer párrafo o un subtítulo H2 (lo verás en el registro de **Actions**).

Las fotos que subas a `static/images/articles/` se convierten solas a WebP en varios tamaños.

Si un artículo enlaza a otro que no existe, la publicación falla y en la
pestaña **Actions** verás el error. Así no quedan enlaces rotos.

## Generar en local (opcional)

    python3 tools/build.py      # la web queda en la carpeta _site/


## Newsletter (MailerLite)

El recuadro "Get solar savings tips by email" aparece automáticamente en la portada,
en "Solar by State" y al final de cada artículo **en cuanto pegues el formulario** en
`content/partials/newsletter-form.html`:

1. En MailerLite: **Forms → Embedded forms → crea uno** (solo el campo email) y copia
   el código HTML (pestaña "HTML code").
2. En GitHub, abre `content/partials/newsletter-form.html`, pega el código y guarda.
   Si el archivo está vacío, el recuadro no aparece en ningún sitio.

## Estructura del repositorio

```
content/articles/        Un archivo por artículo          ← aquí escribes
content/pages/           Páginas fijas: about, contact, privacy, terms, calculadora (quote), 404
content/templates/       Plantilla para artículos nuevos
content/partials/        Fragmentos reutilizables (formulario de la newsletter)
static/                  Se copia tal cual a la raíz de la web:
  images/articles/         fotos y portadas de artículos   ← aquí subes imágenes
  images/og/               imágenes para compartir (portada y categorías)
  images/brand/            logo / favicon
  images/pins/             pines de Pinterest
  style.css                estilos de toda la web
  CNAME, ads.txt, robots.txt, BingSiteAuth.xml, pinterest-541f0.html,
  c997e84b….txt            dominio, AdSense y verificaciones: no los borres
static/js/solar-states.js  Datos por estado (precio, sol, crédito) que usan las calculadoras
tools/build.py           Generador de la web (también crea solar-by-state.html)
tools/pinterest/         Textos de los pines (pins_data.py) y scripts para crearlos
tools/graphics/          Script de las portadas con datos (estados y comparativas)
branding/                Material de marca que no se publica (foto de perfil)
.github/workflows/       Compila, publica en GitHub Pages y avisa a buscadores (IndexNow)
```

**Importante:** todo lo que está dentro de `static/` se publica en la **raíz** de la web.
Por ejemplo, `static/ads.txt` es `vivavoltia.com/ads.txt`. Si un servicio (Google, Bing,
Pinterest, Facebook…) te pide subir un archivo de verificación "a la raíz del sitio",
súbelo a `static/`.

La web publicada (vivavoltia.com/articles/…, /guides/…, /quote.html…) se genera
en `_site/` durante la publicación; esa carpeta no está en el repositorio.

## Crear pines o portadas (opcional, en un ordenador con Playwright)

```
python3 tools/pinterest/make_pins.py && node tools/pinterest/render_pins.js
node tools/graphics/render_heroes.js
```
