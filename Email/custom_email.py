# importing libraries
from flask import Flask
from flask_mail import Mail, Message
# import configparser
#
# # app = Flask('app')
# # print(app)
# print("in custom_email")
# config = configparser.ConfigParser()
# config.read('Email/email_parameter.ini')
# # configuration of mail
# app.config['MAIL_SERVER'] = config.get('EMAIL_PARAMETER', 'MAIL_SERVER')
# app.config['MAIL_PORT'] = config.get('EMAIL_PARAMETER', 'MAIL_PORT')
# app.config['MAIL_USERNAME'] = config.get('EMAIL_PARAMETER', 'MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = config.get('EMAIL_PARAMETER', 'MAIL_PASSWORD')
# app.config['MAIL_USE_SSL'] = config.get('EMAIL_PARAMETER', 'MAIL_USE_SSL')
# mail = Mail(app)


# message object mapped to a particular URL ‘/’
# @app.route("/send_email/<address>")
# def send_email(address):
#     print(address)
#     msg = Message(
#         'Hello',
#         sender='atul00032146@gmail.com',
#         recipients=[address]
#     )
#     msg.body = 'Hello Flask message sent from Flask-Mail'
#     mail.send(msg)
#
#     return 'Sent'


if __name__ == '__main__':
    app.run()