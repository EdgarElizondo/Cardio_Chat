from main_model import ann_model

test_dict = {
    'userid': 1593131899, 
    'Gender': 0, 
    'Pregnant': 0, 
    'Pregnancy_Weeks': 0, 
    'Age': "30-34", 
    'Weight': 77.0, 
    'Height': 1.75, 
    'BMI': 25.14, 
    'Race': 'Latin', 
    'Smoke': 0, 
    'Drink': 0, 
    'Exercise': 1, 
    'Sleep_Time': 8, 
    'Physical_Health': 0, 
    'Mental_Health': 0, 
    'Difficult_Walking': 0, 
    'General_Health': 'Buena', 
    'Stroke': 0, 
    'Asthma': 1, 
    'Diabetis': 0, 
    'Kidney_Disease': 0, 
    'Skin_Cancer': 0}


# Execute Test
model = ann_model()
model.load(test_dict)
prediction = model.evaluate()

print("La predicción es de:",prediction)