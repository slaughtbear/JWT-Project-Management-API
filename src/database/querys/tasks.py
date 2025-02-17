from ..config import supabase

def get_all_tasks():
    response = supabase.table("tasks").select("*").execute()
    return response.data

def get_one_task(id: int):
    response = supabase.table("tasks").select("*").eq("id", id).execute()
    return response.data

def get_one_task_by_title(title: str):
    response = supabase.table("tasks").select("*").eq("title", title).execute()
    return response.data

def create_task(task_data):
    response = supabase.table("tasks").insert(task_data.model_dump()).execute()
    return response.data

    