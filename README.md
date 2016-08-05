# smtp_mail

A simple smtp_mail class `MyMail`

# Install

    pip install git+https://github.com/dneise/smtp_mail

After importing `smtp_mail` the first time, you'll find a config file in `$HOME/.smtp_mail/config.json`.
You'll want to fill some info in here, in order to quickly mail stuff around.

# config file

In case you need to authentify yourself agains the SMTP server use this
```json
  {
      "default_sender": "me@host.com",
      "smtp":{
          "host": "smtp.mail.google.com",
          "port": 465,
          "username": "username",
          "password": "secret"
      },
      "contacts":{
      }
  }
```
If you do not need to authentify yourself:
```json
  {
      "default_sender": "me@host.com",
      "smtp":{
          "host": "smtp",
          "port": 465,
      },
      "contacts":{
      }
  }
```

If you want you can setup a contact list for quickly mailing your friends:
```json
  {
      ...
      "contacts":{
        "me": "yourself@host.com",
        "mom": "your_mom@gmail.com",
        "boss": "your_boss@work.com",
        "bob": "bob@alice.com"
      }
  }
```


# Usage 

You want to quickly mail a plot to a couple of friends? okay ...

```python
import matplotlib.pyplot as plt
plt.plot([1,2,3], [4,5,6])
plt.savefig("awesome_plot.png")

from smtp_mail import MyMail
MyMail("look at this", ["mom", "bob", "alice@bob.com"], attachments=["awesome_plot.png"]).send()
```
