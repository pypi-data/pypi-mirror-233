#Import the headers.
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import re
import json
import html
import pandas as pd

def excel_1drive_toDict(url):

  """
    Returns a dict where the key = sheetnames and value = Dataframe of table inside the sheet.
    Ensure the excel is set to 'anyone with link can view/ edit'.

    :param url: URL of the excel as 'onedrive.live' or '1drv.ms'
    :type url: str
    :return: A dict where the key = sheetnames and value = Dataframe of table inside the sheet.
    :rtype: dict
  """

  # 1. Identify if the url is 1drv.ms or Onedrive.live
  parsed_url = urlparse(url)
  hostname = parsed_url.netloc

  if "1drv.ms" in hostname:
    url_type = "1drv.ms"
  elif "onedrive.live.com" in hostname:
    url_type = "onedrive.live"
  else:
    url_type = "Unknown"

  if url_type == "onedrive.live":

    # Send an HTTP request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <script> tags in the HTML
    script_tags = soup.find_all('script')

    # Search for the "FileGetUrl" value within each <script> tag
    for script_tag in script_tags:
        script_text = script_tag.get_text()
        file_get_url_match = re.search(r'"FileGetUrl":\s*"(.*?)"', script_text)

        if file_get_url_match:

            file_get_url = file_get_url_match.group(1)  # Get the captured URL without quotes
            file_get_url = html.unescape(file_get_url)

            # Extract the JSON-like object from the input string
            json_str = f'{{"FileGetUrl": "{file_get_url}"}}'

            # Parse the JSON-like object
            data = json.loads(json_str)

            # Get the "FileGetUrl" value
            file_get_url = data.get("FileGetUrl", "")

            # Return the extracted URL
            url = file_get_url

            # Stream the Excel file directly into Python
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                # Load the file into a dictionary of DataFrames
                xls = pd.ExcelFile(response.content)
                sheet_names = xls.sheet_names
                excel_data = {}  # Dictionary to store DataFrames.

                for sheet_name in sheet_names:
                    df = xls.parse(sheet_name)
                    excel_data[sheet_name] = df

                # Now you have the Excel data in the 'excel_data' dictionary
                # You can access DataFrames using sheet names as keys, e.g., excel_data['Sheet1']

                #Return the df.
                return excel_data

            else:
                print("Sorry, Failed to stream the file from the URL at the moment.")


            break  # Stop searching once found

    if 'file_get_url' not in locals():
        print("File not found.")


  # When the supplied url is of the 1drv.ms variety.
  elif url_type == "1drv.ms":

    # Send an HTTP request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <meta> tag with property="og:url"

    url_meta_tag = soup.find("meta", property="og:url")
    # Extract the URL attribute from the <meta> tag
    extracted_url1 = url_meta_tag.get("content") if url_meta_tag else None

    # Re-extracting url2 from the extracted_url1.
    # Send an HTTP request to the URL
    response = requests.get(extracted_url1)
    response.raise_for_status()  # Raise an exception for HTTP errors
    soup2 = BeautifulSoup(response.text, 'html.parser')

    # Find the <noscript> tag
    meta_tag = soup2.find('noscript').find("meta")

    # Extract the URL from the content attribute of the <meta> tag
    if meta_tag:
        content = meta_tag.get("content", "")
        url_start = content.find("url=")
        if url_start != -1:
            extracted_url2 = content[url_start + 4:]
            extracted_url2 = extracted_url2.split(";")[0]  # Remove any additional parameters
            extracted_url2 = extracted_url2.strip()
        else:
            extracted_url2 = None
    else:
        extracted_url2 = None

    return excel_1drive_toDict(extracted_url2)


  else:

    print("Sorry, this url is unsupported at the moment.")





def excel_1drive_sheetnames(url):
  """
  Returns a list of the sheet names.
  For large excel files, it is recommended to use 'excel_1drive_toDict(url)' method directly.

  :param url: URL of the excel as 'onedrive.live' or '1drv.ms'
  :type url: str
  :return: A list of sheet names.
  :rtype: list
  """

  return list(excel_1drive_toDict(url).keys())



def excel_1dr_SingleSheet_toDF(url, sheetname):

  """
  Returns Dataframe from the Single, Sheet requested.
  For large excel files, it is recommended to use 'excel_1drive_toDict(url)' method directly.

  :param url: URL of the excel as 'onedrive.live' or '1drv.ms'
  :type url: str
  :param sheetname: Sheet name from the excel file to be loaded onto the DF.
  :type sheetname: str
  :return: A dataframe consisting of the data inside the excel sheet specified.
  :rtype: DataFrame
  """

  # Obtaining the dictionary with all the data.
  dict_output = excel_1drive_toDict(url)

  # If condition to check if the sheet name actually exists in the excel / dict.
  if sheetname in dict_output:

    # Copy the df into df_output
    df_output = dict_output[sheetname]

    # Return the df.
    return df_output

  else:

    print("The sheetname '" + str(sheetname) + "' does not exist.")

