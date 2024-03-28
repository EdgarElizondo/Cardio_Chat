from Constants import *
from Questions import chat_message as msg

from IA_Model.run_model import run_ann

from backend.logger import log
from backend.database import database

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)


dictUsers = {}
dictUsersContinue = {}
# Multiple choice questions answers
boolean_answer = {"Si":1, "No":0}
ethnic_answer = {"Caucasico": 0, "Afroamericano": 1, "Latino": 2, "Asiatico": 3, "Indio Americano": 4, "Otro": 5}
health_answer = {"Excelente": 0, "Muy buena": 1, "Buena": 2, "Regular": 3, "Mala": 4}

# Default messages
bot_name = "Corbot"
ask_cancel_message = "\n\nSi deseas cancelar la encuesta solo escribe o pica aqui ==> /cancel"

# ***********************************************************************************************************************************
# ************************************************************ QUESTIONS ************************************************************
# ***********************************************************************************************************************************
# QUESTION 1
def start(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    dictUsers[user.id] = msg["start"](dictUsers, update)
    return GENDER

# QUESTION 2
def gender(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no"]:
        dictUsers[user.id] = msg["start"](dictUsers, update)
        return GENDER
    dictUsers[user.id] = msg["gender"](dictUsers, update, logger, ConversationHandler)
    return PREGNANT
    
# QUESTION 3
def pregnant(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["masculino","femenino"]:
        dictUsers[user.id] = msg["gender"](dictUsers, update, logger, ConversationHandler)
        return PREGNANT
    dictUsers[user.id] = msg["pregnant"](dictUsers, update, logger)
    return PREGNANCYWEEKS

# QUESTION 4
def pregnancy_weeks(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no","/skip"]:
        dictUsers[user.id] = msg["pregnant"](dictUsers, update, logger)
        return PREGNANCYWEEKS
    dictUsers[user.id] = msg["pregnancy_weeks"](dictUsers, update, logger)
    return AGE

# QUESTION 5
def age(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.isnumeric() == False) & (update.message.text != "/skip"):
        dictUsers[user.id] = msg["pregnancy_weeks"](dictUsers, update, logger)
        return AGE
    dictUsers[user.id] = msg["age"](dictUsers, update, logger)
    return WEIGHT

# QUESTION 6
def weight(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.isnumeric() == False):
        dictUsers[user.id] = msg["age"](dictUsers, update, logger)
        return WEIGHT
    # Age register
    dictUsers[user.id] = msg["weight"](dictUsers, update, logger)
    return HEIGHT

# QUESTION 7
def height(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.replace(".","").isnumeric() == False):
        dictUsers[user.id] = msg["weight"](dictUsers, update, logger)
        return HEIGHT
    # Weight register
    dictUsers[user.id] = msg["height"](dictUsers, update, logger)
    return RACE

# QUESTION 8
def race(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.replace(".","").isnumeric() == False):
        dictUsers[user.id] = msg["height"](dictUsers, update, logger)
        return RACE
    # Height register
    dictUsers[user.id] = msg["race"](dictUsers, update, logger)
    return SMOKE


# QUESTION 9
def smoke(update: Update, context: CallbackContext, ) -> int:
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

    return DRINK


# QUESTION 10
def drink(update: Update, context: CallbackContext, ) -> int:
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

    return EXERCISE


# QUESTION 11
def exercise(update: Update, context: CallbackContext, ) -> int:
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

    return SLEEPTIME


# QUESTION 12
def sleep_time(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    # Exercise register
    dictUsers[user.id]["Exercise"] = boolean_answer[update.message.text]
    logger.info(f"Se ejercita {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Cuantas horas duermes en promedio?"
    )

    return PHYSICALHEALTH


# QUESTION 13
def physical_healt(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    # Sleep time register
    dictUsers[user.id]["Sleep_Time"] = float(update.message.text)
    logger.info(f"Cuantas horas duerme {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", durante el último mes, has tenido alguna enfermedad o lesión. ¿Cuantos días duró?"
    )

    return MENTALHEALTH


# QUESTION 14
def mental_healt(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    # Physical health register
    dictUsers[user.id]["Physical_Health"] = int(update.message.text)
    logger.info(f"Cuantos días ha tenido problemas de salud física {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", durante el último mes, has sentido problemas con tu salud mental. ¿Cuantos días?"
    )

    return DIFWALKING


# QUESTION 15
def difficult_to_walk(update: Update, context: CallbackContext, ) -> int:
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

    return GENHEALTH


# QUESTION 16
def general_health(update: Update, context: CallbackContext, ) -> int:
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

    return STROKE


# QUESTION 17
def stroke(update: Update, context: CallbackContext, ) -> int:
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

    return ASTHMA


# QUESTION 18
def asthma(update: Update, context: CallbackContext, ) -> int:
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

    return DIABETIS


# QUESTION 19
def diabetis(update: Update, context: CallbackContext, ) -> int:
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

    return KIDNEYDISEASE


# QUESTION 20
def kidney_disease(update: Update, context: CallbackContext, ) -> int:
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

    return SKINCANCER


# QUESTION 21
def skin_cancer(update: Update, context: CallbackContext, ) -> int:
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

    return PREDICTION


def prediction(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    # Skin cancer register
    dictUsers[user.id]["Skin_Cancer"] = boolean_answer[update.message.text]
    logger.info(f"Tiene cancer de piel {user.first_name}: {update.message.text}")
    
    print(dictUsers[user.id])

    # Execute ANN Model
    prediction = run_ann(dictUsers[user.id])
    dictUsers[user.id]["Prediction"] = prediction
    text_response = ""
    # Response text based on prediction level
    if prediction <= 0.05:
        text_response = "Excelente"
    elif prediction <= 0.1:
        text_response = "Niveles aceptables"
    elif prediction <= 0.15:
        text_response = "Regular, hay que cuidarse un poco"
    elif prediction <= 0.25:
        text_response = "Corre riesgo leve"    
    elif prediction <= 0.4:
        text_response = "Corre riesgo moderado"
    elif prediction <= 0.75:
        text_response = "Corre riesgo grave"
    else:
        text_response = "Corre un riesgo severo"

    # Database connection
    db.add_user_to_db(dictUsers[user.id])

    # Final Message
    update.message.reply_text(
        "Ha terminado la encuesta, sus datos han sido guardados con exito." + \
        f"\nCorBot considera que corres un {prediction*100}% de riesgo de padecer una enfermedad cardivascular" + \
        f"\n{text_response}"
        )

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext, ) -> int:
    user = update.message.from_user
    update.message.reply_text(
        'Adios, que tengas un buen dia .', reply_markup=ReplyKeyboardRemove()
    )
    if user.id in dictUsers.keys():
        dictUsers.pop(user.id)

    return ConversationHandler.END

# ***********************************************************************************************************************************
# ************************************************************** MAIN ***************************************************************
# ***********************************************************************************************************************************
def main():
    
    updater = Updater(TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    question_handler = ConversationHandler(
        entry_points = [MessageHandler(Filters.all,start)],
        states = {
            GENDER :            [MessageHandler(Filters.text, gender, run_async=True)],
            PREGNANT :          [MessageHandler(Filters.text, pregnant, run_async=True)],
            PREGNANCYWEEKS :    [MessageHandler(Filters.text & ~Filters.command, pregnancy_weeks, run_async=True),CommandHandler('skip',age)],
            AGE :               [MessageHandler(Filters.text & ~Filters.command, age, run_async=True),CommandHandler('skip',age)],
            WEIGHT :            [MessageHandler(Filters.text, weight, run_async=True)],
            HEIGHT :            [MessageHandler(Filters.text, height, run_async=True)],
            RACE :              [MessageHandler(Filters.text, race, run_async=True)],
            SMOKE :             [MessageHandler(Filters.text, smoke, run_async=True)],
            DRINK :             [MessageHandler(Filters.text, drink, run_async=True)],
            EXERCISE :          [MessageHandler(Filters.text, exercise, run_async=True)],
            SLEEPTIME :         [MessageHandler(Filters.text, sleep_time, run_async=True)],
            PHYSICALHEALTH :    [MessageHandler(Filters.text, physical_healt, run_async=True)],
            MENTALHEALTH :      [MessageHandler(Filters.text, mental_healt, run_async=True)],
            DIFWALKING :        [MessageHandler(Filters.text, difficult_to_walk, run_async=True)],
            GENHEALTH :         [MessageHandler(Filters.text, general_health, run_async=True)],
            STROKE :            [MessageHandler(Filters.text, stroke, run_async=True)],
            ASTHMA :            [MessageHandler(Filters.text, asthma, run_async=True)],
            DIABETIS :          [MessageHandler(Filters.text, diabetis, run_async=True)],
            KIDNEYDISEASE :     [MessageHandler(Filters.text, kidney_disease, run_async=True)],
            SKINCANCER :        [MessageHandler(Filters.text, skin_cancer, run_async=True)],
            PREDICTION:         [MessageHandler(Filters.text, prediction, run_async=True)],   
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(question_handler)
    updater.start_polling() 
    updater.idle()

if __name__ == "__main__":
    logger = log(__name__)
    db = database(bot_name)
    main()