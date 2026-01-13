import sys
from datetime import datetime
from src.controllers import Manager
from src.ui import UI
from src.models import Course, Participant
from uuid import uuid4

def manage_courses(manager: Manager):
    while True:
        UI.print_menu(["Aggiungi un corso", "Rimuovi un corso", "Aggiorna lo stato di un corso", "Visualizza la lista dei corsi"], "Gestione Corsi")
        choice = UI.get_input("Scegli opzione")

        if choice == "0":
            break
        elif choice == "1":
            id = str(uuid4())
            name = UI.get_input("Inserisci Nome Corso")
            try:
                manager.add_course(name, id)
                UI.print_message("Corso aggiunto con successo!", "success")
            except ValueError as e:
                UI.print_message(str(e), "error")
        elif choice == "2":
            course = UI.select_item(manager.courses, "Corso")
            if course:
                manager.remove_course(course)
                UI.print_message("Corso rimosso con successo!", "success")
        elif choice == "3":
            course = UI.select_item(manager.courses, "Corso")
            if course:
                new_status = UI.get_input("Inserisci nuovo stato (da iniziare, in corso, completato)")
                manager.update_course_status(course, new_status)
                UI.print_message("Stato aggiornato con successo!", "success")
        elif choice == "4":
            UI.print_courses_table(manager.courses)
            UI.get_input("Premi invio per continuare")
        else:
            UI.print_message("Opzione non valida", "error")
            UI.get_input("Premi invio per continuare")

def manage_participants(manager: Manager):
    while True:
        UI.print_menu(["Aggiungi un partecipante alla lista generale", "Iscrivi un partecipante a un corso", "Rimuovi un partecipante da corso", "Visualizza la lista di tutti i partecipanti"], "Gestione Partecipanti")
        choice = UI.get_input("Scegli opzione")

        if choice == "0":
            break
        elif choice == "1":
            id = str(uuid4())
            first_name = UI.get_input("Inserisci Nome")
            last_name = UI.get_input("Inserisci Cognome")
            try:
                manager.add_participant(id, first_name, last_name)
                UI.print_message("Partecipante aggiunto con successo!", "success")
            except ValueError as e:
                UI.print_message(str(e), "error")
        elif choice == "2":
            course = UI.select_item(manager.courses, "Corso")
            participant = UI.select_item(manager.participants, "Partecipante")
            if course and participant:
                try:
                    manager.enroll_participant(course, participant)
                    UI.print_message("Partecipante iscritto con successo!", "success")
                except ValueError as e:
                    UI.print_message(str(e), "error")
        elif choice == "3":
            course = UI.select_item(manager.courses, "Corso")
            if course:
                participants = manager.get_course_participants(course)
                participant = UI.select_item(participants, "Partecipante")
                if participant:
                    manager.unenroll_participant(course, participant)
                    UI.print_message("Partecipante rimosso con successo!", "success")
        elif choice == "4":
            UI.print_participants_table(manager.participants, manager.courses)
            UI.get_input("Premi invio per continuare")
        else:
             UI.print_message("Opzione non valida", "error")

def manage_attendance(manager: Manager):
    while True:
        UI.print_menu(["Registra/Modifica presenze", "Visualizza le presenze di un corso"], "Gestione Presenze")
        choice = UI.get_input("Scegli opzione")

        if choice == "0":
            break
        elif choice == "1":
            course = UI.select_item(manager.courses, "Corso")
            if not course:
                continue
            
            # Allow user to enter a date or pick today
            date_input = UI.get_input("Inserisci data (YYYY-MM-DD) o lascia vuoto per la data di oggi")
            if not date_input:
                date_input = datetime.now().strftime("%Y-%m-%d")
            
            participants = manager.get_course_participants(course)
            if not participants:
                UI.print_message("Nessun partecipante iscritto a questo corso.", "error")
                UI.get_input("Premi invio per continuare")
                continue

            current_attendance = manager.get_attendance_for_course_date(course, date_input)
            new_attendance = current_attendance.copy()

            print(f"\nRegistrazione presenze per {course.name} il {date_input}")
            print("Inserisci 'p' per Presente, 'a' per Assente. Premi invio per mantenere il valore attuale.")
            
            for p in participants:
                current_val = current_attendance.get(p.id, "N/A")
                val = UI.get_input(f"{p.last_name} {p.first_name} [{current_val}]").lower()
                if val in ['p', 'presente']:
                    new_attendance[p.id] = "presente"
                elif val in ['a', 'assente']:
                    new_attendance[p.id] = "assente"
                                
            manager.register_attendance(course, date_input, new_attendance)
            UI.print_message("Presenze salvate!", "success")
            UI.get_input("Premi invio per continuare")

        elif choice == "2":
            course = UI.select_item(manager.courses, "Corso")
            if course:
                participants = manager.get_course_participants(course)
                full_attendance = manager.get_full_course_attendance(course)
                UI.print_attendance_table(course, participants, full_attendance)
                UI.get_input("Premi invio per continuare")
        else:
            UI.print_message("Opzione non valida", "error")

def main():
    manager = Manager()
    while True:
        UI.print_menu([
            "Gestione Corsi",
            "Gestione Partecipanti",
            "Gestione Presenze"
        ], "Gestione Presenze")
        
        choice = UI.get_input("Scegli opzione")
        
        if choice == "0":
            UI.print_message("Arrivederci!")
            break
        elif choice == "1":
            manage_courses(manager)
        elif choice == "2":
            manage_participants(manager)
        elif choice == "3":
            manage_attendance(manager)
        else:
            UI.print_message("Opzione non valida", "error")
            UI.get_input("Premi invio per continuare")

if __name__ == "__main__":
    main()
