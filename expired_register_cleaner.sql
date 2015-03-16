CREATE EVENT clearExpiredRegistration  ON SCHEDULE  EVERY 1 HOUR DO BEGIN  DELETE FROM yagra.users WHERE TIMESTAMPDIFF(SECOND, yagra.users.register_on, NOW()) > 3600 END;
SET GLOBAL event_scheduler = ON; 

--drop event clearExpiredRegistration;
