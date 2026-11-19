-- name: record_status only holds values the app understands (active or deleted)
-- why: soft delete is how every list in the API hides data
SELECT 'article' AS tbl, record_status, COUNT(*) AS n FROM article WHERE record_status NOT IN ('active','deleted') OR record_status IS NULL GROUP BY record_status
UNION ALL SELECT 'article_comment', record_status, COUNT(*) FROM article_comment WHERE record_status NOT IN ('active','deleted') OR record_status IS NULL GROUP BY record_status
UNION ALL SELECT 'article_favorite', record_status, COUNT(*) FROM article_favorite WHERE record_status NOT IN ('active','deleted') OR record_status IS NULL GROUP BY record_status
UNION ALL SELECT 'article_tag', record_status, COUNT(*) FROM article_tag WHERE record_status NOT IN ('active','deleted') OR record_status IS NULL GROUP BY record_status
UNION ALL SELECT 'user_follow', record_status, COUNT(*) FROM user_follow WHERE record_status NOT IN ('active','deleted') OR record_status IS NULL GROUP BY record_status;
