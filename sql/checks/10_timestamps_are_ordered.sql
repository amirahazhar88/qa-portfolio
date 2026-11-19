-- name: updated_at is never earlier than created_at
SELECT 'article' AS tbl, article_id AS id FROM article WHERE updated_at < created_at
UNION ALL SELECT 'article_comment', article_comment_id FROM article_comment WHERE updated_at < created_at
UNION ALL SELECT 'user', user_id FROM user WHERE updated_at < created_at;
