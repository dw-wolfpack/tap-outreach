import time
import requests
import singer

API_VERSION = 'v2'
LOGGER = singer.get_logger()
RATE_LIMIT_REMAINING = 'X-RateLimit-Remaining'
RATE_LIMIT_RESET = 'X-RateLimit-Reset'

class Server429Error(Exception):
    pass

class OutReachClient():
    def __init__(self, refresh_token, client_id, client_secret):
        self.__referesh_token = refresh_token
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.base_url = 'https://api.outreach.io/api/{}'.format(API_VERSION)

    def generate_token(self):
        if self.__referesh_token is None:
            raise Exception(
                'Error: Refresh token Missing.'
            )
        else:
            refresh = requests.post('https://api.outreach.io/oauth/token',
                                    data={'client_id': self.__client_id,
                                          'client_secret': self.__client_secret,
                                          'grant_type': 'refresh_token',
                                          'refresh_token': self.__referesh_token})
            access_token = refresh.json()['access_token']
            # print('Access token: ', access_token)
            return access_token

    def request_loop_prospect(self, endpoint, config):
        date_start = config['start_date']
        date_end = config['end_date']
        date_tuple = (date_start, date_end)
        all_data = dict()
        all_data["data"] = []

        access_token = self.generate_token()
        req = requests.get(self.base_url+'/'+endpoint.format(*date_tuple), \
                         headers={'Authorization': 'Bearer {0}'.format(access_token)})
        results = req.json()
        endpoint_list = []
        endpoint_list.append(endpoint.format(*date_tuple))


        for i in endpoint_list:

            url = str(self.base_url+'/'+i)
            req = requests.get(url, headers={'Authorization': 'Bearer {0}'.format(access_token)})
            # print(r.status_code, 'top top level')
            if req.status_code == 200:
                results = req.json()
                LOGGER.info('status code: %s', req.status_code)
            elif results.get('id') == 'expiredAccessToken':

                access_token = self.generate_token()
                req = requests.get(url, \
                                   headers={'Authorization': 'Bearer {0}'.format(access_token)})
                results = req.json()
                LOGGER.info('NEW NEW NEW status code: %s', req.status_code)

            elif req.status_code == 504:
                access_token = self.generate_token()
                req = requests.get(url, \
                                   headers={'Authorization': 'Bearer {0}'.format(access_token)})
                time.sleep(5)
            else:
                # print(r.status_code, 'status code in first i loop')
                break

            limit_remaining = int(req.headers[RATE_LIMIT_REMAINING])
            # print(results['meta'])
            LOGGER.info('limit remaining:  %s', str(limit_remaining))
            next_url = url
            next_page = next_url


            while next_page:
                response = requests.get(next_page, \
                        headers={'Authorization': 'Bearer {0}'.format(access_token)})

                # print(response.status_code, 'level 1 while loop')

                if response.status_code == 200:
                    # print('hi - level 1 if', response.status_code)
                    all_data['data'].extend(response.json().get('data'))
                    # print(response.json().get('data'))
                    limit_remaining = int(response.headers[RATE_LIMIT_REMAINING])
                    LOGGER.info('limit remaining:  %s', str(limit_remaining))
                    # for key,val in response.json().items():
                    #     print(key)
                    if response.json().get('links') is not None:
                        # print('response if level 1')
                        if response.json().get('links').get('next') is not None:
                            # print('next page is there')
                            next_page = response.json()['links']['next']
                            time.sleep(2)
                        else:
                            # print('no page, in the break')
                            access_token = self.generate_token()
                            break
                    else:
                        # print('status code 200 failed')
                        break
                elif response.status_code == 504:
                    # print(response.status_code, 'elif level 1')
                    # print(next_page, 'elf')
                    time.sleep(5)
                    next_page = next_page
                else:
                    # print(response.status_code, 'pre token')
                    access_token = self.generate_token()
                    # print(response.status_code, 'post token')
                    next_page = next_page

        return all_data, limit_remaining

    def get(self, url, path):
        pass

    def post(self, url, path):
        pass

    def fetch(self, url, path):
        pass
