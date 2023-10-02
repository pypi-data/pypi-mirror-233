import typer
import fcntl, termios, sys
from halo import Halo
import requests
import pyrebase
from packaging import version as vers
import json, time, jwt
from peregrine import stateutils, client, install, errors, colorutils
import warnings
from requests.exceptions import RequestsDependencyWarning

# Use your Firebase project configuration
firebase_config = {
  "apiKey": "AIzaSyCqZOXQZZ6q1WPzIPIE7anvi3-Hfjuuzh8",
  "authDomain": "peregrine-ai.firebaseapp.com",
  "projectId": "peregrine-ai",
  "storageBucket": "peregrine-ai.appspot.com",
  "messagingSenderId": "517386078622",
  "appId": "1:517386078622:web:716054ea5f5adc15c16e8f",
  "measurementId": "G-WVVENB8ERV",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

class AppState:
    def __init__(self, idToken: str, refreshToken: str, env: dict):
        self.idToken = idToken
        self.refreshToken = refreshToken
        self.env = env

    def __repr__(self):
        return f"<AppState: env: {self.env}, idToken: {self.idToken}>"

app = typer.Typer(context_settings={"allow_extra_args": True, "ignore_unknown_options": True},)

@app.command()
def usage(ctx: typer.Context):
    """
    Print Platitude.ai subscriber info and token usage stats.
    """
    
    ctx.ensure_object(AppState)
    state = ctx.obj

    if not checkTier(state, 1):
        typer.echo("Not subscribed, token usage information is not available.")


    else:
        (idT, _) = stateutils.loadUserTokens()
        email = stateutils.loadUserEmail()
        typer.echo(f"Logged in as: {email}")

        env = stateutils.getEnv()
        uid = env["UID"]
        
        usage = fetchUsage(uid=uid, idT=idT)
        pricing = fetchPricing(uid=uid, idT=idT)
        full_tier = usage['tier']
        
        if full_tier == 0:
            typer.echo("To use Platitude Terminal, sign up for a Platitude.ai plan by running `ai subscribe`")
        elif full_tier in [1,2,3]:
            tokens = usage['tokens']
            total_tokens = pricing[str(full_tier)]['tokens']
            typer.echo(f"Thanks for being a subscriber of Platitude.ai!\n \nYour plan: Plan {full_tier} \nQuota: {total_tokens} tokens per month. \nRemaining tokens: {tokens} tokens this month. \nRemaining tokens are sufficient for an estimated: {int(tokens / 100)} queries or {int(tokens / 400)} explanations. ")


@app.command()
def how(ctx: typer.Context, input: str, force_response= None):
    """
    Get a shell command that completes your INPUT, a natural language task description. 
    """
    ctx.ensure_object(AppState)
    state = ctx.obj

    if not checkTier(state, 1):
        # typer.echo("Subscribe to Platitude.ai's to use natural language shell commands and more! To subscribe, run `ai subscribe`.")
        raise typer.Exit()

    spinner = Halo(text='Loading', spinner='dots')
    
    # print("CTX", getattr(ctx, 'force_response'))
    if force_response:
        response = force_response
    else:
        try:
            spinner.start()
            response = routeQuery(tier=state.env["TIER"], query_type="suggest", query={"query_text": input}, user = {"uid": state.env["UID"], "idToken": state.idToken })
        
        except Exception as e:
            spinner.stop()
            typer.echo(f"{colorutils.colors.FAIL} Error: {colorutils.colors.ENDC} {e}. \n")
            raise typer.Exit()

        else:
            spinner.stop()
    
    action = typer.prompt(f"\n{colorutils.colors.OKGREEN}Suggestion:{colorutils.colors.ENDC} {colorutils.colors.BOLD}{response}{colorutils.colors.ENDC}\n\nUse this command? [y: copy / e: explain / a: alternatives / exit]", type=str)

    if action == "y":
        if response:
            # write generated prompt into terminal input buffer
            writeToTerminal(response)

        raise typer.Exit()

    elif action == "e":

        # ctx.force_response = response
        what(ctx=ctx, command=response)        
        how(ctx=ctx, input="", force_response=response)

    elif action == "a":

        alt_resp = alternatives(ctx=ctx, command=response)

        if alt_resp:
            alt_action = typer.prompt(f"\nSwitch to alternative command or keep original? [y = alternative / N = original]", type=str)

            if alt_action == "y":
                response = alt_resp

        how(ctx, "", force_response=response)
    
    else:
        typer.Exit()


def writeToTerminal(command: str):
    """
    Write a string into the input buffer
    """
    for c in command:
        fcntl.ioctl(sys.stdin, termios.TIOCSTI, c)

@app.command()
def chat(ctx: typer.Context, input: str):
    """
    Talk to ChatGPT in your terminal. 
    """
    ctx.ensure_object(AppState)
    state = ctx.obj
    
    if not checkTier(state, 2):
        # typer.echo("General purppose AI Chat requires a Enthusiast or Professional tier account! To subscribe, run `ai subscribe`.")
        raise typer.Exit()
    
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start()
    
    try:
        chat_response = routeQuery(tier=state.env["TIER"], query_type="chat", query={"query_text": input}, user = {"uid": state.env["UID"], "idToken": state.idToken })
    
    except Exception as e:
        spinner.stop()
        typer.echo(f"{colorutils.colors.FAIL} Error: {e} {colorutils.colors.ENDC}. \n")
        raise typer.Exit()
    else:
        spinner.stop()
        typer.echo(f"{colorutils.colors.OKGREEN}\nResponse: {colorutils.colors.ENDC} {chat_response}\n")

    return chat_response


def checkTier(state: AppState, min_tier: int):
    if min_tier > 0 and state.env["TIER"] != stateutils.tier.PAID:
        typer.echo("Subscribe to Platitude.ai to access this function and more! To do so, run `ai subscribe`.")
        return False
    else:
        full_tier = fetchTier(state.env["UID"], state.idToken, full=True)

        if min_tier > full_tier:
            if min_tier == 2:
                typer.echo(f"This function is only available to Enthusiast or Professional tier subscribers. Use `ai manage` to upgrade your account.")
            elif min_tier == 3:    
                typer.echo(f"This function is only available to Professional tier subscribers. Use `ai manage` to upgrade your account.")
            
            return False
        
    return True


@app.command()
def alternatives(ctx: typer.Context, command: str):
    """
    Get an alternative shell command that accomplishes the same thing as a given COMMAND. Enthusiast & Professional users only.
    """
    ctx.ensure_object(AppState)
    state = ctx.obj

    if not checkTier(state, 2):
        # typer.echo("Shell command alternatives feature requires a Enthusiast or Professional tier account! To manage, run `ai upgrade`.")
        return None
    
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start()

    alt_response = ""
    try:
        alt_response = routeQuery(tier=state.env["TIER"], query_type="alternatives", query={"query_text": command}, user = {"uid": state.env["UID"], "idToken": state.idToken })

    except Exception as e:
        spinner.stop()
        typer.echo(f"{colorutils.colors.FAIL}Error: {colorutils.colors.ENDC} {e}. \n")
        raise typer.Exit()
    else:
        spinner.stop()
        typer.echo(f"{colorutils.colors.HEADER}\nAlternative: {colorutils.colors.ENDC} {colorutils.colors.BOLD}{alt_response}{colorutils.colors.ENDC}.")

    return alt_response


@app.command() 
def what(ctx: typer.Context, command: str):
    """
    Get a natural language description of what the input shell command, COMMAND, does. 
    """
    ctx.ensure_object(AppState)
    state = ctx.obj

    if not checkTier(state, 1):
        raise typer.Exit()

    spinner = Halo(text='Loading', spinner='dots')
    spinner.start()

    try: 
        response = routeQuery(tier=state.env["TIER"], query_type="explain", query={"query_text": command}, user = {"uid": state.env["UID"], "idToken": state.idToken })

    except Exception as e:
        spinner.stop()
        typer.echo(f"{colorutils.colors.FAIL}Error:{colorutils.colors.ENDC} {e}. \n")
        raise typer.Exit()
    else:
        spinner.stop()
        typer.echo(f"{colorutils.colors.HEADER}\nExplanation:{colorutils.colors.ENDC} {response}\n")
    

@app.command()
def login(ctx: typer.Context):
    """
    Log in to an existing Platitude.ai account.
    """
    ctx.ensure_object(AppState)
    state = ctx.obj

    if state.idToken and _isIdTokenValid(state.idToken):
        email = stateutils.loadUserEmail()
        typer.echo(f"Already logged in as {colorutils.colors.BOLD}{email}{colorutils.colors.ENDC}!")
        raise typer.Exit()

    email = typer.prompt("Email", type=str)
    password = typer.prompt("Password", hide_input=True)

    user = refreshUserTokens(email, password)
    if user:
        try:
            server_tier = fetchTier(uid=user["localId"], idT=user["idToken"])
            stateutils.setTier(server_tier)
            state.env["TIER"] = server_tier
            typer.echo("Login Successful!")
            
        except errors.PeregrineConnectionError as e:
            typer.echo(f"{colorutils.colors.FAIL}{e}{colorutils.colors.ENDC}")
            logout()
            raise typer.Exit() 
        except Exception as e:
            typer.echo(f"{colorutils.colors.FAIL}Encountered error during login:{colorutils.colors.ENDC}{e}. Exiting...")
            logout()
            raise typer.Exit()
    else:    
        typer.echo(f"{colorutils.colors.FAIL}Login Unsuccessful!{colorutils.colors.ENDC}")
        stateutils.setTier(stateutils.tier.NONE)
        state.env["TIER"] = stateutils.tier.NONE
        
        raise typer.Exit()


@app.command()
def logout():
    """
    Log out of a Platitude.ai account
    """
    stateutils.removeLocalUser()
    typer.echo("Signed out. All account info removed from local machine.")

    raise typer.Exit()    

@app.command()
def manage(ctx: typer.Context):
    """
    Show subscription management portal to cancel your subscription or change your account tier or payment info. 
    """
    ctx.ensure_object(AppState)
    state = ctx.obj
    
    if not checkTier(state, 1):
        raise typer.Exit()

    else:
        try:
            # here we can assume a signed in user exists, so tokens are available    
            spinner = Halo(text='Loading', spinner='dots')
            idToken = state.idToken
            uid = state.env["UID"]

            typer.echo("Creating your secure account management portal...\n")
            spinner.start()
            time.sleep(2)
            
            auth_headers = {'Authorization': f'Bearer {idToken}', 'Content-Type': 'application/json'}
            
            _cid_body = {"uid": uid}
            _cid_response = requests.post(stateutils.API_DOMAIN + "/stripe-id", data=json.dumps(_cid_body), headers=auth_headers)
            _cid = _cid_response.json()
            
            _cid_TF = _cid["success"]
            if not _cid_TF:
                raise Exception(_cid["response"])
            else:
                cid = _cid["response"]

            body = {"cid": cid, "uid": uid}
            response = requests.post(stateutils.API_DOMAIN + "/create-portal-session", data=json.dumps(body), headers=auth_headers)
            response.raise_for_status()

            session = response.json()
            url = session["url"]

            spinner.stop()
            typer.echo("Done.\n")
            typer.echo(f"{colorutils.colors.BOLD}Here's your unique, secure account management portal:{colorutils.colors.ENDC}\n\n {url}\n\n")

        except Exception as e:
            spinner.stop()
            typer.echo(f'Error creating portal page: {e}')
            typer.echo("Exiting...")
            raise typer.Exit()
            
        else:
            typer.echo("Any changes to your account will be reflected in PlatitudeTerminal shortly. Thanks for being a subscriber! \n")


@app.command()
def subscribe(ctx: typer.Context):
    """
    Upgrade your Platitude.ai account to a paid plan to start using PlatitudeTerminal.
    """
    ctx.ensure_object(AppState)
    state = ctx.obj

    if state.env["TIER"] == stateutils.tier.PAID:
        typer.echo("You're already subscribed, to switch users: `ai login --force` ")
        raise typer.Exit()
    
    if state.env["TIER"] == stateutils.tier.NONE:
        typer.echo("You're not logged in. To subscribe, log in first: `ai login`")
        raise typer.Exit()

    else:
        try:
            # here we can assume a signed in user exists, so tokens are available    
            spinner = Halo(text='Loading', spinner='dots')
            idToken = state.idToken
            uid = state.env["UID"]
            email = stateutils.loadUserEmail()

            p = fetchPricing(uid=uid, idT=idToken)
            

            typer.echo(
                f'''
                                    {colorutils.colors.HEADER}      Select your plan  {colorutils.colors.ENDC}
                ===================================================================
                        All Platitude.ai Plans come with a 7 day free trial!

          {colorutils.colors.BOLD}             Starter               Enthusiast              Professional {colorutils.colors.ENDC}
                ====================    ====================    ====================   
                |                  |    |                  |    |                  | 
                |    ${p['1']['price']} / month    |    |    ${p['2']['price']} / month    |    |    ${p['3']['price']} / month    |
                |    ~{int(p['1']['tokens']/100)} queries  |    |   ~{int(p['2']['tokens']/100)} queries   |    |   ~{int(p['3']['tokens']/100)} queries  |
                |                  |    |                  |    |                  |
                |                  |    |   MOST POPULAR   |    |    BEST VALUE    |
                ====================    ====================    ====================
   {colorutils.colors.BOLD}                     [1]                     [2]                     [3]          {colorutils.colors.ENDC}


                
                Note: Query numbers shown are estimates based on typical usage. 
                       Real-world quota may vary depending on query complexity.\n
                '''
            )
            plan_choice = typer.prompt("Type choice [1 / 2 / 3]", type=int)

            if plan_choice not in [1, 2, 3]:
                typer.echo("Valid choices are 1, 2, or 3")
                raise typer.Abort()
            
            typer.echo(f"\nYou chose plan {plan_choice}. Great choice!")
            typer.echo("\nCreating your secure payment portal...")
            spinner.start()
            time.sleep(2)
            auth_headers = {'Authorization': f'Bearer {idToken}', 'Content-Type': 'application/json'}
            metadata = {"uid": uid, "email": email, "pid": plan_choice}
            checkout_payload = {
                'product_id': plan_choice,
                'metadata': metadata,
                'customer_email': email
            }

            response = requests.post(stateutils.API_DOMAIN + "/create-checkout-session", data=json.dumps(checkout_payload), headers=auth_headers)
            response.raise_for_status()

            session = response.json()
            url = session["url"]

            spinner.stop()
            typer.echo("Done.\n")
            typer.echo(f"{colorutils.colors.BOLD}Here's the link to your unique, secure payment portal:{colorutils.colors.ENDC}\n\n {url}\n\n")

        except Exception as e:
            spinner.stop()
            typer.echo(f'Error creating payment page: {e}')
            typer.echo("Exiting...")
            raise typer.Exit()
            
        else:
            typer.echo("Once you checkout, Platitude Terminal will be ready to use immediately! You can manage your account any time using `ai manage` and show your remaining tokens with `ai usage`.\nIf you don't complete checkout now, you can sign up later using `ai subscribe`. \n\nThanks for subscribing!\n")


@app.command()
def signup(ctx: typer.Context):
    """
    Create a new Platitude.ai account
    """

    ctx.ensure_object(AppState)
    state = ctx.obj

    if not state.env["TIER"] == stateutils.tier.NONE and state.idToken and _isIdTokenValid(state.idToken):
        typer.echo("Already logged in! To log into another account: `ai login --force` ")
        raise typer.Exit()


    typer.echo("""\nEnter your email and create a password. \n""")

    email = typer.prompt("Email", type=str)
    password = typer.prompt("Create a password", hide_input=True, confirmation_prompt=True)

    try:
        headers = {'Content-Type': 'application/json'}
        payload = {
            'email': email,
            'password': password
        }
        response = requests.post(stateutils.API_DOMAIN + "/register", data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        
        user = response.json()["user"]

        # login with the user's credentials
        auth_user = auth.sign_in_with_email_and_password(email, password)
        # print(auth_user)
        idToken = auth_user['idToken']
        refreshToken = auth_user['refreshToken']

        # user assumed to be base here -- user will be upgraded on a restart
        stateutils.setTier(stateutils.tier.BASE)
        stateutils.setUid(user['uid'])
        stateutils.saveUserTokens(email=email, id_token=idToken, refresh_token=refreshToken)

        new_env = {"TIER": stateutils.tier.BASE, "MODEL": stateutils.models.DEFAULT, "UID": user['uid']}
        
        state.env = new_env
        state.idToken = idToken
        state.refreshToken = refreshToken

    except Exception as e:
        stateutils.writeDefaultEnv() # write a Default env 
        typer.echo(f'Error signing up: {e}')
        typer.echo(f'No account was created. Exiting...')
        raise typer.Exit()
    
    else:
        typer.echo(f'Successfully created account with email: {email}.\n ')
        typer.echo("To use Platitude Terminal, subscrbe to a Platitude.ai plan below. \n")
        time.sleep(1)
        
        subscribe(ctx=ctx)

        

@app.command()
def version(verbose = True):
    """
    Print version info.
    """

    try:
        (your_v, latest_v, minimum_v) = fetchVersions()
    
        verboseEcho(f"Currently installed version: {your_v}", verbose)
        
        if vers.parse(your_v) < vers.parse(minimum_v):
            verboseEcho(f"Currently installed version: {your_v} is older than minimum version: {minimum_v}. You'll need to update before you can use Platitude.ai. Please run: `pip install --upgrade PlatitudeTerminal` to get the latest features.", verbose) 
            
            print_branch = typer.prompt("Copy command? [y / N]", type=str)
            if print_branch == 'y':
                writeToTerminal("pip install --upgrade PlatitudeTerminal")
            raise errors.PeregrineVersionOutOfDateError(f"Your version: {your_v}, minnimum version: {minimum_v}, latest version: {latest_v}.")
        
        elif vers.parse(your_v) < vers.parse(latest_v):
            verboseEcho("A new version is available to install! Run: `pip install --upgrade PlatitudeTerminal` to upgrade to get the latest features.", verbose)
            
        else:

            verboseEcho(f"Latest Version: {latest_v}", verbose)
            verboseEcho(f"Minimum Version: {minimum_v}", verbose)

    except errors.PeregrineConnectionError as e:
        typer.echo(f"Local version = {install.__version__}")
        typer.echo(f"Failed to connect to server. Check internet connection and try again: {e}")
        raise typer.Exit()

    except Exception as e:
        typer.echo(f"Error encountered checking version: {e}")
        raise typer.Exit()

def verboseEcho(text: str, active: bool = True):

    if active:
        typer.echo(text)

def fetchVersions():
    your_v = install.__version__
    
    try:
        response = requests.get(stateutils.API_DOMAIN + "/version")
        response.raise_for_status()

        response_json = response.json()
        latest_v = response_json['latest']
        minimum_v = response_json['minimum']

    except Exception as e:
        raise errors.PeregrineConnectionError(f"Versions Failed to connect to server. Check your internet connection. Error {e}")

    else:
        return (your_v, latest_v, minimum_v)


def fetchUsage(uid, idT):
        auth_headers = {'Authorization': f'Bearer {idT}', 'Content-Type': 'application/json'}
        body = {'uid': uid }

        try:
            _response = requests.post(stateutils.API_DOMAIN + "/usage", data=json.dumps(body), headers=auth_headers)
            _response.raise_for_status()

            response = _response.json()
            usage = response["response"]

            return usage
        
        except Exception as e:
            raise errors.PeregrineConnectionError(f"Failed to connect to server to verify user account. Check your internet connection or contact support with this error: {e}")

def fetchPricing(uid, idT):
        auth_headers = {'Authorization': f'Bearer {idT}', 'Content-Type': 'application/json'}
        body = {'uid': uid }

        try:
            _response = requests.get(stateutils.API_DOMAIN + "/pricing")
            _response.raise_for_status()

            pricing = _response.json()
            return pricing
        
        except Exception as e:
            raise errors.PeregrineConnectionError(f"Failed to connect to server to fetch pricing. Check your internet connection or contact support with this error: {e}")


def fetchTier(uid, idT, full = False):
        auth_headers = {'Authorization': f'Bearer {idT}', 'Content-Type': 'application/json'}
        body = {'uid': uid }

        try:
            _response = requests.post(stateutils.API_DOMAIN + "/tier", data=json.dumps(body), headers=auth_headers)
            _response.raise_for_status()

            response = _response.json()
            _tier = response["tier"]

        except Exception as e:
            raise errors.PeregrineConnectionError(f"Tier Failed to connect to server. Check your internet connection. Error {e}")

        else:

            tier = None
            if full:
                tier = _tier
            else:
                if _tier in [1, 2, 3]:
                    tier = stateutils.tier.PAID
                if _tier == 0:
                    tier = stateutils.tier.BASE

            return tier
        
def fetchTokens(uid, idT):

    auth_headers = {'Authorization': f'Bearer {idT}', 'Content-Type': 'application/json'}
    body = {
        'uid': uid
    }

    try:
        _response = requests.post(stateutils.API_DOMAIN + "/usage", data=json.dumps(body), headers=auth_headers)
        _response.raise_for_status()

        response = _response.json()
        _tokens = response["tokens"]

        return _tokens

    except Exception as e:
        raise errors.PeregrineConnectionError(f"Tokens: Failed to connect to server. Check your internet connection. Error {e}")


# @app.command()
# def select_model():
    
#     typer.echo(f"{colorutils.colors.BOLD}Current Model:{stateutils.get_model()} {colorutils.colors.ENDC}")

#     typer.echo("Select from: \n")
#     typer.echo(stateutils.models.MAPPING)
    
#     request = typer.prompt("Select a model [1-4]", type=int)

#     if not request in range(1, 5):
#         request = 1

#     print(request)
#     stateutils.set_model(request)
    
#     typer.echo(f"Model set to {stateutils.models.MAPPING[request]}.")
    

def refreshUserTokens(email, password) -> bool:
    """
    Force a re-auth using Firebase
    """
    
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # print(user)
        stateutils.saveUserTokens(email=email, id_token=user['idToken'], refresh_token=user['refreshToken']) 
        stateutils.setUid(user['localId'])
        
    except Exception as e:
        raise e
        return None
    
    return user

def _isIdTokenValid(id_token):
    """
    Decode and verify JWT token expiration locally
    """
    try:

        # print("Decoding saved token")
        # Decode the ID token without verifying its signature
        payload = jwt.decode(id_token, options={"verify_signature": False})

        # print("Checking expiry time")

        # Get the current time and the token's expiration time
        now = int(time.time())
        exp = payload.get("exp", 0)

        # Check if the token is still valid
        if now < exp:
            # print("exp", exp)
            # print("now", now)
            return True
        else:
            return False
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return False

def savedTokensAreValid() -> bool:
    """
    Return True if saved auth tokens are verified server-side
    """
    try:
        (saved_id_token, saved_refresh_token) = stateutils.loadUserTokens()
        # print("ID", saved_id_token)
        # print("REFRESH", saved_refresh_token)

        if not saved_id_token:
            raise errors.PeregrineExpiredLoginError("Failed to find saved tokens")

        valid = _isIdTokenValid(saved_id_token)
        # print("Token Valid", valid)

        if valid:
            return True
        else:
            # try refreshing 
            refreshed_user = auth.refresh(saved_refresh_token)
            if refreshed_user['idToken']:
                email = stateutils.loadUserEmail()
                stateutils.saveUserTokens(email=email, id_token=refreshed_user['idToken'], refresh_token=refreshed_user['refreshToken'])                
                return True
            else:
                # stored tokens are too old, re-auth!
                raise errors.PeregrineExpiredLoginError()
            
    except errors.PeregrineExpiredLoginError as e:
        typer.echo(f"Your login has expired. Please login again.")
        return False
    
    except Exception as e:
        # user may have no stored tokens
        typer.echo(f"Encountered an error when attempting to login: {e}")
        return False
       

@app.callback()
def main(ctx: typer.Context):

    warnings.simplefilter('ignore')

    try:
        version(verbose=False)

        # create / load env
        tier = None
        if not stateutils.envExists():
            stateutils.createNewEnv()
            _env = stateutils.getEnv()
            tier = _env["TIER"]
        else:
            stateutils.loadFromEnv()
            tier = stateutils.getTier()

        # pass main flow for terminal commands
        if ctx.invoked_subcommand in ['logout']:
            return

        if tier == stateutils.tier.NONE:
            # print sign up flow

            typer.echo(
                '''
                =======================================================================
                |                                                                     |
                |                                                                     |
                |      Platitude Terminal - Natural language command line queries     |
                |                          by Platitiude.ai                           |
                |                                                                     |
                =======================================================================
                '''
            )

            typer.echo("Welcome to Platitude Terminal, an AI assistant for the command line! Create an account or login to get started. \n")
            
            env = stateutils.writeDefaultEnv() #save blank env and copy into memory
            stateutils.clearUserTokens()
            ctx.obj = AppState(idToken = "", refreshToken = "", env = env)

            create_or_login = typer.prompt("1 = Create new Platitude.ai account \n2 = Login with existing account \n\nType choice and press Enter ", type=int)

            if create_or_login == 1:
                signup(ctx)
                raise typer.Exit()    
            elif create_or_login == 2:
                login(ctx)
                raise typer.Exit()

        else:
        # user was once on a paid plan and tokens should exist
            try:
                # first check if tokens exist and are valid / can be refreshed
                existing_idT_is_valid = savedTokensAreValid()

                if existing_idT_is_valid:
                    # get the valid tokens and save them to state
                    (idT, refT) = stateutils.loadUserTokens()   #
                    email = stateutils.loadUserEmail() 
                    env = stateutils.getEnv()        

                    ctx.obj = AppState(idToken = idT, refreshToken = refT, env = env)
                    stateutils.saveUserTokens(email=email, id_token=idT, refresh_token=refT)
                else:
                    # Login has expired
                    typer.echo("Credentials have expired. Please log in again:")
                    stateutils.removeLocalUser() # fully remove any leftover credentials
                    
                    raise typer.Exit()

            except Exception as e:
                typer.echo(f"Error encountered when verifying tokens {e}")
                raise typer.Exit()

            else:
                # check user's tier (may have changed since ENV was written)
                server_tier = fetchTier(uid=env["UID"], idT=idT)
                ctx.obj.env["TIER"] = server_tier
                stateutils.setTier(server_tier)

    except Exception as e:
        typer.echo(f"{e}")
        raise typer.Exit()


def routeQuery(tier, query_type, query: dict, user: dict):

    try:
        _qryFunc = getattr(client, query_type)
        response, _ = _qryFunc(user_text = query['query_text'], idToken = user["idToken"], uid=user["uid"])
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 412:
            raise errors.PeregrineInsufficientTokensError(f"You've run out of tokens for this month. To get more, use `ai manage` to upgrade your account.")
        elif e.response.status_code in  [403, 401]:
            raise errors.PeregrineServerError("Authentication failed")
        elif e.response.status_code in  [500]:
            raise errors.PeregrineServerError("Internal server error")
        
    return response
