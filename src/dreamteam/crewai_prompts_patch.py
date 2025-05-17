"""
Patch module to migrate CrewAI prompt models to Pydantic V2
"""
from pydantic import ConfigDict
import crewai.prompts as prompts_mod

# Apply ConfigDict to all BaseModel subclasses in crewai.prompts
for name, cls in vars(prompts_mod).items():
    try:
        # Check for Pydantic V1 BaseModel subclass
        if hasattr(cls, '__fields__') and hasattr(cls, 'model_fields'):
            setattr(cls, 'model_config', ConfigDict())
    except Exception:
        pass
