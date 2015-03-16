CREATE EVENT clearExpiredRegistration  ON SCHEDULE  EVERY 1 HOUR DO DELETE FROM yagra.users WHERE users.confirmed=0 and TIMESTAMPDIFF(SECOND, yagra.users.register_on, NOW()) > 3600;  
SET GLOBAL event_scheduler = ON; 

--drop event clearExpiredRegistration;
