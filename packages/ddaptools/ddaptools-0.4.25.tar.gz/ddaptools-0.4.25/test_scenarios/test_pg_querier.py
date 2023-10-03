from ddaptools.aws_classes.class_enhancement import *
from ddaptools.dda_constants import *
import pprint



# def common_processor_using_mock():

#     publisher_credentials = {}
#     publisher_settings = {}

#     organizationDBProvider = MockOrganizationQuerier
#     publishingDBProvider = MockStagingDatabaseProviderWithChrome(credentials=publisher_credentials, settings=publisher_settings)
#     processor = BetterCommonProcessor(
#         job_parameters={"guid": "387a26ff-ceed-5015-a6c9-a2cad90329c0" },
#         organization_provider=organizationDBProvider,
#         publishingDBProvider=publishingDBProvider
#     ) # Should expect for transformation Strategies to be automatically updated

#     return processor

# # def test_picks_chrome_enhancement_instantiation(common_processor_using_mock):
# #     processor = common_processor_using_mock
# #     processor.runJobs() # Should also post at the Mock Database

def test_pg_initialization():
    """
    1. Salesforce event.
    2. Publishes in database should result in updated start and updated endtime.
    """
    

    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }

    settings = {
        "GET_TABLENAME": "staging_events",
        "TABLENAME_EVENTS": "event",
        "COLUMN_NAMES_EVENTS": Event.get_attribute_keys(),
        "TABLENAME_TIMESLOTS": "timeslot",
        "COLUMN_NAMES_TIMESLOTS": Timeslot.get_attribute_keys()
    }

    
    organizationDBProvider = PostgresqlOrganizationQuerier(credentials=credentials)
    organizationDBProvider.initialization(organization_guid="123e4567-e89b-12d3-a456-1231231")
    organization_identity_formation = organizationDBProvider.getOrganizationParameters_identity()

    print("organization_identity_formatted")
    USER_TO_BE_PICKED = "nwang@platinumfilings.com"
    pprint.pprint(organization_identity_formation[USER_TO_BE_PICKED])


