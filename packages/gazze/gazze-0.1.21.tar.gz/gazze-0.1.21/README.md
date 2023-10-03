# gazze

A Python Web Framework for High-Performance APIs

### Summary

Gazze is an exciting Python web framework, developed on top of the powerful Starlette and the amazing FastAPI. The primary goal of Gazze is to provide an exceptional experience in developing highly performant APIs in Python.

### Important Notices:

Please be aware that Gazze is an ongoing development and research project. Currently, it is not recommended for use in production environments. We are working diligently to improve and mature the framework, but it is still in its early development stage.

### Installation

```
$ pip install gazze
```

You will also need a ASGI Server like Uvicorn or Hypercorn

```
$ pip install "uvicorn[standard]"
```

### Example

```python
from gazze.responses import JSONResponse
from gazze.applications import Gazze

app = Gazze(
    debug=True,
)

@app.get("/items/{item_id}")
async def read_item(request):
    item_id = request.path_params.get('item_id')
    return JSONResponse({"item_id": item_id})
```

### Run

```
$ uvicorn main:app

INFO:     Started server process [51753]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Key Features:

- Built on top of Starlette and FastAPI.
- Focused on creating high-performance APIs.
- Modern and developer-friendly design.
- Open-source licensing for flexibility and collaboration.

#### Contributions:

We look forward to collaborations and contributions from the community to help Gazze evolve and grow. Your input is highly appreciated in shaping the future of this project.
