from ..config import supabase


def get_all_projects_bd(id_user: int):
    response = supabase.table("projects").select("*").eq("id_user", id_user).execute()
    return response.data


def get_one_project_bd(id_project: int, id_user: int):
    response = supabase.table("projects").select("*").eq("id", id_project).eq("id_user", id_user).execute()
    return None if not response.data else response.data[0]


def get_one_project_by_name_bd(name: str):
    response = supabase.table("projects").select("*").eq("name", name).execute()
    return None if not response.data else response.data[0]


def create_project_bd(project_data, current_user):
    project_dict = project_data.model_dump()
    response = (
        supabase.table("projects")
        .insert({
            "name": project_dict["name"],
            "description": project_dict["description"],
            "id_user": current_user["id"]
        })
        .execute()
    )
    return response.data[0]

    
def update_project_bd(project_data, id: int):
    response = supabase.table("projects").update(project_data.model_dump()).eq("id", id).execute()
    return response.data[0]


def delete_project_bd(id: int):
    response = supabase.table("projects").delete().eq("id", id).execute()
    return response.data