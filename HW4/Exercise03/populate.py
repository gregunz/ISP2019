import sys
import  random
import hashlib
import binascii
import string

entries = 20
message_length = 10 # words

wordlist = """
aeinstein
alanturing
alberteinstein
aleinstein
alturing
amadeus
aphrodite
armstrong
athena
babbage
bacchus
bach
bacon
barnard
beethoven
beowulf
bessel
bismark
brahms
brandon
cabot
caesar
cahill
callahan
calumet
calvary
campbell
carleton
carlin
carlson
carlton
carlyle
carmen
carnegie
carroll
caruso
casanova
casey
castro
cauchy
cbabbage
cepheus
chadwick
chambers
chang
chaplin
chapman
charlesbabbage
chauncey
chester
chopin
christ
claus
clinteastwood
cochran
cody
cohen
cohn
colby
cole
collins
compton
conner
conrad
coolidge
corbett
costello
cpebach
crandall
cranford
cranston
crawford
crusoe
culver
cummings
cupid
curtis
cushing
cushman
custer
daley
daly
danzig
darwin
davinci
davy
dawson
deane
decker
delilah
dempsey
derek
desmond
dewey
dickens
dillon
dionysia
dionysius
dirac
disney
dobbs
doctorjones
donahue
donovan
douglas
dowjones
doyle
dr.jones
dr.seuss
draco
drexel
dreyfuss
drjones
drseuss
drummond
dudley
duncan
durrell
dyson
eastwood
edison
edmonds
edmonton
ehrlichman
einstein
electra
emerson
emmanuel
emowilliams
endicott
enoch
enos
enrico
epstein
erickson
ericsson
erwin
euclid
euler
evanston
ewing
faber
faraday
fargo
faulkner
faust
feldman
fenton
ferguson
fermat
fermi
feynman
fields
finnegan
foley
forbes
ford
forrest
forsythe
fourier
freedman
freemandyson
freud
friedman
fruehauf
fuchs
fulton
gabriel
galois
gates
gaul
gaulle
gauss
geiger
gerhardt
gershwin
ghandi
gibbs
gibson
gideon
gillette
gilligan
gleason
goddard
godfrey
goethe
goldberg
goldman
goode
goodman
goodwin
gorham
grayson
greer
griffith
griswold
grossman
haberman
halley
hamilton
hammond
hancock
handel
hanford
hannibal
hannible
harding
harrison
harvard
hathaway
healey
healy
hearst
hegelian
hepburn
hershel
hess
higgins
hilbert
hines
hitler
holm
holman
holmes
hoover
horowitz
houdini
hubbard
hubbell
humboldt
hurst
huxley
indianajones
indira
jackson
jarvin
jcbach
jehovah
jenkins
jesus
johan amadeus
johan christof
johan sebastian
johanamadeus
johanchristof
johansebastian
joplin
jsbach
judas
judithresnick
judyresnick
kahn
kane
kant
kaplan
keaton
keller
kendall
kennedy
kepler
kermit
kessler
keynes
kipling
kirchner
kirchoff
klaus
klein
knapp
krause
krueger
kruger
lagrange
landis
laplace
larsen
larson
lawrence
lazarus
lehar
leighton
lenin
leonardo
levi
levin
levis
leyden
lincoln
lindberg
lindsey
lipton
livingston
lockhart
lockwood
logan
lombardy
lovelace
lowell
lucas
lucifer
ludwig
luther
lyman
macgregor
madonna
mahoney
malden
manfred
mann
marceau
marshall
mattson
maxwell
mccall
mccarthy
mccarty
mcdonald
mcgee
mcgill
mcgovern
mcgregor
mcguire
mcintosh
mckay
mckenzie
mckinley
metcalf
metzler
meyer
meyers
miller
mills
milton
minsky
mohr
monroe
moriarty
morley
morrison
morse
moses
mozart
mueller
myers
nabisco
napoleon
natchez
nelsen
nelson
newman
nichols
nielsen
nielson
nitzhe
nitzhye
nixon
nixxon
nobel
norris
nostradamus
obrien
oconnor
octavia
odessa
ohare
olson
orpheus
orwell
osborn
osborne
oscar
osgood
oswald
othello
ottoman
paine
palomar
pandora
parks
pascal
pauli
payne
pegasus
penrose
pericles
perkins
pershing
plato
pluto
poincare
poisson
pollard
pollux
poseidon
powell
powers
poynting
prescott
preston
ptolemy
pulitzer
purcell
quixote
rabin
rachmaninoff
raleigh
rayleigh
reagan
reeves
reinhold
resnick
reuben
reubens
rfeynman
richter
riley
ripley
robeling
robinwilliams
robling
rockford
rockwell
roebling
rousseau
ruben
rubens
rushmore
samson
sandburg
sanders
saunders
schafer
schlegel
schmidt
schopenhauer
schubert
schultz
schuster
schwartz
scorpio
scottjoplin
seuss
seville
shaffer
shapiro
shepard
sheppard
sheraton
sheridan
sherlock
sherman
sherwood
shields
shockley
siegmund
siemens
sigmund
simmons
sinclair
snyder
socrates
solomon
spencer
sprague
staley
stalin
stanford
stearns
stevenson
sting
stockton
strauss
strom
tacitus
taurus
taylor
tennyson
tesla
thompson
thomson
thor
thoreau
tolstoy
turing
tyler
valkyrie
vanderbilt
vaughan
vaughn
verde
verdi
waals
walden
waltdisney
wamozart
weinberg
weston
whipple
whitaker
whitman
whitney
wilkes
williams
windsor
winston
winters
wolfgang
yokono
yokoono
"""

words = wordlist.splitlines()

def random_word():
    return random.choice(words)

def random_message(r):
    return " ".join(r.sample(words,r.randint(5,message_length)))

def names(r):
    length = r.randint(5,entries)
    return r.sample(words,length)

def pwd(r, user):
    h = hashlib.sha256()
    letters = r.sample(string.ascii_lowercase,10)
    h.update("".join(letters).encode())
    h.update(user.encode())
    return binascii.hexlify(h.digest()).decode()

def get_data(seed):
    r = random.Random()
    r.seed(seed.encode())
    list_names = names(r)
    users = [ [name,pwd(r,name)] for name in list_names ]
    msgs = [ (u,random_message(r)) for u in list_names ]
    return users,msgs

def populate_db(seed,cursor):
    users,msgs = get_data(seed)
    sql_users = "INSERT INTO users (name,password) VALUES "
    sql_users += ",".join(["('" + u + "','" + p + "')" for u,p in users])
    sql_msgs = "INSERT INTO messages (name, message) VALUES "
    sql_msgs += ",".join(["('" + u + "','" + m + "')" for u,m in msgs])
    cursor.execute(sql_users)
    cursor.execute(sql_msgs)