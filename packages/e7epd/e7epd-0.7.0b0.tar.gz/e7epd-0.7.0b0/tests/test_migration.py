from e7epd import migration
import pymongo

sql = {
    'username': 'ee_parts_db_user',
    'password': 'ee_passw_0707',
    'db_host': 'electro707.com',
    'db_name': 'ee_parts_db_test',
    'type': 'mysql_server'
}

mg_db = pymongo.MongoClient(f"mongodb://localhost:27017/")

migration.update_06_to_07(mg_db, sql)
