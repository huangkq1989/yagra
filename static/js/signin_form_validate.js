$(document).ready(function() {                                                  
    var info = $("#error-info").val();                                            
    if(info) {                                                                    
        alert(info);                                                                
    }                                                                             
    $('#signin_form').bootstrapValidator({                                         
        message: 'This value is not valid',                                         
        fields: {                                                                   
            name: {                                                                  
                validators: {                                                           
                    notEmpty: {                                                           
                        message: 'The name is required and cannot be empty'             
                    },                                                                      
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'The username must be more than 6 and less than 30 characters long'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_]+$/,
                        message: 'The username can only consist of alphabetical, number and underscore'
                    }
                }                                                                       
            },                                                                        
            password: {                                                               
                validators: {                                                           
                    notEmpty: {                                                           
                        message: 'The password is required and cannot be empty'             
                    },                                                                    
                }                                                                       
            },                                                                        
        }                                                                           
    });                                                                           
});
