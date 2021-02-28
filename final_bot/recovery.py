from user import User
from google_db import get_data

def start_rec():
    user_dict = {}
    token_set = set()
    raw_data = get_data()
    for elm in raw_data:
        temp_user = User()
        temp_user.name = elm[0]
        temp_user.surname = elm[1]
        temp_user.success = True
        user_dict[elm[3]] = temp_user
        token_set.add(elm[4])
    return user_dict, token_set