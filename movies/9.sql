SELECT DISTINCT people.name
FROM people
JOIN starts ON people.id = starts.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.year = 2004
ORDER BY people.birth;
