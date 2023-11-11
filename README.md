# Server Tatto

## Requirements

-   Python3.10+
-   Docker
-   MongoDB

## Development

1. Create a venv

```bash
python3 -m venv ./venv
```

2. Activate venv

```bash
source ./venv/bin/active
```

3. Install dependencies

```bash
pip3 install -r requirements.txt
```

4. Run

```bash
sudo docker compose up app --attach app
```

### Docker

`Dockerfile.dev`
`Dockerfile.prod`

Exposed port (in both Dockerfiles): `6060`

## API Reference (Swagger)

#### Swagger ui

```
  GET /api/v1/docs
```

#### Redoc

```
  GET /api/v1/redoc
```
