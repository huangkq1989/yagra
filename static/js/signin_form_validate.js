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
                        message: 'Must be more than 6 and less than 30 characters'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_]+$/,
                        message: 'Alphabetical, number and underscore only'
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
