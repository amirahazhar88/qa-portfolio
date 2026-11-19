-- name: A user favorites an article at most once and follows a user at most once
-- why: the counts shown in the app are derived from these rows
SELECT 'favorite' AS kind, user_id AS who, article_id AS what, COUNT(*) AS n
FROM article_favorite GROUP BY user_id, article_id HAVING COUNT(*) > 1
UNION ALL
SELECT 'follow', follower_id, following_id, COUNT(*)
FROM user_follow GROUP BY follower_id, following_id HAVING COUNT(*) > 1;
