from flask_mail import Message


def send_mail(mailbox, **kwargs):
    pp = {k: v for k, v in kwargs}
    subject = pp.pop('subj')
    recipients = pp.pop('recp')
    body = pp.pop('bd')

    pp['subject'] = subject
    pp['recipients'] = recipients
    pp['body'] = body

    msg = Message(
        **pp
    )
    mailbox.send(msg)
    del pp
    del kwargs
