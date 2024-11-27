from PIL import Image
import os

# Taille cible
target_size = (256, 256)

# Extensions d'images acceptées
valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

# Parcours du dossier courant
for filename in os.listdir('.'):
    if filename.lower().endswith(valid_extensions):
        try:
            # Ouvrir l'image
            with Image.open(filename) as img:
                # Redimensionner l'image
                img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                
                # Sauvegarder en écrasant l'original
                img_resized.save(filename)
                print(f"Image {filename} redimensionnée et sauvegardée (écrasée).")
        except Exception as e:
            print(f"Erreur lors du traitement de {filename}: {e}")

print("Redimensionnement terminé.")
