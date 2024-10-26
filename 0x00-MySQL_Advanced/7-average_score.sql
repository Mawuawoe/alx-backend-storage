-- a SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and update the average score for a student.
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)

-- create the stored procedure

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
DECLARE avg_score FLOAT;

SELECT AVG(score) INTO avg_score
FROM corrections
WHERE user_id = user_id;

UPDATE users
SET average_score = avg_score
WHERE id = user_id;

END $$

DELIMITER ;
