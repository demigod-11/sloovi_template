# REST APi
    Restful Api

    This Project is built with
    - Python, Flask, MongoDB, JWT

## Dependencies
    Modules and versions used are stored in requirements.txt
    the program has no dependency save python >= 3.6



## API Documentation
### EndPoints
### UserController Endpoints
    - @route /register
    - @method POST
    - @access PUBLIC
    - @headers {
                'Accept': 'application/json',
                'Content-Type': 'application/json' 
               }
    - @user {
            first_name : string
            last_name : string
            email : string
            password : string
        }
    - @desc 
        registers user to the application
    - @ returns {
        201} 0r 404 if error ocurred
    
    

    - @route /login
    - @method POST
    - @access PUBLIC
    - @headers {
                'Accept': 'application/json',
                'Content-Type': 'application/json' 
               }
    - @user {
            email : string,
            password : string
        }
    - @desc 
        login user to the application
    - @ returns {
        current_user} 0r 404 if error ocurred
    

### template End Point
    - @route /template
    - @method POST
    - @access PRIVATE
    - @headers {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
               }
    - @user {
            'template_name': string,
            'subject': string,
            'body': string,
        }
    - @desc 
        inputs a template to the database specific to the user
    - @ returns {
        201} 0r 404 if error ocurred
    


    - @route /template
    - @method GET
    - @access PRIVATE
    - @headers {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
               }
    - @user {
           
        }
    - @desc 
        returns all the templates from the database inputed by the user
    - @ returns {
        201} 0r 404 if error occured
    

### template/:id EndPoint
    - @route /template/<string:template_id>
    - @method GET
    - @access PRIVATE
    - @headers {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
               }
    - @user {
           
        }
    - @desc 
        returns template with id=template_id from the database
    - @ returns {
        201} 0r 404 if error occured
    


    - @route /template/<string:template_id>
    - @method PUT
    - @access PRIVATE
    - @headers {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
               }
    - @user {
           
        }
    - @desc 
        edits template with id = tenplate_id
    - @ returns {
        201} 0r 404 if error occured
    


    - @route /template/<string:template_id>
    - @method DELETE
    - @access PRIVATE
    - @headers {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
               }
    - @user {
           
        }
    - @desc 
        deletes template with id = tenplate_id
    - @ returns {
        204} 0r 404 if error occured



## Example Usage
    base_url/register
    base_url/login
    base_url/template
    base_url/template/<string:template_id>


## Environment Variable
    MongoClient = mongodb+srv://Username:Password@cluster0.faczi20.mongodb.net/?retryWrites=true&w=majority





