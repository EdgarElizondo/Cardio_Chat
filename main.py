from Constants import *
from Questions import *

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
ethnic_answer = {"White": 0, "Black": 1, "Latin": 2, "Asian": 3, "Native American": 4, "Other": 5}
health_answer = {"Excelente": 0, "Muy buena": 1, "Buena": 2, "Regular": 3, "Mala": 4}

# Default messages
bot_name = "CorBot"
ask_cancel_message = "\n\nSi deseas cancelar la encuesta solo escribe o pica aqui ==> /cancel"

# ***********************************************************************************************************************************
# ************************************************************ QUESTIONS ************************************************************
# ***********************************************************************************************************************************

# QUESTION 1
def start(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    dictUsers[user.id] = {}
    update.message.reply_text(
        "Hola " + str(user.first_name) + " " + str(user.last_name) 
        + f"\nSoy {bot_name} estoy aquí para ayudarte a predecir si padeces de alguna enfermedad en el corazón con base a unas preguntas, Quieres continuar?" \
        + ask_cancel_message,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
        ),
    )

    return START

# QUESTION 2
def gender(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    reply_keyboard = [['Femenino', 'Masculino']]
    # User register
    dictUsers[user.id]["userid"] = user.id
    logger.info(f"Acepto la conversacion {user.first_name}: {update.message.text}")
    
    if update.message.text == "Si":
        update.message.reply_text(
            str(user.first_name) + " " + str(user.last_name) + ", ¿Cual es tu sexo?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Femenino o Masculino?'
            ),
        )
    elif update.message.text == "No":
        update.message.reply_text(
            "Gracias " + str(user.first_name) + " " + str(user.last_name) + \
            " por tomarte tu tiempo, que tengas buen dia"
        )
        return ConversationHandler.END

    return GENDER


