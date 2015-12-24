# banner-notifications
Script to retrieve and e-mail end-of-semester grades from the Ellucian Banner Web application. The script can be ran as a background process; it terminates when all grades have been posted. I wrote this to automate the grade checking process, as I couldn't find a built-in notification system and I was tired of refreshing the webpage manually.

To run the script:

`settings.py` needs to be updated with your personal information.

`USERNAME` and `PASSWORD` refer to your school-provided username and password used to access the Banner Web system.

`MAILCHIMP_KEY` refers to the API key provided by the [MailChimp](https://login.mailchimp.com/signup) service. That can be left blank and the e-mail notification code within `scrape.py` can be commented out if you don't care for e-mail notifications. The Mandrill API can be installed with `pip install mandrill`.

`BASE_URL` refers to the base URL used by your school's Banner Web portal -- for instance, my school's login page ends with `...edu/prodban/twbkwbis.P_WWWLogin`. Everything up to `prodban/` is used in my BASE_URL. The stored procedures used by Banner Web (like `twbkwbis.P_WWWLogin`) may vary for your school as well and may need to be modified within the `scrape.py` script.

`MY_NAME` and `MY_EMAIL` are used to create and deliver e-mail notifications and may be ignored if you don't care for e-mail notifications.
