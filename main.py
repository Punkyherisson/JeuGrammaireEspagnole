#Jeux grammaire Espagnole
#Nous allons créer un fichier CSV appelé verbes.csv. Ce fichier contiendra les colonnes suivantes :
#Infinitif : Le verbe à l'infinitif.
#Présent : Les formes conjuguées au présent pour chaque personne.
#Imparfait : Les formes conjuguées à l'imparfait.
#Futur : Les formes conjuguées au futur.
#Passé Composé : Les formes conjuguées au passé composé.
#Impératif : Les formes conjuguées à l'impératif.
#Subjonctif : Les formes conjuguées au subjonctif présent.
#Conditionnel : Les formes conjuguées au conditionnel.
#Passé Simple : Les formes conjuguées au passé simple.
import tkinter as tk
import random
import csv
import os

def load_verbs_from_csv(filepath):
    verbs = {}
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            infinitif = row['Infinitif']
            verbs[infinitif] = {
                'présent': row['Présent'].split(),
                'imparfait': row['Imparfait'].split(),
                'futur': row['Futur'].split(),
                'passé_composé': row['Passé Composé'].split(),
                'impératif': row['Impératif'].split(),
                'subjonctif': row['Subjonctif'].split(),
                'conditionnel': row['Conditionnel'].split(),
                'passé_simple': row['Passé Simple'].split()
            }
    return verbs

# Charger les verbes depuis le fichier CSV
verbs = load_verbs_from_csv('verbes.csv')
#Maintenant que nous avons notre fichier CSV, 
# nous allons écrire du code Python pour lire ce fichier 
# et l'utiliser dans notre jeu.
# Initialiser la fenêtre Tkinter
# Initialiser la fenêtre Tkinter
root = tk.Tk()
root.title("Jeu de Grammaire Espagnole")

# Initialiser la variable de score
current_score = 0

# Fonction pour afficher le menu principal
def show_menu():
    global current_score
    save_score(current_score)  # Sauvegarder le score actuel
    current_score = 0  # Réinitialiser le score pour chaque nouvelle partie
    
    # Effacer les widgets actuels
    for widget in root.winfo_children():
        widget.destroy()

    # Créer les boutons du menu
    tk.Label(root, text="Menu Principal", font=("Helvetica", 16)).pack(pady=20)
    
    tk.Button(root, text="1) Déterminer le temps des verbes", command=start_game, width=30, height=2).pack(pady=10)
    tk.Button(root, text="2) Consulter la liste des Verbes", command=show_verbs_list, width=30, height=2).pack(pady=10)
    tk.Button(root, text="3) Afficher les 5 meilleurs scores", command=show_high_scores, width=30, height=2).pack(pady=10)
    tk.Button(root, text="4) Quitter", command=quit_program, width=30, height=2).pack(pady=10)

# Fonction pour quitter le programme
def quit_program():
    save_score(current_score)  # Sauvegarder le score avant de quitter
    root.destroy()  # Ferme la fenêtre et détruit l'instance Tk

# Fonction pour démarrer le jeu
def start_game():
    global current_score

    # Effacer les widgets actuels
    for widget in root.winfo_children():
        widget.destroy()

    # Afficher le score actuel en haut à droite
    score_label = tk.Label(root, text=f"Score: {current_score}", font=("Helvetica", 12))
    score_label.pack(anchor="ne", padx=20, pady=10)

    # Variable pour afficher la question
    question_label = tk.Label(root, text="")
    question_label.pack(pady=20)

    # Variables pour les boutons de réponse
    buttons = []
    for i in range(8):  # Créer 8 boutons pour les 8 temps
        button = tk.Button(root, text="", width=20, height=2)
        button.pack(pady=5)
        buttons.append(button)
    
    # Bouton pour revenir au menu principal
    tk.Button(root, text="Menu Précédent", command=show_menu, width=20, height=2).pack(pady=10)

    def ask_question():
        # Si le score est négatif, arrêter le jeu
        if current_score < 0:
            save_score(current_score)
            question_label.config(text=f"Votre score est négatif. Le jeu est terminé. Score final : {current_score}")
            return
        
        # Choisir un verbe et un temps au hasard
        verb = random.choice(list(verbs.keys()))
        tense = random.choice(list(verbs[verb].keys()))

        # Choisir la bonne réponse
        correct_answer = random.choice(verbs[verb][tense])

        # Créer la question et l'afficher
        question_label.config(text=f"Quel est le temps de ce verbe : {correct_answer} ?")

        # Générer des réponses aléatoires (avec la bonne réponse)
        possible_answers = list(verbs[verb].keys())
        random.shuffle(possible_answers)

        # Afficher les réponses sous forme de boutons
        for i, tense in enumerate(possible_answers):
            buttons[i].config(text=tense, command=lambda t=tense: check_answer(t, verb, correct_answer))

    def check_answer(selected_tense, verb, correct_answer):
        global current_score

        # Vérifier si la réponse est correcte
        if correct_answer in verbs[verb][selected_tense]:
            current_score += 2  # Ajouter 2 points pour une bonne réponse
            result = "Correct !"
        else:
            current_score -= 5  # Retirer 5 points pour une mauvaise réponse
            result = "Incorrect..."

        # Mettre à jour l'affichage du score
        score_label.config(text=f"Score: {current_score}")

        question_label.config(text=result)
        
        # Attendre un moment avant de poser la prochaine question
        root.after(2000, ask_question)

    # Démarrer la première question
    ask_question()

# Fonction pour enregistrer le score dans un fichier
def save_score(score):
    with open("scores.txt", "a") as file:
        file.write(f"{score}\n")

# Fonction pour afficher les 5 meilleurs scores
def show_high_scores():
    # Effacer les widgets actuels
    for widget in root.winfo_children():
        widget.destroy()

    # Lire les scores du fichier
    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
        scores.sort(reverse=True)  # Trier les scores dans l'ordre décroissant
        top_scores = scores[:5]  # Garder les 5 meilleurs scores
    else:
        top_scores = []

    # Afficher les scores
    tk.Label(root, text="Les 5 meilleurs scores", font=("Helvetica", 16)).pack(pady=20)
    for i, score in enumerate(top_scores, start=1):
        tk.Label(root, text=f"{i}. {score} points").pack()

    # Bouton pour revenir au menu principal
    tk.Button(root, text="Menu Précédent", command=show_menu, width=20, height=2).pack(pady=20)

# Fonction pour afficher la liste des verbes
def show_verbs_list():
    # Effacer les widgets actuels
    for widget in root.winfo_children():
        widget.destroy()

    # Titre de la liste
    tk.Label(root, text="Liste des Verbes", font=("Helvetica", 16)).pack(pady=20)

    # Afficher les verbes
    for verb in verbs.keys():
        tk.Label(root, text=verb).pack()

    # Bouton pour revenir au menu principal
    tk.Button(root, text="Menu Précédent", command=show_menu, width=20, height=2).pack(pady=20)

# Afficher le menu principal au démarrage
show_menu()

# Démarrer la boucle principale Tkinter
root.mainloop()