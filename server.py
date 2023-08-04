
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
    red_weight = 0
    inc_weight = 0
    if bmi in ['Extremely Weak','Weak']:
        for i in range(int(input['weight'])):
            inc_weight = i
            x = [model['lb'].fit_transform([input['gender']])[0]]
            x.extend([input['height'], input['weight'] + i])
            temp_bmi = data[model['mn'].predict([x])[0]]
            if temp_bmi == 'Normal':
                break

    if bmi in ['Overweight','Obesity','Extreme Obesity']:
        for i in range(int(input['weight'])):
            red_weight = i
            x = [model['lb'].fit_transform([input['gender']])[0]]
            x.extend([input['height'], input['weight'] - i])
            temp_bmi = data[model['mn'].predict([x])[0]]
            if temp_bmi == 'Normal':
                break

    print(inc_weight,red_weight)
    if inc_weight == 0:
        message = 'You need to lose {} kg of weight.'.format(red_weight)
    else:
        message = 'You need to gain {} kg of weight.'.format(inc_weight)


    return templates.TemplateResponse("result.html", {"request": request, "bmi": bmi,'message':message})



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
