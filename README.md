## Login/Logout Sequence

### Manual run

* Step 1: Install the necessary requirements

```bash
pip install -r requirements.txt
```

* Step 2: Start the app

```bash
python api.py
```

### Docker commands

* Step 1: Build the docker

```bash
docker build -t login -f Dockerfile .
```

* Step 2: Run the app

```bash
docker run -it -p 8000:8000 login
```

### REST API

* Step 1: Create user

```bash
http POST http://localhost:8000/users/create first_name=John last_name=Doe email=john.doe@mail.com password=johndoe
```

* Step 2: Get the token

```bash
http POST http://localhost:8000/login email=admin@mail.com password=admin
```

* Step 3: Verify the token

```bash
http GET http://localhost:8000/verify Authorization:<token>
```

