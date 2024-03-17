#!/usr/bin/python

"""
Title: Crediting and debiting main and bonus balance of subscriber's line(s)
Author: DEEWHY - Suleiman Dayo Abdullahi
Script Name: credit_debit.py
"""

# Importing required modules and functions
import datetime
import requests
import xml.etree.ElementTree as ET
import os
import sys
import re
import ConfigParser
import logging
import time


def session_login(a, cf):
    # Extract parameters from the configuration file
    if len(a) == 0:
        logging.info("Error: Configuration file config.ini not found in current directory :%s" ,workdir)
        sys.exit()    
    try:
        soap_url = cf.get('parameters', 'soap_url').split(',')
        url_info = cf.get('parameters', 'eSM_url').split(',')#Default url for the SOAP service 
        url = "http://{}:{}/{}".format(url_info[0], url_info[1], url_info[2])
        header = cf.get('parameters', 'header').split(',')
        headers = {header[0] :  "; ".join(header[1:])} # headers for the HTTP request
        # Open session to retrieve the session ID        
        session_id = get_session_id(cf, url, headers, soap_url)
        return soap_url, url, headers, session_id
        
    except Exception as e:
        logging.info("TIME: " + str(time.strftime("%H:%M:%S", time.localtime(time.time()))) +
                     " Error occurred at session_login " + str(e))
        sys.exit() 




def get_session_id(cf, url, headers, soap_url):
    key=cf.get('parameters', 'key')
    print(key)
    soap_username = cf.get('parameters', 'Soap_username')
    logging.info('Logged in using :%s', soap_username)
    
    soap_password = cf.get('parameters', 'Soap_password')
    session_id_request = """
    <soapenv:Envelope xmlns:soapenv=\"{soap_url[0]}\" xmlns:v2=\"{soap_url[1]}\">
       <soapenv:Header/>
       <soapenv:Body>
          <v2:LoginRequest>
             <v2:loginId>{soap_username}</v2:loginId>
             <v2:passwd>{soap_password}</v2:passwd>
             <v2:wsdlVersion>V_1</v2:wsdlVersion>
          </v2:LoginRequest>
       </soapenv:Body>
    </soapenv:Envelope>
    """
    session_id_request = session_id_request.format(soap_username=soap_username, soap_password=soap_password, soap_url=soap_url)
    response = requests.request("POST", url, headers=headers, data=session_id_request)
    root = ET.fromstring(response.text)
    session_id = root.find(".//{" + soap_url[1] + "}sessionId").text
    return session_id

    
    
def close_session(session_id, url, headers, soap_url):
    logout_request = """
    <soapenv:Envelope xmlns:soapenv=\"{soap_url[0]}\" xmlns:v2=\"{soap_url[1]}\">
       <soapenv:Header/>
       <soapenv:Body>
          <v2:LogoutRequest>
             <v2:SessionInfo>
                <v2:sessionId>{session_id}</v2:sessionId>
             </v2:SessionInfo>
          </v2:LogoutRequest>
       </soapenv:Body>
    </soapenv:Envelope>
    """
    response = requests.request("POST", url, data=logout_request.format(session_id=session_id, soap_url=soap_url), headers=headers)


    
    
    
