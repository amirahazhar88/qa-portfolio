-- name: Every user email looks like an email address
-- known: BUG-005 (registration accepts an invalid email, so bad rows get in)
SELECT user_id, username, email
FROM user
WHERE email NOT REGEXP '^[^@ ]+@[^@ ]+[.][^@ ]+$';
