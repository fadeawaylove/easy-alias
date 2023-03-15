import os
import shutil

shutil.rmtree("./dist")
os.system("python -m pip install build -U")
os.system("python -m build")
os.system(f"twine upload -u {input('username: ')} -p {input('password: ')}  dist/*  --verbose")
