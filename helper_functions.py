def username_in_list(user, list):

    for i in list:

        if i.username == user:

            return True

    return False

def remove_leading_and_trailing_spaces(list):

    modified_list = []

    for i in list:

        str = i.strip()

        modified_list.append(str)
    
    return modified_list
    


        