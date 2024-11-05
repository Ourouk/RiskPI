import matplotlib.pyplot as plt
import cv2
import skimage.exposure as exposure

# Affiche des images avec leurs titres
# images : liste de tulpes image-titre
#   exemple -> [(img1, "image source"), (img2, "image traitée")]
# grid_shape : format d'affichage en (row, col)
#   exemple -> (3,2) pour afficher 6 images en 2 par 2
# RGB : est-ce que l'image est RGB ou HSV 
def displayImages(images, grid_shape):
    x,y = grid_shape
    # Create subplots
    fig, axs = plt.subplots(x, y, figsize=(15,10))
    axs = axs.flatten()

    for i, (image, title, RGB) in enumerate(images):
        if not RGB:
            image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
        axs[i].imshow(image, cmap='gray')
        axs[i].axis('off')
        if title is None:
            title = ".."
        axs[i].set_title(title)

    return axs

# Cette fonction récupère l'histogramme de la liste des images passées
# images : liste de tulpes image-titre (comme fonction ci-dessus)
# removeValueZero : retire les valeurs 0 de l'histogramme 
#           -> (car si on applique un masque, il y aura beaucoup de pixels noirs qui parasitent l'information)
def displayRGBHistogram(images, removeValueZero=True):
    fig, axes = plt.subplots(nrows=3, ncols=len(images), figsize=(8, 8)) 
    for i, (img, name) in enumerate(images):
        for c, c_color in enumerate(('red', 'green', 'blue')): 
            channel_data = img[..., c]
            if removeValueZero:
                channel_data = channel_data[channel_data > 0]
            
            img_hist, bins = exposure.histogram(channel_data,  
                                                    source_range='dtype')
            axes[c,i].plot(bins, img_hist / img_hist.max()) 
            img_cdf, bins = exposure.cumulative_distribution(img[..., c]) 
            axes[c,i].plot(bins, img_cdf) 
            axes[c,0].set_ylabel(c_color) 
            axes[0, i].set_title(name) 
    
    plt.tight_layout() 
    plt.show()