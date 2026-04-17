CREATE DATABASE matches;
USE matches;

-- Si la table n'est pas créée par le script python, il est possible de la créer ici
CREATE TABLE matchs (
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


-- ANALYSE DES DONNEES --

-- Top 5 des années avec le plus de matchs nul 
SELECT edition, count(*) AS match_nul
FROM matchs 
WHERE result = 'draw'
GROUP BY edition
ORDER BY match_nul DESC
LIMIT 5; 

-- Pourcentage de matchs nuls par edition
WITH tot_matchs AS (
		SELECT edition, COUNT(*) nb_matchs FROM matchs
        GROUP BY edition)
SELECT matchs.edition result, ROUND(COUNT(id_match) / nb_matchs * 100, 2) pourcentage_nuls 
FROM matchs
JOIN tot_matchs on tot_matchs.edition = matchs.edition
GROUP BY matchs.edition, result
HAVING result = 'draw'
ORDER BY pourcentage_nuls DESC;
-- Comme il n'y a pas autant de matchs d'une édition à l'autre, on prend le pourcentage de matchs nuls, et pas le nombre brut.
-- C'est en 1958 qu'il y a le plus de matchs nuls : 28.57%

-- Moyenne de buts par match
-- Sur toutes les éditions, la moyenne de but marqués par match et de 2.82.
select round(avg(home_result + away_result),2) as moyenne_buts
from matchs;

-- Moyenne de buts marqués par match par edition
-- L'édition de 1954 est la plus prolifique, avec plus de 5 buts par match en moyenne
SELECT edition, ROUND(AVG(home_result + away_result),2) moyenne_ecart 
FROM matchs
GROUP BY edition
ORDER BY moyenne_ecart DESC;

-- TOP 20 des matchs avec le plus gros écart de buts
SELECT edition, round, home_team, away_team, result, ABS(home_result - away_result) difference_de_but 
FROM matchs
WHERE ABS(home_result - away_result) > 2
ORDER BY difference_de_but DESC
LIMIT 20;
-- Le plus gros écart de but en un match est de 9, avec 3 occurences
-- Puis 3 matchs à 8 buts d'écart
-- La grande majorité de ces matchs sont en Poules, où l'écart de niveau est encore grand.

-- Top 10 des années avec le plus de buts marqués en finale
select edition, sum(home_result + away_result) as buts
from matchs 
where round = 'Finale'
group by edition
order by buts desc 
limit 10 ; 

-- Moyenne de buts par type de matchs : 
select round, round(avg(home_result + away_result),2) as moyenne_buts
from matchs 
group by round
order by moyenne_buts desc 
limit 10 ;
-- La phase avec le plus de buts en moyenne est la Poule Finale,
-- Un format qui n'est arrivé qu'une seule fois en 1950,
-- Il n'y avait pas eu de demi finales et finales, mais une poule.
-- Beaucoup de spectacle en Poule Finale --> Format à réinstaurer ?

-- Match avec le plus de buts : 12 buts marqués
select *, (home_result + away_result) as total_buts 
from matchs 
order by total_buts desc
limit 1;
DROP TABLE matchs