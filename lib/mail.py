import smtplib

server=smtplib.SMTP('smtp.gmail.com',587)

server.ehlo()
server.starttls()
server.ehlo()
server.login('karthikeyansenthilkumar0@gmail.com','kS4193#975')
server.sendmail("karthikeyansenthilkumar0@gmail.com","deviljoker884@gmail.com","mailsent")