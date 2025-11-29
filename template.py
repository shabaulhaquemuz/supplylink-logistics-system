import os  
from pathlib import Path 
import logging 

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "logistics_system"

list_of_files = [
    # ==================== BACKEND ====================
    # User Backend
    "backend/user_backend/main.py",
    "backend/user_backend/database.py",
    "backend/user_backend/models.py",
    
    # Admin Backend
    "backend/admin_backend/main.py",
    "backend/admin_backend/database.py",
    "backend/admin_backend/models.py",
    
    # Driver Backend
    "backend/driver_backend/main.py",
    "backend/driver_backend/database.py",
    "backend/driver_backend/models.py",
    
    # AI Agents (Essential)
    "backend/ai_agents/base_agent.py",
    "backend/ai_agents/dispatch_agent.py",
    "backend/ai_agents/driver_agent.py",
    "backend/ai_agents/customer_agent.py",
    
    # AI Features (Essential)
    "backend/ai_features/route_optimization.py",
    "backend/ai_features/delivery_prediction.py",
    "backend/ai_features/fraud_detection.py",
    
    # Shared (for AI & backends)
    "backend/shared/config.py",
    "backend/shared/utils.py",
    
    # Backend requirements
    "backend/requirements.txt",
    
    # ==================== FRONTEND ====================
    # User Frontend
    "frontend/user/index.html",
    "frontend/user/style.css",
    "frontend/user/script.js",
    
    # Admin Frontend
    "frontend/admin/index.html",
    "frontend/admin/style.css",
    "frontend/admin/script.js",
    
    # Driver Frontend
    "frontend/driver/index.html",
    "frontend/driver/style.css",
    "frontend/driver/script.js",
    
    # ==================== ML FILES ====================
    "ml/model.py",
    "ml/embeddings.py",
    "ml/train.ipynb",
    
    # ==================== DATA & LOGS ====================
    "data/.gitkeep",
    "logs/.gitkeep",
    
    # ==================== CONFIG ====================
    "config/config.yaml",
    ".env.example",
    ".gitignore",
    "README.md",
    "requirements.txt",
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

logging.info(f"\n✅ {project_name} - SIMPLE AI-POWERED structure created!\n")
logging.info("=" * 60)
logging.info("\n📁 STRUCTURE:")
logging.info("Backend: main.py, database.py, models.py (3 apps)")
logging.info("AI Agents: 4 agents (dispatch, driver, customer, base)")
logging.info("AI Features: 3 features (route, prediction, fraud)")
logging.info("Frontend: index.html, style.css, script.js (3 interfaces)")
logging.info("ML: model.py, embeddings.py, train.ipynb")
logging.info("Shared: config.py, utils.py")
logging.info("\n" + "=" * 60)
logging.info("\n🤖 AI COMPONENTS:")
logging.info("   ├── ai_agents/")
logging.info("   │   ├── base_agent.py        → Base class for all agents")
logging.info("   │   ├── dispatch_agent.py    → Auto dispatch decisions")
logging.info("   │   ├── driver_agent.py      → Driver assistance")
logging.info("   │   └── customer_agent.py    → Customer support")
logging.info("   └── ai_features/")
logging.info("       ├── route_optimization.py    → Smart routing")
logging.info("       ├── delivery_prediction.py   → ETA prediction")
logging.info("       └── fraud_detection.py       → Fraud monitoring")
logging.info("\n🚀 Start simple, add files when needed!")