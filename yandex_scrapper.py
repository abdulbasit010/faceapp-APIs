import requests
import json
import time
from base64 import b64decode
from PIL import Image
import time



def get_results_similar_v2(bs64):
    
    def main():
        try:
           
            file_path = bs64

            url = "https://yandex.com/images/search?rpt=imageview&format=json&request={\"blocks\":[{\"block\":\"b-page_type_search-by-image__link\"}]}"

            payload = {}
            files=[
            ('upfile',('T9KSFBR7S-U9PKJ0YMS-5ddd90bb0050-512.png',open(file_path,'rb'),'image/png'))
            ]
            headers = {
            'Cookie': '_yasc=9GHmz2poKskMg/a6Hg0mkkCosRfT7k3D0AjV41cBrhE71XvVn+E3NGaLzLqFgVvZFa+CdJ7qCsTHKKQtXA0=; bh=YMT+lsEGagOh/gE=; i=YvmDV4KW7jdGubZmv/GNGM+BXO5CiG85iNRY4K6nONr2WNC69xi7aqkTOjYhVWuy50DzFh/zMYi1C9HR9ND2+p2+BrE=; is_gdpr=0; is_gdpr_b=CO/qYRDEwAI=; receive-cookie-deprecation=1; yandexuid=8802835321747303079; yashr=1996210761747303079'
            }

            
            try:
                response = requests.request("POST", url, headers=headers, data=payload, files=files)

                cbirId = json.loads(response.content)['blocks'][0]['params']['cbirId']
            except:
                try:
                    time.sleep(3)
     
                    url = "https://yandex.com/images/search?rpt=imageview&format=json&request={\"blocks\":[{\"block\":\"b-page_type_search-by-image__link\"}]}"
                    response = requests.request("POST", url, headers=headers, data=payload, files=files)
                    print('ris_apis_except: '+ str(response.content))

                    cbirId = json.loads(response.content)['blocks'][0]['params']['cbirId']
                except Exception as ec:
                    print(f"Error exceptvris: {str(ec)}")
            


            url = "https://yandex.com/images/search?tmpl_version=releases%2Ffrontend%2Fimages%2Fv1.1539.0%23f740c203506b197d95092045cf09b252510ec08c&format=json&request=%7B%22blocks%22%3A%5B%7B%22block%22%3A%22extra-content%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%7B%22block%22%3A%22i-react-ajax-adapter%3Aajax%22%7D%2C%22params%22%3A%7B%22type%22%3A%22ImagesApp%22%2C%22ajaxKey%22%3A%22serpList%2FfetchByFilters%22%7D%2C%22version%22%3A2%7D%5D%7D&yu=4682095031737099617&cbir_id="+cbirId+"&cbir_page=similar&rpt=imageview&source-serpid=Qxxe5O0q2S64EhlKKWFPXA&uinfo=sw-1536-sh-864-ww-1536-wh-434-pd-1.25-wp-16x9_1920x1080&url=https%3A%2F%2Favatars.mds.yandex.net%2Fget-images-cbir%2F4570405%2FDCcrk-Zr95kshTD4kV0mgQ9231%2Forig"

            payload = {}
            headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9,ur;q=0.8,ca;q=0.7,ig;q=0.6,ro;q=0.5,la;q=0.4,he;q=0.3,ku;q=0.2,hr;q=0.1,sv;q=0.1,bn;q=0.1,kn;q=0.1,hu;q=0.1,el;q=0.1,uz;q=0.1,ms;q=0.1,be;q=0.1,ug;q=0.1,id;q=0.1,gu;q=0.1,hi;q=0.1,uk;q=0.1,ta;q=0.1,or;q=0.1,kk;q=0.1,mai;q=0.1,mr;q=0.1,te;q=0.1,az;q=0.1,pt;q=0.1,fr;q=0.1,no;q=0.1,es;q=0.1,da;q=0.1,cs;q=0.1,pl;q=0.1',
            'device-memory': '8',
            'downlink': '0.65',
            'dpr': '1.25',
            'ect': '4g',
            'priority': 'u=1, i',
            'referer': 'https://yandex.com/images/search?tmpl_version=releases%2Ffrontend%2Fimages%2Fv1.1539.0%23f740c203506b197d95092045cf09b252510ec08c&cbir_page=similar&crop=0.211%3B0.0032%3B0.7968%3B0.6365&rpt=imageview&url=https%3A%2F%2Favatars.mds.yandex.net%2Fget-images-cbir%2F4570405%2FDCcrk-Zr95kshTD4kV0mgQ9231%2Forig&cbir_id='+cbirId,
            'rtt': '250',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"135.0.7049.115"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="135.0.7049.115", "Not-A.Brand";v="8.0.0.0", "Chromium";v="135.0.7049.115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'viewport-width': '1536',
            'x-requested-with': 'XMLHttpRequest',
            'Cookie': 'is_gdpr=0; yandexuid=4682095031737099617; yashr=3676687731737099617; receive-cookie-deprecation=1; font_loaded=YSv1; is_gdpr_b=CM2BIhCZvwIoAg==; i=bgnR2c/Pws8LwcDxO2Ac7HB8hHsb4SqFq+68A6Dgpekr3PiWaPcseYd/j6fli1URDnyn790x7adRbNjpckAp7I2v6HQ=; bltsr=1; KIykI=1; yandex_gid=114013; my=YwA=; _yasc=G+PDsR+dd425CODC3RqW0LzYH+E86CTsSOUHwQVtRZ6uJKGtxbfjC3DrZPcTbK8PBWGVg6JP5mR2Q4YEN9Q=; yp=1762464321.szm.1_25:1536x864:1521x434#1749288315.ygu.1#1749374727.csc.1; bh=EkAiR29vZ2xlIENocm9tZSI7dj0iMTM1IiwgIk5vdC1BLkJyYW5kIjt2PSI4IiwgIkNocm9taXVtIjt2PSIxMzUiGgUieDg2IiIQIjEzNS4wLjcwNDkuMTE1IioCPzAyAiIiOgkiV2luZG93cyJCCCIxOS4wLjAiSgQiNjQiUlwiR29vZ2xlIENocm9tZSI7dj0iMTM1LjAuNzA0OS4xMTUiLCAiTm90LUEuQnJhbmQiO3Y9IjguMC4wLjAiLCAiQ2hyb21pdW0iO3Y9IjEzNS4wLjcwNDkuMTE1IloCPzBgoovywAZqHtzK4f8IktihsQOfz+HqA/v68OcN6//99g/E08+HCA==; _yasc=8AQ8raUP0utP13D/uvZCh94r+Lcltug5UXdEonmhmhfQmKwr3tK8+eZGCRZujyLoNOJ1VlHwa9A0MdTLaLDU8ENQ; bh=EkAiR29vZ2xlIENocm9tZSI7dj0iMTM1IiwgIk5vdC1BLkJyYW5kIjt2PSI4IiwgIkNocm9taXVtIjt2PSIxMzUiGgUieDg2IiIQIjEzNS4wLjcwNDkuMTE1IioCPzAyAiIiOgkiV2luZG93cyJCCCIxOS4wLjAiSgQiNjQiUlwiR29vZ2xlIENocm9tZSI7dj0iMTM1LjAuNzA0OS4xMTUiLCAiTm90LUEuQnJhbmQiO3Y9IjguMC4wLjAiLCAiQ2hyb21pdW0iO3Y9IjEzNS4wLjcwNDkuMTE1IloCPzBg16PywAZqHtzK4f8IktihsQOfz+HqA/v68OcN6//99g/E08+HCA==; i=4Ny5ZEfE1lBJd3PYQ4SSIj2T9NVDGX6PzTZ7Pw0iMf+KVld6XSvoWWGTjLvI/vTaYK1of0DrZl1BKBSk6EacNSs/TSE=; is_gdpr=0; is_gdpr_b=CM2BIhD4vgI=; receive-cookie-deprecation=1; spravka=dD0xNzE0MjIzNDUwO2k9MTAzLjE0OC4xMjguMjk7RD0yNTU1MzFGQ0NDOUNGODNCRjI0MzE0ODBBRTdFNTc1NTU2Rjg1QzMwOTZEOTc5NUNCQzY3MDQ3REQzNjE0OUUzQTJCMzU2OTgzRUIyMTZDODt1PTE3MTQyMjM0NTA5NDIzNTg4OTA7aD05ZTA4ZTY2NzM3MTExYmJiN2NlYjFkZjA4YzAxNDk5MA==; yandexuid=5101038581745759450; yashr=6908798791745759450'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
    
            out_json1= {}
            main_json= {}
            out_json1["similar"] = []
            out_json1["duplicates"] = []
            res = json.loads(response.text)
            reqq = res['blocks'][1]['params']['adapterData']['serpList']['items']['entities']
            for rr in reqq:
                image_url = 'https:'+reqq[rr]['image']
                url = reqq[rr]['snippet']['url']
                title = reqq[rr]['snippet']['title']
                duplis = reqq[rr]['viewerData']['dups']
                inn = {"imageUrl":image_url,'sourceUrl':url,"title":title}
                out_json1["similar"].append(inn)
                for dups in duplis:
                    dupimage_url = dups['url']
                    innDupli = {"imageUrl":dupimage_url,'sourceUrl':url,"title":title}
                    out_json1["duplicates"].append(innDupli)


            faces = 0 #detect_faces_from_Image(file_path)
            main_json['results'] = out_json1
            main_json['faces'] = faces
            return main_json
        except Exception as e:
            print(f"Error: {str(e)}")

    res = main()
    return res