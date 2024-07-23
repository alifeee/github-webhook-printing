# GitHub webhook printing

Print (certain) GitHub webhook events with a thermal printer.

## Install

```bash
mkdir -p /var/www/cgi/
git clone git@github.com:alifeee/github-webhook-printing.git
mv github-webhook-printing githubwebhooks
cd githubwebhooks
chown -R alifeee:www-data .
```

## Use Nginx to turn on CGI scripts

```bash
apt install nginx fcgiwrap
service nginx start
echo 'server {
        listen 80;
        listen [::]:80;

	server_name <server-address>;

	location / {
		fastcgi_intercept_errors on;
		include fastcgi_params;
		fastcgi_param SCRIPT_FILENAME /var/www/cgi/$fastcgi_script_name;
		fastcgi_pass unix:/var/run/fcgiwrap.socket;
	}
}' > /etc/nginx/sites-available/githubwebhook
ln -s /etc/nginx/sites-available/githubwebhook /etc/nginx/sites-enabled/githubwebhook
nginx -t
ufw allow 80
service nginx restart
```

## Test ping CGI script

```bash
curl "http://<server-address>/githubwebhooks/ping.cgi"
```

## Collect example webhook payloads

Go to a GitHub user, repository, or organisation settings page > webhooks. Add a webhook that points to `http://<server-address>/githubwebhooks/hook.cgi`.

Send some webhook requests (by activating GitHub events).

Copy and paste the `env` output and data from the `log` file to files like `webhook-examples/push.env` and `webhook-examples/push.json`.

## Test webhook

Set the webhook to point to `http://<server-address>/githubwebhooks/hook.cgi`

```bash
# push
curl -s --request POST -i -H "X-GITHUB-EVENT: push" "http://<server-address>/githubwebhooks/hook.cgi" -d "@webhook-examples/push.json"
# issue_comment
curl -s --request POST -i -H "X-GITHUB-EVENT: issue_comment" "http://<server-address>/githubwebhooks/hook.cgi" -d "@webhook-examples/issue_comment.json"
# create
curl -s --request POST -i -H "X-GITHUB-EVENT: create" "http://<server-address>/githubwebhooks/hook.cgi" -d "@webhook-examples/create.json"
# pull_request
curl -s --request POST -i -H "X-GITHUB-EVENT: pull_request" "http://<server-address>/githubwebhooks/hook.cgi" -d "@webhook-examples/pull_request.json"
```

## To-do

- print a QR code that links to the event (QR code printing with ESCPOS *without* using a library like [python-escpos] or [node-escpos] is difficult)
- add more events!

[python-escpos]: https://github.com/python-escpos/python-escpos/
[node-escpos]: https://github.com/node-escpos/driver
