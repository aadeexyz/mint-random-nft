from brownie import AdvanceCollectible, network
from pathlib import Path
from metadata.template import metadata_template
from scripts.upload_to_ipfs import upload_to_pinata
import json

SHAPE_MAPPING = {
    0: "Circle",
    1: "Square",
    2: "Rectangle",
}


def get_shape(shape_number):
    return SHAPE_MAPPING[shape_number]


def create_metadata():
    advance_collectible = AdvanceCollectible[-1]
    number_of_collectibles = advance_collectible.tokenCounter()
    metadata_hashes = {}
   
    print(f"Number of collectibles: {number_of_collectibles}")
    
    for token_id in range(number_of_collectibles):
        shape = get_shape(advance_collectible.tokenIdToShape(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{shape}.json"
        collectible_metadata = metadata_template

        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists!")
        else:
            print(f"Creating {metadata_file_name}")
            image_path = f"./img/{shape.lower()}.png"
            image_uri = upload_to_pinata(image_path)
            collectible_metadata["name"] = shape
            collectible_metadata["description"] = f"A super cool {shape}!"
            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as f:
                json.dump(collectible_metadata, f, indent=4)
            metadata_uri = upload_to_pinata(metadata_file_name)
            metadata_hashes[token_id] = metadata_uri

    metadata_hashes_file_name = f"./metadata/{network.show_active()}/metadata-hashes.json"
  
    if Path(metadata_hashes_file_name).exists():
        print(f"{metadata_hashes_file_name} already exists!")
    else:
        print(f"Creating {metadata_hashes_file_name}")
        with open(metadata_hashes_file_name, "w") as f:
            json.dump(metadata_hashes, f, indent=4)


def main():
    create_metadata()
