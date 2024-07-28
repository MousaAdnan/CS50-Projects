SELECT people.name
FROM people
JOIN starts ON people.id = starts.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.title = 'Toy Story';
