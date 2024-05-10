import datetime

def convert_footer_to_dow(dow_footer):
    dow_footer = dow_footer.lower()
    dow=-1
    if (dow_footer=="2a" or dow_footer== "segunda" or dow_footer== "2a-feira" or dow_footer== "segunda-feira"):
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
        feedback_str = "Agendei a seguinte nota: **\"{}\"** para **{}, dia {}**".format(nota,convert_datetime_to_name(event_datetime),formatted_datetime)
    except Exception as e:
        feedback_str = "Houve um problema com a sua nota! O que se passou: " + str(e)
    
    print("!nota command received. Feedback: ",feedback_str)
    return feedback_str


# testing
# if __name__ == "__main__":
def test_parser():
    test_message1 = "!nota cortar o cabelo 6a"
    test_message2 = "bro faz ai uma bela de uma !nota estar com amigos sabado"
    test_message3 = "!nota   aula de cerâmis  3a "

    parse_nota(test_message1)
    print()
    parse_nota(test_message2)
    print()
    parse_nota(test_message3)