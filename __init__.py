import sublime, sublime_plugin, socket, json
from diff_match_patch import diff_match_patch as dmp
from editor import MajesticEditor

class Majestic(sublime_plugin.EventListener):
    def __init__(self):
        self.previous_text = ""
        self.editor = MajesticEditor()
        self.dmp = dmp()
        
    def on_modified(self, view):
        text = view.substr(view.visible_region())
        diff = self.dmp.diff_main(self.previous_text, text)
        filename = view.file_name()
        self.dmp.diff_cleanupSemantic(diff)
        self.editor.sync(filename, diff)
        self.previous_text = text
