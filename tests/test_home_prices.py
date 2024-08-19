from report_card.HomePrices import HomePrices

class TestHomePrices:
    test_case: HomePrices = HomePrices()

    def test_scrape(self):
        res = self.test_case.scrape_data()
        assert res.shape == (52, 3)

    def test_compile_home_prices(self):
        res = self.test_case.compile_homeprices()
        assert res['amount'].dtype == 'int64'