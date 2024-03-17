# Credit and Debit Operations Automation Script

## Introduction
The Credit and Debit Operations Automation Script is a Python script designed to automate the process of crediting and debiting main and bonus balances of subscriber lines for a Telecommunication company. It aims to address the inefficiencies and potential errors associated with manual operations. By automating these tasks, the script offers significant improvements in:
- Efficiency
- Accuracy
- Ease of troubleshooting

The script prioritizes security by masking sensitive credentials and eliminating their hardcoding.

## Problem Statement
The existing process of crediting and debiting subscriber balances at Globacom Nigeria suffers from several shortcomings:
- Multiple and Individual Operations: Manual credit and debit operations require separate actions, leading to time consumption and potential inconsistencies.
- Difficult Output Interpretation: Manual outputs can be challenging to interpret, hindering clear understanding of the actions performed.
- Troubleshooting Challenges: Troubleshooting manual operations can be cumbersome due to a lack of clear audit trails.
- Human Error: Manual processes are prone to human error, which can have financial and service-related consequences.

## Solution Overview
The Credit and Debit Operations Automation Script tackles these challenges by:
- Automating Operations: Combining all credit and debit operations into a single script streamlines the process.
- Enhancing Output Readability: The script generates clear and well-formatted outputs for easy interpretation.
- Logging Operations: Script execution is logged for effective troubleshooting purposes.
- Simplifying Input Data Injection: The script offers flexible input options for both individual operations and bulk processing through files.
- Future Web Service Integration: The script's design allows for potential future integration with a web service for a graphical user interface (GUI).

## Script Functionality
The script offers the following functionalities:
- Session Management: Establishes and manages connections to the relevant systems.
- Balance Adjustment: Automates credit and debit adjustments for both main and bonus balances.
- Bucket Adjustment: Enables adjustments to specific bonus buckets.
- Logging: Records script execution details for audit purposes.
- Input Parsing: Effectively handles user input for individual and bulk operations.
- Main and Bonus Operations: Supports independent operations on main and bonus balances.
- Error Handling: Implements mechanisms to gracefully handle potential errors during script execution.

## Getting Started
To use the script, follow these steps:
1. Clone the Repository
2. Install Dependencies
3. Run the Script
4. Follow Usage Instructions

## Usage
1. Installation
2. Configuration
3. Running the Script
4. Output

## Configuration File
The `config.ini` file requires the following configurations:
- `soap_url`
- `eSM_url`
- `header`
- `key`
- `Soap_username`
- `Soap_password`
- `acct_query_names`
- `bundle_query_names`
- `main_adj_names`

## Logging
- Log files are stored in the `IN_Operations_logs/Credit_Debit_logs` directory.

## Contributing
Contributions to the project are welcome. To contribute, follow these steps:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request.

## Future Enhancements
The script is designed for continuous improvement, and future enhancements are planned:
- Graphical User Interface (GUI)
- Error Handling
- Security Enhancements


## Author
This project was authored by Suleiman Dayo Abdullahi.


## Additional Sections
For additional information, refer to the script's source code and comments.

**Note:** The script is built for Python 2.7. Other modules are inbuilt in Python 2.7. Required dependencies are listed in `Requirement.txt`.

---

This README provides an overview of the script's functionality, usage instructions, configuration details, logging information, contribution guidelines, and author attribution. It aims to facilitate understanding and usage of the `credit_debit.py` script for performing credit and debit operations on subscriber balances.

