from ..config import supabase

def get_all_tasks_bd():
    response = supabase.table("tasks").select("*").execute()
    return response.data


def get_one_task_bd(id: int):
    response = supabase.table("tasks").select("*").eq("id", id).execute()
    return response.data[0]


def get_one_task_by_title_bd(title: str):
    response = supabase.table("tasks").select("*").eq("title", title).execute()
    return response.data


def create_task_bd(task_data):
    response = supabase.table("tasks").insert(task_data.model_dump()).execute()
    return response.data[0]

    
def update_task_bd(task_data, id):
    response = supabase.table("tasks").update(task_data.model_dump()).eq("id", id).execute()
    return response.data[0]


def delete_task_bd(id):
    response = supabase.table('tasks').delete().eq('id', id).execute()
    return response.data
