from wit import Wit#, Error
import datetime, os

access_token = os.environ['WIT_AI_TOKEN']

client = Wit(access_token = access_token)

def wit_response(message_text):
    resp = client.message(message_text)
    print(resp)

    entities = None
    values = ["", ""]


    try:
        entities = list(resp['entities'])

        for i in range(len(entities)):
            if i > 1:
                continue

            values[i] = (resp['entities'][(entities[i])][0]['value'])

            print("parsing")

            if values[i] != "" and "-" in values[i]:
                try:
                    print("date time parse")
                    #print(values[i])
                    values[i] = values[i][:-10]
                    #print (values[i])
                    xyz = datetime.datetime.strptime(str(values[i]), "%Y-%m-%dT%H:%M:%S") #Need to find a better way of parsing iso 8601 date time strings while keeping timezone i.e. -8:00 UTC
                    #print(xyz)
                    values[i] = xyz
                except: #Not an iso 8601 date time string
                    print("date time parse fail")
                    pass

    except: #Error as e:
        print("WIT AI EXCEPTION")
        pass




    return (entities, values)


#print(wit_response("check if i have class tomorrow"))
