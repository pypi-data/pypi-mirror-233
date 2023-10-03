#!/usr/bin/env python3
import datetime
import logging
import sys

import connexion
from connexion import NoContent

# our memory-only pet storage
PETS = {}


def get_pets(limit, animal_type=None):
    return {"pets": [pet for pet in PETS.values() if not animal_type or pet['animal_type'] == animal_type][:limit]}


def get_pet(pet_id):
    pet = PETS.get(pet_id)
    return pet or ('Not found', 404)


def put_pet(pet_id, pet):
    exists = pet_id in PETS
    pet['id'] = pet_id
    if exists:
        logging.info('Updating pet %s..', pet_id)
        PETS[pet_id].update(pet)
    else:
        logging.info('Creating pet %s..', pet_id)
        pet['created'] = datetime.datetime.utcnow()
        PETS[pet_id] = pet
    return NoContent, (200 if exists else 201)


def delete_pet(pet_id):
    if pet_id in PETS:
        logging.info('Deleting pet %s..', pet_id)
        del PETS[pet_id]
        return NoContent, 204
    else:
        return NoContent, 404



def build_api_server_one(port, base_url= None):
    logging.basicConfig(level=logging.INFO)
    app = connexion.App(
        __name__,
        port=port,
        options={
            'swagger_ui': True,

            # Show Swagger UI at root
            'swagger_url': '/',
        }
    )
    app.add_api(
        'swagger.yaml',
        base_path=base_url,
    )
    return app


if __name__ == '__main__':
    # run our standalone gevent server
    if len(sys.argv) == 3:
        port = sys.argv[1]
        port = int(port) if port else 8080

        base_url = f"{sys.argv[2]}"
        base_url = base_url if base_url else None
        app = build_api_server_one(port, base_url)
        app.run()
    else:
        raise ValueError('Usage: python ./app.py {port} {base_url}')
