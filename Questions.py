# Question requiere to do the diagnosis
from telegram import ReplyKeyboardMarkup

boolean_answer = {"Si":1, "No":0}

# QUESTION 1
def start(dictUsers, update):
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    dictUsers[user.id] = {}
    
    update.message.reply_text(
        "Hola " + str(user.first_name) + " " + str(user.last_name) 
        + f"\nSoy CorBot estoy aquí para ayudarte a predecir si padeces de alguna enfermedad en el corazón con base a unas preguntas, Quieres continuar?" \
        + "\n\nSi deseas cancelar la encuesta solo escribe o pica aqui ==> /cancel",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
        ),
    )
    return dictUsers[user.id]

# QUESTION 2
def gender(dictUsers, update, logger, ConversationHandler):
    user = update.message.chat
    reply_keyboard = [['Femenino', 'Masculino']]
    # User register
    if "userid" not in dictUsers[user.id]:
        dictUsers[user.id]["userid"] = user.id
        dictUsers[user.id]["agreed"] = update.message.text
        logger.info(f"Acepto la conversacion {user.first_name}: {update.message.text}")
    
    if dictUsers[user.id]["agreed"] == "Si":
        update.message.reply_text(
            str(user.first_name) + " " + str(user.last_name) + ", ¿Cual es tu sexo?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Femenino o Masculino?'
            ),
        )

    elif dictUsers[user.id]["agreed"] == "No":
        update.message.reply_text(
            "Gracias " + str(user.first_name) + " " + str(user.last_name) + \
            " por tomarte tu tiempo, que tengas buen dia"
        )
        return ConversationHandler.END

    return dictUsers[user.id]

# QUESTION 3
def pregnant(dictUsers, update, logger):
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]

    if "Gender" not in dictUsers[user.id]:
        if update.message.text == 'Femenino':
            dictUsers[user.id]["Gender"] = 0
        else:
            dictUsers[user.id]["Gender"] = 1
        logger.info(f"Genero de {user.first_name}: {update.message.text}")
    
    if dictUsers[user.id]["Gender"] == 0:
        update.message.reply_text(
            str(user.first_name) + " " + str(user.last_name) + ", Estas embarazada?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
        )
    elif dictUsers[user.id]["Gender"] == 1:
        dictUsers[user.id]["Pregnant"] = 0
        dictUsers[user.id]["Pregnancy_Weeks"] = 0

        update.message.reply_text(
            " " + str(user.first_name) + " " + str(user.last_name) + \
            " toca aqui por favor para avanzar ==> /skip.",
        )
    
    return dictUsers[user.id]
    
# QUESTION 4
def pregnancy_weeks(dictUsers, update, logger):
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    if "Pregnant" not in dictUsers[user.id]:
        dictUsers[user.id]["Pregnant"] = update.message.text
        logger.info(f"Esta embarazado {user.first_name}: {update.message.text}")

    if dictUsers[user.id]["Pregnant"] == 'Si':
        dictUsers[user.id]["Pregnant"] = 1
        update.message.reply_text(
            str(user.first_name) + " " + str(user.last_name) + ", ¿Cuantas semanas llevas de embarazo?",
        )
    elif dictUsers[user.id]["Pregnant"] == 'No':
        dictUsers[user.id]["Pregnant"] = 0
        update.message.reply_text(
            " " + str(user.first_name) + " " + str(user.last_name) + \
            " toca aqui por favor para avanzar ==> /skip.",
        )
    return dictUsers[user.id]

# QUESTION 5
def age(dictUsers, update, logger) -> int:
    user = update.message.chat
    if dictUsers[user.id]["Pregnant"] == 1:
        # Pregnancy weeks register
        dictUsers[user.id]["Pregnancy_Weeks"] = int(update.message.text)
        logger.info(f"Semanas de embarazo tiene {user.first_name}: {update.message.text}")
    else:
        # Pregnancy weeks register
        logger.info(f"Semanas de embarazo tiene {user.first_name}: 0")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ".¿Cuantos años tienes?"
    )
    return dictUsers[user.id]

