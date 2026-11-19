-- name: Every user_follow row points at existing users on both sides
-- why: user_follow has no foreign keys
SELECT f.user_follow_id, f.follower_id, f.following_id
FROM user_follow f
LEFT JOIN user u1 ON u1.user_id = f.follower_id
LEFT JOIN user u2 ON u2.user_id = f.following_id
WHERE u1.user_id IS NULL OR u2.user_id IS NULL;
