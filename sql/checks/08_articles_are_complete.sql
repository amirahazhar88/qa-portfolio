-- name: Every article has an author, a title and a slug
SELECT article_id, user_id, title, slug
FROM article
WHERE user_id IS NULL
   OR title IS NULL OR TRIM(title) = ''
   OR slug  IS NULL OR TRIM(slug)  = '';
