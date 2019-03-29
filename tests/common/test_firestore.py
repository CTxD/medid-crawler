import pytest
import mockfirestore
import source.common.firestore as firestore
from source.crawling import pill


firestore.db = mockfirestore.MockFirestore()

def mock_data():
    firestore.db.reset()
    # pill_1 = AutoFixture(pill, field_values={"pillname": "Panodil", "substance": "100"})
    # pill_2 = AutoFixture(pill, field_values={"pillname": "Panodil", "substance": "500"})
    pics_1 = pill.PhotoIdentification('Filmovertrukne tabletter  500 mg  (novum)', '/resource/media/37171ea6-9e38-473a-b491-00cadae42273', 'Ingen kærv', 'Gul', '8,8 x 18,8', '/resource/media/C9697D2P?ptype=1')
    pics_2_1 = pill.PhotoIdentification('Filmovertrukne tabletter  500 mg', '/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09', 'Ingen kærv', 'Hvid', '9 x 18,8', '/resource/media/MSUC458E?ptype=1')
    photos_1 = [pics_1, pics_2_1]
    pill_1 = pill.PillData(photos_1, "Abboticin", "Erythromycin")

    pics_2 = pill.PhotoIdentification('Filmovertrukne tabletter  500 mg  (novum)', '/resource/media/37171ea6-9e38-473a-b491-00cadae42273', 'Ingen kærv', 'Gul', '8,8 x 18,8', '/resource/media/C9697D2P?ptype=1')
    pics_2_2 = pill.PhotoIdentification('Filmovertrukne tabletter  500 mg', '/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09', 'Ingen kærv', 'Hvid', '9 x 18,8', '/resource/media/MSUC458E?ptype=1')
    photos_2 = [pics_2, pics_2_2]
    pill_2 = pill.PillData(photos_2, "Viagra", "Villigril")

    firestore.db.collection("Pills").document(pill_1.pillname).set(pill_1)
    firestore.db.collection("Pills").document(pill_2.pillname).set(pill_2)


def test_convert_to_json():
    class TestingClass():
        def foo(self):
            pass

    result = firestore._convert_obj_to_dict(TestingClass)
    assert result == {}

def test_add_valid():
    mock_data()
    pics_3 = pill.PhotoIdentification('Filmovertrukne tabletter  500 mg  (novum)', '/resource/media/37171ea6-9e38-473a-b491-00cadae42273', 'Ingen kærv', 'Gul', '8,8 x 18,8', '/resource/media/C9697D2P?ptype=1')
    pics_3_3 = pill.PhotoIdentification('Filmovertrukne tabletter  500 mg', '/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09', 'Ingen kærv', 'Hvid', '9 x 18,8', '/resource/media/MSUC458E?ptype=1')
    photos_3 = [pics_3, pics_3_3]
    pill_3 = pill.PillData(photos_3, "Abboti", "Erythromycin")

    firestore.add_or_update("Pills", pill_3)

    assert len(firestore.get_all("Pills")) == 3


def test_update_valid():
    mock_data()
    pics_2 = pill.PhotoIdentification('Filmovertrukne tabletter  500 mg  (novum)', '/resource/media/37171ea6-9e38-473a-b491-00cadae42273', 'Ingen kærv', 'Gul', '8,8 x 18,8', '/resource/media/C9697D2P?ptype=1')
    pics_2_2 = pill.PhotoIdentification('Filmovertrukne tabletter  500 mg', '/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09', 'Ingen kærv', 'Hvid', '9 x 18,8', '/resource/media/MSUC458E?ptype=1')
    photos_2 = [pics_2, pics_2_2]
    pill_2 = pill.PillData(photos_2, "Viagra", "Villigrilli")

    firestore.add_or_update("Pills", pill_2)
    get_pill_result = firestore.db.collection("Pills").document(pill_2.pillname).get().to_dict()

    assert get_pill_result["pillname"] == "Viagra"
    assert get_pill_result["substance"] == "Villigrilli"


def test_get_pill():
    mock_data()
    pill_result = firestore.get("Pills", "Viagra").to_dict()
    assert pill_result.pillname == "Viagra" and pill_result.substance == "Villigril"


def test_get_all_pills():
    mock_data()
    pills = firestore.get_all("Pills")
    assert len(pills) == 2
