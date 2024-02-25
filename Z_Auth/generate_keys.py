import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["demo", "anotheruser"]
usernames = ["demo", "anotheruser"]
passwords = ["XYZ", "ZYX"] #change them after running the pass generation script

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

### python3 generate_keys.py
### python3 ./Z_Auth/generate_keys.py