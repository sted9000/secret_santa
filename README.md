# Secret Santa Generator
## Description
A quick and simple secret santa generator with a few extra features.
- Organize without the organizer knowing who has who
- Avoid couples having each other
- Avoid people having the same person as last year

## Usage
1. Create a config.yml file with the following format:
    ```yaml
    # config.yml
    participants:
      alice:
        email: example@email.com
        partner: bob
      bob:
        email: example@email.com
        partner: alice
      charlie:
        email: example@email.com
        partner: null
    previous_matches:
      alice:
      - charlie
      bob:
      - null
      charlie:
      - alice
    ```
2. Place sendgrid api and sender email in .env file
    ```bash
    # .env
    SENDGRID_API_KEY='<SENDGRID_API_KEY>'
    SENDGRID_EMAIL='<SENDGRID_EMAIL>'
    ```
   Tip: If you don't want your email to end up in spam, make sure to verify your sender email and domain.
3. Run `python3 secret_santa.py`
