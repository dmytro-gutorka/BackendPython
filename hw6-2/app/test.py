import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates/')


print(BASE_DIR)
print(UPLOAD_FOLDER)
print(TEMPLATE_FOLDER)