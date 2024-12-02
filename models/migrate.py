from models import Base, engine, init_models

def return_target_metadata():
    return Base.metadata

init_models()
Base.metadata.create_all(bind=engine)
