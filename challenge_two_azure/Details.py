
# imports
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
from challenge_two_azure.Database import Database
import logging
import pymongo
logging.basicConfig(filename='log/app.log', filemode='w',level=logging.INFO)


class Details():
    def __init__(self):
        self.url = "https://www.youtube.com/youtubei/v1/next?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"

    def table_insert(self, name, comment, last_setails_row_id):
        try:
            comment = json.dumps(comment)
            obj_db = Database()
            connection = obj_db.mysql_connect()
            cursor = connection.cursor()
            sql = "insert into comments(details_id,persion_name,comment) values(%s, %s, %s)"
            cursor.execute(sql, (last_setails_row_id, name, comment))
            connection.commit()
        except Exception as ex:
            logging.info("Comment insersation issue")


    # resursive finding all comment
    def resursive_fun(self, params, token, last_setails_row_id, name_comment_list):
        try:
            header = {"context":{"client":{"hl":"en","gl":"IN","remoteHost":"202.160.145.70","deviceMake":"","deviceModel":"","visitorData":"CgtuWjhiNHd6LTRzNCjQjsyfBg%3D%3D","userAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20230217.01.00","osName":"X11","osVersion":"","originalUrl":"https://www.youtube.com/watch?v=cWOpkTWg2vE","platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{"appInstallData":"CNCOzJ8GEOLUrgUQzPWuBRDM364FEIfdrgUQtpz-EhC41K4FEKLsrgUQ2umuBRCJ6K4FEJT4rgUQjvGuBRCC3a4FEPuj_hIQ5aD-EhDn964FELiLrgUQ58KuBRD6xa4FEJH4_BI%3D"},"timeZone":"Asia/Calcutta","browserName":"Chrome","browserVersion":"110.0.0.0","acceptHeader":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","deviceExperimentId":"ChxOekU1T0RRME1UYzVOemMxTVRReU5qYzBOdz09ENCOzJ8GGK2BmJ8G","screenWidthPoints":1366,"screenHeightPoints":150,"screenPixelDensity":1,"screenDensityFloat":1,"utcOffsetMinutes":330,"userInterfaceTheme":"USER_INTERFACE_THEME_LIGHT","connectionType":"CONN_CELLULAR_4G","memoryTotalKbytes":"8000000","mainAppWebInfo":{"graftUrl":"https://www.youtube.com/watch?v=cWOpkTWg2vE","pwaInstallabilityStatus":"PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":"false"}},"user":{"lockedSafetyMode":"false"},"request":{"useSsl":"true","consistencyTokenJars":[{"encryptedTokenJarContents":"AEhaiyuC55N3FWtT4NMwN146bt-FMS7i3mJ6DgZCPmizodDjffaXiCq34hRcvxqQ6NDJAJhQ-kYHqdwuGSUw9wVE8i_shoJSmrZK3K8W3SD-VusB8pJD_yzqool1K0wQ6FKf6ZT_EXpPs4RZJ8dR1B2F"}],"internalExperimentFlags":[]},"clickTracking":{"clickTrackingParams":params},"adSignalsInfo":{"params":[{"key":"dt","value":"1676871505202"},{"key":"flash","value":"0"},{"key":"frm","value":"0"},{"key":"u_tz","value":"330"},{"key":"u_his","value":"3"},{"key":"u_h","value":"768"},{"key":"u_w","value":"1360"},{"key":"u_ah","value":"741"},{"key":"u_aw","value":"1360"},{"key":"u_cd","value":"24"},{"key":"bc","value":"31"},{"key":"bih","value":"150"},{"key":"biw","value":"1351"},{"key":"brdim","value":"0,27,0,27,1360,27,1366,741,1366,150"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}]}},"continuation":token}
            response_data = requests.post(self.url, json = header)
            json_data = json.loads(response_data.text)
            first_response = json_data['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems']
            
            for i in first_response:
                if 'commentThreadRenderer' in i.keys():
                    try:
                        name = i['commentThreadRenderer']['comment']['commentRenderer']['authorText']['simpleText']
                        comment = i['commentThreadRenderer']['comment']['commentRenderer']['contentText']['runs']
                        self.table_insert(name, comment, last_setails_row_id)
                        list = {"name":name, "comment":comment}
                        name_comment_list.append(list)
                    except:
                        logging.info("Name details not exist")

                elif 'continuationItemRenderer' in i.keys():
                    params = i['continuationItemRenderer']['continuationEndpoint']['clickTrackingParams']
                    token = i['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
                    
                    #Calling resuesive function
                    return self.resursive_fun(params, token, last_setails_row_id, name_comment_list)
                else:
                    return name_comment_list
        except:
            logging.info("resursive_fun top call problem!")

        return name_comment_list

    # finding first time comment
    def find_commend(self, main_script, last_setails_row_id):
        tracking_main = (main_script[43]).text
        tracking_text = tracking_main[20:-1]
        tracking_json = json.loads(tracking_text)
        itemSectionRenderer = tracking_json['contents']['twoColumnWatchNextResults']['results']['results']['contents']
        
        for item in itemSectionRenderer:
            try:
                itemSectionRenderer = item.get('itemSectionRenderer')
            except:
                itemSectionRenderer = ""


        if itemSectionRenderer:
            try:
                # After page load try to get all comment
                params = itemSectionRenderer['contents'][0]['continuationItemRenderer']['continuationEndpoint']['clickTrackingParams']
                token = itemSectionRenderer['contents'][0]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
               
                header = {"context":{"client":{"hl":"en","gl":"IN","remoteHost":"202.160.145.70","deviceMake":"","deviceModel":"","visitorData":"CgtuWjhiNHd6LTRzNCjQjsyfBg%3D%3D","userAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20230217.01.00","osName":"X11","osVersion":"","originalUrl":"https://www.youtube.com/watch?v=cWOpkTWg2vE","platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{"appInstallData":"CNCOzJ8GEOLUrgUQzPWuBRDM364FEIfdrgUQtpz-EhC41K4FEKLsrgUQ2umuBRCJ6K4FEJT4rgUQjvGuBRCC3a4FEPuj_hIQ5aD-EhDn964FELiLrgUQ58KuBRD6xa4FEJH4_BI%3D"},"timeZone":"Asia/Calcutta","browserName":"Chrome","browserVersion":"110.0.0.0","acceptHeader":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","deviceExperimentId":"ChxOekU1T0RRME1UYzVOemMxTVRReU5qYzBOdz09ENCOzJ8GGK2BmJ8G","screenWidthPoints":1366,"screenHeightPoints":150,"screenPixelDensity":1,"screenDensityFloat":1,"utcOffsetMinutes":330,"userInterfaceTheme":"USER_INTERFACE_THEME_LIGHT","connectionType":"CONN_CELLULAR_4G","memoryTotalKbytes":"8000000","mainAppWebInfo":{"graftUrl":"https://www.youtube.com/watch?v=cWOpkTWg2vE","pwaInstallabilityStatus":"PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":"false"}},"user":{"lockedSafetyMode":"false"},"request":{"useSsl":"true","consistencyTokenJars":[{"encryptedTokenJarContents":"AEhaiyuC55N3FWtT4NMwN146bt-FMS7i3mJ6DgZCPmizodDjffaXiCq34hRcvxqQ6NDJAJhQ-kYHqdwuGSUw9wVE8i_shoJSmrZK3K8W3SD-VusB8pJD_yzqool1K0wQ6FKf6ZT_EXpPs4RZJ8dR1B2F"}],"internalExperimentFlags":[]},"clickTracking":{"clickTrackingParams":params},"adSignalsInfo":{"params":[{"key":"dt","value":"1676871505202"},{"key":"flash","value":"0"},{"key":"frm","value":"0"},{"key":"u_tz","value":"330"},{"key":"u_his","value":"3"},{"key":"u_h","value":"768"},{"key":"u_w","value":"1360"},{"key":"u_ah","value":"741"},{"key":"u_aw","value":"1360"},{"key":"u_cd","value":"24"},{"key":"bc","value":"31"},{"key":"bih","value":"150"},{"key":"biw","value":"1351"},{"key":"brdim","value":"0,27,0,27,1360,27,1366,741,1366,150"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}]}},"continuation":token}
                response_data = requests.post(self.url, json = header)
                json_data = json.loads(response_data.text)
                first_response = json_data['onResponseReceivedEndpoints'][1]['reloadContinuationItemsCommand']['continuationItems']
                
                # List of all comment and name 
                name_comment_list = []
                
                for i in first_response:
                    if 'commentThreadRenderer' in i.keys():
                        try:
                            name = i['commentThreadRenderer']['comment']['commentRenderer']['authorText']['simpleText']
                            comment = i['commentThreadRenderer']['comment']['commentRenderer']['contentText']['runs']
                            list = {"name":name, "comment":comment}
                            #append data to comment table
                            self.table_insert(name, comment, last_setails_row_id)
                            name_comment_list.append(list)
                        except:
                            logging.info("Name details not exist")

                    elif 'continuationItemRenderer' in i.keys():
                        params = i['continuationItemRenderer']['continuationEndpoint']['clickTrackingParams']
                        token = i['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

                        #Calling resuesive function
                        return self.resursive_fun(params, token, last_setails_row_id, name_comment_list)
                    else:
                        logging.info("commentThreadRenderer and continuationItemRenderer not found")
            except:
                logging.info('Something went wring wuth resursive!')
        else:
            return "Item not found"
        



    def get_details(self, url):
        try:
            uclient = uReq(url)
            mainpage = uclient.read()
            main_html = bs(mainpage ,"html.parser")
            main_script = main_html.find_all("script")
            main_text = (main_script[18]).text
            new_text = main_text[30:-1]
            json_data = json.loads(new_text)
            video = json_data['videoDetails']
            title = video['title']
            description = video['shortDescription']
            try:
                obj_db = Database()
                connection = obj_db.mysql_connect()
                cursor = connection.cursor()
                sql = "insert into details(title,description) values(%s, %s)"
                cursor.execute(sql, (title, description))
                connection.commit()
                last_setails_row_id  = cursor.lastrowid
                if last_setails_row_id:
                    main_list_of_all_comment = self.find_commend(main_script, last_setails_row_id)
                    response = {"title": title, "description": description, "commentLists": main_list_of_all_comment}
                    return response

            except:
                logging.info('Insert sql issue')
            
        except Exception as ex:
            print("First Request", ex)

