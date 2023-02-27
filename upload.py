import os
import shutil

shutil.rmtree("./dist")
os.system("python -m pip install build -U")
os.system("python -m build")

# upload
# twine upload dist/*
