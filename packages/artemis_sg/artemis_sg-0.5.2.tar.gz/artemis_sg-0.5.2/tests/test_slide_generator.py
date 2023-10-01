import pytest
from googleapiclient.discovery import build

import artemis_sg.slide_generator as slide_generator
from artemis_sg.app_creds import app_creds
from artemis_sg.config import CFG
from artemis_sg.gcloud import GCloud
from artemis_sg.items import Items
from artemis_sg.vendor import Vendor


def test_blacklisted_keys():
    """
    Given a SlideGenerator object
    When the create_slide_text() method is called on it
    Then the object's blacklisted keys do not appear in text
    """

    class MockItem(object):
        def __init__(self):
            self.data = {"AUTHOR": "Dr. Seuss"}
            self.isbn_key = "ISBN"
            for blacklisted in sg_obj.BLACKLIST_KEYS:
                self.data[blacklisted] = "I should not be here!"

    sg_obj = slide_generator.SlideGenerator("foo", "bar", "baz")
    text = sg_obj.create_slide_text(MockItem(), 99)

    assert "Seuss" in text
    for blacklisted in sg_obj.BLACKLIST_KEYS:
        assert blacklisted not in text


@pytest.mark.database()
@pytest.mark.integration()
def test_slide_generator():
    """
    GIVEN a Vendor object  # for vendor specific slide logic
    AND a Google Sheet ID
    AND a Google Sheet tab
    AND a Slides API object
    AND a GCloud API object
    AND a Items dataset unified from sheet and scraped data
    AND a SlideGenerator object given Vendor, GCloud, and Slides objects
    WHEN we call the generate() method given Items, and title
    THEN a Google slide deck is created with given title and data
    """
    # vendor object
    vendr = Vendor("sample")
    vendr.set_vendor_data()

    # sheet id
    sheet_id = CFG["asg"]["test"]["sheet"]["id"]
    sheet_tab = CFG["asg"]["test"]["sheet"]["tab"]

    creds = app_creds()
    SLIDES = build("slides", "v1", credentials=creds)

    # GCloud object
    bucket_name = CFG["google"]["cloud"]["bucket"]
    cloud_key_file = CFG["google"]["cloud"]["key_file"]
    gcloud = GCloud(cloud_key_file=cloud_key_file, bucket_name=bucket_name)

    # Items dataset
    SHEETS = build("sheets", "v4", credentials=creds)
    sheet_data = (
        SHEETS.spreadsheets()
        .values()
        .get(range=sheet_tab, spreadsheetId=sheet_id)
        .execute()
        .get("values")
    )
    sheet_keys = sheet_data.pop(0)
    items_obj = Items(sheet_keys, sheet_data, vendr.isbn_key)
    items_obj.load_scraped_data("scraped_items.json")

    sg = slide_generator.SlideGenerator(SLIDES, gcloud, vendr)

    bucket_prefix = CFG["google"]["cloud"]["bucket_prefix"]
    slide_deck = sg.generate(items_obj, bucket_prefix, "Cool title")

    assert slide_deck
