from uvicorn import run


if __name__ == '__main__':
    run("apps.fastapi_client.api_client:app", reload=True, workers=2, host='192.168.88.96')