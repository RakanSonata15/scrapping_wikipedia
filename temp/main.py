from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CalculationRequest(BaseModel):
    expression: str

@app.post("/calculate")
async def calculate(request: CalculationRequest):
    try:
        result = eval(request.expression)
        return {"result": result}
    except:
        return {"error": "Invalid expression"}
