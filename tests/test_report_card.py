from report_card.ReportCard import ReportCard


class TestReportCard:
    test_case: ReportCard = ReportCard()

    def test_get_report_card(self):
        res = self.test_case.get_report_card()

        assert (res['status'] == 200)
        assert (res['result'][0].get('variableLabel', '') == 'All students')

    def test_compile_math_prof(self):
        df = self.test_case.compile_math_prof()
        assert df.shape == (51, 18)
