import datetime
from modules import scheduling

def convert_footer_to_dow(dow_footer):
    dow_footer = dow_footer.lower()
    dow=-1
    if(dow_footer=="hoje"):
        dow=-1
    elif (dow_footer=="2a" or dow_footer== "segunda" or dow_footer== "2a-feira" or dow_footer== "segunda-feira"):
        dow = 0
    elif(dow_footer=="3a" or dow_footer== "terca" or dow_footer== "terça" or dow_footer== "3a-feira" or dow_footer== "terca-feira" or dow_footer== "terça-feira"):
        dow = 1
    elif(dow_footer=="4a" or dow_footer== "quarta" or dow_footer== "4a-feira" or dow_footer== "quarta-feira"):
        dow = 2
    elif(dow_footer=="5a" or dow_footer== "quinta" or dow_footer== "5a-feira" or dow_footer== "quinta-feira"):
        dow = 3
    elif(dow_footer=="6a" or dow_footer== "sexta" or dow_footer== "6a-feira" or dow_footer== "sexta-feira"):
        dow = 4
    elif(dow_footer=="sabado" or dow_footer== "sábado"):
        dow = 5
    elif(dow_footer=="domingo"):
        dow = 6
    else:
        raise Exception("A mensagem não termina num dia da semana válido!")
    return dow

def convert_datetime_to_name(datetime):
    dow = datetime.weekday()
    weekday = ""
    if(dow==0):
        weekday="2a feira"
    elif(dow==1):
        weekday="3a feira"
    elif(dow==2):
        weekday="4a feira"
    elif(dow==3):
        weekday="5a feira"
    elif(dow==4):
        weekday="6a feira"
    elif(dow==5):
        weekday="Sábado"
    elif(dow==6):
        weekday="Domingo"

    return weekday

def interpret_time(dow_footer):
    current_date = datetime.datetime.now()
    current_dow = current_date.weekday()
    next_dow = convert_footer_to_dow(dow_footer)
    if (next_dow == -1):
        days_until_event = 0
    else:
        days_until_event = next_dow-current_dow
        if(days_until_event<=0):
            days_until_event=days_until_event+7

    return current_date + datetime.timedelta(days=days_until_event)

def parse_nota(message):
    header = "!nota"
    feedback_str = ""
    try:
        if(message.strip() == header):
           raise Exception("A sua !nota está vazia")

        # split original message, header might be in the middle, lets go to start
        message_parts = message.split(header)

        if(len(message_parts)>2):
           raise Exception("Lamentamos mas só conseguimos uma nota de cada vez")

        message_payload=message_parts[len(message_parts)-1].strip()
        parts = message_payload.split()

        dow_footer = parts[len(parts)-1].strip()
        nota  = message_payload.split(dow_footer); nota = nota[0].strip()

        if(nota == ""):
            raise Exception("A sua nota está vazia")

        event_datetime = interpret_time(dow_footer)
        output_format = "%d-%m"
        formatted_datetime = event_datetime.strftime(output_format)

        event_id = scheduling.add_event(nota, formatted_datetime)

        feedback_str = "Agendei a seguinte nota: **\"{}\"** para **{}, dia {}**. Para cancelar usar o comando !cancelar {}".format(
            nota,convert_datetime_to_name(event_datetime),
            formatted_datetime,
            event_id
            )
    except Exception as e:
        feedback_str = "Houve um problema com a sua nota! O que se passou: " + str(e)
    
    return feedback_str

#TODO: add days of week
def list_notas():
    try:
        feedback_str = ""
        json_data = scheduling.get_sched()
        for event_str, event in json_data.items():
                event_number = -1
                if(event_str.startswith("event_")):
                    event_number = int(event_str.split('_')[1])
                    nota = event["nota"]
                    formatted_datetime = event["event_datetime"]
                    feedback_str = feedback_str + "\nNota **{}**: **\"{}\"**, no dia **{}**".format(
                        event_number,
                        nota,
                        formatted_datetime
                        )
    except Exception as e:
        feedback_str = "Houve um problema! O que se passou: " + str(e)
    return feedback_str

def erase_nota(message):
    header = "!cancelar"
    feedback_str = ""
    try:
        if(message.strip() == header):
           raise Exception("O seu !cancelar precisa de um número de nota")

        message_parts = message.split(header)
        event_id=message_parts[len(message_parts)-1].strip()

        if(event_id.isdigit()):
            nota, formatted_datetime = scheduling.erase_event(event_id)
        elif (event_id == "todas" or event_id == "tudo"):
            scheduling.erase_all()
            return "Todos os eventos foram apagados!"
        else:
            raise Exception("O seu número de nota não é um número!")

        feedback_str = "O evento número {}: **\"{}\"**, dia **{}**, foi cancelado com sucesso".format(
            event_id,
            nota,
            formatted_datetime
            )
    except Exception as e:
        feedback_str = "Houve um problema com o cancelamento da sua nota! O que se passou: " + str(e)

    return feedback_str

def update_streak(message):
    header = "!streak"
    feedback_str = ""
    try:
        if(message.strip() == header):
           raise Exception("A sua !streak precisa de um tópico! Exemplo: !streak sax")

        message_parts = message.split(header)
        topic=message_parts[len(message_parts)-1].strip()

        streak_datetime = interpret_time("hoje")
        output_format = "%d-%m"
        formatted_datetime = streak_datetime.strftime(output_format)
        days = scheduling.increment_streak(topic, formatted_datetime)

        if days > 0:
            feedback_str = "Renovamos a sua streak de {}! Já vai em {} dias! :fire:".format(
                topic,
                days
                )
        else:
            feedback_str = "Já renovaste a streak de {} hoje!!! Tenta amanhã outra vez :sweat_smile:".format(topic)
    except Exception as e:
        feedback_str = "Houve um problema com a sua streak! O que se passou: " + str(e)

    return feedback_str