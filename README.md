Credit and Debit Operations Automation Script
Introduction
The Credit and Debit Operations Automation Script is a Python script developed to automate the process of crediting and debiting main and bonus balances of subscriber lines for Globacom Nigeria. The script aims to address the challenges faced in manually performing these operations, including tediousness, time consumption, and the potential for human error. By automating these operations, the script improves efficiency, accuracy, and ease of troubleshooting. The script was designed with security considerations and masking to eliminate hardcoding of sensitive credentials.

Problem Statement
The existing process of crediting and debiting main and bonus balances for subscriber lines at Globacom Nigeria suffers from several shortcomings:

Multiple and Individual Operations
Difficult Output Interpretation
Troubleshooting Challenges
Human Error
Solution Overview
The Credit and Debit Operations Automation Script addresses the above challenges by automating the process of crediting and debiting main and bonus balances. The script combines all operations into a single script, enhances output readability, logs operations for troubleshooting, simplifies input data injection, and is designed with the future prospect of integration with a web service for GUI use.

Script Functionality
Session Management
Balance Adjustment
Bucket Adjustment
Logging
Input Parsing
Main and Bonus Operations
Error Handling
Getting Started
To get started with the script, follow these steps:

Clone the repository.
Install the required dependencies mentioned in Requirement.txt.
Run the script using Python 2.7.
Follow the usage instructions provided below.
Usage
Installation:
Clone the repository to your local machine.
Ensure Python is installed (python --version).
Install required dependencies (pip install requests).
Configuration:
Ensure a config.ini file is available in the script directory, containing necessary configuration parameters.
Running the Script:
Execute the script using Python (python credit_debit.py).
Pass single operation to Command Line Arguments i.e:
./credit_debit.py 234xxxxxxxxx main +amount bonus +amount bucket_id
./credit_debit.py 234xxxxxxxxx main -amount bonus -amount
Alternatively, provide a filename containing MSISDNs as input for bulk operations i.e.:
./credit_debit.py filename.txt
Output:
The script will generate output files in the IN_Operations_logs/Credit_Debit_logs directory.
Output files contain details of credit and debit operations performed on subscriber lines.
Configuration File
The config.ini file must be configured with the following parameters:

soap_url: URL for the SOAP service.
eSM_url: Default URL for the SOAP service.
header: Headers for the HTTP request.
key: Key for authentication.
Soap_username: Username for SOAP service authentication.
Soap_password: Password for SOAP service authentication.
acct_query_names: XML names for account query.
bundle_query_names: XML names for bundle query.
main_adj_names: XML names for main balance adjustment.
bucket_adj_names: XML names for bucket adjustment.
Logging
Log files are stored in the IN_Operations_logs/Credit_Debit_logs directory.
Logs include timestamps, log levels, and execution details.
Contributing
Contributions to the project are welcome. To contribute, follow these steps:

Fork the repository.
Make your changes.
Submit a pull request.
Future Enhancements
The script is designed for continuous improvement, and future enhancements are planned:

Graphical User Interface (GUI)
Error Handling
Security Enhancements
License
This project is licensed under the Globacom License.

Author
This project was authored by Suleiman Dayo Abdullahi.

Acknowledgements
Special thanks to my Globacom colleagues (Intelligent Network Unit TEAM) for their contributions and support.

Additional Sections
For additional information, refer to the script's source code and comments.

Note: The script is built for Python 2.7. Other modules are inbuilt in Python 2.7. Required dependencies are listed in Requirement.txt.

This README provides an overview of the script's functionality, usage instructions, configuration details, logging information, contribution guidelines, and author attribution. It aims to facilitate understanding and usage of the credit_debit.py script for performing credit and debit operations on subscriber balances.
