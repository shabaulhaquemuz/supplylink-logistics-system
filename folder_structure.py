import os  
from pathlib import Path 
import logging 

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "logistics_system"

list_of_files = [
    # GitHub workflows
    ".github/workflows/.gitkeep",
    
    # Backend structure
    "backend/__init__.py",
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/config.py",
    
    # API structure
    "backend/app/api/__init__.py",
    "backend/app/api/deps.py",
    "backend/app/api/v1/__init__.py",
    "backend/app/api/v1/api.py",
    "backend/app/api/v1/endpoints/__init__.py",
    "backend/app/api/v1/endpoints/shipments.py",
    "backend/app/api/v1/endpoints/orders.py",
    "backend/app/api/v1/endpoints/tracking.py",
    "backend/app/api/v1/endpoints/inventory.py",
    "backend/app/api/v1/endpoints/warehouse.py",
    "backend/app/api/v1/endpoints/dispatch.py",
    "backend/app/api/v1/endpoints/auth.py",
    
    # Core
    "backend/app/core/__init__.py",
    "backend/app/core/config.py",
    "backend/app/core/security.py",
    
    # Database
    "backend/app/db/__init__.py",
    "backend/app/db/base.py",
    "backend/app/db/session.py",
    
    # Models (SQLAlchemy)
    "backend/app/models/__init__.py",
    "backend/app/models/shipment.py",
    "backend/app/models/order.py",
    "backend/app/models/inventory.py",
    "backend/app/models/warehouse.py",
    "backend/app/models/tracking.py",
    "backend/app/models/user.py",
    
    # Schemas (Pydantic)
    "backend/app/schemas/__init__.py",
    "backend/app/schemas/shipment.py",
    "backend/app/schemas/order.py",
    "backend/app/schemas/inventory.py",
    "backend/app/schemas/warehouse.py",
    "backend/app/schemas/tracking.py",
    "backend/app/schemas/user.py",
    
    # CRUD operations
    "backend/app/crud/__init__.py",
    "backend/app/crud/base.py",
    "backend/app/crud/shipment.py",
    "backend/app/crud/order.py",
    "backend/app/crud/inventory.py",
    "backend/app/crud/warehouse.py",
    
    # Services (Business Logic)
    "backend/app/services/__init__.py",
    "backend/app/services/shipment_service.py",
    "backend/app/services/order_service.py",
    "backend/app/services/embedding_service.py",
    "backend/app/services/tracking_service.py",
    
    # Embeddings
    "backend/app/embeddings/__init__.py",
    "backend/app/embeddings/vector_db.py",
    "backend/app/embeddings/embedder.py",
    "backend/app/embeddings/search.py",
    
    # Utils
    "backend/app/utils/__init__.py",
    "backend/app/utils/helpers.py",
    "backend/app/utils/validators.py",
    
    # Backend requirements
    "backend/requirements.txt",
    
    # Frontend structure
    "frontend/pages/index.html",
    "frontend/pages/dashboard.html",
    "frontend/pages/shipments.html",
    "frontend/pages/orders.html",
    "frontend/pages/tracking.html",
    "frontend/pages/inventory.html",
    "frontend/pages/warehouse.html",
    "frontend/pages/dispatch.html",
    
    # Frontend CSS
    "frontend/css/style.css",
    "frontend/css/dashboard.css",
    "frontend/css/components.css",
    "frontend/css/responsive.css",
    
    # Frontend JavaScript
    "frontend/js/app.js",
    "frontend/js/api.js",
    "frontend/js/config.js",
    "frontend/js/utils.js",
    "frontend/js/modules/dashboard.js",
    "frontend/js/modules/shipments.js",
    "frontend/js/modules/orders.js",
    "frontend/js/modules/tracking.js",
    "frontend/js/modules/inventory.js",
    "frontend/js/modules/warehouse.js",
    
    # Frontend components
    "frontend/components/navbar.html",
    "frontend/components/sidebar.html",
    "frontend/components/footer.html",
    
    # Frontend assets
    "frontend/assets/images/.gitkeep",
    "frontend/assets/icons/.gitkeep",
    
    # Static files (served by FastAPI)
    "static/uploads/.gitkeep",
    
    # Data directories
    "data/vector_store/.gitkeep",
    "data/uploads/.gitkeep",
    
    # Tests
    "tests/__init__.py",
    "tests/test_api/__init__.py",
    "tests/test_api/test_shipments.py",
    "tests/test_api/test_orders.py",
    "tests/test_embeddings/__init__.py",
    "tests/test_embeddings/test_vector_search.py",
    
    # Research/trials
    "research/trials.ipynb",
    "research/embedding_experiments.ipynb",
    
    # Config files
    "config/config.yaml",
    "config/database.yaml",
    "params.yaml",
    "dvc.yaml",
    
    # Root files
    ".env.example",
    ".gitignore",
    "README.md",
    "requirements.txt",
    "setup.py",
    "docker-compose.yml",
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

logging.info(f"\n{project_name} folder structure created successfully!")
logging.info("Don't forget to create your virtual environment: python -m venv venv")