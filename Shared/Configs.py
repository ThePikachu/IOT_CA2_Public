
class Configs:
    def __init__(self):
        #self.db_host = "mysql.c8asbmisnjvi.us-east-1.rds.amazonaws.com"
        self.db_host = ""
        self.db_user = ""
        self.db_password = ""
        #self.db_host = "localhost"
        #self.db_user = "root"
        #self.db_password = "12345"
        self.databaseName = ""
        self.aws_region = ""
        self.aws_endpoint = ""
        self.aws_access_key = ""
        self.aws_secret_key = ""
        self.aws_S3_access_key = ""
        self.aws_S3_secret_key = ""
        self.aws_S3_bucket = ''
        self.aws_S3_endpoint = ''

global Config
Config = Configs()
