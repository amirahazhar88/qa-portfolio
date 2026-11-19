-- name: A banned user has no active articles
SELECT a.article_id, a.slug, u.username
FROM article a
JOIN user u ON u.user_id = a.user_id
WHERE u.record_status = 'banned' AND a.record_status = 'active';
