import time
import pandas as pd
import json

from WrenchCL import ApiSuperClass
from WrenchCL import wrench_logger
from WrenchCL import rdsInstance

"""
    "contracts": {
        "A": "BPA Call",
        "B": "Purchase Order",
        "C": "Delivery Order",
        "D": "Definitive Contract"
    },
    "loans": {
        "07": "Direct Loan",
        "08": "Guaranteed/Insured Loan"
    },
    "idvs": {
        "IDV_A": "GWAC Government Wide Acquisition Contract",
        "IDV_B": "IDC Multi-Agency Contract, Other Indefinite Delivery Contract",
        "IDV_B_A": "IDC Indefinite Delivery Contract / Requirements",
        "IDV_B_B": "IDC Indefinite Delivery Contract / Indefinite Quantity",
        "IDV_B_C": "IDC Indefinite Delivery Contract / Definite Quantity",
        "IDV_C": "FSS Federal Supply Schedule",
        "IDV_D": "BOA Basic Ordering Agreement",
        "IDV_E": "BPA Blanket Purchase Agreement"
    },
    "grants": {
        "02": "Block Grant",
        "03": "Formula Grant",
        "04": "Project Grant",
        "05": "Cooperative Agreement"
    },
    "other_financial_assistance": {
        "09": "Insurance",
        "11": "Other Financial Assistance"
    },
    "direct_payments": {
        "06": "Direct Payment for Specified Use",
        "10": "Direct Payment with Unrestricted Use"
    }
}
"""

# https://api.usaspending.gov/api/v2/search/spending_by_award/

class GovGrantsAPI(ApiSuperClass):
    def __init__(self, keywords, date_range):
        super().__init__('https://api.usaspending.gov/api/v2/search/')
        self.keywords = keywords
        self.date_range = date_range

    def get_count(self):
        url_count = f'{self.base_url}spending_by_award_count/'
        payload = {
            'filters': {
                'keywords': self.keywords,
                'time_period': [{
                    'start_date': self.date_range['start_date'],
                    'end_date': self.date_range['end_date']
                }]
            }
        }
        response = self._fetch_from_api(url_count, '', payload)
        return int(response['results']['grants']) if response else None

    def fetch_data(self, batch_size=100, last_record_sort_value=None, last_record_unique_id=None, page=None):
        url_data = f'{self.base_url}spending_by_award/'
        payload = {
            'AwardTypeResult': ['grants'],
            'filters': {
                'keywords': self.keywords,
                'time_period': [{
                    'start_date': self.date_range['start_date'],
                    'end_date': self.date_range['end_date']
                }],
                # 'award_type_codes': ['A', 'B', 'C', 'D']
                'award_type_codes': ['02', '03', '04', '05']
            },
            'fields': [
                'Award ID',
                'Award Type',
                'Recipient Name',
                'Place of Performance City Code',
                'Place of Performance State Code',
                'Place of Performance Zip5',
                'Place of Performance Country Code',
                'Description',
                'Award Amount',
                'Awarding Agency',
                'Funding Agency',
                'Start Date',
                'End Date',
                'Contract Award Type',
                'CFDA Number',
            ],
            'limit': batch_size,
            'last_record_sort_value': last_record_sort_value,
            'last_record_unique_id': last_record_unique_id,
            'page': page
        }

        try:
            response = self._fetch_from_api(url_data, '', payload)
        except Exception as e:
            response = None

        if response is not None:
            return response['results'], response['page_metadata'].get('last_record_sort_value'), response[
                'page_metadata'].get('last_record_unique_id'), response['page_metadata'].get('hasNext')
        else:
            return None, None, None, None

# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------

