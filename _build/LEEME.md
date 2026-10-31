# Cómo publicar artículos en VivaVoltia

La web se genera automáticamente a partir de los archivos de `_src/`.
**No edites a mano** `index.html`, `articles/`, `guides/` ni `sitemap.xml`:
se sobrescriben en cada publicación.

## Publicar un artículo nuevo

1. En GitHub, entra en la carpeta `_src/articles/` y pulsa **Add file → Create new file**.
2. Llama al archivo con la URL que quieras, en minúsculas y con guiones:
   por ejemplo `solar-panels-for-rv.html`. Esa será la dirección:
   `vivavoltia.com/articles/solar-panels-for-rv.html`.
3. Copia el contenido de `_src/templates/article-template.txt` y rellénalo.
4. Pulsa **Commit changes**.

En 1–2 minutos GitHub regenera la web (pestaña **Actions**, flujo "Build site"):
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
| `image`, `image_alt` | no | Nombre del archivo de `images/articles/` (solo el nombre, sin carpeta). Sin foto se usa el icono de la categoría |
| `takeaway` | no | Puntos clave (repite la línea para cada uno) |
| `source` | no | Fuente: `Nombre | URL` (repite la línea) |
| `related` | no | Artículos relacionados (slug, repite la línea) |
| `featured` | no | `yes` para destacarlo en la portada |
| `order` | no | Número para ordenar artículos publicados el mismo día |

## Comprobaciones automáticas

Cada publicación ejecuta una auditoría SEO: avisa si el título o la descripción
son demasiado largos o si la palabra clave falta en el título, la descripción,
el primer párrafo o un subtítulo H2 (lo verás en el registro de **Actions**).

Las fotos que subas a `images/articles/` se convierten solas a WebP en varios tamaños.

Si un artículo enlaza a otro que no existe, la publicación falla y en la
pestaña **Actions** verás el error. Así no quedan enlaces rotos.

## Generar en local (opcional)

    python3 _build/build.py


## Estructura del repositorio

```
/                      Páginas públicas generadas (index, about, contact, privacy, terms,
                       quote, 404), feed.xml, sitemap.xml, style.css y archivos que deben
                       estar en la raíz: CNAME, ads.txt, robots.txt y verificaciones
                       (BingSiteAuth.xml, pinterest-541f0.html, clave IndexNow .txt)
articles/              Artículos generados        (no editar: salen de _src/articles)
guides/                Páginas de categoría       (no editar: generadas)
images/articles/       Fotos y portadas de artículos  ← aquí subes imágenes nuevas
images/og/             Imágenes para compartir de portada y categorías
images/brand/          Logo / favicon
images/opt/            Versiones WebP             (no editar: generadas)
images/pins/           Pines de Pinterest         (generados con _build/pinterest)
_src/articles/         Fuente de cada artículo    ← aquí escribes
_src/pages/            Fuente de las páginas fijas (about, contact, calculadora…)
_src/templates/        Plantilla para artículos nuevos
_build/build.py        Generador de la web (lo ejecuta GitHub Actions)
_build/pinterest/      Textos de los pines (pins_data.py) y scripts para crearlos
_build/graphics/       Script de las portadas con datos (estados y comparativas)
_assets/branding/      Material de marca que no se publica en la web (foto de perfil)
.github/workflows/     Automatización: compilar la web y avisar a buscadores (IndexNow)
```

Las carpetas que empiezan por `_` no se publican en vivavoltia.com.

## Crear pines o portadas (opcional, en un ordenador con Playwright)

```
python3 _build/pinterest/make_pins.py && node _build/pinterest/render_pins.js
node _build/graphics/render_heroes.js
```
