# """_summary_
# """

# from tests.mock_flask import MockFlask
# from werkzeug.test import TestResponse
# from pprint import pprint

# from os import path, getcwd

# # url = "http://host:port/endpoint"
# # path_img = os.path(os.getcwd(), "upload", "Screenshot_2024-04-19_172523.png")
# # with open(path_img, "rb") as img:
# #     name_img = os.path.basename(path_img)
# #     files = {"image": (name_img, img, "multipart/form-data", {"Expires": "0"})}
# #     with requests.Session() as s:
# #         r = s.post(url, files=files)
# #         print(r.status_code)


# class TestUserViews(MockFlask):

#     def test_user_register(self):
#         path_img = path.join(getcwd(), "upload", "Screenshot_2024-04-19_172523.png")
#         # print(path.join(getcwd(), "halo"))
#         print(path_img)
#         with open(path_img, "rb") as img:
#             name_img = path.basename(path_img)
#             files = {"image": (name_img, img, "multipart/form-data", {"Expires": "0"})}
#             with requests.Session() as s:
#                 r = s.post(url, files=files)
#                 print(r.status_code)
#         response: TestResponse = self.client.post(
#             "image",
#             headers={
#                 "content-type": "multipart/form-data",
#                 "accept": "application/json",
#             },
#             data={"image": path_img},
#         )
#         pprint("\nRegister response")
#         pprint(response.get_json(), indent=2)
