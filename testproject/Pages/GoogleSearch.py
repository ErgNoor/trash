class GoogleSearch:
    def __init__(self):
        self.locators = {
            "search_input": "id='lst-ib'",
            "submit_search_button": "name='btnK'",
        }

    def get_locators(self):
        return self.locators