class GovGrantsProcessor(GovGrantsAPI):

    def __init__(self, deal_id, keywords, date_range, connect_options):
        super().__init__(keywords, date_range)
        self.deal_id = deal_id
        self.connect_options = connect_options
        self.batch_size = 100
        self.count = None

    def _connect_to_rds(self):
        rdsInstance.load_configuration(self.connect_options)
        rdsInstance._connect()
        sql = f"SET SESSION myapp.deal_id_var TO {self.deal_id}"
        rdsInstance.execute_query(sql)

    def process_grants(self, download_count):

        wrench_logger.debug('Start of process grants')

        # count is not needed
        # if self.count is None:
        #     self.count = self.get_count()
        # if self.count is not None:
        #     wrench_logger.debug(
        #         f'Found {self.count} grants for keywords {self.keywords} between {self.date_range["start_date"]} and {self.date_range["end_date"]}.')
        # else:
        #     wrench_logger.error('Failed to get the grant count.')

        try:
            self._connect_to_rds()

            done = False
            retrieve_count = 0
            page = 1
            retries = 0
            last_record_sort_value = None
            last_record_unique_id = None
            while (not done) and (retrieve_count < download_count) and (retries < 3):
                try:
                    wrench_logger.debug('Grant: Before fetch_data')
                    batch_size = min(download_count - retrieve_count, self.batch_size)
                    data, last_record_sort_value, last_record_unique_id, hasnext = self.fetch_data(batch_size,
                                                                                                   last_record_sort_value=last_record_sort_value,
                                                                                                   last_record_unique_id=last_record_unique_id,
                                                                                                   page=page)
                    wrench_logger.debug(f'Grant: After fetch_data: {hasnext}')
                except Exception as e:
                    wrench_logger.error(f'Grants fetch error: {e}')
                    data = None

                if data is not None:
                    retries = 0
                    page += 1
                    wrench_logger.debug(f'Fetched {len(data)} grants in batch {page}.')
                    wrench_logger.debug(
                        f'Fetched {len(data)} grants in batch {page}. Last record sort value: {last_record_sort_value}, Last record unique ID: {last_record_unique_id}')

                    if len(data) == 0:
                        done = True
                        continue

                    record = {
                        'award_id': [],
                        'grant_type': [],
                        'recipient_name': [],
                        'city_code': [],
                        'state_code': [],
                        'zip5': [],
                        'country_code': [],
                        'description': [],
                        'award_amount': [],
                        'awarding_agency': [],
                        'funding_agency': [],
                        'start_date': [],
                        'end_date': [],
                        'cfda_number': [],
                    }
                    df_grants = pd.DataFrame(record)

                    # wrench_logger.debug(json.dumps(data, indent=2))

                    for grant in data:
                        # create a DF based on the JSON
                        df_grants = self.retrieve_grants(grant, df_grants)
                        retrieve_count += 1
                        if retrieve_count > download_count:
                            break

                    # save DF to RDS
                    self.insert_grants_df(df_grants)

                    wrench_logger.debug(f'Grants retrieved: {retrieve_count:,}')

                    done = not hasnext

                else:
                    wrench_logger.error('Failed to fetch the grant data.')
                    retries += 1

        except Exception as e:
            wrench_logger.error(f'Grant ERROR fetch_data: {e}')
        finally:
            rdsInstance.close()

    def retrieve_grants(self, grant, df_grants):
        # wrench_logger.debug(json.dumps(grant, indent=2))
        record = {
            'award_id': [grant['Award ID']],
            'grant_type': [self.escape_special_characters(self.handle_none_string(grant['Award Type']))],
            'recipient_name': [self.escape_special_characters(grant['Recipient Name'])],
            'city_code': [self.escape_special_characters(grant['Place of Performance City Code'])],
            'state_code': [self.escape_special_characters(grant['Place of Performance State Code'])],
            'zip5': [self.escape_special_characters(grant['Place of Performance Zip5'])],
            'country_code': [self.escape_special_characters(grant['Place of Performance Country Code'])],
            'description': [self.escape_special_characters(grant['Description'])],
            'award_amount': [self.handle_none_int(grant['Award Amount'])],
            'awarding_agency': [self.escape_special_characters(grant['Awarding Agency'])],
            'funding_agency': [self.escape_special_characters(grant['Funding Agency'])],
            'start_date': [self.handle_none_string(grant['Start Date'])],
            'end_date': [self.handle_none_string(grant['End Date'])],
            'cfda_number': [self.handle_none_string(grant['CFDA Number'])],
        }

        # return df_grants.append(record, ignore_index=True)
        return pd.concat([df_grants, pd.DataFrame(record)], ignore_index=True)

    def insert_grants_df(self, df_grants):
        sql_statements = ''

        for _, row in df_grants.iterrows():
            sql = f'''
                -- Get the deal_id_var from the session variable' 
                -- DECLARE deal_id_var := current_setting('myapp.deal_id_var')::INTEGER;   
                
                -- Insert into svs_grants only if grant_id doesn't already exist
                INSERT into {self.set_table_name('svs_grants')} (
                        award_id,
                        grant_type, 
                        recipient_name,
                        city_code, 
                        state_code, 
                        zip5, 
                        country_code, 
                        description, 
                        award_amount, 
                        awarding_agency, 
                        funding_agency, 
                        start_date, 
                        end_date,
                        cfda_number 
                    )
                SELECT 
                    '{row["award_id"]}', 
                    '{row["grant_type"]}', 
                    '{row["recipient_name"]}', 
                    '{row["city_code"]}', 
                    '{row["state_code"]}', 
                    '{row["zip5"]}', 
                    '{row["country_code"]}', 
                    '{row["description"]}', 
                    '{row["award_amount"]}', 
                    '{row["awarding_agency"]}', 
                    '{row["funding_agency"]}', 
                    to_date('{row["start_date"]}', 'yyyy-mm-dd'), 
                    to_date('{row["end_date"]}', 'yyyy-mm-dd'),
                    '{row["cfda_number"]}' 
                WHERE NOT EXISTS
                    (
                        SELECT award_id FROM {self.set_table_name('svs_grants')}
                        WHERE award_id = '{row['award_id']}'
                    );
            
                -- Insert or update svs_relational_deals_patents
                INSERT INTO {self.set_table_name('svs_relational_deals_grants(deal_id, award_id)')}
                VALUES ({self.deal_id}, '{row['award_id']}')
                ON CONFLICT (deal_id, award_id) DO NOTHING;
            '''

            # wrench_logger.debug(sql)
            sql_statements += sql

        if len(sql_statements) != 0:
            # wrench_logger.debug(sql_statements)
            sql_results = rdsInstance.execute_query(sql_statements)
            if sql_results == 'ERROR':
                wrench_logger.error(
                    f'An Exception Occurred: Failed to execute SQL query for inserting grant data. {sql_results}')
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
        if value in [None]:
            return 0
        return int(value)


    @staticmethod
    def set_table_name(name):
        return f'"SummitVentureStudios".{name}'
        # return name  # this is for prod


