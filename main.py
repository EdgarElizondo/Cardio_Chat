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
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["start"](dictUsers, update)
        return GENDER
    dictUsers[user.id] = msg["gender"](dictUsers, update, logger, ConversationHandler)
    return PREGNANT
    
# QUESTION 3
def pregnant(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["masculino","femenino"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Masculino, Femenino")
        dictUsers[user.id] = msg["gender"](dictUsers, update, logger, ConversationHandler)
        return PREGNANT
    dictUsers[user.id] = msg["pregnant"](dictUsers, update, logger)
    return PREGNANCYWEEKS

# QUESTION 4
def pregnancy_weeks(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no","/skip"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["pregnant"](dictUsers, update, logger)
        return PREGNANCYWEEKS
    dictUsers[user.id] = msg["pregnancy_weeks"](dictUsers, update, logger)
    return AGE

# QUESTION 5
def age(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.isnumeric() == False) & (update.message.text != "/skip"):
        update.message.reply_text("Respuesta no valida." \
                                  + " Opciones válidas: unicamente valores númericos entre 0-36")
        dictUsers[user.id] = msg["pregnancy_weeks"](dictUsers, update, logger)
        return AGE
    dictUsers[user.id] = msg["age"](dictUsers, update, logger)
    return WEIGHT

# QUESTION 6
def weight(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.isnumeric() == False):
        update.message.reply_text("Respuesta no valida." \
                                  + " Opciones válidas: unicamente valores númericos entre 0-100")
        dictUsers[user.id] = msg["age"](dictUsers, update, logger)
        return WEIGHT
    dictUsers[user.id] = msg["weight"](dictUsers, update, logger)
    return HEIGHT

# QUESTION 7
def height(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.replace(".","").isnumeric() == False):
        update.message.reply_text("Respuesta no valida." \
                                  + " Opciones válidas: unicamente valores númericos entre 10-250")
        dictUsers[user.id] = msg["weight"](dictUsers, update, logger)
        return HEIGHT
    dictUsers[user.id] = msg["height"](dictUsers, update, logger)
    return RACE

# QUESTION 8
def race(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.replace(".","").isnumeric() == False):
        update.message.reply_text("Respuesta no valida." \
                                  + " Opciones válidas: unicamente valores númericos entre 0.50-2.50")
        dictUsers[user.id] = msg["height"](dictUsers, update, logger)
        return RACE
    dictUsers[user.id] = msg["race"](dictUsers, update, logger)
    return SMOKE

# QUESTION 9
def smoke(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["caucasico","afroamericano","latino","asiatico","indio americano","otro"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Caucasico, Afroamericano, Latino, Asiatico, Indio Americano, Otro")
        dictUsers[user.id] = msg["race"](dictUsers, update, logger)
        return SMOKE
    dictUsers[user.id] = msg["smoke"](dictUsers, update, logger)
    return DRINK

# QUESTION 10
def drink(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["smoke"](dictUsers, update, logger)
        return DRINK
    dictUsers[user.id] = msg["drink"](dictUsers, update, logger)
    return EXERCISE

# QUESTION 11
def exercise(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["drink"](dictUsers, update, logger)
        return EXERCISE
    dictUsers[user.id] = msg["exercise"](dictUsers, update, logger)
    return SLEEPTIME

# QUESTION 12
def sleep_time(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["exercise"](dictUsers, update, logger)
        return SLEEPTIME
    dictUsers[user.id] = msg["sleep_time"](dictUsers, update, logger)
    return PHYSICALHEALTH

# QUESTION 13
def physical_health(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.replace(".","").isnumeric() == False):
        update.message.reply_text("Respuesta no valida." \
                                  + " Opciones válidas: unicamente valores númericos entre 0-24")
        dictUsers[user.id] = msg["sleep_time"](dictUsers, update, logger)
        return PHYSICALHEALTH
    dictUsers[user.id] = msg["physical_health"](dictUsers, update, logger)
    return MENTALHEALTH

# QUESTION 14
def mental_health(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.replace(".","").isnumeric() == False):
        update.message.reply_text("Respuesta no valida." \
                                  + " Opciones válidas: unicamente valores númericos entre 0-31")
        dictUsers[user.id] = msg["physical_health"](dictUsers, update, logger)
        return MENTALHEALTH
    dictUsers[user.id] = msg["mental_health"](dictUsers, update, logger)
    return DIFWALKING

# QUESTION 15
def difficult_to_walk(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if (update.message.text.replace(".","").isnumeric() == False):
        update.message.reply_text("Respuesta no valida." \
                                  + " Opciones válidas: unicamente valores númericos entre 0-31")
        dictUsers[user.id] = msg["mental_health"](dictUsers, update, logger)
        return DIFWALKING
    dictUsers[user.id] = msg["difficult_to_walk"](dictUsers, update, logger)
    return GENHEALTH

# QUESTION 16
def general_health(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["difficult_to_walk"](dictUsers, update, logger)
        return GENHEALTH
    dictUsers[user.id] = msg["general_health"](dictUsers, update, logger)
    return STROKE

# QUESTION 17
def stroke(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["excelente", "muy buena", "buena", "regular", "mala"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Excelente, Muy buena, Buena, Regular, Mala")
        dictUsers[user.id] = msg["general_health"](dictUsers, update, logger)
        return STROKE
    dictUsers[user.id] = msg["stroke"](dictUsers, update, logger)
    return ASTHMA

# QUESTION 18
def asthma(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["stroke"](dictUsers, update, logger)
        return ASTHMA
    dictUsers[user.id] = msg["asthma"](dictUsers, update, logger)
    return DIABETIS

# QUESTION 19
def diabetis(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["asthma"](dictUsers, update, logger)
        return DIABETIS
    dictUsers[user.id] = msg["diabetis"](dictUsers, update, logger)
    return KIDNEYDISEASE

# QUESTION 20
def kidney_disease(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["diabetis"](dictUsers, update, logger)
        return KIDNEYDISEASE
    dictUsers[user.id] = msg["kidney_disease"](dictUsers, update, logger)
    return SKINCANCER

# QUESTION 21
def skin_cancer(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["kidney_disease"](dictUsers, update, logger)
        return SKINCANCER
    dictUsers[user.id] = msg["skin_cancer"](dictUsers, update, logger)
    return PREDICTION

def prediction(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text.lower() not in ["si","no"]:
        update.message.reply_text("Respuesta no valida, favor de seleccionar alguna de las opciones disponibles que aparecen." \
                                  + " Opciones válidas: Si, No")
        dictUsers[user.id] = msg["skin_cancer"](dictUsers, update, logger)
        return PREDICTION
    
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
            PHYSICALHEALTH :    [MessageHandler(Filters.text, physical_health, run_async=True)],
            MENTALHEALTH :      [MessageHandler(Filters.text, mental_health, run_async=True)],
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