# QUESTION 6
def weight(dictUsers, update, logger) -> int:
    user = update.message.chat
    # Age register
    dictUsers[user.id]["Age"] = int(update.message.text)
    # Se categoriza la edad para coincidir con el dataset de la red neuronal
    if dictUsers[user.id]["Age"] >= 80:
        dictUsers[user.id]["Age"] = "80+"
    elif dictUsers[user.id]["Age"] >= 75:
        dictUsers[user.id]["Age"] = "75-79"
    elif dictUsers[user.id]["Age"] >= 70:
        dictUsers[user.id]["Age"] = "70-74"
    elif dictUsers[user.id]["Age"] >= 65:
        dictUsers[user.id]["Age"] = "65-69"
    elif dictUsers[user.id]["Age"] >= 60:
        dictUsers[user.id]["Age"] = "60-64"
    elif dictUsers[user.id]["Age"] >= 55:
        dictUsers[user.id]["Age"] = "55-59"
    elif dictUsers[user.id]["Age"] >= 50:
        dictUsers[user.id]["Age"] = "50-54"
    elif dictUsers[user.id]["Age"] >= 45:
        dictUsers[user.id]["Age"] = "45-49"
    elif dictUsers[user.id]["Age"] >= 40:
        dictUsers[user.id]["Age"] = "40-44"
    elif dictUsers[user.id]["Age"] >= 35:
        dictUsers[user.id]["Age"] = "35-39"
    elif dictUsers[user.id]["Age"] >= 30:
        dictUsers[user.id]["Age"] = "30-34"
    elif dictUsers[user.id]["Age"] >= 25:
        dictUsers[user.id]["Age"] = "25-29"
    else:
        dictUsers[user.id]["Age"] = "18-24"
    

    logger.info(f"Edad de {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Cuanto pesas (Kilogramos)?"
    )
    return dictUsers[user.id]

# QUESTION 7
def height(dictUsers, update, logger) -> int:
    user = update.message.chat
    # Weight register
    dictUsers[user.id]["Weight"] = float(update.message.text)
    logger.info(f"Peso de {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Cuanto mides (metros)?"
    )
    return dictUsers[user.id]

def bmi(weight,height):
    return round(weight/(height**2),2)

# QUESTION 8
def race(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Caucasico', 'Afroamericano', "Latino", "Asiatico", "Indio Americano", "Otro"]]
    # Height register
    if float(update.message.text) > 100:
        dictUsers[user.id]["Height"] = float(update.message.text)/100
    else:
        dictUsers[user.id]["Height"] = float(update.message.text)
    logger.info(f"Estatura de {user.first_name}: {update.message.text}")
    # BMI register
    dictUsers[user.id]["BMI"] = bmi(dictUsers[user.id]["Weight"],dictUsers[user.id]["Height"])
    logger.info(f"Indice de masa corporal de {user.first_name}: {dictUsers[user.id]['BMI']}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + "¿A qué etnía perteneces?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Caucasico, Afroamericano, Latino, Asiatico, Indio Americano, Otro?'
        ),
    )
    return dictUsers[user.id]

