from source.crawling import iteration
from source.common import firestore

def test_getFBM_uninitialized(firebasemanager, monkeypatch): # noqa
    # Hard-set the _fbm to None
    iteration._fbm = None # noqa

    def getfirebasemanagerfixture():
        return firebasemanager
    
    # Monkeypatch firestore.FBManager() to return the firebasemanager obj
    original = firestore.FBManager
    firestore.FBManager = getfirebasemanagerfixture
    fbm = iteration.getFBM()
    assert isinstance(fbm, original)

    firestore.FBManager = original
    

def test_getFBM_initialized(firebasemanager): # noqa
    iteration._fbm = firebasemanager # noqa

    assert iteration.getFBM() == firebasemanager # noqa


# ## MAKE TESTS FOR ITERATION FILE WHEN IT BEGINS TO ACTUALLY WRAP FUNCTIONALITY!