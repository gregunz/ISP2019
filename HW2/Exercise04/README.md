# Solutions

Replace default page by `index.html`:

`nano /www/index.html` 

Put the certificates in:

`/etc/nginx/ssl/`

Replace default nginx conf with `ex4a.conf` or `ex4b.conf`:

`nano /etc/nginx/conf.d/default.conf`

Launch nginx:

`nginx`

Verify with:

`./verify.sh a` or `./verify.sh b` depending on the conf your want to test.