
from fastapi import FastAPI, Request,Response,Form
from fastapi.templating import Jinja2Templates
import uvicorn
import pickle

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve the HTML template
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Handle form submission
@app.post("/submit")
def submit_bmi(request: Request, gender: str = Form(...), height: float = Form(...), weight: float = Form(...)):
    data = {
        0: 'Extremely Weak',
        1: 'Weak',
        2: 'Normal',
        3: 'Overweight',
        4: 'Obesity',
        5: 'Extreme Obesity'
    }
    f = open('bmimodel', 'rb')
    model = pickle.load(f)
    f.close()
    input = {
        "gender": gender,
        "height": height,
        "weight": weight
    }

    x = [model['lb'].fit_transform([input['gender']])[0]]
    # x.extend(list(model['sd'].transform([[input['height'],input['weight']]])[0]))
    x.extend([input['height'], input['weight']])
    bmi = data[model['mn'].predict([x])[0]]
    print(bmi)
    return templates.TemplateResponse("result.html", {"request": request, "bmi": bmi})



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
