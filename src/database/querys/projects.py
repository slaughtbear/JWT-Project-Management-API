from ..config import supabase


def get_all_projects_bd():
    response = supabase.table("projects").select("*").execute()
    return response.data


def get_one_project_bd(id: int):
    response = supabase.table("projects").select("*").eq("id", id).execute()
    return None if not response.data else response.data[0]


def get_one_project_by_name_bd(name: str):
    response = supabase.table("projects").select("*").eq("name", name).execute()
    return None if not response.data else response.data[0]


def create_project_bd(project_data):
    response = supabase.table("projects").insert(project_data.model_dump()).execute()
    return response.data[0]

    
def update_project_bd(project_data, id: int):
    response = supabase.table("projects").update(project_data.model_dump()).eq("id", id).execute()
    return response.data[0]


def delete_project_bd(id: int):
    response = supabase.table("projects").delete().eq("id", id).execute()
    return response.data