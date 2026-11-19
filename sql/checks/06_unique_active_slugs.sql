-- name: Article slugs are unique, ignoring case
-- why: the slug is the public URL of an article
SELECT LOWER(slug) AS slug, COUNT(*) AS n
FROM article
GROUP BY LOWER(slug)
HAVING COUNT(*) > 1;
