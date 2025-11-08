import os

class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content

class NoteManager:
    def __init__(self, notes_dir='notes'):
        self.notes_dir = notes_dir
        os.makedirs(notes_dir, exist_ok=True)

    def save_note(self, note: Note):
        with open(os.path.join(self.notes_dir, f"{note.title}.txt"), 'w', encoding='utf-8') as f:
            f.write(note.content)

    def load_note(self, title):
        try:
            with open(os.path.join(self.notes_dir, f"{title}.txt"), 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None

    def delete_note(self, title):
        path = os.path.join(self.notes_dir, f"{title}.txt")
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def list_notes(self):
        return [f[:-4] for f in os.listdir(self.notes_dir) if f.endswith('.txt')]
