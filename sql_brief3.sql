CREATE DATABASE matches;

USE matches;

CREATE TABLE matches (
edition INT,
round VARCHAR(255),
home_team VARCHAR(255),
away_team VARCHAR(255),
date VARCHAR(255),
home_result INT,
away_result INT,
result VARCHAR(255),
city VARCHAR(255),
id_match VARCHAR(255))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Nombre de matchs nuls en Poules par edition
SELECT edition, round, result, COUNT(id_match) nb_nuls 
FROM matches
GROUP BY edition, round, result
HAVING round = 'Poules' AND result = 'draw'
ORDER BY nb_nuls DESC;

-- Moyenne de buts marqués par match par edition
SELECT edition, ROUND(AVG(home_result + away_result),2) moyenne_ecart 
FROM matches
GROUP BY edition
ORDER BY moyenne_ecart DESC;

-- TOP 20 des matchs avec le plus gros écart de buts
SELECT edition, round, home_team, away_team, result, ABS(home_result - away_result) difference_de_but 
FROM matches
WHERE ABS(home_result - away_result) > 2
ORDER BY difference_de_but DESC
LIMIT 20;

-- Moyenne de buts par match
select round(avg(home_result + away_result),2) as moyenne_buts
from matches;

-- Top 5 des années avec le plus de matchs nul 
select edition, count(*) as match_nul
from matches 
where result = 'draw'
group by edition
order by match_nul desc
limit 5; 

-- Top 10 des années avec le plus de buts marqués en finale
select edition, sum(home_result + away_result) as buts
from matches 
where round = 'Finale'
group by edition
order by buts desc 
limit 10 ; 

-- Moyenne de buts par type de matchs : 
select round, round(avg(home_result + away_result),2) as moyenne_buts
from matches 
group by round
order by moyenne_buts desc 
limit 10 ; 

-- Match avec le plus de buts 
select *, (home_result + away_result) as total_buts 
from matches 
order by total_buts desc
limit 1
