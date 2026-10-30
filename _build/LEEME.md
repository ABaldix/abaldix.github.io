# Cómo publicar artículos en VivaVoltia

La web se genera automáticamente a partir de los archivos de `_src/`.
**No edites a mano** `index.html`, `articles/`, `guides/` ni `sitemap.xml`:
se sobrescriben en cada publicación.

## Publicar un artículo nuevo

1. En GitHub, entra en la carpeta `_src/articles/` y pulsa **Add file → Create new file**.
2. Llama al archivo con la URL que quieras, en minúsculas y con guiones:
   por ejemplo `solar-panels-for-rv.html`. Esa será la dirección:
   `vivavoltia.com/articles/solar-panels-for-rv.html`.
3. Copia el contenido de `_src/articles/_TEMPLATE.txt` y rellénalo.
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
| `description` | sí | Resumen corto (tarjetas y Google) |
| `category` | sí | `costs`, `panels`, `batteries`, `inverters` o `installation` |
| `published` | sí | Fecha de publicación `AAAA-MM-DD` (ordena "Latest Guides") |
| `updated` | no | Fecha de la última revisión |
| `seo_title` | no | Título alternativo para Google |
| `image`, `image_alt` | no | Foto de `images/`. Sin foto se usa el icono de la categoría |
| `takeaway` | no | Puntos clave (repite la línea para cada uno) |
| `source` | no | Fuente: `Nombre | URL` (repite la línea) |
| `related` | no | Artículos relacionados (slug, repite la línea) |
| `featured` | no | `yes` para destacarlo en la portada |
| `order` | no | Número para ordenar artículos publicados el mismo día |

## Comprobaciones automáticas

Si un artículo enlaza a otro que no existe, la publicación falla y en la
pestaña **Actions** verás el error. Así no quedan enlaces rotos.

## Generar en local (opcional)

    python3 _build/build.py
