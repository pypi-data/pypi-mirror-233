import json
import pandas as pd

from tenacity import retry, wait_random_exponential, stop_after_attempt
from WrenchCL import ApiSuperClass
from WrenchCL import wrench_logger
from WrenchCL import rdsInstance
from datetime import datetime

# https://patentsview.org/apis/api-endpoints/patentsbeta
# Alternative: https://patentsview.org/apis/api-endpoints/patents

pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)

"""
This is from the documentation
Usage Limits
Each application is allowed to make 45 requests/minute. If your application 
exceeds this limit, you will receive a “429 Too many Requests” response to 
your API query.

Query format
'q': {
    '_and': [
        {
            '_or' : [
                {"_text_any": {'patent_abstract': keywords_str1}},
                {"_text_any": {'patent_abstract': keywords_str2}},
                {"_text_any": {'patent_abstract': keywords_str3}},
            ]
        },
        {'_gte': {'patent_date': self.date_range['start_date']}},
        {'_lte': {'patent_date': self.date_range['end_date']}}
    ]
},
"""

class PatentAPI(ApiSuperClass):


    # the API call requires a list of all fields to return - this is all of them
    format_fields = [
        'appcit_app_number', 'appcit_category', 'appcit_date', 'appcit_kind', 'appcit_sequence',
        'app_country', 'app_date', 'app_number', 'app_type', 'assignee_city',
        'assignee_country', 'assignee_county', 'assignee_county_fips', 'assignee_first_name',
        'assignee_first_seen_date',
        'assignee_id', 'assignee_last_name', 'assignee_last_seen_date', 'assignee_lastknown_city',
        'assignee_lastknown_country',
        'assignee_lastknown_latitude', 'assignee_lastknown_location_id', 'assignee_lastknown_longitude',
        'assignee_lastknown_state',
        'assignee_latitude', 'assignee_location_id', 'assignee_longitude', 'assignee_organization', 'assignee_sequence',
        'assignee_state', 'assignee_state_fips', 'assignee_total_num_inventors', 'assignee_total_num_patents',
        'assignee_type',
        'cited_patent_category', 'cited_patent_date', 'cited_patent_kind', 'cited_patent_number',
        'cited_patent_sequence',
        'cited_patent_title', 'citedby_patent_category', 'citedby_patent_date', 'citedby_patent_kind',
        'citedby_patent_number',
        'citedby_patent_title', 'cpc_category', 'cpc_first_seen_date', 'cpc_group_id', 'cpc_group_title',
        'cpc_last_seen_date', 'cpc_section_id', 'cpc_sequence', 'cpc_subgroup_id', 'cpc_subgroup_title',
        'cpc_subsection_id', 'cpc_subsection_title', 'cpc_total_num_assignees', 'cpc_total_num_inventors',
        'cpc_total_num_patents', 'detail_desc_length', 'examiner_first_name', 'examiner_id', 'examiner_last_name',
        'examiner_role', 'examiner_group', 'forprior_country', 'forprior_date', 'forprior_docnumber',
        'forprior_kind', 'forprior_sequence', 'govint_contract_award_number', 'govint_org_id', 'govint_org_level_one',
        'govint_org_level_two', 'govint_org_level_three', 'govint_org_name', 'govint_raw_statement', 'inventor_city',
        'inventor_country', 'inventor_county', 'inventor_county_fips', 'inventor_first_name',
        'inventor_first_seen_date', 'inventor_id',
        'inventor_last_name', 'inventor_last_seen_date', 'inventor_lastknown_city', 'inventor_lastknown_country',
        'inventor_lastknown_latitude',
        'inventor_lastknown_location_id', 'inventor_lastknown_longitude', 'inventor_lastknown_state',
        'inventor_latitude', 'inventor_location_id',
        'inventor_longitude', 'inventor_sequence', 'inventor_state', 'inventor_state_fips',
        'inventor_total_num_patents', 'ipc_action_date', 'ipc_class', 'ipc_classification_data_source',
        'ipc_classification_value',
        'ipc_first_seen_date', 'ipc_last_seen_date', 'ipc_main_group', 'ipc_section', 'ipc_sequence',
        'ipc_subclass', 'ipc_subgroup', 'ipc_symbol_position', 'ipc_total_num_assignees', 'ipc_total_num_inventors',
        'ipc_version_indicator', 'lawyer_first_name', 'lawyer_first_seen_date', 'lawyer_id', 'lawyer_last_name',
        'lawyer_last_seen_date', 'lawyer_organization', 'lawyer_sequence', 'lawyer_total_num_assignees',
        'lawyer_total_num_inventors', 'lawyer_total_num_patents', 'nber_category_id', 'nber_category_title',
        'nber_first_seen_date', 'nber_last_seen_date', 'nber_subcategory_id', 'nber_subcategory_title',
        'nber_total_num_assignees', 'nber_total_num_inventors', 'nber_total_num_patents', 'patent_abstract',
        'patent_average_processing_time', 'patent_date', 'patent_firstnamed_assignee_city',
        'patent_firstnamed_assignee_country',
        'patent_firstnamed_assignee_id', 'patent_firstnamed_assignee_latitude',
        'patent_firstnamed_assignee_location_id', 'patent_firstnamed_assignee_longitude',
        'patent_firstnamed_assignee_state', 'patent_firstnamed_inventor_city', 'patent_firstnamed_inventor_country',
        'patent_firstnamed_inventor_id',
        'patent_firstnamed_inventor_latitude', 'patent_firstnamed_inventor_location_id',
        'patent_firstnamed_inventor_longitude', 'patent_firstnamed_inventor_state',
        'patent_kind', 'patent_num_cited_by_us_patents', 'patent_num_claims', 'patent_num_combined_citations',
        'patent_num_foreign_citations', 'patent_num_us_application_citations', 'patent_num_us_patent_citations',
        'patent_number',
        'patent_processing_time', 'patent_title', 'patent_type', 'patent_year',
        'pct_102_date', 'pct_371_date', 'pct_date', 'pct_docnumber', 'pct_doctype',
        'pct_kind', 'rawinventor_first_name', 'rawinventor_last_name', 'uspc_first_seen_date', 'uspc_last_seen_date',
        'uspc_mainclass_id', 'uspc_mainclass_title', 'uspc_sequence', 'uspc_subclass_id', 'uspc_subclass_title',
        'uspc_total_num_assignees', 'uspc_total_num_inventors', 'uspc_total_num_patents',
        'wipo_field_id', 'wipo_field_title', 'wipo_sector_title', 'wipo_sequence',
    ]

    # Beta AP_I
    # # the API call requires a list of all fields to return - this is all of them
    # format_fields = [
    #     "applicants", "application", "assignees", "attorneys", "botanic", "cpc_at_issue",
    #     "cpc_current", "examiners", "figures", "foreign_priority", "gov_interest_contract_award_numbers",
    #     "gov_interest_organizations", "gov_interest_statement", "granted_pregrant_crosswalk",
    #     "inventors", "ipcr", "patent_abstract", "patent_cpc_current_group_average_patent_processing_days",
    #     "patent_date", "patent_detail_desc_length", "patent_earliest_application_date",
    #     "patent_id", "patent_num_foreign_documents_cited", "patent_num_times_cited_by_us_patents",
    #     "patent_num_total_documents_cited", "patent_num_us_applications_cited", "patent_num_us_patents_cited",
    #     "patent_processing_days", "patent_term_extension", "patent_title", "patent_type",
    #     "patent_uspc_current_mainclass_average_patent_processing_days", "patent_year",
    #     "pct_data", "us_related_documents", "us_term_of_grant", "uspc_at_issue", "wipo",
    #     "wipo_kind",
    # ]

    def __init__(self, api_key, keywords, date_range):
        super().__init__('https://api.patentsview.org/patents/query')  # this is the legacy API
        # super().__init__('https://search.patentsview.org/api/v1/patent')  # This is the Beta API- it has issues - 2023-09-26

        self.keywords = keywords
        self.date_range = date_range
        self._api_key = api_key

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(10))
    def get_count(self):

        payload = {
            'q': {
                '_and': [
                    {
                        '_or': []
                    },
                    {'_gte': {'patent_date': self.date_range['start_date']}},
                    {'_lte': {'patent_date': self.date_range['end_date']}}
                ]
            },
            # 'f': ['patent_id'],   Beta API
            'f': ['patent_number'],
            'o': {
                'per_page': 1
            }
        }

        # add keywords to the query
        for word in self.keywords:
            payload['q']['_and'][0]['_or'].append({"_text_phrase": {"patent_abstract": word}})

        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': f'{self._api_key}'
        }

        # wrench_logger.debug(json.dumps(headers, indent=2))
        # wrench_logger.debug(json.dumps(payload, indent=2))

        response = self._fetch_from_api(self.base_url, headers, payload)
        # wrench_logger.debug(json.dumps(response, indent=2))
        return int(response.get('total_patent_count')) if response else 0
        # return response.get('total_hits') if response else 0   # Beta API

    def fetch_data(self, batch_size, last_record_unique_id=None):
        """
            last_record_unique_id: contains the page number to retrieve.  If None, then page 1
                                   is assumed.
        :return:
        """

        payload = {
            'q': {
                '_and': [
                    {
                        '_or': []
                    },
                    {'_gte': {'patent_date': self.date_range['start_date']}},
                    {'_lte': {'patent_date': self.date_range['end_date']}}
                ]
            },
            'f': self.format_fields,
            'o': {
                'page': last_record_unique_id,
                'per_page': batch_size
            }
        }

        # add keywords to the query
        for word in self.keywords:
            payload['q']['_and'][0]['_or'].append({"_text_phrase": {"patent_abstract": word}})

        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': f'{self._api_key}'
        }

        # if last_record_unique_id is not None:
        #     payload['o']['after'] = last_record_unique_id  # Assuming 'after' is used for pagination

        # wrench_logger.debug(json.dumps(payload, indent=2))

        try:
            response = self._fetch_from_api(self.base_url, headers, payload)
            # import requests
            # response = requests.post(self.base_url, headers, payload)
            # wrench_logger.debug(response)
            # wrench_logger.debug(response.raw)
            # wrench_logger.debug(response.headers)
        except Exception as e:
            response = None

        if response is not None:
            # wrench_logger.debug(json.dumps(response, indent=2))

            # Beta API - debugging
            # # get last patent id returned
            # pats = ''
            # for pat in response['patents']:
            #     pats += f'{pat["patent_id"]}, '
            # wrench_logger.debug(f"PAT: {pats}")
            # pat = response['patents'][-1]
            # last_record_unique_id = pat['patent_id']

            return response, None, last_record_unique_id
        else:
            return None, None, None


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------