def get_sub_info(session_id, cf, msisdn, url, headers, soap_url):
    try:
        sub_xml_names = cf.get('parameters', 'acct_query_names').split(',')
        bid_xml_names = cf.get('parameters', 'bundle_query_names').split(',')
        retrieve_request = """
        <soap-env:Envelope xmlns:soap-env="{soap_url[0]}">
            <soap-env:Body>
                <ns0:RetrieveRequest xmlns:ns0="{soap_url[1]}">
                    <ns0:SessionInfo>
                        <ns0:sessionId>{session_id}</ns0:sessionId>
                    </ns0:SessionInfo>
                    <ns0:RequestInfo>
                        <ns0:ReqID></ns0:ReqID>
                    </ns0:RequestInfo>
                    <ns0:TaskList>
                        <ns0:Task>
                            <ns0:Name>{sub_xml_names[0]}</ns0:Name>
                            <ns0:QueryCriteria>
                                <ns0:Param>
                                    <ns0:Name>{sub_xml_names[1]}</ns0:Name>
                                    <ns0:Value>{msisdn}</ns0:Value>
                                </ns0:Param>
                            </ns0:QueryCriteria>
                            <ns0:QueryData>
                                <ns0:Collection>
                                    <ns0:CollectionName>{sub_xml_names[2]}</ns0:CollectionName>
                                    <ns0:Attributes>
                                        <ns0:item>{sub_xml_names[1]}</ns0:item>
                                        <ns0:item>{sub_xml_names[3]}</ns0:item>
                                        <ns0:item>{sub_xml_names[4]}</ns0:item>
                                        <ns0:item>{sub_xml_names[5]}</ns0:item>
                                        <ns0:item>{sub_xml_names[6]}</ns0:item>
                                        <ns0:item>{sub_xml_names[7]}</ns0:item>
                                        <ns0:item>{sub_xml_names[8]}</ns0:item>
                                    </ns0:Attributes>
                                </ns0:Collection>
                            </ns0:QueryData>
                        </ns0:Task>
                        <ns0:Task>
                            <ns0:Name>{bid_xml_names[0]}</ns0:Name>
                            <ns0:QueryCriteria>
                                <ns0:Param>
                                    <ns0:Name>{bid_xml_names[1]}</ns0:Name>
                                    <ns0:Value>{msisdn}</ns0:Value>
                                </ns0:Param>
                            </ns0:QueryCriteria>
                            <ns0:QueryData>
                                <ns0:Collection>
                                    <ns0:CollectionName>{bid_xml_names[2]}</ns0:CollectionName>
                                    <ns0:Attributes>
                                        <ns0:item>{bid_xml_names[3]}</ns0:item>
                                        <ns0:item>{bid_xml_names[4]}</ns0:item>
                                        <ns0:item>{bid_xml_names[5]}</ns0:item>
                                        <ns0:item>{bid_xml_names[6]}</ns0:item>
                                        <ns0:item>{bid_xml_names[7]}</ns0:item>
                                        <ns0:item>{bid_xml_names[8]}</ns0:item>
                                    </ns0:Attributes>
                                </ns0:Collection>
                            </ns0:QueryData>
                        </ns0:Task>
                    </ns0:TaskList>
                </ns0:RetrieveRequest>
            </soap-env:Body>
        </soap-env:Envelope>
        """  
        # Populate the SOAP request template with data
        retrieve_request = retrieve_request.format(
            session_id=session_id,
            msisdn=msisdn,
            soap_url=soap_url,
            sub_xml_names=sub_xml_names,
            bid_xml_names=bid_xml_names    
        )

        # Send the SOAP request to get bucket information
        response = requests.request("POST", url, data=retrieve_request, headers=headers)
       
        # Parse the response XML
        root1 = ET.fromstring(response.text)

        # Return the subscribers' information as a tuple
        xml_data = response.text
        pattern = r"<Name>(.*?)</Name>.*?<[V|R].*?>(.*?)</[V|R].*?>"
        pattern_err = r"<ErrorCode>(.*?)</ErrorCode>.*?<ErrorMsg>(.*?),/ErrorMsg>"
        matches = re.findall(pattern, xml_data, re.DOTALL)
        find_err = [(key.encode('utf-8'), value.encode('utf-8')) for key, value in re.findall(pattern, xml_data, re.DOTALL)]
        match_list = [(key.encode('utf-8'), value.encode('utf-8')) for key, value in matches]
        result = [value[1] if match_list[0][1] == 'SUCCESS' else msisdn for value in match_list[1:8]]
        match_str = " ".join([" ".join([match[0], match[1]]) for match in match_list[9:]])
        main_status = match_list[0][1] if match_list[0][1] else 'FAILURE'
        bonus_status = match_list[8][1] if main_status == 'SUCCESS' else 'FAILURE'
        pattern1 = r'Bundle\sID\s(bdl\w+|\d+_\w\w|\d\d{1})\sBundle\sState\s(\S*)\sEnd\sDate\sTime\s(\S*)\sTariff\sPlan\sCOSP\sID\s(\S*)\sBucket/Discount\sID\s1\s(\S*)\sBucket/UBD\sCounter\s1\s(\S*)'
        pattern2 = r'Bundle\sID\s(sbcALWAYSON)\sBundle\sState\s(\S*)\sEnd\sDate\sTime\s(\S*)\sTariff\sPlan\sCOSP\sID\s(\S*)\sBucket/Discount\sID\s1\s(\S*)\sBucket/UBD\sCounter\s1\s(\S*)'
        result1 = re.findall(pattern1, match_str)
        result2 = re.findall(pattern2, match_str)
        return main_status, result, bonus_status, result1, result2

    except Exception as e:
        logging.info("TIME: " + str(time.strftime("%H:%M:%S", time.localtime(time.time()))) +
                     " Error occurred while getting sub infomation" + str(e))
        print("Error in get_sub_info: {}".format(e)) 



        

