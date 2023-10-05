import json
import os
import time
import math
from OSMPythonTools.nominatim import Nominatim
import requests
import argparse

def dvf1312(commune,codeinsee):
    def append(features,list,count):
        list.append(features)
        count+=1
    def notappend(features,list,count):
        pass
    dict_={1:append,0:notappend}
    nominatim = Nominatim()
    "python automation to query dvf+ etalab public api and calculate surface prices"
    boundingbox = nominatim.query(f'{commune}')._json[0]["boundingbox"]
    minlat0 = float(boundingbox[0])
    maxlat0 = float(boundingbox[1])
    minlon0 = float(boundingbox[2])
    maxlon0 = float(boundingbox[3])

    url0 = "https://apidf-preprod.cerema.fr/dvf_opendata/geomutations/?"
    latrange=math.ceil((maxlat0-minlat0)/0.02)
    lonrange=math.ceil((maxlon0-minlon0)/0.02)
    count=0
    featuresbati=[]
    featuresnonbati=[]
    baticount=0
    nonbaticount=0
    for i in range(0,int(latrange)):
        for j in range(0,int(lonrange)):
            count+=1
            minlat=minlat0+i*0.02
            maxlat=minlat+0.02
            minlon=minlon0+j*0.02
            maxlon=minlon+0.02
            print(f'downloading {count}/{int(latrange)*int(lonrange)}')
            url =url0+ f"anneemut_max=2023&anneemut_min=2010&code_insee={codeinsee}&in_bbox={minlon}%2C{minlat}%2C{maxlon}%2C{maxlat}&page_size=200"
            r=requests.get(url,timeout=10).json()
            for k in r["features"]:
                try:
                    k["properties"]["valeurfonc"]=float(k["properties"]["valeurfonc"])
                except:
                    k["properties"]["valeurfonc"]=0
                try:
                    k["properties"]["sterr"]=float(k["properties"]["sterr"])
                except:
                    k["properties"]["sterr"]=0
                try:
                    k["properties"]["sbati"]=float(k["properties"]["sbati"])
                except Exception as err:
                    print(err)
                    k["properties"]["sbati"]=0
                try:
                    k["properties"]["sbati€/m2"]=int(k["properties"]["valeurfonc"]/k["properties"]["sbati"])
                except:
                    k["properties"]["sbati€/m2"]=0
                try:
                    k["properties"]["sterr€/m2"]=int(k["properties"]["valeurfonc"]/k["properties"]["sterr"])
                except:
                    k["properties"]["sterr€/m2"]=0
                try:
                    k["properties"]["sterr€/ha"]=int(10000*k["properties"]["valeurfonc"]/k["properties"]["sterr"])
                except:
                    k["properties"]["sterr€/ha"]=0
                dict_[bool(k["properties"]["sbati"]>0)](k,featuresbati,baticount)
                dict_[bool(k["properties"]["sbati"]==0)](k,featuresnonbati,nonbaticount)
            bati_json=r.copy()
            bati_json["features"]=featuresbati
            bati_json["count"]=baticount
            nonbati_json=r.copy()
            nonbati_json["features"]=featuresnonbati
            nonbati_json["count"]=nonbaticount
            bati_json_object = json.dumps(bati_json, indent=4)
            nonbati_json_object = json.dumps(nonbati_json, indent=4)
            with open(f'{codeinsee}-bati-{commune}-{count}-{int(latrange*lonrange)}','w') as fileo:
                fileo.write(bati_json_object)
            with open(f'{codeinsee}-nonbati-{commune}-{count}-{int(latrange*lonrange)}','w') as fileo:
                fileo.write(nonbati_json_object)
            if count>1:
                os.remove(f'{codeinsee}-bati-{commune}-{count-1}-{int(latrange*lonrange)}')
                os.remove(f'{codeinsee}-nonbati-{commune}-{count-1}-{int(latrange*lonrange)}')
            if count==int(latrange*lonrange):
                os.rename(f'{codeinsee}-bati-{commune}-{count}-{int(latrange*lonrange)}',f'{codeinsee}-bati-{commune[6:]}')
                os.rename(f'{codeinsee}-nonbati-{commune}-{count}-{int(latrange * lonrange)}',
                          f'{codeinsee}-nonbati-{commune}')
            time.sleep(4)
            result=(bati_json,nonbati_json)
    return result
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    python dvf132.py -f commune_name
    """)
    parser.add_argument('-f',
                        '--commune',
                        required=True,
                        metavar='commune',
                        type=str,
                        help='commune to process')
    parser.add_argument('-p',
                        '--postcode',
                        required=True,
                        metavar='commune',
                        type=str,
                        help='commune to process')
    arguments = vars(parser.parse_args())
    dvf1312(arguments['commune'],arguments['postcode'])
