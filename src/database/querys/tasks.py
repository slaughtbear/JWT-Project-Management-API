from ..config import supabase

def get_all_tasks_bd(id_user: int):
    response = supabase.table("tasks").select("*").eq("id_user", id_user).execute()
    return response.data


def get_one_task_bd(id_project: int, id_user: int):
    response = supabase.table("tasks").select("*").eq("id", id_project).eq("id_user", id_user).execute()
    return None if not response.data else response.data[0]


def get_one_task_by_title_bd(title: str):
    response = supabase.table("tasks").select("*").eq("title", title).execute()
    return None if not response.data else response.data[0]


def create_task_bd(task_data, current_user):
    task_dict = task_data.model_dump()
    response = (
        supabase.table("tasks")
        .insert({
            "title": task_dict["title"],
            "description": task_dict["description"],
            "project_id": task_dict["project_id"],
            "id_user": current_user["id"]
        })
        .execute()
    )
    return response.data[0]

    
def update_task_bd(task_data, id):
    response = supabase.table("tasks").update(task_data.model_dump()).eq("id", id).execute()
    return response.data[0]


def delete_task_bd(id):
    response = supabase.table('tasks').delete().eq('id', id).execute()
    return response.data
