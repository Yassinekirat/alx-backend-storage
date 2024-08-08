-- SQL script to create a trigger that resets the valid_email attribute when the email is changed

DELIMITER //

CREATE TRIGGER reset_valid_email_before_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;

//

DELIMITER ;