# pylint:disable=protected-access
import time 

import mockfirestore

from source.crawling import pill


def mock_data(firebasemanager):
    firebasemanager.db = mockfirestore.MockFirestore()
    firebasemanager.db.reset()

    pics_1 = pill.PhotoIdentification(
        'Filmovertrukne tabletter  500 mg  (novum)',
        '5',
        ['/resource/media/37171ea6-9e38-473a-b491-00cadae42273'], 
        'Ingen kærv', 
        ['Gul'], 
        '8,8 x 18,8', 
        ['/resource/media/C9697D2P?ptype=1']
    )
    pics_2_1 = pill.PhotoIdentification(
        'Filmovertrukne tabletter  500 mg',
        '5', 
        ['/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09'], 
        'Ingen kærv', 
        ['Hvid'], 
        '9 x 18,8', 
        ['/resource/media/MSUC458E?ptype=1']
    )
    photos_1 = [pics_1, pics_2_1]
    pill_1 = pill.PillData("Abboticin", "Erythromycin", photos_1)

    pics_2 = pill.PhotoIdentification(
        'Filmovertrukne tabletter  500 mg  (novum)',
        '5', 
        ['/resource/media/37171ea6-9e38-473a-b491-00cadae42273'], 
        'Ingen kærv', 
        ['Gul'],
        '8,8 x 18,8',
        ['/resource/media/C9697D2P?ptype=1']
    )
    pics_2_2 = pill.PhotoIdentification(
        'Filmovertrukne tabletter  500 mg',
        '5',
        ['/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09'],
        'Ingen kærv',
        ['Hvid'],
        '9 x 18,8',
        ['/resource/media/MSUC458E?ptype=1']
    )
    photos_2 = [pics_2, pics_2_2]
    pill_2 = pill.PillData("Viagra", "Villigril", photos_2)

    firebasemanager.db.collection("Pills").document(pill_1.pillname).set(pill_1)
    firebasemanager.db.collection("Pills").document(pill_2.pillname).set(pill_2)
    
    return firebasemanager


def test_convert_to_json(firebasemanager):
    class TestingClass():
        def foo(self): # noqa
            pass

    result = firebasemanager._convert_obj_to_dict(TestingClass)
    assert result == {}


def test_add_valid(firebasemanager):
    firebasemanager = mock_data(firebasemanager)
    pics_3 = pill.PhotoIdentification(
        'Filmovertrukne tabletter  500 mg  (novum)',
        '5',
        ['/resource/media/37171ea6-9e38-473a-b491-00cadae42273'],
        'Ingen kærv',
        ['Gul'],
        '8,8 x 18,8',
        ['/resource/media/C9697D2P?ptype=1']
    )
    pics_3_3 = pill.PhotoIdentification(
        'Filmovertrukne tabletter  500 mg',
        '5',
        ['/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09'],
        'Ingen kærv',
        ['Hvid'],
        '9 x 18,8',
        ['/resource/media/MSUC458E?ptype=1']
    )
    photos_3 = [pics_3, pics_3_3]
    pill_3 = pill.PillData("Abboti", "Erythromycin", photos_3)

    firebasemanager.add_or_update("Pills", pill_3)

    assert len(firebasemanager.get_all("Pills")) == 3


def test_update_valid(firebasemanager):
    firebasemanager = mock_data(firebasemanager)
    pics_2 = pill.PhotoIdentification(
        'Filmovertrukne tabletter  500 mg  (novum)',
        '5',
        '/resource/media/37171ea6-9e38-473a-b491-00cadae42273',
        'Ingen kærv',
        'Gul',
        '8,8 x 18,8',
        '/resource/media/C9697D2P?ptype=1'
    )
    pics_2_2 = pill.PhotoIdentification(
        'Filmovertrukne tabletter  500 mg',
        '5',
        '/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09',
        'Ingen kærv',
        'Hvid',
        '9 x 18,8',
        '/resource/media/MSUC458E?ptype=1'
    )
    photos_2 = [pics_2, pics_2_2]
    pill_2 = pill.PillData("Viagra", "Villigrilli", photos_2)

    firebasemanager.add_or_update("Pills", pill_2)
    get_pill_result = firebasemanager.db.collection("Pills").document(pill_2.pillname).get().to_dict()

    assert get_pill_result["pillname"] == "Viagra"
    assert get_pill_result["substance"] == "Villigrilli"


def test_get_pill(firebasemanager):
    firebasemanager = mock_data(firebasemanager)
    pill_result = firebasemanager.get("Pills", "Viagra").to_dict()
    assert pill_result.pillname == "Viagra" and pill_result.substance == "Villigril"


def test_get_all_pills(firebasemanager):
    firebasemanager = mock_data(firebasemanager)
    pills = firebasemanager.get_all("Pills")
    assert len(pills) == 2


def test_update_crawling_meta(firebasemanager):
    crawling_data = {
        'links_by_letter': {'a': 22, 'b': 42},
        'drugs_by_letter': {'a': 21, 'b': 38}
    }
    intime = str(int(time.time()))
    firebasemanager.update_crawling_meta(crawling_data)

    stored_data = firebasemanager.db.collection('crawls').document(intime).get().to_dict()

    assert stored_data['links_by_letter'] == {'a': 22, 'b': 42}
    assert stored_data['drugs_by_letter'] == {'a': 21, 'b': 38}