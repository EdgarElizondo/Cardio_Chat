from Constants import *
from Questions import *

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

# Default messages
bot_name = "[Asignar nombre]"
ask_cancel_message = "\n\nSi deseas cancelar la encuesta solo escribe o pica aqui ==> /cancel"

# ***********************************************************************************************************************************
# ************************************************************ QUESTIONS ************************************************************
# ***********************************************************************************************************************************
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


def gender(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Femenino', 'Masculino']]
    user = update.message.chat
    
    if update.message.text == "Si":
        update.message.reply_text(
            "Cual es tu sexo " + str(user.first_name) + " " + str(user.last_name) + "? ",
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


def pregnant(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    if update.message.text == 'Femenino':
        dictUsers[user.id].append(1)
        update.message.reply_text(
            "Estas embarazada " + str(user.first_name) + " " + str(user.last_name) + "?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
            )
    elif update.message.text == 'Masculino':
        dictUsers[user.id].extend([0,0])
        update.message.reply_text(
            " " + str(user.first_name) + " " + str(user.last_name) + \
            " toca aqui por favor para avanzar ==> /skip.",
            )

    return PREGNANT


def pregnancy_weeks(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    if update.message.text == 'Si':
        dictUsers[user.id].append(1)
        update.message.reply_text(
            "Cuantas semanas llevas de embarazo " + str(user.first_name) + " " + str(user.last_name) + "?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
            )
    elif update.message.text == 'No':
        dictUsers[user.id].append(0)
        update.message.reply_text(
            " " + str(user.first_name) + " " + str(user.last_name) + \
            " toca aqui por favor para avanzar ==> /skip.",
            )

    return PREGNANCYWEEKS


def age(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        "Cuantos años tienes " + str(user.first_name) + " " + str(user.last_name) + "?"
    )
    return AGE


def weight(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        "Cuanto pesas " + str(user.first_name) + " " + str(user.last_name) + "?"
    )
    return WEIGHT


def height(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        "Cuanto mides " + str(user.first_name) + " " + str(user.last_name) + "?"
    )
    return HEIGHT


def bmi(weight,height):
    return round(weight/(height**2),2)


def race(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['White', 'Black', "Latin", "Asian", "Navive American", "Other"]]
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    dictUsers[user.id].append(bmi(dictUsers[user.id][-2],dictUsers[user.id][-1]))
    update.message.reply_text(
        "A que etnía perteneces " + str(user.first_name) + " " + str(user.last_name) + "?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='White, Black, Latin, Asian, Navive American, Other?'
        ),
    )
    return RACE


def smoke(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        "Eres un fumador " + str(user.first_name) + " " + str(user.last_name) + "?" + \
        "\n\n*NOTA: Se considera como fumador si has fumado mas de 100 cigarrillos en tu vida",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return SMOKE


def drink(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    if update.message.text == "Si":
        dictUsers[user.id].append(1)
    elif update.message.text == "No":
        dictUsers[user.id].append(0)
    
    update.message.reply_text(
        "Eres tomador habitual" + str(user.first_name) + " " + str(user.last_name) + "?" + \
        "\n\n*NOTA: Se considera tomador habitual si tomas:" + \
        "\n-Hombres: 14 bebidas o más a la semana." + \
        "\n-Muheres: 7 bebidas o más a la semana",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return DRINK


def exercise(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    if update.message.text == "Si":
        dictUsers[user.id].append(1)
    elif update.message.text == "No":
        dictUsers[user.id].append(0)

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Has ejercitado durante el último mes?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return EXERCISE


def sleep_time(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    if update.message.text == "Si":
        dictUsers[user.id].append(1)
    elif update.message.text == "No":
        dictUsers[user.id].append(0)

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Cuantas horas duermes en promedio?"
    )
    return SLEEPTIME


def physical_healt(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", durante el último mes, has tenido alguna enfermedad o lesión. ¿Cuantos tiempo duró?"
    )
    return PHYSICALHEALTH

def mental_healt(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", durante el último mes, has sentido problemas con tu salud mental. ¿Cuantos días?"
    )
    return MENTALHEALTH


def difficult_to_walk(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Tienes problemas graves para caminar o subir escaleras?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return DIFWALKING


def general_health(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Excelente', 'Muy buena', 'Buena', 'Regular', 'Mala']]
    user = update.message.chat
    if update.message.text == "Si":
        dictUsers[user.id].append(1)
    elif update.message.text == "No":
        dictUsers[user.id].append(0)

    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", En términos generales, ¿Cómo considerarías tu salud?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return GENHEALTH


def stroke(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Alguna vez has tenido un infarto?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return STROKE


def asthma(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Padeces de asma?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return ASTHMA

def diabetis(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Padeces diabetis?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return DIABETIS

def kidney_disease(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Padeces de alguna enfermedad en los riñones?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return KIDNEYDISEASE

def skin_cancer(update: Update, context: CallbackContext, ) -> int:
    reply_keyboard = [['Si', 'No']]
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    update.message.reply_text(
        str(user.first_name) + " " + str(user.last_name) + ", ¿Tienes o has tenido cáncer de piel?",
        reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
    )
    return SKINCANCER


def end_query(update: Update, context: CallbackContext, ) -> int:
    user = update.message.chat
    dictUsers[user.id].append(update.message.text)
    print(dictUsers)
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
            RACE : [MessageHandler(Filters.regex('^(White| \
                                                    Black| \
                                                    Latin| \
                                                    Asian| \
                                                    Native American| \
                                                    Other|)$'), smoke, run_async=True)],
            SMOKE : [MessageHandler(Filters.regex('^(Si|No)$'), drink, run_async=True)],
            DRINK : [MessageHandler(Filters.regex('^(Si|No)$'), exercise, run_async=True)],
            EXERCISE : [MessageHandler(Filters.text & ~Filters.command, sleep_time, run_async=True)],
            SLEEPTIME : [MessageHandler(Filters.text & ~Filters.command, physical_healt, run_async=True)],
            PHYSICALHEALTH : [MessageHandler(Filters.text & ~Filters.command, mental_healt, run_async=True)],
            MENTALHEALTH : [MessageHandler(Filters.text & ~Filters.command, difficult_to_walk, run_async=True)],
            DIFWALKING : [MessageHandler(Filters.regex('^(Si|No)$'), general_health, run_async=True)],
            GENHEALTH : [MessageHandler(Filters.regex('^(Excelente| \
                                                        Muy buena| \
                                                        Buena| \
                                                        Regular| \
                                                        Mala)$'), stroke, run_async=True)],
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
    main()