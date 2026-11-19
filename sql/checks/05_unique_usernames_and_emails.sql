-- name: Usernames and emails are unique, ignoring case
-- why: "Amy@x.com" and "amy@x.com" must not be two accounts
SELECT 'username' AS field, LOWER(username) AS value, COUNT(*) AS n FROM user GROUP BY LOWER(username) HAVING COUNT(*) > 1
UNION ALL
SELECT 'email', LOWER(email), COUNT(*) FROM user GROUP BY LOWER(email) HAVING COUNT(*) > 1;
