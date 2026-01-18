import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from utils.storage import load_state, save_state
from utils.utils import one_in_x
from fastapi.responses import HTMLResponse
from characters.animated_characters import characters,description
from characters.animals import characters as animals
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Impostor")

@app.get("/root")
def root():
    amount_players = 4

    amount_characters = len(characters)


    state = load_state()

    count_players_in = state["count"]
    impostor_assigned = state["impostor_assigned"]
    character = state["character"]
    first_assigned = state["first_assigned"]

    if count_players_in >= amount_players:
        return {"Mensaje": "La sala ya está llena"}
    is_first = False
    if not first_assigned:
        is_first = one_in_x(amount_players-count_players_in)


    if not character:
        index_character = random.randint(0, amount_characters-1)
        character = characters[index_character]

    is_impostor = False
    if not impostor_assigned:
        is_impostor = one_in_x(amount_players-count_players_in)
        if is_impostor:
            impostor_assigned = True

    new_data = {
        "count": count_players_in+1,
        "impostor_assigned": impostor_assigned,
        "character": character,
        "first_assigned":is_first
    }   

    save_state(new_data)

    msj_impostor = "Sos el impostor!!!"
    url = f"https://www.google.com/search?q={character.replace(" ","+")}{description.replace(" ","+") if description else ''}"

    html_content = f"""
    <html>
        <head>
            <title>Impostor</title>
        </head>
        <body>
            <h1 style="font-size: 70px;">{msj_impostor if is_impostor else character}</h1>
            {f"<a style='font-size: 50px'; target='_blank' href={url}> Link </a>"if not is_impostor else ""}
            
            <h2 style="font-size: 40px;">{"Te toca arrancar" if is_first else ""}</h2>
            <a style='font-size: 50px' href="/">Recargar</a> 
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)


@app.get("/reset")
def reset():
    new_data = {
        "count": 0,
        "impostor_assigned": False,
        "character": None,
        "first_assigned": False
    }

    save_state(new_data)

    return {"Mensaje": "Se reseteo la ronda"}


class Player:
    def __init__(self, websocket: WebSocket, name: str):
        self.websocket = websocket
        self.name = name
        self._role = "normal"
        self._is_first = False
        self._is_admin = False

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value: bool):
        self._is_admin = value

    @property
    def role(self):
        return self._role
    
    @role.setter
    def role(self, new_role:str):
        self._role = new_role

    @property
    def is_first(self):
        return self._is_first
    
    @is_first.setter
    def is_first(self, value: bool):
        self._is_first = value

    def set_as_impostor(self):
        self.role = "impostor"

    def clear_role(self):
        self.role = "normal"

    def clear_first(self):
        self.is_first = False

    async def send_state_in_round(self, character:str):
        data_ws = {
            "code_ws": 2,
            "data": self.info_in_round(character)
        }
        await self.websocket.send_json(data_ws)

    def clear_state(self):
        self.clear_first()
        self.clear_role()

    @property
    def is_impostor(self):
        return True if self.role == "impostor" else False
    
    @property
    def info_in_room(self)-> dict:
        return {
            "name": self.name,
            "is_admin": self.is_admin
        }
    
    def info_in_round(self, character: str)-> dict:
        return {
            "name": self.name,
            "character": character if not self.is_impostor else None,
            "is_impostor": self.is_impostor,
            "is_first": self.is_first,
            "is_admin": self.is_admin
        }




class ManagerGame:
    def __init__(self, quota_players:int, characters: list[str]):
        self.manager_connection: ManagerConnection = ManagerConnection()
        self.quota_players = quota_players
        self._current_character = None
        self.characters = characters

    @property
    def players(self):
        return self.manager_connection.active_players

    @property
    def is_complete(self):
        return True if self.manager_connection.count_active_players == self.quota_players else False

    @property
    def count_active_players(self):
        return self.manager_connection.count_active_players
    
    @property
    def current_character(self):
        return self._current_character
    
    @current_character.setter
    def current_character(self, new_character: str | None):
        self._current_character = new_character

    def clear_character(self):
        self.current_character = None
    
    @property
    def have_admin(self):
        return any([player for player in self.players if player.is_admin])
    
    def clear_round(self):
        self.clear_character()
        for player in self.players:
            player.clear_state()

    def assign_impostor(self):
        impostor_player = random.choice(self.players)
        impostor_player.set_as_impostor()

    def assing_first(self):
        first_player = random.choice(self.players)
        first_player._is_first = True

    def assign_admin(self):
        if not self.players:
            return
        if not self.have_admin:
            admin_player = random.choice(self.players)
            admin_player.is_admin = True

    async def send_info_to_players(self):
        for player in self.players:
            await player.send_state_in_round(self.current_character)

    async def new_round(self):
        self.clear_round()

        self.current_character = random.choice(self.characters)

        self.assign_impostor()
        self.assing_first()

        await self.send_info_to_players()

    @property
    def waiting_state(self):
        return {
            "quota_players": self.quota_players,
            "active_players": self.count_active_players,
            "players": [player.info_in_room for player in self.players]
        }

    
    async def waiting(self):
        await self.manager_connection.broadcast(self.waiting_state, 1)

    def disconnect(self, player: Player):
        self.manager_connection.disconnect(player)

        if player.is_admin:
            self.assign_admin()

    def connect(self, player: Player):
        if self.is_complete:
            print("Sala llena")
            return False
        connected = self.manager_connection.connect(player)

        if not connected:
            return False

        self.assign_admin()
        return True
        


class ManagerConnection:
    def __init__(self):
        self._active_players : list[Player] = []

    @property
    def active_players(self):
        return self._active_players

    def connect(self, player: Player):
        if player in self.active_players:
            return False
        self._active_players.append(player)
        return True

    def disconnect(self, player: Player):
        if player in self.active_players:
            self._active_players.remove(player)

    async def broadcast(self, data: dict, code_ws: int):
        data_ws = {
            "code_ws": code_ws,
            "data": data
        }

        for player in self.active_players:
            await player.websocket.send_json(data_ws)

    @property
    def count_active_players(self):
        return len(self.active_players)


manager_game = ManagerGame(2, animals)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.websocket("/ws/{player_name}")
async def ws(websocket: WebSocket, player_name: str):

    if not player_name or player_name == "null":
        return None
    
    player = Player(websocket, player_name)
    connection_success = manager_game.connect(player)

    if not connection_success:
        return None
    
    try:
        await websocket.accept()
    except:
        manager_game.disconnect(player)
        return None

    try:
        await manager_game.waiting()
        while True:
            data = await websocket.receive_json()
            print(data)
            if player.is_admin and data["action"] == "next_round":
                if manager_game.is_complete:
                    print("Ejecutando nueva ronda")

                    await manager_game.new_round()
                else:
                    await manager_game.waiting()
                

    except WebSocketDisconnect:
        print("SE DESCONECTO PLAYER CAPA HTTP")
        manager_game.disconnect(player)
        await manager_game.waiting()
        return None
    
@app.get("/status/room")
def home():

    players = manager_game.players

    admins = [player.name for player in players if player.is_admin]

    new_data = {
        "players": [player.name for player in players],
        "admins": admins
    }

    return {"Mensaje": new_data}
