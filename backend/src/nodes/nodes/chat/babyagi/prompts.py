# Zero shot agent prompts
agent_prefix = """You are an AI who performs one task based on the following objective: {objective}. Take into account these previously completed tasks: {context}."""
agent_suffix = """Question: {task}
{agent_scratchpad}"""

# Task creation agent prompt
task_creation_template = (
    "You are an task creation AI that uses the result of an execution agent"
    " to create new tasks with the following objective: {objective},"
    " The last completed task has the result: {result}."
    " This result was based on this task description: {task_description}."
    " These are incomplete tasks: {incomplete_tasks}."
    " Based on the result, create minimum number of new tasks to be completed"
    " by the AI system that do not overlap with incomplete tasks."
    " Return the tasks as an array."
)

# Task prioritization agent prompt
task_prioritization_template = (
    "You are an task prioritization AI tasked with cleaning the formatting of and re-prioritizing"
    " the following tasks: {task_names}."
    " Consider the ultimate objective of your team: {objective}."
    " Do not add new tasks to the list."
    " Remove tasks that are unnecessary for the objective. Return the result as a numbered list, like:"
    " #. First task"
    " #. Second task"
    " Start the task list with number {next_task_id}."
)
