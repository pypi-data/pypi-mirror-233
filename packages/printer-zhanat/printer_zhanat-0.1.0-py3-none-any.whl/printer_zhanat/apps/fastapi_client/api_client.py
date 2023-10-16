from fastapi import FastAPI


app = FastAPI()


@app.get("/client/payment/{code_id}")
async def get(code_id):
    return f"welcome test payment your id:{code_id}"