class PatentProcessor(PatentAPI):
    # these data frame are set/created in the retrieve_? methods
    df_patent = None
    df_inventors = None
    df_assignees = None

    def __init__(self,
                 deal_id,
                 keywords,
                 date_range,
                 api_key,
                 connect_options):
        super().__init__(api_key, keywords, date_range)
        self.deal_id = deal_id
        self.connect_options = connect_options
        self.batch_size = 100
        self.count = None

    def _connect_to_rds(self):
        rdsInstance.load_configuration(self.connect_options)
        rdsInstance._connect()
        sql = f"SET SESSION myapp.deal_id_var TO {self.deal_id};"
        rdsInstance.execute_query(sql)

    def process_patents(self, download_count):

        wrench_logger.debug(f'Start of process patents.  Download count = {download_count}')

        if self.count is None:
            self.count = self.get_count()
        if self.count is not None:
            wrench_logger.debug(
                f'Found {self.count} patents for keywords {self.keywords} between {self.date_range["start_date"]} and {self.date_range["end_date"]}.')
        else:
            wrench_logger.error('Failed to get the patent count.')

        try:
            self._connect_to_rds()

            self.patent_retrieve_count = 0
            self.assignee_retrieve_count = 0
            self.inventor_retrieve_count = 0

            done = False
            retrieve_count = 0
            page = 1
            retries = 0

            download_count = min(download_count, self.count)
            wrench_logger.debug(f'{download_count = }')

            last_record_unique_id = None
            while (not done) and (retrieve_count < download_count) and (retries < 3):
                try:
                    batch_size = min(download_count - retrieve_count, self.batch_size)
                    data, last_record_sort_value, last_record_unique_id = self.fetch_data(batch_size, page)
                except Exception as e:
                    wrench_logger.error(f'process_patents(): error in fetch_data() call')
                    data = None

                if data is not None:
                    retries = 0
                    page += 1
                    wrench_logger.debug(f'Fetched {data["count"]} patents in batch {page}.')
                    wrench_logger.debug(
                        f'Fetched {data["count"]} patents in batch {page}. Last record sort value: {last_record_sort_value}, Last record unique ID: {last_record_unique_id}')

                    if data['count'] == 0:
                        done = True
                        continue

                    sql_all_statements = ''
                    for patent in data['patents']:
                        retrieve_count += 1
                        self.patent_retrieve_count += 1

                        if retrieve_count > download_count:
                            break

                        # create a DF based on the JSON
                        # wrench_logger.debug(json.dumps(patent, indent=2))
                        self.retrieve_patent(patent)
                        self.retrieve_inventors(patent)
                        self.retrieve_assignees(patent)
                        self.fill_in_assignee_details()   # NOT WRITTEN YET

                        # print('PATENTS ---------------------------------------------------')
                        # print(self.df_patent)
                        # print('ASSIGNEES ---------------------------------------------------')
                        # print(self.df_assignees)
                        # print('INVENTORS ---------------------------------------------------')
                        # print(self.df_inventors)

                        # save DF to RDS
                        # sql_all_statements += self.insert_dataframes(patent['patent_id'])  Beta API
                        sql_all_statements += self.insert_dataframes(patent['patent_number'])

                        wrench_logger.debug(f'Patents retrieved: {retrieve_count:,}')

                    # apply sql statements
                    # wrench_logger.debug(sql_all_statements)
                    if len(sql_all_statements) != 0:
                        # wrench_logger.debug(sql_statements)
                        sql_results = rdsInstance.execute_query(sql_all_statements)
                        wrench_logger.debug(f'SQL_RESULTS: {sql_results}')

                        if sql_results == 'ERROR':
                            wrench_logger.error(
                                f'An Exception Occurred: Failed to execute SQL query for inserting Patent data. {sql_results}')
                            wrench_logger.debug(f'Failed Query: {sql_all_statements}')
                            rdsInstance.close()
                            self._connect_to_rds()



                else:
                    wrench_logger.error('Failed to fetch the patent data.')
                    retries += 1


        finally:
            rdsInstance.close()
            wrench_logger.info(f'{self.patent_retrieve_count} patents saved to RDS')
            wrench_logger.info(f'{self.assignee_retrieve_count} assignees saved to RDS')
            wrench_logger.info(f'{self.inventor_retrieve_count} inventors saved to RDS')

    def retrieve_patent(self, patent):
        # Beta API
        # patent_id = patent['patent_id']
        # patent_title = patent['patent_title']
        # patent_description = patent['patent_abstract']
        # filing_date = patent['application'][0]['filing_date'] or ''
        #
        # if patent.get('pct_data') is not None:
        #     publication_date = patent['pct_data'][0]['published_filed_date']
        # else:
        #     publication_date = None
        #
        # cpc_codes = ','.join(
        #     set(cpc['cpc_subclass_id'] for cpc in patent.get('cpc_current', []) if cpc['cpc_subclass_id'])) or ''
        # retrieval_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        patent_id = patent['patent_number']
        patent_title = patent['patent_title']
        patent_description = patent['patent_abstract']
        filing_date = patent['applications'][0]['app_date'] or ''
        publication_date = patent['pct_data'][0]['pct_date'] or ''
        cpc_codes = ','.join(
            set(cpc['cpc_subgroup_id'] for cpc in patent.get('cpcs', []) if cpc['cpc_subgroup_id'])) or ''

        retrieval_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        json_dump = json.dumps(patent).replace("'", "''").replace("-", "\\-")

        record = {
            'deal_id': [self.deal_id],
            'patent_id': [patent_id],
            'patent_title': [self.escape_characters(patent_title)],
            'patent_description': [self.escape_characters(patent_description)],
            'filing_date': [self.handle_none_string(filing_date)],
            'publication_date': [self.handle_none_string(publication_date)],
            'cpc_codes': [self.escape_characters(cpc_codes)],
            'retrieval_date': [retrieval_date],
            'json_dump': [self.escape_characters(json_dump)]
        }

        self.df_patent = pd.DataFrame(record)
        # wrench_logger.debug(self.df_patent.columns)

    def retrieve_inventors(self, patent):
        records = {
            'patent_id': [],
            'id': [],
            'first': [],
            'last': [],
            # 'key_id': [],
        }

        for invent in patent['inventors']:
            # print('INVENT:', invent)
            if invent['inventor_key_id'] is not None:
                records['patent_id'].append(patent['patent_number'])
                records['id'].append(invent['inventor_id'])
                # records['key_id'].append(int(invent['inventor_key_id']))
                records['first'].append(self.escape_characters(invent["inventor_first_name"]))
                records['last'].append(self.escape_characters(invent["inventor_last_name"]))


        # Beta API
        # for invent in patent['inventors']:
        #     # wrench_logger.debug('INVENT:', invent)
        #     if invent.get('inventor') is not None:
        #         records['patent_id'].append(patent['patent_id'])  Beta API
        #
        #         # id = "https://search.patentsview.org/api/v1/inventor/fl:wi_ln:becker-9/",
        #         inventor_id = invent['inventor'].split('/inventor/')[1][:-1]
        #         records['id'].append(inventor_id)
        #
        #         records['first'].append(self.escape_characters(invent["inventor_name_first"]))
        #         records['last'].append(self.escape_characters(invent["inventor_name_last"]))
        #
        #         # records['key_id'].append(int(invent['inventor_key_id']))

        self.df_inventors = pd.DataFrame(records)
        # wrench_logger.debug(self.df_inventors.columns)

    def retrieve_assignees(self, patent):
        records = {
            'patent_id': [],
            'organization_name': [],
            'organization_description': [],
            'city': [],
            'external_id': [],
            'assignee_type': [],
            'assignee_first_name': [],
            'assignee_last_name': [],
            # 'full_url': [],
            # 'county_fips': [],
            # 'state_fips': [],
            # 'country': [],
            # 'total_num_patents': [],
            # 'total_num_inventors': [],
            # 'assignee_key_id': [],
        }

        if patent.get('assignees') is not None:
            for assign in patent['assignees']:
                # print('ASSIGNEE:', assign)
                if assign['assignee_id'] not in (None, '', 'None'):
                    records['patent_id'].append(patent['patent_number'])

                    records['organization_name'].append(self.handle_none_string(assign['assignee_organization']))
                    records['organization_description'].append('None')
                    # records['country'].append(
                    #     self.handle_none_string(self.escape_special_characters(assign['assignee_country'])))
                    records['city'].append(self.handle_none_string(self.escape_characters(assign['assignee_city'])))
                    # records['total_num_patents'].append(self.handle_none_int(assign['assignee_total_num_patents']))
                    # records['total_num_inventors'].append(self.handle_none_int(assign['assignee_total_num_inventors']))
                    records['external_id'].append(self.handle_none_string(assign['assignee_id']))
                    records['assignee_type'].append(self.handle_none_int(assign['assignee_type']))
                    records['assignee_first_name'].append(
                        self.handle_none_string(self.escape_characters(assign['assignee_first_name'])))
                    records['assignee_last_name'].append(
                        self.handle_none_string(self.escape_characters(assign['assignee_last_name'])))
                    # records['assignee_key_id'].append(self.handle_none_string(assign['assignee_key_id']))

            self.df_assignees = pd.DataFrame(records)
        else:
            self.df_assignees = pd.DataFrame()


        # Beta API
        # if patent.get('assignees') is not None:
        #     for assign in patent.get('assignees'):
        #         # wrench_logger.debug('ASSIGNEE:', assign)
        #         if assign.get('assignee') not in (None, '', 'None'):
        #
        #             # id = "https://search.patentsview.org/api/v1/assignee/95af1856-28ec-45d2-b8c9-4780db48a5bb/",
        #             assign_id = assign['assignee'].split('/assignee/')[1][:-1]
        #             records['external_id'].append(self.escape_characters(self.handle_none_string(assign_id)))
        #             records['full_url'].append(assign['assignee'])
        #
        #             # records['patent_id'].append(patent['patent_id']) Beta API
        #             records['patent_id'].append(patent['patent_number'])
        #
        #             records['organization_name'].append(self.handle_none_string(assign['assignee_organization']))
        #             records['organization_description'].append('None')
        #             records['city'].append(self.handle_none_string(self.escape_characters(assign['assignee_city'])))
        #             records['assignee_type'].append(self.handle_none_int(assign['assignee_type']))
        #             records['assignee_first_name'].append(
        #                 self.handle_none_string(self.escape_characters(assign['assignee_individual_name_first'])))
        #             records['assignee_last_name'].append(
        #                 self.handle_none_string(self.escape_characters(assign['assignee_individual_name_last'])))
        #
        #             # records['country'].append(
        #             #     self.handle_none_string(self.escape_special_characters(assign['assignee_country'])))
        #             # records['total_num_patents'].append(self.handle_none_int(assign['assignee_total_num_patents']))
        #             # records['total_num_inventors'].append(self.handle_none_int(assign['assignee_total_num_inventors']))
        #             # records['county_fips'].append(self.handle_none_int(assign['assignee_county_fips']))
        #             # records['state_fips'].append(self.handle_none_int(assign['assignee_state_fips']))
        #             # records['assignee_key_id'].append(self.handle_none_string(assign['assignee_key_id']))


    def fill_in_assignee_details(self):
        # TODO: the DF field full_url is used to get more details
        #       for each assignee.  That info needs to be added to the DF
        pass

    def insert_dataframes(self, patent_id):
        sql_statements = f"\nSET SESSION myapp.patent_id_var TO '{patent_id}';\n"

        # patent - MUST be one
        for _, row in self.df_patent.iterrows():
            sql = f'''
                -- Get the deal_id_var from the session variable' 
                -- DECLARE deal_id_var := current_setting('myapp.deal_id_var')::INTEGER;   
                
                -- Insert into svs_patents only if patent_id doesn't already exist
                INSERT INTO {self.set_table_name('svs_patents')} (
                    patent_id, 
                    patent_title, 
                    patent_description, 
                    filing_date, 
                    publication_date, 
                    cpc_code,
                    retrieval_date, 
                    json_dump)
                SELECT
                    '{row['patent_id']}', 
                    '{row['patent_title']}', 
                    '{row['patent_description']}', 
                    to_date('{row["filing_date"]}', 'yyyy-mm-dd'), 
                    to_date('{row["publication_date"]}', 'yyyy-mm-dd'), 
                    '{row['cpc_codes']}', 
                    to_timestamp('{row["retrieval_date"]}','yyyy-mm-dd hh24:mi:ss'), 
                    '{row['json_dump']}'
                WHERE NOT EXISTS
                    (
                        SELECT patent_id FROM {self.set_table_name('svs_patents')}
                        WHERE patent_id = '{row['patent_id']}'
                    );
            
                -- Insert or update svs_relational_deals_patents
                INSERT INTO {self.set_table_name('svs_relational_deals_patents(deal_id, patent_id)')}
                VALUES ({self.deal_id}, '{row['patent_id']}')
                ON CONFLICT (deal_id, patent_id) DO NOTHING;
            '''

            # wrench_logger.debug(sql)
            sql_statements += sql

        # inventors
        for _, row in self.df_inventors.iterrows():
            self.inventor_retrieve_count += 1

            sql = f'''
                INSERT INTO {self.set_table_name('svs_inventors')} (
                    first_name, 
                    last_name, 
                    external_id
                    )
                SELECT 
                    '{self.escape_characters(row['first'])}', 
                    '{self.escape_characters(row['last'])}', 
                    '{self.escape_characters(row['id'])}'
                WHERE NOT EXISTS
                (
                    SELECT external_id FROM {self.set_table_name('svs_inventors')}
                    WHERE external_id = '{self.escape_characters(row['id'])}'
                );
           '''
            sql_statements += sql

        # assignees
        for _, row in self.df_assignees.iterrows():
            self.assignee_retrieve_count += 1

            sql = f'''
                INSERT INTO {self.set_table_name('svs_assignees')} (organization_name,
                                           organization_description,
                                           city,
                                           external_id,
                                           assignee_type,
                                           assignee_first_name,
                                           assignee_last_name
                                           )
                SELECT
                    '{self.escape_characters(row["organization_name"])}',
                    '{self.escape_characters(row["organization_description"])}',
                    '{self.escape_characters(row["city"])}',
                    '{self.escape_characters(row["external_id"])}',
                    '{row["assignee_type"]}',
                    '{self.escape_characters(row["assignee_first_name"])}',
                    '{self.escape_characters(row["assignee_last_name"])}'
                WHERE NOT EXISTS
                (
                    SELECT external_id FROM {self.set_table_name('svs_assignees')}
                    WHERE external_id = '{self.escape_characters(row["external_id"])}'
                );
            '''
            sql_statements += sql

        # if len(sql_statements) != 0:
        #     # wrench_logger.debug(sql_statements)
        #     sql_results = rdsInstance.execute_query(sql_statements)
        #
        #     if sql_results == 'ERROR':
        #         wrench_logger.error(
        #             f'An Exception Occurred: Failed to execute SQL query for inserting Patent data. {sql_results}')
        #         wrench_logger.debug(f'Failed Query: {sql}')
        #         rdsInstance.close()
        #         self._connect_to_rds()

        return sql_statements


    @staticmethod
    def escape_characters(value):
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


