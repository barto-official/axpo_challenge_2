# IoT Data Collection, Aggregation, Access Layer using Microsoft Azure

This project aims to create a data engineering infrastructure for IoT domain to build a system that allows for an easy access of data to Business Intelligence (BI) specialists and Data Scientists. The solution is implemented using Microsoft Azure and involves:

* generating (fake, for simuluation) IoT data — implemented as Docker container inside Azure Web App
* aggregating data for analysis — in the same Docker container inside Azure Web App
* collecting and storing data in raw format — in MySQL on Azure
* API service to provide access to IoT data collected and stored in a MySQL database — implemented as a separate Docker container inside Azure Web App
