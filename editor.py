import os, sys, json

WEBUI_ROOT = os.path.dirname(os.path.realpath(__file__))[:-5]
sys.path.append(WEBUI_ROOT)
from infinote import *

example_log = [ ['i', (0,' ', 0, 'foobar foobar bar foo')], ]

class InfinoteEditor(object):
    
    def __init__(self):
        self._state = State()

    def _handleInsert(self, offset, text):
        buffer = Buffer([Segment(0, text)])
        operation = Insert(offset, buffer)
        request = DoRequest(0, self._state.vector, operation)
        self._postCommand("insert", [0, str(request.vector), offset, text])
        executedRequest = self._state.execute(request)
  
    def _handleDelete(self, offset, text):
        buffer = self._state.buffer.slice(offset, offset + len(text))
        operation = Delete(offset, buffer)
        request = DoRequest(0, self._state.vector, operation)
        self._postCommand("delete", [0, str(request.vector), offset, len(text)])
        executedRequest = self._state.execute(request)
        
    def _handleUndo(self, diffText):
        request = UndoRequest(self._localUser, self._state.vector)
        if self._state.canExecute(request):
            executedRequest = self._state.execute(request)

    def _postCommand(self, command, args):
        print json.dumps([command, args])
            
    def sync(self, diffs):
        """ Takes a diff array and applies it to the buffer."""
        offset = 0
        for diff in diffs:
            diffType = diff[0]
            diffText = diff[1]
            if diffType == 1:
                self._handleInsert(offset, diffText)
                offset += len(diffText)
            elif diffType == -1:
                self._handleDelete(offset, diffText)
            elif diffType == -2: # this is never used
                self._handleUndo(diffText) # deprecated
            else:
                offset += len(diffText)

def main():
    editor = InfinoteEditor()
    editor.sync(example_log)
    print editor._state.buffer
