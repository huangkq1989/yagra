$(document).ready(function() {                                                  
    var info = $("#error-info").val();                                            
    if(info) {                                                                    
        alert(info);                                                                
    }                                                                             
    $('#register_form').bootstrapValidator({                                         
        message: 'This value is not valid',                                         
        fields: {                                                                   
            email: {
                validators: {
                    notEmpty: {                                                           
                        message: 'The email is required and cannot be empty'             
                    },                                                                      
                    emailAddress: {
                        message: 'The input is not a valid email address'
                    },
                    remote: {
                        message: 'Email exists',
                        url: '/yagra/register.py/check_email', 
                        type: 'POST', 
                        delay: 2000,
                    }
                }
            },
            name: {                                                                  
                validators: {                                                           
                    notEmpty: {                                                           
                        message: 'The name is required and cannot be empty'             
                    },                                                                      
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'Must be more than 6 and less than 20 characters'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_]+$/,
                        message: 'Alphabetical, number and underscore only'
                    },
                   remote: {
                        message: 'name exists',
                        url: '/yagra/register.py/check_name', 
                        type: 'POST', 
                        delay: 2000,
                    }
                }                                                                       
            },                                                                        
            passwd: {                                                               
                validators: {                                                           
                    notEmpty: {                                                           
                        message: 'The password is required and cannot be empty'             
                    },                                                                    
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'Must be more than 6 and less than 20 characters'
                    },
                }                                                                       
            },                                                                        
        }                                                                           
    });                                                                           
});