def balance_adjustment(session_id, msisdn, amount, adjust_method, cf, url, headers, soap_url):
    try:
        bal_xml_names = cf.get('parameters', 'main_adj_names').split(',')
        submit_request = """
        <S:Envelope
                xmlns:S="{soap_url[0]}">
                <S:Body>
                        <SubmitRequest
                                xmlns="{soap_url[1]}">
                                <SessionInfo>
                                        <sessionId>{session_id}</sessionId>
                                </SessionInfo>
                                <RequestInfo>
                                        <ReqID></ReqID>
                                </RequestInfo>
                                <TaskList>
                                        <Task>
                                                <Name>{bal_xml_names[0]}</Name>
                                                <ParamList>
                                                        <Param>
                                                                <Name>{bal_xml_names[1]}</Name>
                                                                <!-- Required -->
                                                                <Value>{msisdn}</Value>
                                                        </Param>
                                                        <Param>
                                                                <Name>{bal_xml_names[2]}</Name>
                                                                <Value>{adjust_method}</Value>
                                                        </Param>
                                                        <Param>
                                                                <Name>{bal_xml_names[3]}</Name>
                                                                <Value>N</Value>
                                                        </Param>
                                                        <Param>
                                                                <Name>{bal_xml_names[4]}</Name>
                                                                <Value>N</Value>
                                                        </Param>
                                                        <Param>
                                                                <Name>{bal_xml_names[5]}</Name>
                                                                <Value>{amount}</Value>
                                                        </Param>
                                                 </ParamList>
                                                <ContinueOnFailure>True</ContinueOnFailure>
                                        </Task>
                                </TaskList>
                        </SubmitRequest>
                </S:Body>
        </S:Envelope>
        """
        
        # Populate the SOAP request template with data
        submit_request = submit_request.format(
                        session_id = session_id, 
                        msisdn = msisdn, 
                        amount = amount, 
                        adjust_method = adjust_method, 
                        soap_url = soap_url,
                        bal_xml_names = bal_xml_names
        )

        # Send the SOAP request to increase the bucket
        response = requests.request("POST", url, data=submit_request, headers=headers)
        
        # Return the subscribers' information as a tuple
        xml_data = response.text
        pattern = r"<Name>(.*?)</Name>.*?<[V|R].*?>(.*?)</[V|R].*?>"
        matches = re.findall(pattern, xml_data, re.DOTALL)
        match_list = [(key.encode('utf-8'), value.encode('utf-8')) for key, value in matches]
        adj_status = match_list[0][1]
        pattern1 = r"\d+"
        balance = re.findall(pattern1, match_list[-1][1])
        return adj_status, balance[0]
        
    except Exception as e:
        logging.info("TIME: " + str(time.strftime("%H:%M:%S", time.localtime(time.time()))) +
                     "Error occurred while adjusting balance" + str(e))
        print("Error in balance_adjustment: {}".format(e))


        
        
