-- If user does not click the confirm link in time, 
-- registration is expired, should be delete it.

-- create event.
CREATE EVENT clearExpiredRegistration  
ON SCHEDULE  
EVERY 1 HOUR 
DO  
    DELETE FROM yagra.users WHERE users.confirmed=0 and TIMESTAMPDIFF(SECOND, yagra.users.register_on, NOW()) > 3600;  

-- enable event.
SET GLOBAL event_scheduler = ON; 

--drop event.
--drop event clearExpiredRegistration;
