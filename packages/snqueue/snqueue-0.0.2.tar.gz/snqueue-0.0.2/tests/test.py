from snqueue import SnQueue

profile_name = "email-automation"
sqs_url = "https://sqs.us-east-1.amazonaws.com/284584416663/incoming_mail"
sns_topic_arn = "arn:aws:sns:us-east-1:284584416663:public_test"

try:
  messenger = SnQueue(profile_name)
  messages = messenger.retrieve(sqs_url, False)
  print(messages)

  response = messenger.notify(sns_topic_arn, "This is a test notification.")
  print(response)
except Exception as e:
  print(e)