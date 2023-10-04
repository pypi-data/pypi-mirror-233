import enum


class PrefixEnums(enum.Enum):
    S3 = 's3://'
    GOOGLE_CLOUD = 'gs://'
    DROPBOX = 'dbx://'
    GOOGLE_DRIVE = 'gdrive://'


class StorageIdentifierEnum(enum.Enum):
    LOCAL = 1
    S3 = 2
    GOOGLE_CLOUD = 3
    DROPBOX = 4
    GOOGLE_DRIVE = 5
