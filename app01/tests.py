from django.test import TestCase

# Create your tests here.


oral_list = [{'permissions__url': '/users/',
              'permissions__group_id': 1,
              'permissions__action': 'list'},

             {'permissions__url': '/users/add/',
              'permissions__group_id': 1,
              'permissions__action': 'add'},

             {'permissions__url': '/users/delete/(\\d+)',
              'permissions__group_id': 1,
              'permissions__action': 'delete'},

             {'permissions__url': 'users/edit/(\\d+)',
              'permissions__group_id': 1,
              'permissions__action': 'edit'},

             {'permissions__url': '/roles/',
              'permissions__group_id': 2,
              'permissions__action': 'list'}
             ]

new_dict = {}

for i in oral_list:
    name = i["permissions__group_id"]
    if not new_dict.get(name):
        new_dict[name] = {
            "urls":[i["permissions__url"]],
            "actions":[i["permissions__action"]]
        }
    else:
        new_dict[name]["urls"].append(i["permissions__url"])
        new_dict[name]["actions"].append(i["permissions__action"])



print(new_dict)
