# Spotify End-To-End Data Engineering Project

### Introduction
In this project, we will build an ETL (Extract, Transform & Load) pipeline using the Spotify API on AWS. The pipeline will retrieve data from the Spotify API, transform it to a desired format, and load it into an AWS data store

### Architecture
![Architure Diagram](https://github.com/nirakar-sahu/spotify-end-to-end-data-engineering-project/blob/main/Spotify_Data_Architecture.PNG) 

###Services Used
1. **S3 (Simple Storage Services):** Amazon S3 is a highly scalable object storage service that can store and retrive any amount of data from anywhere on the web. It is commonly used to store and distribute larger media files , data backups, and static website files.

2.  **AWS Lambda:** AWS Lambda is an event-driven, serverless computing platform provided by Amazon as a part of Amazon Web Services. It is designed to enable developers to run code without provisioning or managing servers.

3.  **Cloud Watch:** Amazon CloudWatch is a component of Amazon Web Services that provides monitoring for AWS resources and the customer applications running on the Amazon infrastructure.

4.  **Glue Crawlers:** The CRAWLER creates the metadata that allows GLUE and services such as ATHENA to view the S3 information as a database with tables. That is, it allows you to create the Glue Catalog. This way you can see the information that s3 has as a database composed of several tables.
*For example if you want to create a crawler you must specify the following fields:*
*Database --> Name of database Service role service-role/AWSGlueServiceRole Selected classifiers --> Specify Classifier Include path --> S3 location*
