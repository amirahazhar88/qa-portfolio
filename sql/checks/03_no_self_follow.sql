-- name: Nobody follows themselves
-- why: the API rejects it (400); the table must agree
SELECT user_follow_id, follower_id
FROM user_follow
WHERE follower_id = following_id;