def bucket_adjustment(session_id, msisdn, amount, bucket_id, adjust_method, cf, url, headers, soap_url):
    try:
        buc_xml_names = cf.get('parameters', 'bucket_adj_names').split(',')
        submit_request = """
        <S:Envelope
                xmlns:S="{soap_url[0]}">
                <S:Body>
                        <SubmitRequest
                                xmlns="{soap_url[1]}">
                                <SessionInfo>
                                        <sessionId>{session_id}</sessionId>
                                </SessionInfo>
                                <RequestInfo>
                                        <ReqID>{amount}</ReqID>
                                </RequestInfo>
                                <TaskList>
                                        <Task>
                                                <Name>{buc_xml_names[0]}</Name>
                                                <ParamList>
                                                        <Param>
                                                                <Name>{buc_xml_names[1]}</Name>
                                                                <!-- Required -->
                                                                <Value>{msisdn}</Value>
                                                        </Param>
                                                        <Param>
                                                                <Name>{buc_xml_names[2]}</Name>
                                                                <!-- Required -->
                                                                <Value>bdlBERVOBM_{bucket_id}</Value>
                                                        </Param>
                                                </ParamList>
                                                <ContinueOnFailure>True</ContinueOnFailure>
                                        </Task>
                                        <Task>
                                                <Name>{buc_xml_names[3]}</Name>
                                                <ParamList>
                                                        <Param>
                                                                <Name>{buc_xml_names[1]}</Name>
                                                                <!-- Required -->
                                                                <Value>{msisdn}</Value>
                                                        </Param>
                                                        <Param>
                                                                <Name>{buc_xml_names[4]}</Name>
                                                                <!-- Required -->
                                                                <Value>{bucket_id}</Value>
                                                        </Param>
                                                        <Param>
                                                                <Name>{buc_xml_names[5]}</Name>
                                                                <!-- Required -->
                                                                <Value>{adjust_method}</Value>
                                                        </Param>
                                                        <Param>
                                                                <Name>{buc_xml_names[6]}</Name>
                                                                <!-- Required -->
                                                                <Value>{amount}</Value>
                                                        </Param>
                                                </ParamList>
                                        </Task>
                                </TaskList>
                        </SubmitRequest>
                </S:Body>
        </S:Envelope>
        """

        # Populate the SOAP request template with data
        submit_request = submit_request.format(
            session_id=session_id,
            msisdn=msisdn,
            amount=amount,
            bucket_id=bucket_id,
            adjust_method = adjust_method,
            soap_url = soap_url,
            buc_xml_names=buc_xml_names
        )

        # Send the SOAP request to increase the bucket
        response = requests.request("POST", url, data=submit_request, headers=headers)

        # Parse the response XML
        root1 = ET.fromstring(response.text)

        # Extract the subscribers information from the response
        #data = root1.findall(".//{" + soap_url[1] + "}Value")

        xml_data = response.text
        pattern = r"<Name>(.*?)</Name>.*?<[V|R].*?>(.*?)</[V|R].*?>"
        matches = re.findall(pattern, xml_data, re.DOTALL)
        match_list = [(key.encode('utf-8'), value.encode('utf-8')) for key, value in matches]
        main_status = match_list[1][1]
        return main_status

    except Exception as e:
        logging.info("TIME: " + str(time.strftime("%H:%M:%S", time.localtime(time.time()))) +
                     "Error occurred while adjusting bucket " + str(e))
        print("Error in bucket_adjustment: {}".format(e))    

        
        
        
