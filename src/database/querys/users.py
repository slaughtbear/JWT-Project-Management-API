from ..config import supabase


def get_all_users_db():
    response = supabase.table("users").select("*").execute()
    return response.data


def get_one_user_db(id: int):
    response = supabase.table("users").select("*").eq("id", id).execute()
    return response.data[0]

def get_one_user_by_username_bd(username):
    response = supabase.table("users").select("*").eq("username", username).execute()
    return response.data[0]