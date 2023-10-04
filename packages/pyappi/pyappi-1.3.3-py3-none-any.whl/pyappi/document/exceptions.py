class DocumentNotLocked(Exception):
    "Raised when access to a document is attempted outside of its lifetime."
    pass

class PathDoesntExist(Exception):
    "Raised when access to a document is attempted outside of its lifetime."
    pass

class ReadOnlyDocument(Exception):
    "Raised when access to a document is attempted outside of its lifetime."
    pass

class UserWriteProtectedRegion(Exception):
    "Raised when access to a document is attempted outside of its lifetime."
    pass

class ListsAreNotAllowed(Exception):
    "Lists just make things harder"
    pass

class DictionaryReassignmentProhibited(Exception):
    "In some cases we don't allow this"
    pass

class NoPrepopulatedObjects(Exception):
    "Raised when assigned objects have values or subkeys, as this bypasses the preprocessor."
    pass

class ValueReassignmentToDictProhibited(Exception):
    "Once a value always a value"
    pass

class BulkAssignmentProhibited(Exception):
    "When the flag is enabled, bulk dict assignment can be prohibitied"
    pass