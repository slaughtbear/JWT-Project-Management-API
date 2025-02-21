from ..config import supabase


def get_all_projects_bd():
    response = supabase.table("projects").select("*").execute()
    return response.data


def get_one_project(id: int):
    response = supabase.table("projects").select("id").eq("id", id).execute()
    return response.data[0]