def setup_logging(now, logdirname):
    logfilename = logdirname + '/' + now.strftime('Credit_Debit_Ops_Tool_%d%m%Y_%H%M.log')
    if not os.path.exists(logdirname):
        os.makedirs(logdirname)
    logging.basicConfig(
        filename=logfilename, filemode='w',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    
def parse_argument(session_id, cf, url, headers, soap_url, details):
    try:
        args = re.sub(r"[\t\s;,:]{1,10}", " ", details)
        msisdn = args.split()[0]
        msisdn = msisdn if msisdn.startswith("234") else "234" + msisdn
        debit_amt_main = " ".join(re.findall(r"MAIN|main\s\-(\d+\.?\d?\d?)", args)) 
        debit_amt_main = float(debit_amt_main) if debit_amt_main else ""
        debit_amt_bonus = " ".join(re.findall(r"BONUS|bonus\s\-(\d+\.?\d?\d?)", args))
        debit_amt_bonus = int(float(debit_amt_bonus) * 10000) if debit_amt_bonus else ""
        credit_amt_main = " ".join(re.findall(r"MAIN|main\s\+(\d+\.?\d?\d?)", args)) 
        credit_amt_main = float(credit_amt_main) if credit_amt_main else ""
        credit_amt_bonus = " ".join(re.findall(r"BONUS|bonus\s\+(\d+\.?\d?\d?)", args))
        credit_amt_bonus = float(credit_amt_bonus) * 10000 if credit_amt_bonus else ""
        sub_info = get_sub_info(session_id, cf, msisdn, url, headers, soap_url)
        status = sub_info[1][3] if sub_info[0]=="SUCCESS" else ""
        deactivated = re.match(r"\w{3}_DE\w{4,6}\d*", status)
        valid_state = re.match(r"\w{3}_VA\w{3}\d*", status)
        
        return debit_amt_main, debit_amt_bonus, credit_amt_main, credit_amt_bonus, deactivated, valid_state, msisdn, sub_info
        
    except Exception as e:
        logging.info("TIME: " + str(time.strftime("%H:%M:%S", time.localtime(time.time()))) +
                     "Error occurred while parsing argument" + str(e))
        print("Error in parse_argument: {}".format(e))    
    

    
def debit_operations(args, sub_info, session_id, current_date, cf, url, headers, soap_url):
    try:
        debit_amt_main, debit_amt_bonus, deactivated, valid_state = args[:2]+args[4:6]
        main_status, main_info = sub_info[:2]
        msisdn, status, balance = main_info[0], main_info[3], main_info[6] 
        
        if debit_amt_main:
            if main_status == 'SUCCESS' and not deactivated and not valid_state:
                if float(balance) >= debit_amt_main:
                    adj_status, adj_balance = balance_adjustment(session_id, msisdn, debit_amt_main, 'DECR', cf, url, headers, soap_url)
                    main_debit = "main debiting " + adj_status + ", current main balance -> NGN" + str(float(adj_balance)/10000)
                else:
                    main_debit = "Current main balance of NGN" + str(float(balance)/10000) + " not sufficient for debiting NGN" + str(debit_amt_main)
            elif deactivated:
                main_debit = "The line is deactive, can't debit"
            elif valid_state:
                main_debit = "The line is in valid state, can't debit"
        else:
            main_debit = ""
            
        
        if debit_amt_bonus:
            bonus_status, bonus_info1, bonus_info2 = sub_info[2:]
            if bonus_status == "SUCCESS" and not deactivated and not valid_state:  
                bonus_debit_detail = list(filter(lambda x: (x[2] >= current_date or x[2] =="") and (float(x[5]) >= debit_amt_bonus), bonus_info1)) 
                #bucket_id, adj_bonus = bonus_debit_detail[0][4:6]
                if  len(bonus_debit_detail) == 1:
                    bucket_id, adj_bonus = bonus_debit_detail[0][4:6]
                    bonus_debit = bucket_adjustment(session_id, msisdn, debit_amt_bonus, bucket_id, 'DECR', cf, url, headers, soap_url)
                    bonus_debit = "bonus debiting " + bonus_debit    + ", current bonus balance -> NGN" + str((int(adj_bonus) - float(debit_amt_bonus))/10000)    
                elif len(bonus_debit_detail)> 1 and float(bonus_info1[0][5]) >= debit_amt_bonus:
                    bucket_id, adj_bonus = bonus_debit_detail[0][4:6]
                    bonus_debit = bucket_adjustment(session_id, msisdn, debit_amt_bonus, bonus_id, 'DECR', cf, url, headers, soap_url)
                    bonus_debit = "bonus debiting " + bonus_debit    + ", current bonus balance -> NGN" + str((int(bonus_info1[0][5]) - float(debit_amt_bonus))/10000)
                elif len(bonus_debit_detail)> 1 and float(bonus_info1[1][5]) >= debit_amt_bonus:
                    bucket_id, adj_bonus = bonus_debit_detail[1][4:6]
                    bonus_debit = bucket_adjustment(session_id, msisdn, debit_amt_bonus, bucket_id, 'DECR', cf, url, headers, soap_url)
                    bonus_debit = "bonus debiting " + bonus_debit    + ", current bonus balance -> NGN" + str((int(bonus_info[0][5]) - float(debit_amt_bonus))/10000)

                else:
                    bonus_debit = "Current bonus balance not sufficient for debiting NGN" + str(float(debit_amt_bonus)/10000)
            elif deactivated:
                bonus_debit = "The line is deactive, can't debit bonus"
            elif valid_state:
                bonus_debit = "The line is in valid state, can't debit bonus"
            else:
                bonus_debit = "Insufficient bonus balance for debiting"
        else:
            bonus_debit = ""
        
        demarcate = " | " if main_debit and bonus_debit else ""
        return "{}: {}{}{}".format(main_info[0], main_debit or "", demarcate, bonus_debit or "")

    except Exception as e:
        logging.info("TIME: " + str(time.strftime("%H:%M:%S", time.localtime(time.time()))) +
                     " Error occurred while carrying out debit operations " + str(e))
        print("Error in debit_operations: {}".format(e))  



def credit_operations(args, sub_info, details, session_id, cf, url, headers, soap_url):
    try:
        credit_amt_main, credit_amt_bonus, deactivated, valid_state = args[2:4]+args[4:6]
        main_status, main_info, bonus_status, bonus_info1 = sub_info[:4]
        msisdn, status, balance = main_info[0], main_info[3], main_info[6] 
        
        if credit_amt_main:
            if main_status == 'SUCCESS':
                if not deactivated and not valid_state:
                    adj_status, adj_balance = balance_adjustment(session_id, msisdn, credit_amt_main, 'INCR', cf, url, headers, soap_url)
                    #main_credit = [float(main_info[6]) + credit_amt_main, "SUCCESSFUL"]
                    #print(main_credit)
                    main_credit = "main crediting " + adj_status + ", current main balance -> NGN" + str(float(adj_balance)/10000)
                elif valid_state:
                    main_credit = "The line is in valid state, can't credit main."
                elif deactivated:
                    main_credit = "The line is deactive, can't credit main"
                else:
                    main_credit = "call the script_writer attention"
            else:
                main_credit = "not on IN"
        else:
            main_credit = ""    
        
        
        if credit_amt_bonus:
            if bonus_status == 'SUCCESS' and not deactivated and not valid_state:
                bonus_balance = float(bonus_info1[0][5])/10000 if bonus_info1 else 0
                credit_bucket_id = "MAA" if "MAA" in details else "MA4" if "MA4" in details else None
                #bucket_id_input = str(input("Please input bucket_id (MAA or MA4) for" + str(main_info[0]) +" or press enter to skip and continue : "))
                #credit_bucket_id = "MAA" if "MAA" in details else "MA4" if "MA4" in details else "" 
                #credit_bucket_id = credit_bucket_id if credit_bucket_id else str(bucket_id_input)
                if credit_bucket_id:
                    adj_status = bucket_adjustment(session_id, msisdn, int(credit_amt_bonus), credit_bucket_id, 'INCR', cf, url, headers, soap_url)
                    total_bal = str(bonus_balance + (credit_amt_bonus)/10000) if adj_status == 'SUCCESS' else str(bonus_balance)
                    bonus_credit = "bonus crediting " + adj_status + ", current bonus balance -> " + total_bal
                else:
                    bonus_credit = "Bucket id was not inputed, bonus credit was not executed"               
            elif valid_state:
                bonus_credit = "can't be credit in valid state"
            elif deactivated:
                bonus_credit = "can't be credited in deactivate state"
            else:
               bonus_credit = "call the script_writer attention"
        else:
            bonus_credit = ""
            
        demarcate = " | " if main_credit and bonus_credit else ""
        return "{}: {}{}{}".format(msisdn, main_credit or "", demarcate, bonus_credit or "" )
    
    except Exception as e:
        logging.info("TIME: " + str(time.strftime("%H:%M:%S", time.localtime(time.time()))) +
                     " Error occurred while carrying out credit operations " + str(e))
        print("Error in credit_operations: {}".format(e))     
    
    
    


def debit_credit_logic(session_id, msisdn, details, current_date, cf, url, headers, soap_url, filename, logdirname, now, args):
    output_info = logdirname + '/' + now.strftime('debit_credit_' + filename +'_%d%m%Y_%H%M.txt')
    sub_info = args[7]
    if details.count("-") >= 1 and details.count("+") == 0 and len(sub_info[1]) == 7:
        debited = debit_operations(args, sub_info, session_id, current_date, cf, url, headers, soap_url)
        with open(output_info, 'a') as file:
            file.write(debited + '\n')        
        print(debited)

    if details.count("+") >= 1 and details.count("-") == 0 and len(sub_info[1]) == 7:
        credited = credit_operations(args, sub_info, details, session_id, cf, url, headers, soap_url)
        with open(output_info, 'a') as file:
            file.write(credited + '\n')
        print(credited)
        
    elif len(sub_info[1]) < 7:
        info = msisdn+": " + 'not on IN'
        with open(output_info, 'a') as file:
            file.write(info + '\n')
        print(info)     
    
    

    
    


def main():
    """
    Main function to handle balance adjustment operations.
    """
 
    workdir = os.getcwd()
    #workdir = "/sms/IN_TEAM/IN_OPERATIONS"
    workdir1 = "/sms/IN_TEAM/dayo/CUSTOMIZED-SCRIPT"
    #print(workdir)

    # Get the current working directory and time
    now = datetime.datetime.now()
    current_date = now.strftime("%Y%m%d%H%M")
    
    # Create a directory for logging files
    #log_path =workdir + '/' + now.strftime('IN_Operations_%d%m%Y%H%M')
    logdirname =workdir + '/' + 'IN_Operations_logs'+ '/' + 'Credit_Debit_logs' + '/' + now.strftime('Credit_Debit_%m%Y')

    logs = setup_logging(now, logdirname)
        
    logging.info('Log Execution Directory is at path :%s', logdirname)
        
    fnm = "config1.ini"
    cf = ConfigParser.ConfigParser(allow_no_value=True)
    a = cf.read(os.path.join(workdir1, fnm))
    logged_in = session_login(a, cf)
    soap_url, url, headers, session_id = logged_in
    if len(logged_in) == 3:
        logging.info("Logged in successfully")
    try:
        # Get the MSISDN or filename from command line arguments
        arg = sys.argv
        if len(arg) > 1:
            file_name = arg[1]
            isFile = os.path.isfile(file_name)
            if isFile:
                # Try to open the argument as a file
                with open(file_name, 'r') as file:
                    for details in file:
                        args = parse_argument(session_id, cf, url, headers, soap_url, details)
                        msisdn = args[6]
                        debit_credit_logic(session_id, msisdn, details, current_date, cf, url, headers, soap_url, file_name, logdirname, now, args)

            else:
                # If it's not a file, assume it's a MSISDN
                details = " ".join(arg[1:])
                args = parse_argument(session_id, cf, url, headers, soap_url, details)
                msisdn = args[6]
                debit_credit_logic(session_id, msisdn, details, current_date, cf, url, headers, soap_url, msisdn, logdirname, now, args)
      

    except Exception as e:
        logging.info("TIME: " + str(time.strftime("%H:%M:%S", time.localtime(time.time()))) +
                     " Error occurred in the main " + str(e))
        # Handle exceptions and print an error message
        print("Error in main: {}".format(e))
        
    finally:
        # Close the session
        if session_id:
            close_session(session_id, url, headers, soap_url)
            logging.info('Session properly closed and tool Execution Ended ')
        

# Execute the main function if the script is run as the main module
if __name__ == '__main__':
    main()
