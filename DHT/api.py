import os
from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv
from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from twilio.rest import Client
import requests
from .models import Dht11, Incident

# Charger les variables d'environnement
load_dotenv()

person_counter = 0

@api_view(["GET", "POST"])
def Dlist(request):
    global person_counter

    if request.method == "GET":
        all = Dht11.objects.all()
        data_ser = DHT11serialize(all, many=True)
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)
            
            #alertes
            if derniere_temperature > 25:
                Incident.objects.create(temperature=derniere_temperature)

                if person_counter == 0:
                    #alert mail
                    subject = 'Alerte'
                    message = 'La température dépasse le seuil, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['ibrahimalaoui001@gmail.com']
                    send_mail(subject, message, email_from, recipient_list)
                    
                elif person_counter == 1:
                    
                    # alert mail
                    subject = 'Alerte'
                    message = 'La température dépasse le seuil, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['ibrahimalaoui001@gmail.com']
                    send_mail(subject, message, email_from, recipient_list)

                person_counter += 1

            if derniere_temperature < 25:
                person_counter = 0
            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)