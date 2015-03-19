$(document).ready(function() {                                                  
    var request_root = $("#request_root").val();
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
                        url: request_root + '/app.py/check_email', 
                        type: 'POST', 
                        delay: 50,
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
                        max: 20,
                        message: 'Must be more than 6 and less than 20 characters'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_]+$/,
                        message: 'Alphabetical, number and underscore only'
                    },
                    remote: {
                        message: 'name exists',
                        url: request_root + '/app.py/check_name', 
                        type: 'POST', 
                        delay: 50,
                    }
                }                                                                       
            },                                                                        
            passwd: {                                                               
                validators: {                                                           
                    notEmpty: {                                                           
                        message: 'The password is required and cannot be empty'             
                    },                                                                    
                    callback: {
                        message: 'At least three types of num, lower alphabetical, upper alphabetical and @#$%^&*+=',
                        callback: function(password, validator) {
                            var validCount = 0;
                            var patternStrArray = new Array();
                            patternStrArray.push("^(?=.*[0-9]).{1,}$"); 
                            patternStrArray.push("^(?=.*[a-z]).{1,}$"); 
                            patternStrArray.push("^(?=.*[A-Z]).{1,}$");
                            patternStrArray.push("^(?=.*[@#$%^&\*+=]).{1,}$");
                            for(var idx in patternStrArray) {
                                var patt = new RegExp(patternStrArray[idx]);
                                if(patt.test(password)){
                                    validCount++;
                                }
                            }
                            return validCount >= 3 ? true : false;
                        }
                    },
                    stringLength: {
                        min: 6,
                        max: 13,
                        message: 'Must be 6-13 characters'
                    },
                }                                                                       
            },                                                                        
        }                                                                           
    });                                                                           
});
