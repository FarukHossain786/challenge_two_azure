# imports
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
import logging
logging.basicConfig(filename='log/app.log', filemode='w',level=logging.INFO)

class Totalvideos():
    def __init__(self):
        self.count = 0


    def count_fun(self, video_render, count):
        if not isinstance(video_render, list):
            return count
        
        
        for i in video_render:
            if 'richItemRenderer' in i.keys():
                count = count + 1
            elif 'continuationItemRenderer' in i.keys():
                try:
                    # Getting key for load more video
                    url = 'https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false'
                    first_key = i['continuationItemRenderer']['continuationEndpoint']['clickTrackingParams']
                    second_key = i['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
                    header = {"context":{"client":{"hl":"en","gl":"IN","remoteHost":"202.160.145.70","deviceMake":"","deviceModel":"","visitorData":"CgtuWjhiNHd6LTRzNCik_cefBg%3D%3D","userAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20230217.01.00","osName":"X11","osVersion":"","originalUrl":"https://www.youtube.com/@krishnaik06/videos","platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{"appInstallData":"CKT9x58GEOWg_hIQ5_euBRDa6a4FEJT4rgUQ-6P-EhCJ6K4FELjUrgUQuIuuBRC2nP4SEKLsrgUQh92uBRDM9a4FEMzfrgUQgt2uBRCO8a4FEOLUrgUQ-sWuBRDnwq4FEJH4_BI%3D"},"timeZone":"Asia/Calcutta","browserName":"Chrome","browserVersion":"110.0.0.0","acceptHeader":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","deviceExperimentId":"ChxOekU1T0RRME1UYzVOemMxTVRReU5qYzBOdz09EKT9x58GGK2BmJ8G","screenWidthPoints":702,"screenHeightPoints":636,"screenPixelDensity":1,"screenDensityFloat":1,"utcOffsetMinutes":330,"userInterfaceTheme":"USER_INTERFACE_THEME_LIGHT","connectionType":"CONN_CELLULAR_4G","memoryTotalKbytes":"8000000","mainAppWebInfo":{"graftUrl":"https://www.youtube.com/@krishnaik06/videos","pwaInstallabilityStatus":"PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":"false"}},"user":{"lockedSafetyMode":"false"},"request":{"useSsl":"true","internalExperimentFlags":[],"consistencyTokenJars":[]},"clickTracking":{"clickTrackingParams":first_key},"adSignalsInfo":{"params":[{"key":"dt","value":"1676803749623"},{"key":"flash","value":"0"},{"key":"frm","value":"0"},{"key":"u_tz","value":"330"},{"key":"u_his","value":"10"},{"key":"u_h","value":"768"},{"key":"u_w","value":"1360"},{"key":"u_ah","value":"741"},{"key":"u_aw","value":"1360"},{"key":"u_cd","value":"24"},{"key":"bc","value":"31"},{"key":"bih","value":"636"},{"key":"biw","value":"687"},{"key":"brdim","value":"0,27,0,27,1360,27,1366,741,702,636"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}]}},"continuation":second_key}
                    # POST Request
                    response_data = requests.post(url, json = header)
                    json_data = json.loads(response_data.text)
                    video_render = json_data['onResponseReceivedActions'][0]['appendContinuationItemsAction']['continuationItems']
                    return self.count_fun(video_render, count)
                except:
                    logging.info('Regursion connection issue')
            else:
                break
                
        return count


        
    def videos(self):
        # url = "https://www.youtube.com/@CollegeWallahbyPW/videos"
        # url = "https://www.youtube.com/@krishnaik06/videos"
        # url = "https://www.youtube.com/@iNeuroniNtelligence/videos"

        urls = ['https://www.youtube.com/@CollegeWallahbyPW/videos', 'https://www.youtube.com/@krishnaik06/videos', 'https://www.youtube.com/@iNeuroniNtelligence/videos']
        try:
            total_count ={}
            for url in urls:
                uclient = uReq(url)
                mainpage = uclient.read()
                main_html = bs(mainpage ,"html.parser")
                main_script = main_html.find_all("script")
                main_text =  (main_script[33]).text
                new_text = main_text[20:-1]
                json_data = json.loads(new_text)
                video_render = json_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['richGridRenderer']['contents']
                response = self.count_fun(video_render, self.count)
                total_count[url] = response

        except:
            logging.info('First Request problem')


        return total_count