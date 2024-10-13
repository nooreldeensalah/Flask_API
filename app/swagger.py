from flask_restx import Api, Namespace, Resource, fields


# Create a Namespace
api = Namespace('Users', description='User related operations')

# Define User Model for Swagger
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='User email'),
    'phone_number': fields.String(required=True, description='Phone number'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(required=True, description='Admin status')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Define Swagger security schemes
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Bearer Token. Example: "Bearer <your-token>"'
    }
}

# Function to initialize and return the API instance
def create_api(app):
    api = Api(
        app,
        title='Flask Demo API',
        version='1.0',
        description='A simple demonstration of a Flask REST API with Swagger',
        doc='/docs',
        authorizations=authorizations
    )
    return api
