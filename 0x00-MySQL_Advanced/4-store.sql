-- SQL script that creates a trigger to decrease item quantity after adding a new order
-- create the trigger
DELIMITER $$

CREATE TRIGGER after_add_new_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Adjust the quantity of the item in the items table
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END$$

DELIMITER ;