# QUESTION 3
def pregnant(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    logger.info(f"Genero de {user.first_name}: {update.message.text}")

    if update.message.text == 'Femenino':
        dictUsers[user.id]["Gender"] = 1
        update.message.reply_text(
            str(user.first_name) + " " + str(user.last_name) + ", Estas embarazada?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
        )
    elif update.message.text == 'Masculino':
        dictUsers[user.id]["Gender"] = 0
        dictUsers[user.id]["Pregnant"] = 0
        dictUsers[user.id]["Pregnancy_Weeks"] = 0

        update.message.reply_text(
            " " + str(user.first_name) + " " + str(user.last_name) + \
            " toca aqui por favor para avanzar ==> /skip.",
        )

    return PREGNANT


# QUESTION 4
def pregnancy_weeks(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    logger.info(f"Esta embarazado {user.first_name}: {update.message.text}")

    if update.message.text == 'Si':
        dictUsers[user.id]["Pregnant"] = 1
        update.message.reply_text(
            str(user.first_name) + " " + str(user.last_name) + ", ¿Cuantas semanas llevas de embarazo?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
        )
    elif update.message.text == 'No':
        dictUsers[user.id]["Pregnant"] = 0
        update.message.reply_text(
            " " + str(user.first_name) + " " + str(user.last_name) + \
            " toca aqui por favor para avanzar ==> /skip.",
        )

    return PREGNANCYWEEKS


# QUESTION 5
def age(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if dictUsers[user.id]["Pregnant"] == 1:
        # Pregnancy weeks register
        dictUsers[user.id]["Pregnancy_Weeks"] = update.message.text
        logger.info(f"Semanas de embarazo tiene {user.first_name}: {update.message.text}")
    else:
        # Pregnancy weeks register
        logger.info(f"Semanas de embarazo tiene {user.first_name}: 0")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ".¿Cuantos años tienes?"
    )

    return AGE


# QUESTION 6
def weight(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    # Age register
    dictUsers[user.id]["Age"] = update.message.text
    logger.info(f"Edad de {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Cuanto pesas (Kilogramos)?"
    )

    return WEIGHT


# QUESTION 7
def height(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    # Weight register
    dictUsers[user.id]["Weight"] = float(update.message.text)
    logger.info(f"Pes de {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Cuanto mides (metros)?"
    )

    return HEIGHT


def bmi(weight,height):
    return round(weight/(height**2),2)


# QUESTION 8
def race(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    reply_keyboard = [['White', 'Black', "Latin", "Asian", "Navive American", "Other"]]
    # Height register
    dictUsers[user.id]["Height"] = float(update.message.text)
    logger.info(f"Estatura de {user.first_name}: {update.message.text}")
    # BMI register
    dictUsers[user.id]["BMI"] = bmi(dictUsers[user.id]["Weight"],dictUsers[user.id]["Height"])
    logger.info(f"Indice de masa corporal de {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + "¿A qué etnía perteneces?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='White, Black, Latin, Asian, Navive American, Other?'
        ),
    )

    return RACE


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

    return SMOKE


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

    return DRINK


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

    return EXERCISE


# QUESTION 12
def sleep_time(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    # Exercise register
    dictUsers[user.id]["Exercise"] = boolean_answer[update.message.text]
    logger.info(f"Se ejercita {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Cuantas horas duermes en promedio?"
    )

    return SLEEPTIME


# QUESTION 13
def physical_healt(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    # Sleep time register
    dictUsers[user.id]["Sleep_Time"] = update.message.text
    logger.info(f"Cuantas horas duerme {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", durante el último mes, has tenido alguna enfermedad o lesión. ¿Cuantos días duró?"
    )

    return PHYSICALHEALTH


# QUESTION 14
def mental_healt(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    # Physical health register
    dictUsers[user.id]["Physical_Health"] = update.message.text
    logger.info(f"Cuantos días ha tenido problemas de salud física {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", durante el último mes, has sentido problemas con tu salud mental. ¿Cuantos días?"
    )

    return MENTALHEALTH


# QUESTION 15
def difficult_to_walk(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    reply_keyboard = [['Si', 'No']]
    # Mental health register
    dictUsers[user.id]["Mental_Health"] = update.message.text
    logger.info(f"Cuantos días ha tenido problemas de salud mental {user.first_name}: {update.message.text}")

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Tienes problemas graves para caminar o subir escaleras?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )

    return DIFWALKING


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

    return GENHEALTH


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

    return STROKE


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

    return ASTHMA


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

    return DIABETIS


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

    return KIDNEYDISEASE


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

    return SKINCANCER


def end_query(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    # Skin cancer register
    dictUsers[user.id]["Skin_Cancer"] = boolean_answer[update.message.text]
    logger.info(f"Tiene cancer de piel {user.first_name}: {update.message.text}")
    
    # Database connection
    db.add_user_to_db(dictUsers[user.id])
    
    # Final Message
    update.message.reply_text(
        "Ha terminado la encuesta, sus datos han sido guradados con exito." + \
        "\nLa función de predicción esta en proceso, favor de intentarlo en otro momento"
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
        entry_points = [CommandHandler('start',start)],
        states = {
            START : [MessageHandler(Filters.regex('^(Si|No)$'), gender, run_async=True)],
            GENDER : [MessageHandler(Filters.regex('^(Femenino|Masculino)$'), pregnant, run_async=True)],
            PREGNANT : [MessageHandler(Filters.regex('^(Si|No)$'), pregnancy_weeks, run_async=True),CommandHandler('skip',age)],
            PREGNANCYWEEKS : [MessageHandler(Filters.text & ~Filters.command, age, run_async=True),CommandHandler('skip',age)],
            AGE : [MessageHandler(Filters.text & ~Filters.command, weight, run_async=True)],
            WEIGHT : [MessageHandler(Filters.text & ~Filters.command, height, run_async=True)],
            HEIGHT : [MessageHandler(Filters.text & ~Filters.command, race, run_async=True)],
            RACE : [MessageHandler(Filters.regex('^(White|Black|Latin|Asian|Native American|Other|)$'), smoke, run_async=True)],
            SMOKE : [MessageHandler(Filters.regex('^(Si|No)$'), drink, run_async=True)],
            DRINK : [MessageHandler(Filters.regex('^(Si|No)$'), exercise, run_async=True)],
            EXERCISE : [MessageHandler(Filters.text & ~Filters.command, sleep_time, run_async=True)],
            SLEEPTIME : [MessageHandler(Filters.text & ~Filters.command, physical_healt, run_async=True)],
            PHYSICALHEALTH : [MessageHandler(Filters.text & ~Filters.command, mental_healt, run_async=True)],
            MENTALHEALTH : [MessageHandler(Filters.text & ~Filters.command, difficult_to_walk, run_async=True)],
            DIFWALKING : [MessageHandler(Filters.regex('^(Si|No)$'), general_health, run_async=True)],
            GENHEALTH : [MessageHandler(Filters.regex('^(Excelente|Muy buena|Buena|Regular|Mala)$'), stroke, run_async=True)],
            STROKE : [MessageHandler(Filters.regex('^(Si|No)$'), asthma, run_async=True)],
            ASTHMA : [MessageHandler(Filters.regex('^(Si|No)$'), diabetis, run_async=True)],
            DIABETIS : [MessageHandler(Filters.regex('^(Si|No)$'), kidney_disease, run_async=True)],
            KIDNEYDISEASE : [MessageHandler(Filters.regex('^(Si|No)$'), skin_cancer, run_async=True)],
            SKINCANCER: [MessageHandler(Filters.text & ~Filters.command, end_query, run_async=True)],   
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