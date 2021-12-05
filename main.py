import cv2
import numpy as np
import smtplib
import playsound
import threading

Alarm_Status = False
Email_Status = False
Fire_Reported = 0


def play_alarm_sound_function():
    while True:
        playsound.playsound('danger.mp3.mp3', True)


def send_mail_function():#fonction bech nab3thou email
    sender_email = 'jbeliramy@gmail.com'
    password = '********'
    rec_email = 'rymjbeli22@gmail.com'
    message = 'fire here, please check ur house '
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    server.login(sender_email, password)
    print('test after login')


    server.sendmail(sender_email, rec_email, message)
    print('mail teb3ath')


video = cv2.VideoCapture(0)

while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (960, 700))

    blur= cv2.GaussianBlur(frame, (21, 21), 0)# dhbeeba bech najmou nkharjou pixel asheel puisque akber
     #cv2.imshow("rrr",blur)
    #blur1 = cv2.imshow('frame', frame)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)# bech  nconvertiw les couleur ll hsv bech najmou mbaad nahsrou loon enar
     #cv2.imshow('ttt',hsv)
    lower = [160,100,20]
    upper = [179,255,255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")#lena badelna type mta3 lower w upper khater range mta3 unit8[0.255]

    mask = cv2.inRange(hsv, lower, upper)#in range tkharjena range  mta3 couleur rouge
    cv2.imshow('vvv',mask)
    output = cv2.bitwise_and(frame, frame,mask=mask )
    cv2.imshow('test',output)
    nored = cv2.countNonZero(mask)

    if int(nored) > 4000:
        Fire_Reported = Fire_Reported + 1


    #cv2.imshow("output", output)

    if Fire_Reported >= 1:

        if Alarm_Status == False:

            threading.Thread(target=play_alarm_sound_function).start()

            Alarm_Status = True

        if Email_Status == False:
            threading.Thread(target=send_mail_function).start()

            Email_Status = True


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()