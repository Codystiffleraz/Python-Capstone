import os
import json
from random import choice, randint

import crud 
import model
import server

os.system('dropdb jungle')
os.system('createdb jungle')

model.connect_to_db(server.app)
model.db.create_all()

with open('Data/clothes.json') as f:
    clothes_data = json.loads(f.read())

clothes_in_db = []
for cloth in clothes_data:
    name, description, price, size, image_path = (
        cloth["name"],
        cloth["description"],
        cloth["price"],
        cloth["size"],
        cloth["image_path"]
    )
    
    db_cloth = crud.create_clothes(name, description, price, size, image_path)
    clothes_in_db.append(db_cloth)
    
    
model.db.session.add_all(clothes_in_db)
model.db.session.commit()