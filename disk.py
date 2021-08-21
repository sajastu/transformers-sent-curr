import os

home_dir = "/home/code-base"
archive_space = os.environ['INTERACTIVE_SESSION_ARCHIVE']
scratch_space = os.environ['SENSEI_SCRATCH_DIR']
user_space = os.environ['SENSEI_USERSPACE_SELF']
session_id = os.environ['tensorboard_base_url'].split("/")[1]
# print("Home directory at: " + home_dir)
# print("Archive space at: " + archive_space)
# print("Scratch space at: " + scratch_space)
print(user_space)


# print("Interactive session id: " + session_id)
# pattern = re.compile("SENSEI_USERSPACE.*ADOBE")
# for env in os.environ:
#     if pattern.match(env):
#         print(env)
# user_space_str = "user_space"
# archive_space_str = "archive_space"
# scratch_space_str = "scratch_space"

