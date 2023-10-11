import random
import yaml
from dotenv import load_dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# set variables
config_path = 'config.yml'

# load config
load_dotenv()
config = yaml.safe_load(open(config_path))
participants, previous_matches = config['participants'], config['previous_matches']
names = list(participants.keys())


def generate_santas():
    """Generate a list of secret santas"""
    secret_santa = {}
    while len(secret_santa) < len(names):

        for name in names:

            """Get a list of possible recipients"""
            possible_recipients = names.copy()

            # remove your own name
            possible_recipients.remove(name)

            # remove your partner's name
            if participants[name]['partner'] in possible_recipients:
                possible_recipients.remove(participants[name]['partner'])

            # remove people you've been matched with in prior years
            for previous_match in previous_matches[name]:
                if previous_match in possible_recipients:
                    possible_recipients.remove(previous_match)

            # remove people who have already been matched with someone else
            for recipient in secret_santa.values():
                if recipient in possible_recipients:
                    possible_recipients.remove(recipient)

            """Make sure the list of possible recipients is not empty"""
            if len(possible_recipients) == 0:
                secret_santa = {}
                break

            """Choose a random recipient"""
            recipient = random.choice(possible_recipients)
            secret_santa[name] = recipient

    return secret_santa


def email_santas(secret_santa):
    """Email secret santas"""
    for santa, recipient in secret_santa.items():

        # format email
        message = Mail(
            from_email=os.environ.get('SENDGRID_EMAIL'),
            to_emails=participants[santa]['email'],
            subject='Secret Santa Assignments',
            plain_text_content=f'{santa.capitalize()} you are the secret santa of {recipient.capitalize()}. Gifts are '
                               f'to be used, handmade, recycled, or re-gifts. No gifts for or gifting of children :) '
        )

        # send email
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
        except Exception as e:
            print(e.message)


def append_to_config(secret_santa):
    """Append secret santas to config.yml"""
    for santa, recipient in secret_santa.items():
        config['previous_matches'][santa].append(recipient)
    with open('config.yml', 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)


if __name__ == '__main__':
    santas = generate_santas()
    email_santas(santas)
    append_to_config(santas)
