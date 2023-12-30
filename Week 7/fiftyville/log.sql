-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Trying to get a feel of the database.
.schema

-- Get description about the crime
SELECT description FROM 
crime_scene_reports 
WHERE year = 2021 AND day = 28 AND 
month = 7 AND street = "Humphrey Street";

-- Get witness reports about incidents at a bakery
SELECT * FROM interviews WHERE transcript LIKE "%bakery%";

-- Get lisence plate number of people that left about ten minutes after theft
SELECT activity, license_plate FROM 
bakery_security_logs 
WHERE year = 2021 AND month = 7 
AND day = 28 AND hour = 10 AND 
minute <= 25 AND minute > 22;

--Get the caller and reciever numbers of potential suspect, just need to cross reference with 
-- liscence plate numbers
SELECT caller, receiver FROM phone_calls 
WHERE year = 2021 AND day = 28 AND month = 7 
AND duration < 60;

-- Get names of people in the caller list whose licence plates we found previously
SELECT name FROM people WHERE phone_number 
in (SELECT caller FROM phone_calls WHERE 
year = 2021 AND day = 28 AND month = 7 
AND duration < 60) 
INTERSECT 
SELECT name FROM people WHERE 
license_plate IN 
(SELECT license_plate FROM bakery_security_logs 
WHERE year = 2021 AND month = 7 AND 
day = 28 AND minute <= 25 AND minute > 22);

-- Get diana , bruce and kelsey's phone numbers since the license plates were 
--registered to them
SELECT phone_number FROM people WHERE name = "Diana" OR name = "Kelsey" or name = "Bruce";

-- get the numbers of the people they called
SELECT caller, receiver FROM 
phone_calls WHERE year = 2021 
AND day = 28 AND month = 7 AND 
duration < 60 AND caller IN 
(SELECT phone_number FROM 
people WHERE name = "Diana" 
OR name = "Kelsey" or name = "Bruce");

-- Get info about withdrawls made from Leggett street ATM
SELECT * FROM atm_transactions 
WHERE year = 2021 AND month = 7 
AND day = 28 AND atm_location = "Leggett Street" 
AND transaction_type = "withdraw";

-- get person ids of people who made the sus transaction from leggett street 
SELECT person_id FROM bank_accounts 
WHERE account_number IN 
(SELECT account_number FROM 
atm_transactions WHERE year = 2021 
AND day = 28 AND month = 7 
AND atm_location = "Leggett Street" 
AND transaction_type = "withdraw");

-- Get their names , kelsey eliminated, diana and bruce prime suspect
SELECT name FROM people WHERE id IN 
(SELECT person_id FROM bank_accounts 
WHERE account_number IN 
(SELECT account_number FROM atm_transactions 
WHERE year = 2021 AND day = 28 AND month = 7 
AND atm_location = "Leggett Street" 
AND transaction_type = "withdraw"));

-- Get the number of the people they called
SELECT receiver FROM phone_calls 
WHERE year = 2021 AND day = 28 
AND month = 7 AND duration < 60 
AND caller IN 
(SELECT phone_number FROM people WHERE name = "Diana"
or name = "Bruce");

-- Get their names (robin)
-- How could they! they were suppoused to be the protecters of gotham
SELECT name from people WHERE phone_number = 
(SELECT receiver FROM phone_calls 
WHERE year = 2021 AND day = 28 
AND month = 7 AND duration < 60 
AND caller IN 
(SELECT phone_number FROM people WHERE name = "Diana"
or name = "Bruce"));

-- Get fight information abou the first flight out of the 
--city the day after the crime

SELECT * FROM flights 
WHERE day = 29 AND year = 2021 AND month = 7 
AND origin_airport_id IN 
(SELECT id FROM airports 
WHERE city = "Fiftyville") 
ORDER BY hour LIMIT 1;

-- confirm that bruce was on the flight
SELECT passport_number FROM passengers 
WHERE flight_id = 36 
INTERSECT 
SELECT passport_number 
FROM people WHERE name = "Bruce";

-- get info about the airport where the flight landed
SELECT * FROM airports WHERE id = 4;


-- Sooo... Bruce and Robin stole the CS50 duck and then
-- escaped to Gotham... I mean... NYC...

-- Wow... solving this mystery was the most fun ive had in a while... Thnaks CS50!

