"""
Interface with PitchBook API
Documentation: https://documenter.getpostman.com/view/5190535/TzCV1iRc
"""

import json
import time
import os
import requests
import csv
import pandas as pd

from WrenchCL import ApiSuperClass
from WrenchCL import wrench_logger
from WrenchCL import rdsInstance
from datetime import date, datetime


class PitchBookAPI(ApiSuperClass):
    def __init__(self, api_key, keywords, date_range):
        super().__init__('')
        self.keywords = keywords
        self.date_range = date_range
        self.api_key = api_key


    def _fetch_from_api(self, url, headers, payload):
        response = requests.get(url, headers=headers, params=payload)
        if response.status_code == 200:
            return response.json()
        else:
            wrench_logger.error(f'Failed to get data, status code: {response.status_code}')
            wrench_logger.error(f'Payload: {payload}')
            wrench_logger.error(f'Url: {response.url}')
            wrench_logger.error(f'Response text: {response.text}')
            return None


    def fetch_data(self,
                   keywords,
                   search_options,
                   last_record_sort_value=None,
                   last_record_unique_id=None,
                   page=None):

        """
            Call this method to get search results from PitchBook

            - if an option is '', then it isn't included in the API call
            - you can indicate any retry count and sleep time.  A retry_count of 0
              means no reties.

        Returns:
            a dictionary: each key in dictionary is a keyword, the value is a list
            of deal ids.
            if the total is not found in PitchBook, total will be an empty list
        """
        api_endpoint = 'https://api-v2.pitchbook.com/deals/search'

        results = {}

        headers = {
            # "Content-Type": "application/json",
            "Authorization": f"{self.api_key}",
        }

        for keyword in keywords:

            # default value if the following code doesn't retrieve the total
            results[keyword] = None

            # fill in parameters - only the ones that are not empty strings
            params = {'keywords': keyword}
            params.update(search_options)

            deals_list = []
            done = False
            retries = 0
            retry_count = 3
            retry_sleep = 3
            while not done:
                try:
                    # print(api_endpoint)
                    # print(json.dumps(headers, indent=2))
                    # print(json.dumps(params, indent=2))
                    data = self._fetch_from_api(api_endpoint, headers, params)

                    if data is not None:
                        # print(json.dumps(data, indent=2))
                        stats = data.get('items')
                        if stats:
                            for dealer in stats:
                                if 'dealId' in dealer:
                                    deals_list.append(dealer['dealId'])
                        done = True
                    else:
                        raise Exception

                except Exception:
                    # TODO = log error
                    wrench_logger.error('Error in retrieving pitchbook data')
                    wrench_logger.error(api_endpoint, params)
                    retries += 1
                    done = retries > retry_count
                    if not done:
                        time.sleep(retry_sleep)
                    continue

            # print(deals_list)
            results[keyword] = deals_list
        
        return results

    def search_deal_details(self,
                            ids,
                            retry_count = 3,
                            retry_sleep = 1
                            ):
        api_endpoint = 'https://api-v2.pitchbook.com'

        wrench_logger.debug(f'search_deal_details(): id list = {ids}')

        headers = {
            # "Content-Type": "application/json",
            "Authorization": f"{self.api_key}",
        }

        record = {
            "dealid": [],
            "dealnumber": [],
            "companyid": [],
            "companyname": [],
            "dealdate": [],
            "dealamount": [],
            "dealcurrency": [],
            "dealestimated": [],
            "dealsizestatus": [],
            "dealcode": [],
            "dealdescription": [],
            "dealsynopsis": [],
            "dealtype1": [],
            "dealtype2": [],
            "dealtype3": [],
            "json_dump": [],
        }

        results = pd.DataFrame(record)

        for pb_id in ids:
            url = f'{api_endpoint}/deals/{pb_id}/detailed'
            wrench_logger.debug(url)

            done = False
            retries = 0
            while not done:
                try:
                    data = self._fetch_from_api(url, headers, '')
                    if data is not None:
                        # wrench_logger.debug(json.dumps(data, indent=2))

                        json_dump = json.dumps(data).replace("'", "''").replace("-", "\\-")

                        dealamount = self.handle_none_int(data['dealSize']['amount']) if data['dealSize'] else 0
                        dealcurrency = self.handle_none_string(data['dealSize']['currency']) if data['dealSize'] else ''
                        dealest = self.handle_none_bool(data['dealSize']['estimated']) if data['dealSize'] else False

                        dealtype1 = self.escape_special_characters(data['dealType1']['code']) if data['dealType1'] else ''
                        dealtype2 = self.escape_special_characters(data['dealType2']['code']) if data['dealType2'] else ''
                        dealtype3 = self.escape_special_characters(data['dealType3']['code']) if data['dealType3'] else ''

                        record = {
                            "dealid": [data['dealId']],
                            "dealnumber": [self.handle_none_int(data['dealNumber'])],
                            "companyid": [data['companyId']],
                            "companyname": [self.escape_special_characters(data['companyName'])],
                            "dealdate": [self.handle_none_string(data['dealDate'])],

                            "dealamount": [dealamount],
                            "dealcurrency": [dealcurrency],
                            "dealestimated": [dealest],

                            "dealsizestatus": [self.escape_special_characters(data['dealSizeStatus'])],
                            "dealcode": [self.escape_special_characters(data['dealStatus']['code'])],
                            "dealdescription": [self.escape_special_characters(data['dealStatus']['description'])],
                            "dealsynopsis": [self.escape_special_characters(data['dealSynopsis'])],

                            'dealtype1': [dealtype1],
                            'dealtype2': [dealtype2],
                            'dealtype3': [dealtype3],

                            "json_dump": [self.escape_special_characters(json_dump)],
                        }
                        # wrench_logger.debug(record)

                        results = pd.concat([results, pd.DataFrame(record)], ignore_index=True)

                        done = True
                    else:
                        raise Exception

                except Exception as e:
                    wrench_logger.error(f'ERROR retrieving details of a pitchbook, {e}')

                    retries += 1
                    done = retries > retry_count
                    if not done:
                        time.sleep(retry_sleep)

                    continue

        convert_dict = {'dealnumber': int, 'dealestimated': bool}
        return results.astype(convert_dict)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class PitchBookProcessor(PitchBookAPI):

    def __init__(self,
                 deal_id,
                 keywords,
                 date_range,
                 api_key,
                 connect_options):

        super().__init__(api_key, keywords, date_range)
        self.deal_id = deal_id
        self.connect_options = connect_options
        self.date_range = date_range
        self.date_range_option = f'{date_range["start_date"]}^{date_range["end_date"]}'
        self.batch_size = 100
        self.count = None
        self.PGHOST = connect_options['PGHOST']
        self.PGPORT = connect_options['PGPORT']
        self.PGDATABASE = connect_options['PGDATABASE']
        self.PGUSER = connect_options['PGUSER']
        self.PGPASSWORD = connect_options['PGPASSWORD']

    def _connect_to_rds(self):
        rdsInstance.load_configuration(self.connect_options)
        rdsInstance._connect()
        sql = f"SET SESSION myapp.deal_id_var TO {self.deal_id}"
        rdsInstance.execute_query(sql)

    def get_count(self):
        return len(self._get_pitchbook_ids()[1])

    def process_pitchbook(self, download_count):

        wrench_logger.debug('Start of process pitchbook')
        try:
            self._connect_to_rds()

            query_results, ids_list = self._get_pitchbook_ids()

            # wrench_logger.debug('%' * 100)
            # wrench_logger.debug('%' * 100)
            # wrench_logger.debug('%' * 100)
            # wrench_logger.debug('%' * 100)

            # wrench_logger.debug(ids_list)
            # wrench_logger.debug(json.dumps(query_results, indent=2))
            # wrench_logger.debug(ids_list[:download_count])

            to_download = min(download_count, len(ids_list))

            data = self.search_deal_details(ids_list[:to_download])   # only the first N records
            # wrench_logger.debug(data.to_string())

            self._insert_pitchbooks(query_results, data)

            wrench_logger.info(f'{to_download} PitchBook records downloaded')
        finally:
            rdsInstance.close()

    def _get_pitchbook_ids(self):
        search_options1 = {
            'dealSize': '.5^100',
            'dealDate': self.date_range_option,
            'verticals': 'SAAS, AT, ET, HT',
            'industry': '10, 20, 50, 60',
            'industryAndVertical': 'FALSE',
            'country': 'USA, CAN',
            'dealStatus': 'COMP',
            'onlyMostRecentTransaction': 'TRUE',
            'dealType': 'BYSTG',
        }

        # 2) Failed Companies
        search_options2 = {
            'verticals': 'SAAS, AT, ET, HT',
            'industry': '10, 20, 50, 60',
            'industryAndVertical': 'FALSE',
            'country': 'USA, CAN, GBR, DEU, FRA, ESP, ITA, SWE, FIN, BRA, ARG, MEX',
            'dealStatus': 'COMP',
            'dealType': 'CH11, CH7, DISTRESS, OutOfBus',
        }

        # 3) M&A past five years
        search_options3 = {
            'dealDate': self.date_range_option,
            'verticals': 'SAAS, AT, ET, HT',
            'industry': '10, 20, 50, 60',
            'industryAndVertical': 'FALSE',
            'country': 'USA, CAN',
            'dealStatus': 'COMP',
            'dealType': 'ALL_BO, LBO_, ACQ_PEAcq, ACQ_STRAcq, ACQ_VCAcq, IPO, ACQ, CTRL_TRAN, LBO_MBO, MER, RMER',
        }

        # 4) Acquisitions in past 5 years
        search_options4 = {
            'dealDate': self.date_range_option,
            'verticals': 'SAAS, AT, ET, HT',
            'industry': '10, 20, 50, 60',
            'industryAndVertical': 'FALSE',
            'country': 'USA, CAN',
            'dealStatus': 'COMP',
            'dealType': 'ACQF, AACQ',
        }

        # 5) Early Stage Deals / new product launches
        search_options5 = {
            'dealDate': self.date_range_option,
            'verticals': 'SAAS, AT, ET, HT',
            'industry': '10, 20, 50, 60',
            'industryAndVertical': 'FALSE',
            'country': 'USA, CAN',
            'dealStatus': 'COMP',
            'dealType': 'SeedA',
        }

        options = [
            ('q1', search_options1),
            ('q2', search_options2),
            ('q3', search_options3),
            ('q4', search_options4),
            ('q5', search_options5)]

        ids_set = set()
        query_results = {}

        try:

            # there are 5 different types of calls
            for qkey, opt in options:
                data = self.fetch_data(self.keywords, opt)
                query_results[qkey] = data
                # wrench_logger.debug(json.dumps(data, indent=2))
                for key, value in data.items():
                    ids_set.update(value)

        finally:
            pass

        wrench_logger.debug(f'IDS SET: {len(ids_set)}')
        wrench_logger.debug(f'{ids_set}')
        return query_results, list(ids_set)


    def _insert_pitchbooks(self, query_results, df_data):
        sql_statements = ''

        def _get_query_flags(id):

            def _found_in_query(data):
                for key, value in data.items():
                    if id in value:
                        return True
                return False

            q1 = _found_in_query(query_results['q1'])
            q2 = _found_in_query(query_results['q2'])
            q3 = _found_in_query(query_results['q3'])
            q4 = _found_in_query(query_results['q4'])
            q5 = _found_in_query(query_results['q5'])

            return q1, q2, q3, q4, q5


        for _, row in df_data.iterrows():

            query1, query2, query3, query4, query5 = _get_query_flags(row['dealid'])

            # get query flags
            sql = f'''
                INSERT INTO {self.set_table_name('svs_pitchbook')} (
                    pitchbook_id,
                    dealnumber, 
                    companyid, 
                    companyname, 
                    dealdate, 
                    dealamount, 
                    dealcurrency, 
                    dealestimated, 
                    dealsizestatus, 
                    dealcode, 
                    dealdescription, 
                    dealsynopsis,
                    dealtype1, 
                    dealtype2, 
                    dealtype3,
                    query1, 
                    query2, 
                    query3, 
                    query4, 
                    query5, 
                    json_dump)
                SELECT
                    '{row['dealid']}', 
                    '{row['dealnumber']}', 
                    '{row['companyid']}', 
                    '{row['companyname']}', 
                    to_date('{row["dealdate"]}', 'yyyy-mm-dd'),
                    '{row['dealamount']}', 
                    '{row['dealcurrency']}', 
                    '{row['dealestimated']}', 
                    '{row['dealsizestatus']}', 
                    '{row['dealcode']}', 
                    '{row['dealdescription']}', 
                    '{row['dealsynopsis']}', 
                    '{row['dealtype1']}', 
                    '{row['dealtype2']}', 
                    '{row['dealtype3']}', 
                    {query1},
                    {query2},
                    {query3},
                    {query4},
                    {query5},
                    '{row['json_dump']}'
                WHERE NOT EXISTS
                    (
                        SELECT pitchbook_id FROM {self.set_table_name('svs_pitchbook')}
                        WHERE pitchbook_id = '{row['dealid']}'
                            AND dealnumber = '{row['dealnumber']}' 
                    );

                -- Insert or update {self.set_table_name('svs_relational_deals_pitch_book')}
                INSERT INTO {self.set_table_name('svs_relational_deals_pitch_book(deal_id, pitchbook_id)')}
                VALUES ({self.deal_id}, '{row['dealid']}')
                ON CONFLICT (deal_id, pitchbook_id) DO NOTHING;                    
           '''
            # wrench_logger.debug(sql)
            sql_statements += sql

        if len(sql_statements) != 0:
            # wrench_logger.debug(sql_statements)
            sql_results = rdsInstance.execute_query(sql_statements)

            if sql_results == 'ERROR':
                wrench_logger.error(
                    f'An Exception Occurred: Failed to execute SQL query for inserting pitchbook data. {sql_results}')
                wrench_logger.debug(f'Failed Query: {sql}')
                rdsInstance.close()
                self._connect_to_rds()



    @staticmethod
    def escape_special_characters(value):
        if value is None:
            return "NULL"
        elif isinstance(value, str):
            # Escape single quotes, hyphens, and periods
            return value.replace("'", "''").replace("-", "\\-")
        else:
            return value

    @staticmethod
    def handle_none_string(value):
        if value in [None]:
            return ''
        return value


    @staticmethod
    def handle_none_int(value):
        if value in [None, 'None', '']:
            return 0
        return int(value)


    @staticmethod
    def handle_none_bool(value):
        if value in [None, '', 'None', 'False', 'false']:
            return False
        return True


    @staticmethod
    def set_table_name(name):
        return f'"SummitVentureStudios".{name}'
        # return name  # this is for prod


