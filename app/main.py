import random
from fastapi import FastAPI
from app.utils.storage import load_state, save_state
from app.utils.utils import one_in_x
from fastapi.responses import HTMLResponse
from app.characters.animated_characters import characters,description

app = FastAPI(title="Impostor")



@app.get("/")
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)