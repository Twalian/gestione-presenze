import os
from typing import List, Dict, Tuple
from src.models import Course, Participant

class UI:

    @staticmethod
    def print_menu(options: List[str], title: str = "Menu"):
        print(f"\n--- {title} ---")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("0. Esci/Torna indietro")

    @staticmethod
    def get_input(prompt: str) -> str:
        return input(f"{prompt}: ").strip()

    @staticmethod
    def print_message(message: str, type: str = "info"):
        if type == "error":
            print(f"[ERROR] {message}")
        elif type == "success":
            print(f"[SUCCESS] {message}")
        else:
            print(f"[INFO] {message}")

    @staticmethod
    def print_courses_table(courses: List[Course]):
        print(f"\n{'ID':<40} | {'Nome':<20} | {'Status':<15} | {'Partecipanti'}")
        print("-" * 100)
        for c in courses:
            print(f"{c.id:<40} | {c.name:<20} | {c.status:<15} | {len(c.participant_ids)}")

    @staticmethod
    def print_participants_table(participants: List[Participant]):
        print(f"\n{'ID':<40} | {'Cognome':<20} | {'Nome':<20}")
        print("-" * 80)
        for p in participants:
            print(f"{p.id:<40} | {p.last_name:<20} | {p.first_name:<20}")

    @staticmethod
    def print_attendance_table(course: Course, participants: List[Participant], attendance_data: Dict[str, Dict[str, str]]):
        # attendance_data: date -> participant_id -> status
        dates = sorted(list(attendance_data.keys()))
        
        # Header
        header = f"{'Partecipante':<20}"
        for date in dates:
            header += f" | {date:<10}"
        print("\n" + header)
        print("-" * len(header))

        for p in participants:
            row = f"{p.last_name + ' ' + p.first_name:<20}"
            for date in dates:
                status = attendance_data.get(date, {}).get(p.id, "N/A")
                # Format specific status to be short if needed, e.g., P, A
                display_status = status[0].upper() if status else "-"
                row += f" | {display_status:^10}"
            print(row)
        print("\nLegenda: P=Presente, A=Assente")

    @staticmethod
    def select_item(items, item_name):
        if not items:
            print(f"Nessun {item_name} disponibile.")
            return None
        
        print(f"\nSeleziona {item_name}:")
        for i, item in enumerate(items, 1):
            if hasattr(item, 'name'):
                label = item.name
            elif hasattr(item, 'last_name'):
                label = f"{item.last_name} {item.first_name}"
            else:
                label = str(item)
            print(f"{i}. {label}")
        
        choice = UI.get_input(f"Inserisci scelta (1-{len(items)})")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                return items[idx]
        return None
