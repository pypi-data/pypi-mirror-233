# Firelit
### 🔥👑 FireLit: Streamlit App with Firebase Authentication

### Installation
You can install Firelit as a pip package.

```bash
pip install firelit
```

You can check the installation by running the following command in your terminal.

```bash
python -c "import firelit as ft; print(ft.__version__)"
```

## Getting started

### Configuration

Firelit needs to be connected to a firebase Web App.

You can create a new Web App in your Firebase project by following the steps below.

 * TODO

The configuration file can be provided as a firelit_config.yml file in the root directory of your Streamlit app.

```yaml
  apiKey: <apiKey>
  authDomain: <authDomain>
  databaseURL: <databaseURL>
  projectId: <projectId>
  storageBucket: <storageBucket>
  messagingSenderId: <messagingSenderId>
  appId: <appId>
  measurementId: <measurementId>
```

or can be passed to the FirebaseAdmin class as a python dictionary or as a path to the
desired configuration file.

```python
import firelit as ft

ft.FirebaseAdmin(config="firelit_config.yml")
```

or

```python
import firelit as ft
from firelit.utils import load_yaml

config_dict = load_yaml("firelit_config.yml")
```

### Using Firelit (backend)

```python
import firelit as ft

user_info = dict(email="user@gmail.com",
                 password="firelit")

admin = ft.admin.FirebaseAdmin()
admin.login(user_info["email"], user_info["password"])

```

### Using Firelit (frontend)

```python
import streamlit as st

from firelit.frontend import firelit_login_form

if __name__ == "__main__":
    st.set_page_config(
        page_title="Firelit Demo App",
        page_icon="🔥",
        layout="wide",
    )

    st.title("🔥 Firelit Demo App")
    st.subheader("This is a demo app for the Firelit package")
    sidebar = st.toggle("Show login form in the sidebar", key="sidebar_login")

    admin = firelit_login_form(sidebar=sidebar)

    if not admin.authentication_status:
        st.write("Please login to continue")
    else:
        st.write("You are logged in")
        st.balloons()
```
