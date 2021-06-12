# NetflixLike

La base de données IMDb est composées d'une multitude de fichier CSV. 
Notre première étape a donc été de faire du trie parmi les 3 250 000 œuvres et regrouper toutes les informations que nous avons jugé important dans un même table.
Notre CSV final est composé de 15 000 films, qui sont disponibles au moins en français.
Afin d’effectuer des recommandations pertinentes en fonction d’un film choisi par l’utilisateur, 
nous avons regroupés toutes les colonnes contenant des mots clés importants en une (description, acteurs, réalisateur, etc..), 
que nous avons ensuite vectorisé pour ensuite calculer la « cosine similarity » entre chaque films. 
Notre système de recommandation retourne les films ayant les trois meilleurs scores pour un film donnée
