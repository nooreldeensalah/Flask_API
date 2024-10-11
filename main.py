from app import create_app
from app.models import Product, Order, OrderItem, User
from sqlalchemy_data_model_visualizer import generate_data_model_diagram

# Create the app instance
app = create_app()

# Generate ER Diagram
generate_data_model_diagram([Product, Order, OrderItem, User], "diagram")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

