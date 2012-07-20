import os, sys, json

WEBUI_ROOT = os.path.dirname(os.path.realpath(__file__))[:-5]
sys.path.append(WEBUI_ROOT)
from subliminal import *

class MajesticEditor(object):
    def __init__(self):
        self._state = State()

    def _handleInsert(self, filename, offset, text):
        buffer = Buffer([Segment(0, text)])
        operation = Insert(offset, buffer)
        request = DoRequest(0, self._state.vector, operation)
        self._postCommand("insert", [0, str(request.vector), offset, text, filename])
        executedRequest = self._state.execute(request)
  
    def _handleDelete(self, filename, offset, text):
        buffer = self._state.buffer.slice(offset, offset + len(text))
        operation = Delete(offset, buffer)
        request = DoRequest(0, self._state.vector, operation)
        self._postCommand("delete", [0, str(request.vector), offset, len(text), filename])
        executedRequest = self._state.execute(request)
        
    def _handleUndo(self, diffText):
        request = UndoRequest(self._localUser, self._state.vector)
        if self._state.canExecute(request):
            executedRequest = self._state.execute(request)

    def _postCommand(self, command, args):
        print json.dumps([command, args])
            
    def sync(self, filename, diffs):
        """ Takes a diff array and applies it to the buffer."""
        offset = 0
        for diff in diffs:
            diffType = diff[0]
            diffText = diff[1]
            if diffType == 1:
                self._handleInsert(filename, offset, diffText)
                offset += len(diffText)
            elif diffType == -1:
                self._handleDelete(filename, offset, diffText)
            elif diffType == -2: # this is never used
                self._handleUndo(diffText) # deprecated
            else:
                offset += len(diffText)
