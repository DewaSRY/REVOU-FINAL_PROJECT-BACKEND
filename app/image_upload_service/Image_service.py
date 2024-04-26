# import os
# import re
# from typing import Union
# from werkzeug.datastructures import FileStorage
# from flask_uploads import UploadSet, IMAGES


# class ImageService:
#     IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions

#     @classmethod
#     def save_image(cls, image: FileStorage, folder: str = None, name: str = None) -> str:
#         return cls.IMAGE_SET.save(image, folder, name)

#     @classmethod
#     def get_path(cls, filename: str = None, folder: str = None) -> str:
#         return cls.IMAGE_SET.path(filename, folder)

#     @classmethod
#     def find_image_any_format(cls, filename: str, folder: str) -> Union[str, None]:
#         """
#         Given a format-less filename, try to find the file by appending each of the allowed formats to the given
#         filename and check if the file exists
#             :param filename: formatless filename
#             :param folder: the relative folder in which to search
#             :return: the path of the image if exists, otherwise None
#         """
#         for _format in cls.IMAGES:  # look for existing avatar and delete it
#             avatar = f"{filename}.{_format}"
#             avatar_path = cls\
#                     .IMAGE_SET\
#                     .path(filename=avatar, folder=folder)
#             if os.path.isfile(avatar_path):
#                 return avatar_path
#         return None

#     @classmethod
#     def _retrieve_filename(file: Union[str, FileStorage]) -> str:
#         """
#         Make our filename related functions generic, able to deal with FileStorage object as well as filename str.
#         """
#         if isinstance(file, FileStorage):
#             return file.filename
#         return file

#     @classmethod
#     def is_filename_safe(cls, file: Union[str, FileStorage]) -> bool:
#         """
#         Check if a filename is secure according to our definition
#             - starts with a-z A-Z 0-9 at least one time
#             - only contains a-z A-Z 0-9 and _().-
#             - followed by a dot (.) and a allowed_format at the end
#         """
#         filename =cls._retrieve_filename(file)
#         allowed_format = "|".join(IMAGES)
#         # format IMAGES into regex, eg: ('jpeg','png') --> 'jpeg|png'
#         regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
#         return re.match(regex, filename) is not None

#     @classmethod
#     def get_basename(cls, file: Union[str, FileStorage]) -> str:
#         """
#             Return file's basename, for example
#             get_basename('some/folder/image.jpg') returns 'image.jpg'
#         """
#         filename = cls._retrieve_filename(file)
#         return os.path.split(filename)[1]

#     @classmethod
#     def get_extension(cls, file: Union[str, FileStorage]) -> str:
#         """
#         Return file's extension, for example
#         get_extension('image.jpg') returns '.jpg'
#         """
#         filename = cls._retrieve_filename(file)
#         return os.path.splitext(filename)[1]
