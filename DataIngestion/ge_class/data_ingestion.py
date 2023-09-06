import boto3
from datetime import datetime, timedelta
from django.conf import settings
import json
import random
import time






class DataIngestion():
    def __init__(self):
        pass

    def Merge(self,dict1, dict2):
        res = {**dict1, **dict2}
        return res

    def generate_wind_data(self,wind_speed, wind_dir, turbines, turbine_status, plant_):
        try:
            # print(settings.BASE_DIR)
            json_file_with_app = 'DataIngestion/turbine_inverter_details.json'
            turbine_details = json.loads(open(settings.BASE_DIR.joinpath(json_file_with_app)).read())
            plant_turbines = turbine_details["wind"]
            # return 1
            wind_plant_maping = {
                "Plant-1": {"plant_name": "Plant-1", "plant_id": "GE-P-01", "oem": "GE", "Capacity": 70},
                "Plant-2": {"plant_name": "Plant-2", "plant_id": "RE-P-02", "oem": "REGEN", "Capacity": 25},
                "Plant-3": {"plant_name": "Plant-3", "plant_id": "GA-P-03", "oem": "GAMESA", "Capacity": 30},
                "Plant-4": {"plant_name": "Plant-4", "plant_id": "SZ-P-04", "oem": "SUZLON", "Capacity": 40}
            }
            wind_plants = [plant_]
            now_ = datetime.now()
            wind_bucket = "windcleanzone"
            s3_conn_resource = boto3.resource('s3', region_name='us-east-1', aws_access_key_id='AKIAYDAPTQILM5KDG2AO',
                                              aws_secret_access_key='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')
            now_plus_10 = now_
            curr_day = str(now_).split(" ")[0].split("-")
            for plant in wind_plants:
                plant_data = []
                for turbine in plant_turbines[plant]:

                    # for t in range(1, 11):
                    # print(plant, curr_day[2])
                    avg_wind_speed={"1":0, "2":0, "3":9.7,  "4":3.7, "5":77.8, "6":141.4,"7":234.7,"8":348,"9":498.1,"10":656.4,"11":781.2,"12":799.2,
                                    "13":813,"14":822,"15":818.4,"16":823.6,"17":824.7,"18":824.7,"19":824.7,"20":824.7}

                    five_percent_in_wind_speed = (avg_wind_speed[wind_speed]/100)*5

                    active_power = avg_wind_speed[wind_speed] + random.randint(0,int(five_percent_in_wind_speed))
                    # print(avg_wind_speed[wind_speed], five_percent_in_wind_speed)
                    # print(active_power)

                    if turbine_status == 0 or turbine_status == "0":
                        turbine_status_ = 1
                    else:
                        turbine_status_ = 0

                    if turbine in turbines:
                        turbine_status_ = turbine_status

                    if turbine_status_ == 0 or turbine_status_=="0":
                        active_power = 0.0

                    tag_list = {
                        "turbine_status":int(turbine_status_),
                        "turbine":turbine,
                        "P_ACT": float(active_power),
                        "WIND_SPEED": float(wind_speed),
                        "V_WIN": float(wind_dir),
                        "DATA_TIME": now_plus_10.isoformat()
                    }
                    r = self.Merge(wind_plant_maping[plant], tag_list)
                    # print(r,plant,"data ingetion")
                    plant_data.append(r)
                    # ingesting in to s3

                print(plant_data)
                s3_path = str(plant) + "/" + curr_day[0] + "/" + curr_day[1] + "/" + curr_day[2] + "/" + str(time.time()) + ".json"
                s3_conn_resource.Object(wind_bucket, s3_path).put(Body=json.dumps(plant_data))
                time.sleep(0.50)
            return True
        except Exception as e:
            print(e)
            return False



    def generate_solar_data(self,poa, ghi, inverters, inverter_status, plant):
        try:
            json_file_with_app = 'DataIngestion/turbine_inverter_details.json'
            turbine_details = json.loads(open(settings.BASE_DIR.joinpath(json_file_with_app)).read())
            plant_inverters = turbine_details["solar"]

            solar_plant_maping =  {
                "Plant-1": {"plant_name": "Plant-1", "plant_id": "P-01","Capacity": 70},
                "Plant-2": {"plant_name": "Plant-2", "plant_id": "P-02","Capacity": 25},
                "Plant-3": {"plant_name": "Plant-3", "plant_id": "P-03","Capacity": 30},
                "Plant-4": {"plant_name": "Plant-4", "plant_id": "P-04","Capacity": 40}
            }
            solar_plants = [plant]
            now_ = datetime.now()
            solar_bucket = "resolarcleanzone"
            s3_conn_resource = boto3.resource('s3', region_name='us-east-1', aws_access_key_id='AKIAYDAPTQILM5KDG2AO',
                                              aws_secret_access_key='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')
            now_plus_10 = now_
            curr_day = str(now_).split(" ")[0].split("-")
            for plant in solar_plants:
                plant_data = []
                for inverter in plant_inverters[plant]:

                    # for t in range(1, 11):
                    # print(plant, curr_day[2])
                    avg_wind_speed = {"1": 0, "2": 0, "3": 9.7, "4": 3.7, "5": 77.8, "6": 141.4, "7": 234.7, "8": 348,
                                      "9": 498.1, "10": 656.4, "11": 781.2, "12": 799.2,
                                      "13": 813, "14": 822, "15": 818.4, "16": 823.6, "17": 824.7, "18": 824.7,
                                      "19": 824.7, "20": 824.7}



                    active_power = 0.5 * 1.225 * random.randint(350,450) * int(poa)
                    # print(avg_wind_speed[wind_speed], five_percent_in_wind_speed)
                    # print(active_power)

                    if inverter_status == 0 or inverter_status == "0":
                        inverter_status_ = 1
                    else:
                        inverter_status_ = 0

                    if inverter in inverters:
                        inverter_status_ = inverter_status

                    if inverter_status_ == 0 or inverter_status_ == "0":
                        active_power = 0.0

                    tag_list = {
                        "inverter_status": int(inverter_status_),
                        "inverter": inverter,
                        "active_power": float(active_power),
                        "POA": float(poa),
                        "GHI": float(ghi),
                        "DATA_TIME": now_plus_10.isoformat()
                    }
                    r = self.Merge(solar_plant_maping[plant], tag_list)
                    # print(r,plant,"data ingetion")
                    plant_data.append(r)
                    # ingesting in to s3

                print(plant_data)
                s3_path = str(plant) + "/" + curr_day[0] + "/" + curr_day[1] + "/" + curr_day[2] + "/" + str(
                    time.time()) + ".json"
                s3_conn_resource.Object(solar_bucket, s3_path).put(Body=json.dumps(plant_data))
                time.sleep(0.50)
            return True
        except Exception as e:
            return False

