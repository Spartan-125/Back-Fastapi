# alembic_init.py
import os
import subprocess

def init_alembic():
    # Initialize alembic
    subprocess.run(["alembic", "init", "migrations"])
    
    # Update alembic.ini
    with open('alembic.ini', 'r') as file:
        content = file.read()
        
    # Replace sqlalchemy.url with our dynamically configured URL
    content = content.replace(
        'sqlalchemy.url = driver://user:pass@localhost/dbname',
        'sqlalchemy.url = '  # Leave empty to be configured in env.py
    )
    
    with open('alembic.ini', 'w') as file:
        file.write(content)
    
    # Update env.py to use our database configuration
    with open('migrations/env.py', 'r') as file:
        content = file.read()
    
    # Add imports for our app configuration
    import_str = """
from app.config.settings import get_settings
from app.config.database import Base
from app.domain.entities import User, Item

settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
target_metadata = Base.metadata
    """
    
    # Replace the target_metadata line
    content = content.replace(
        'target_metadata = None',
        'target_metadata = Base.metadata'
    )
    
    # Find the place to insert our imports
    import_loc = content.find('from alembic import context')
    if import_loc != -1:
        # Find the end of the import section
        import_end = content.find('\n\n', import_loc)
        if import_end != -1:
            # Insert our imports after the existing imports
            content = content[:import_end] + import_str + content[import_end:]
    
    with open('migrations/env.py', 'w') as file:
        file.write(content)
    
    print("Alembic initialized with the proper configuration!")
    print("Run 'alembic revision --autogenerate -m \"Initial migration\"' to create your first migration!")

if __name__ == "__main__":
    init_alembic()