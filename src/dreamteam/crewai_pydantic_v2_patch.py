"""
Patch module to migrate CrewAI internal Pydantic models to V2
"""
from pydantic import ConfigDict
import crewai
import crewai.agents.executor as executor_mod
import crewai.task as task_mod
# Patch CrewAgentExecutor
class CrewAgentExecutorV2(executor_mod.CrewAgentExecutor):
    # Use Pydantic V2 ConfigDict
    model_config: ConfigDict = ConfigDict()
executor_mod.CrewAgentExecutor = CrewAgentExecutorV2
# Patch Task
class TaskV2(task_mod.Task):
    # Use Pydantic V2 ConfigDict
    model_config: ConfigDict = ConfigDict()
task_mod.Task = TaskV2
# Alias field_validator to model_validator for Pydantic V2
task_mod.field_validator = task_mod.model_validator
