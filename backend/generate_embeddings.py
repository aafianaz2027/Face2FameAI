from deepface import DeepFace
import os
import pickle

ACTORS_FOLDER = "actors"

embeddings = []

for actor_img in os.listdir(ACTORS_FOLDER):

    if not actor_img.lower().endswith(
        (".png", ".jpg", ".jpeg", ".jfif")
    ):
        continue

    actor_path = os.path.join(
        ACTORS_FOLDER,
        actor_img
    )

    try:

        embedding = DeepFace.represent(
            img_path=actor_path,
            model_name="Facenet",
            enforce_detection=False
        )

        embeddings.append({
            "actor": actor_img.split(".")[0],
            "embedding": embedding[0]["embedding"]
        })

        print(actor_img, "done")

    except Exception as e:
        print("Error:", e)

with open("embeddings.pkl", "wb") as f:
    pickle.dump(embeddings, f)

print("Embeddings saved!")