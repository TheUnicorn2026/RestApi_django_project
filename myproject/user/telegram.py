# /Desktop/REST_API2/RestApi_django_project/myproject$ curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates" | jq .
# {
#   "ok": true,
#   "result": [
#     {
#       "update_id": 354117298,
#       "message": {
#         "message_id": 1,
#         "from": {
#           "id": 1321713645,
#           "is_bot": false,
#           "first_name": "Kaushal",
#           "last_name": "Shinde",
#           "username": "Kaushal008",
#           "language_code": "en"
#         },
#         "chat": {
#           "id": 1321713645,
#           "first_name": "Kaushal",
#           "last_name": "Shinde",
#           "username": "Kaushal008",
#           "type": "private"
#         },
#         "date": 1768063005,
#         "text": "/start",
#         "entities": [
#           {
#             "offset": 0,
#             "length": 6,
#             "type": "bot_command"
#           }
#         ]
#       }
#     }
#   ]
# }