import logging

from run import BaseTestCase
from call_server.political_data.countries.us_state import USStateData
from call_server.campaign.constants import (TARGET_CHAMBER_BOTH, TARGET_CHAMBER_UPPER, TARGET_CHAMBER_LOWER,
        ORDER_IN_ORDER, ORDER_UPPER_FIRST, ORDER_LOWER_FIRST)
from call_server.political_data.constants import US_STATES

class TestData(BaseTestCase):
    def setUp(self):
        # quiet sunlight cache logging
        logging.getLogger('cache').setLevel(logging.WARNING)
        testCache = {}
        self.us_state_data = USStateData(testCache, 'localmem')
        self.us_state_data.load_data()

    def test_cache(self):
        self.assertIsNotNone(self.us_state_data)

    def test_locate_targets(self):
        oakland_ca = "37.804417,-122.267747"
        uids = self.us_state_data.locate_targets(oakland_ca, TARGET_CHAMBER_BOTH, ORDER_IN_ORDER)
        # returns a list of bioguide ids
        self.assertEqual(len(uids), 2)

        senator = self.us_state_data.get_uid(uids[0])
        self.assertEqual(senator['chamber'], 'upper')
        self.assertEqual(senator['state'].upper(), 'CA')
        self.assertEqual(senator['active'], True)

        house_rep = self.us_state_data.get_uid(uids[1])
        self.assertEqual(house_rep['chamber'], 'lower')
        self.assertEqual(house_rep['state'].upper(), 'CA')
        self.assertEqual(house_rep['active'], True)

    def test_locate_targets_house_only(self):
        oakland_ca = "37.804417,-122.267747"
        uids = self.us_state_data.locate_targets(oakland_ca, TARGET_CHAMBER_LOWER)
        # returns a list of bioguide ids
        self.assertEqual(len(uids), 1)

        house_rep = self.us_state_data.get_uid(uids[0])
        self.assertEqual(house_rep['chamber'], 'lower')
        self.assertEqual(house_rep['state'].upper(), 'CA')
        self.assertEqual(house_rep['active'], True)

    def test_locate_targets_senate_only(self):
        oakland_ca = "37.804417,-122.267747"
        uids = self.us_state_data.locate_targets(oakland_ca, TARGET_CHAMBER_UPPER)
        # returns a list of bioguide ids
        self.assertEqual(len(uids), 1)

        senator = self.us_state_data.get_uid(uids[0])
        self.assertEqual(senator['chamber'], 'upper')
        self.assertEqual(senator['state'].upper(), 'CA')
        self.assertEqual(senator['active'], True)

    def test_locate_targets_ordered_house_first(self):
        oakland_ca = "37.804417,-122.267747"
        uids = self.us_state_data.locate_targets(oakland_ca, TARGET_CHAMBER_BOTH, ORDER_LOWER_FIRST)
        self.assertEqual(len(uids), 2)

        first = self.us_state_data.get_uid(uids[0])
        self.assertEqual(first['chamber'], 'lower')

        second = self.us_state_data.get_uid(uids[1])
        self.assertEqual(second['chamber'], 'upper')

    def test_locate_targets_ordered_senate_first(self):
        oakland_ca = "37.804417,-122.267747"
        uids = self.us_state_data.locate_targets(oakland_ca, TARGET_CHAMBER_BOTH, ORDER_UPPER_FIRST)
        self.assertEqual(len(uids), 2)

        first = self.us_state_data.get_uid(uids[0])
        self.assertEqual(first['chamber'], 'upper')

        second = self.us_state_data.get_uid(uids[1])
        self.assertEqual(second['chamber'], 'lower')

    def test_incorrect_state(self):
        boston_ma = "42.355662, -71.065483"
        uids = self.us_state_data.locate_targets(boston_ma, TARGET_CHAMBER_BOTH, ORDER_UPPER_FIRST, state="CA")
        self.assertEqual(len(uids), 0)

    def test_50_governors(self):
        NO_GOV = ['AS', 'GU', 'MP', 'PR', 'VI', '']
        for (abbr, state) in US_STATES:
            gov = self.us_state_data.get_governor(state)
            if not gov:
                self.assertIn(abbr, NO_GOV)
                continue
            self.assertEqual(len(gov.keys()), 3)
            self.assertEqual(gov['title'], 'Governor')

    def test_ca_governor(self):
        gov = self.us_state_data.get_governor('California')
        self.assertEqual(gov['name'], 'Edmund G. (Jerry) Brown Jr.')
        self.assertEqual(gov['phone'], '18008076755')
