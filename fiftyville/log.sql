-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports
WHERE street = 'Humphrey Street';

23/7/28
Robbery took place at 10:15 AM. 3 witnesses. Bakery mentioned.
Check transcript of witnesses mentioning the bakery.
SELECT * FROM interviews
WHERE transcript LIKE '%bakery%';

Robber left at around 10:25AM (Ruth) and is booking a flight for the 23/7/29 (Raymond)
They stopped by the ATM (Eugene)

Ruth said we should check the footage in the bakery.
SELECT * FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10;

check the names
SELECT * FROM people, bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10;
shorten time frame
SELECT * FROM people, bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 10 AND 30;
Too much, simplify and shorten
SELECT bsl.year, bsl.month, bsl.day, bsl.hour, bsl.minute, p.name, bsl.activity, bsl.license_plate
FROM bakery_security_logs bsl
JOIN people p ON p.license_plate = bsl.license_plate
WHERE bsl.year = 2023 AND bsl.month = 7 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute BETWEEN 10 AND 30;

check atm transactions on leggat street based on witness 2:

SELECT * FROM atm_transactions
WHERE atm_location = 'Leggett Street'
AND year = 2023 AND month = 7 AND day = 28;

check name of withdraws:
SELECT a.*, p.name
FROM atm_transactions a
JOIN bank_accounts b ON a.account_number = b.account_number
JOIN people p ON b.person_id = p.id
WHERE a.atm_location = 'Leggett Street' AND a.year = 2023 AND a.month = 7 AND a.day = 28 AND a.transaction_type = 'withdraw';

check phone call logs from witness 3. Around 60 seconds long
SELECT *
FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60;

check names
SELECT p.name, pc.caller, pc.receiver, pc.year, pc.month, pc.day, pc.duration
FROM phone_calls pc
JOIN people p ON pc.caller = p.phone_number
WHERE pc.year = 2023 AND pc.month = 7 AND pc.day = 28 AND pc.duration <= 60;

next I have to find the next airport out of fiftyville
SELECT * FROM airports;
--> fiftyville is id 8

I need to check id 8 flights out of fiftyville.
SELECT f.*, origin.full_name AS origin_airport_id, destination.full_name AS destination_airport
FROM flights f
JOIN airports origin ON f.origin_airport_id = origin_airport_id
JOIN airports destination ON f.destination_airport_id = destination.id
WHERE origin.id = 8 AND f.year = 2023 AND f.month = 7 AND f.day = 29
ORDER BY f.hour, f.minute;
Flight out id 36
Fiftyville to LaGuardia airport in New york.

Finding the final name:
SELECT p.name
FROM bakery_security_logs bsl
JOIN people p ON p.license_plate = bsl.license_plate
JOIN bank_accounts ba ON ba.person_id = p.id
JOIN atm_transactions at ON at.account_number = ba.account_number
JOIN phone_calls pc ON pc.caller = p.phone_number
WHERE bsl.year = 2023 AND bsl.month = 7 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute BETWEEN 10 AND 30
AND at.atm_location = 'Leggett Street' AND at.year = 2023 AND at.month = 7 AND at.day = 28 AND at.transaction_type = 'withdraw'
AND pc.year = 2023 AND pc.month = 7 AND pc.day = 28 AND pc.duration <= 60;

Singles out Bruce and Diana. They all fit the requirements. We need to find out which one was on the flight 36.

SELECT p.name
FROM people p
JOIN passengers ps ON p.passport_number = ps.passport_number
WHERE ps.flight_id = 36
AND p.name IN ('Bruce', 'Diana');

Bruce is the Thief

Need to find bruce's accompliss. So Ill check who he calls.

SELECT p2.name AS receiver
FROM phone_calls pc
JOIN people p1 ON pc.caller = p1.phone_number
JOIN people p2 ON pc.receiver = p2.phone_number
WHERE p1.name = 'Bruce' AND pc.year = 2023 AND pc.month = 7 AND pc.day = 28 AND pc.duration <= 60;

He called Robin
