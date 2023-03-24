from main import describe_url

class MockWebhook:
    def __init__(self, json_data):
        self.json_data = json_data

    def get_json(self):
        return self.json_data

def main():
    data = {'gem_url': 'https://www.balancepro.org/resources/articles/five-steps-to-smart-tax-management/', 'new_page_id': 'c7a5bebc-a76c-4f26-a7ae-3c8ddddd41ea'}
    describe_url(MockWebhook(data))

if __name__ == '__main__':
    main()
