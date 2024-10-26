-- SQL script that creates a trigger to reset the attribute valid_email only when the email has been changed.
-- create the trigger
DELIMITER $$

CREATE TRIGGER on_email_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email has been changed
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END$$

DELIMITER ;
