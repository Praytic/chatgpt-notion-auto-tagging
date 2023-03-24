from main import describe_url

class MockWebhook:
    def __init__(self, json_data):
        self.json_data = json_data

    def get_json(self):
        return self.json_data

def main():
    data = {'gem_url': 'https://www.shouselaw.com/ca/labor/wrongful-termination/warn-act/', 'new_page_id': '610fd5b3-78a6-4119-96a4-dcc1ed3d1f3a'}
    describe_url(MockWebhook(data))

if __name__ == '__main__':
    main()
