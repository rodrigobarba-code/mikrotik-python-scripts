# Importing Necessary Libraries
from sqlalchemy import func
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# Importing Necessary Libraries

# Creating Instances of SQLAlchemy and Migrate
func = func
db = SQLAlchemy()
migrate = Migrate()
# Creating Instances of SQLAlchemy and Migrate
