-- name: Every article_tag row points at an existing article
-- why: article_tag has no foreign key, so orphans are possible
SELECT t.article_tag_id, t.article_id, t.tag
FROM article_tag t
LEFT JOIN article a ON a.article_id = t.article_id
WHERE a.article_id IS NULL;
