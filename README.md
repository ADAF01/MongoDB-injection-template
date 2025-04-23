Below is a proposed **README.md** for the [ADAF01/MongoDB-injection-template](https://github.com/ADAF01/MongoDB-injection-template) repository. It explains that this code is meant for MongoDB injection testing and includes instructions to download and run it using **uv**.

---

## MongoDB Injection Template

A minimal Flask application and template for testing MongoDB NoSQL‐injection scenarios.  
It exposes both GET and POST endpoints for user “login” against a MongoDB collection, demonstrating how unfiltered inputs can be abused—and how simple whitelisting mitigates injection attacks.

---

## Features

- **MongoDB connection** with configurable URI (defaults to `mongodb://localhost:27017/`)  
- **Seed data** for a `testdb.users` collection (runs once on startup)  
- **GET `/login`** endpoint accepting `username` & `password` as query params  
- **POST `/login`** endpoint accepting JSON payload  
- **Basic NoSQL-injection protection** via an allow-list (commented out in code for testing)  
- **Simple HTML form** at `/` to exercise both endpoints in-browser  

---

## Prerequisites

- **Python 3.8+**  
- **MongoDB** server or Atlas cluster  
- **uv** (a fast, lockfile-based Python package manager)  

---

## Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/ADAF01/MongoDB-injection-template.git  
   cd MongoDB-injection-template  
   ``` citeturn1view0

2. **Install `uv`**  
   - **Standalone installer (macOS/Linux):**  
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ``` citeturn10view0  
   - **Or via PyPI:**  
     ```bash
     pip install uv
     ``` citeturn10view0

3. **Install project dependencies**  
   ```bash
   uv sync
   ```  
   This will read `pyproject.toml` + `uv.lock` and install exactly those versions into a `.venv` citeturn7view0

---

## Configuration

- By default the app connects to `mongodb://localhost:27017/`.  
- To point at a different MongoDB URI (e.g. Atlas), set the `ATLAS_URI` environment variable:
  ```bash
  export ATLAS_URI="mongodb+srv://<user>:<pass>@cluster0.mongodb.net"
  ```

---

## Running the App

```bash
# start the Flask server in a uv-managed environment
uv run python main.py
```
The server will listen on `0.0.0.0:5000` (debug mode enabled). citeturn7view0

---

## Endpoints

| Method | Route               | Description                                                |
| ------ | ------------------- | ---------------------------------------------------------- |
| GET    | `/login?username=&password=` | Returns matching users as JSON array (injection-vulnerable) |
| POST   | `/login` (JSON body)         | Returns matching users as JSON array                       |
| GET    | `/`                          | Simple HTML form to test both endpoints                   |

**Example GET**  
```bash
curl "http://localhost:5000/login?username=admin&password=secret"
```

**Example POST**  
```bash
curl -X POST http://localhost:5000/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"secret"}'
```

---

## Testing Injection

1. **Unsafe query** (no whitelist):
   ```bash
   # returns all users
   curl "http://localhost:5000/login?username[$ne]=&password[$ne]="
   ```
2. **With whitelist** (uncomment `sanitize_input` in code):
   ```python
   # in main.py, switch to:
   query = sanitize_input(request.args.to_dict(flat=False))
   ```

---

## Contributing

1. Fork the repo  
2. Create a feature branch  
3. Submit a pull request  

---

## License

This project is released under the **MIT License**.  

---

*Happy injection-testing!*
