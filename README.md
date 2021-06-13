# NetflixLike

La base de données IMDb est composée d'une multitude de fichier CSV. 
Notre première étape a donc été de faire du tri parmi les 3 250 000 œuvres et regrouper toutes les informations que nous avons jugé importantes dans une même table.
Notre CSV final est composé de 15 000 films, qui sont disponibles au moins en français.
Afin d’effectuer des recommandations pertinentes en fonction d’un film choisi par l’utilisateur, 
nous avons regroupé toutes les colonnes contenant des mots clés importants en une (description, acteurs, réalisateur, etc..), 
que nous avons ensuite vectorisée pour ensuite calculer la « cosine similarity » entre chaque film. 
Notre système de recommandation retourne les films ayant les trois meilleurs scores de similarité par rapport à un film donné.
Nous avons ensuite développé une web-app avec Dash, qui permet de naviguer dans notre base de données et avoir accès à notre système de recommandation.
