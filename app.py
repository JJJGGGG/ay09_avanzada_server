from flask import Flask, request
import json

Datos = [
    {"apellido":"Huerta","estado":"rechazado","id":1,"motivacion":"ser admin","n_alumno":"12233445","nombre":"Julio"},
    {"apellido":"García","estado":"aceptado","id":2,"motivacion":"ser master","n_alumno":"22332443","nombre":"Julian"},
    {"apellido":"Campos","estado":"pendiente","id":3,"motivacion":"ffdfdfdfdfdfdfdf","n_alumno":"10002993","nombre":"Clemente"},
    {"apellido":"Toledo","estado":"aceptado","id":4,"motivacion":"","n_alumno":"10993856","nombre":"Diego"},
    {"apellido":"Olguín","estado":"aceptado","id":5,"motivacion":"","n_alumno":"8849300J","nombre":"Carlos"},
    {"apellido":"Miranda","estado":"aceptado","id":6,"motivacion":"","n_alumno":"94883928","nombre":"Catalina"},
    {"apellido":"Perez-Cotapos","estado":"pendiente","id":7,"motivacion":"","n_alumno":"13233452","nombre":"Cristobal"}
]

ID_COUNTER = 3

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return {"texto": "Hello, World!"}

@app.route("/delete_db", methods=["GET"])
def delete_db():
    with open("data/ayudantes.json", "w") as info:
        json.dump(Datos, info, indent=4)
    return {"ok": True}

@app.route("/ayudantes", methods=["GET", "POST"])
def ayudantes():
    if request.method == "GET":
        with open("data/ayudantes.json") as info:
            data = json.load(info)
        return {"status_message": "OK", "Ayudantes": data}, 200
    
    elif request.method == "POST":
        nuevo = request.get_json()

        with open("data/ayudantes.json") as info:
            data = json.load(info)

        new_id = max(ayudante["id"] for ayudante in data) + 1
        nuevo["id"] = new_id
        nuevo["estado"] = "pendiente"
        nuevo["motivacion"] = ""

        data.append(nuevo)

        with open("data/ayudantes.json", "w") as info:
            json.dump(data, info, indent=4)

        return {"message": "CREATED", "Ayudante": nuevo}, 201
    

@app.route("/ayudantes/<int:id>", methods=["GET"])
def get_ayudante(id):
    with open("data/ayudantes.json") as info:
        data = json.load(info)
    
    ayudante = next(filter(lambda ayudante: ayudante["id"] == id, data))
    
    if ayudante:
        return {"status_message" : "OK", "Ayudante" : ayudante}, 200
    else:
        return {"message": "Not Found"}, 404


@app.route("/ayudantes/<int:id>/motivacion", methods=["POST"])
def set_motivacion(id):
    body_data = request.get_json()
    
    with open("data/ayudantes.json") as info:
        data = json.load(info)
    
    ayudante = next(filter(lambda ayudante: ayudante["id"] == id, data))
    
    if ayudante:
        ayudante["motivacion"] = body_data["motivacion"]
        
        with open("data/ayudantes.json", "w") as info:
            json.dump(data, info, indent=4)
        
        return {"message" : "OK", "Ayudante" : ayudante}, 200
    else:
        return {"message": "Not Found"}, 404


@app.route("/ayudantes/<int:id>/veredicto", methods=["POST"])
def set_veredicto(id):
    estado = request.args.get('estado')

    with open("data/ayudantes.json") as info:
        data = json.load(info)

    ayudante = next(filter(lambda ayudante: ayudante["id"] == id, data))
    
    print(ayudante)

    if ayudante:
        ayudante["estado"] = estado

        with open("data/ayudantes.json", "w") as info:
            json.dump(data, info, indent=4)

        return {"message" : "OK", "Ayudante" : ayudante}, 200

    else:
        return {"message": "Not Found"}, 404

if __name__ == '__main__':
    app.run(debug=True, port=4444)