# QUESTION 9
def smoke(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    # Race register
    dictUsers[user.id]["Race"] = update.message.text
    logger.info(f"Etnía de {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Eres fumador?" + \
        "\n\n*NOTA: Se considera fumador si has fumado mas de 100 cigarrillos en tu vida",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return dictUsers[user.id]

# QUESTION 10
def drink(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    # Smoke register
    dictUsers[user.id]["Smoke"] = boolean_answer[update.message.text]
    logger.info(f"Es fumador {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Eres tomador habitual?" + \
        "\n\n*NOTA: Se considera tomador habitual si tomas:" + \
        "\n-Hombres: 14 bebidas o más a la semana." + \
        "\n-Muheres: 7 bebidas o más a la semana",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return dictUsers[user.id]

# QUESTION 11
def exercise(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    # Drink register
    dictUsers[user.id]["Drink"] = boolean_answer[update.message.text]
    logger.info(f"Es bebedor habitual {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Has ejercitado durante el último mes?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return dictUsers[user.id]

# QUESTION 12
def sleep_time(dictUsers, update, logger) -> int:
    user = update.message.chat
    # Exercise register
    dictUsers[user.id]["Exercise"] = boolean_answer[update.message.text]
    logger.info(f"Se ejercita {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Cuantas horas duermes en promedio?"
    )
    return dictUsers[user.id]

# QUESTION 13
def physical_health(dictUsers, update, logger) -> int:
    user = update.message.chat
    # Sleep time register
    dictUsers[user.id]["Sleep_Time"] = float(update.message.text)
    logger.info(f"Cuantas horas duerme {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", durante el último mes, has tenido alguna enfermedad o lesión. ¿Cuantos días duró?"
    )
    return dictUsers[user.id]

# QUESTION 14
def mental_health(dictUsers, update, logger) -> int:
    user = update.message.chat
    # Physical health register
    dictUsers[user.id]["Physical_Health"] = int(update.message.text)
    logger.info(f"Cuantos días ha tenido problemas de salud física {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", durante el último mes, has sentido problemas con tu salud mental. ¿Cuantos días?"
    )
    return dictUsers[user.id]

# QUESTION 15
def difficult_to_walk(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    # Mental health register
    dictUsers[user.id]["Mental_Health"] = int(update.message.text)
    logger.info(f"Cuantos días ha tenido problemas de salud mental {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Tienes problemas graves para caminar o subir escaleras?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return dictUsers[user.id]

# QUESTION 16
def general_health(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Excelente', 'Muy buena', 'Buena', 'Regular', 'Mala']]
    # Difficult walking register
    dictUsers[user.id]["Difficult_Walking"] = boolean_answer[update.message.text]
    logger.info(f"Tiene problemas para caminar {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", En términos generales, ¿Cómo considerarías tu salud?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return dictUsers[user.id]

# QUESTION 17
def stroke(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    # General health register
    dictUsers[user.id]["General_Health"] = update.message.text
    logger.info(f"Salud general de {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Alguna vez has tenido un infarto?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return dictUsers[user.id]

# QUESTION 18
def asthma(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    # Stroke register
    dictUsers[user.id]["Stroke"] = boolean_answer[update.message.text]
    logger.info(f"Ha tenido un infarto {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Padeces de asma?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return dictUsers[user.id]

# QUESTION 19
def diabetis(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    # Asthma register
    dictUsers[user.id]["Asthma"] = boolean_answer[update.message.text]
    logger.info(f"Tiene asma {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Padeces diabetis?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return dictUsers[user.id]

# QUESTION 20
def kidney_disease(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    # Diabetis register
    dictUsers[user.id]["Diabetis"] = boolean_answer[update.message.text]
    logger.info(f"Tiene diabetis {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Padeces de alguna enfermedad en los riñones?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return dictUsers[user.id]

# QUESTION 21
def skin_cancer(dictUsers, update, logger) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    # Kidney disease register
    dictUsers[user.id]["Kidney_Disease"] = boolean_answer[update.message.text]
    logger.info(f"Tiene problemas con el riñon {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Tienes o has tenido cáncer de piel?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return dictUsers[user.id]

chat_message = {"start":start,
                "gender":gender,
                "pregnant":pregnant,
                "pregnancy_weeks":pregnancy_weeks,
                "age":age,
                "weight":weight,
                "height":height,
                "race":race,
                "smoke":smoke,
                "drink":drink,
                "exercise":exercise,
                "sleep_time":sleep_time,
                "physical_health":physical_health,
                "mental_health":mental_health,
                "difficult_to_walk":difficult_to_walk,
                "general_health":general_health,
                "stroke":stroke,
                "asthma":asthma,
                "diabetis":diabetis,
                "kidney_disease":kidney_disease,
                "skin_cancer":skin_cancer}