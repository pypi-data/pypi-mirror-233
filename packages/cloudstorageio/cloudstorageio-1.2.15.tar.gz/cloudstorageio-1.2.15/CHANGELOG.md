`# Changelog
All major cloudstorageio changes and pypi releases are listed here 

# Changes 
## [0.0.1] - 2019-01-29
- Created project skeleton
## [0.0.2] - 2019-02-14
- Implemented S3 & Google Cloud Storage Interfaces 
## [0.0.3] - 2019-02-28
- Implemented Cloud Storage Interface
- Implemented Local interface 
## [0.0.4] - 2019-05-31
- Add delete, listdir & isfile/isdir methods for all interfaces
## [0.0.5] - 2019-07-09
- Implemented DropBox interface
## [0.0.6] - 2019-07-24
- Add copy_batch for folder copying 
## [0.0.7] - 2019-08-08
- Add Google Drive interface
## [0.0.8] - 2019-08-30
- Add Async Cloud Interface 
## [0.0.9] - 2019-10-18
- Structure changes (file renames/moves)
- Implemented scalable unittests
## [0.0.10] - 2020-07-16
- Commented Overwriting loggers, 
- add cognaize logo in Readme
## [0.1.0] - 2020-08-05
- Add copy_dir for path to path copy
- Change copy_batch for list to list copy 
- Usages in README
## [0.1.1] - 2020-08-14
- README changes
## [0.1.2] - 2020-11-10
- Using multipart upload when copying from local to S3


# Pypi releases
See CHANGES references  
### [0.12.1] - 2019-03-12
- [0.0.3]

### [1.0.5] - 2019-06-18
- [0.0.4]
### [1.0.8] - 2019-08-01
- [0.0.6]
### [1.0.9] - 2019-10-24
- [0.0.9]
### [1.1.0] - 2020-08-05
- [0.1.0]
### [1.1.1] - 2020-08-14
- [0.1.1]
### [1.1.2] - 2020-11-10
- [0.1.2]
### [1.1.3] - 2020-11-10
- Update listdir for s3
### [1.2.1] - 2020-11-10
- Add AWS session token support
### [1.2.3] - 2020-11-10
- Remove dropbox package dependency (dropbox will not be supported with this version)
### [1.2.4] - 2020-11-10
- Add option include_files for listdir
### [1.2.7] - 2022-10-05
- Updated build to setuptools
### [1.2.8] - 2022-05-04
- Fix error on listdir for s3 if the folder did not include subfolders
- Add option include_files for listdir for non-recursive case
### [1.2.9] - 2022-05-05
- Add github workflows for merging
- Update tests to use AWS mocker
- Move moto dependency to dev-requirements
### [1.2.10] - 2023-06-30
- Fix listdir implementation to include full paths in S3
- Fix path concatenation in S3

### [1.2.11] - 2023-07-03
- Add `moto` to test requirements

### [1.2.12] - 2023-07-06
- Add exclude options to `copy_dir` function in S3

### [1.2.15] - 2023-09-29
- Fix issue with document deepcopy
- Add Dropbox, Google Storage and Drive as extra dependencies
