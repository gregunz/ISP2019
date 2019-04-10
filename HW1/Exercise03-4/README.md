To repeat the attack:

1. `chmod +x run_dockers_new.sh`
2. `./run_dockers_new.sh gregoire.clement@epfl.ch`
3. `docker exec -it attacker /bin/bash`
4. `cd /shared`
5. `chmod +x startup_commands.sh`
6. `./startup_commands.sh`
7. `python3 interceptor.py`

Token will automatically be printed!
