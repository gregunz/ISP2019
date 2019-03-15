To repeat the attack:

1. Go to website `http://com402.epfl.ch/hw1/ex2/login`
2. Login with whatever username and password but remember it
3. You will be logged in with a cookie named `LoginCookie` encoded in base64.
4. Decode it, replace the username used with `gregoire.clement@epfl.ch` and `user` with `administrator`, encode it and replace the previous cookie.

Now if you access the page `http://com402.epfl.ch/hw1/ex2/list` with the new cookie, and click on the button, token will be displayed on the webpage.
