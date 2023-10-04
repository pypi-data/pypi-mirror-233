import weaviate
import json
import pandas as pd
import traceback
import datetime
from flask import request
import loggerutility as logger
import commonutility as common

class Weaviate:
    modelScope      =   "E"
    group_size      =    10000
    entity_type     =    ""
    def traindata(self,weaviate_jsondata):
        try:
            logger.log(f'\n Print Weaviate start time for traning : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            result  = ""
            df      = None
            columnnamelist = []
            schemaClasslist = []
            logger.log("inside Weaviate Hybrid class trainData()","0")
            logger.log(f"jsondata Weaviate Hybrid class trainData() ::: {weaviate_jsondata} ","0")
            if "openAI_apiKey" in weaviate_jsondata and weaviate_jsondata["openAI_apiKey"] != None:
                self.openAI_apiKey = weaviate_jsondata["openAI_apiKey"]           
                logger.log(f"\ntrain_Weaviate Hybrid openAI_apiKey:::\t{self.openAI_apiKey} \t{type(self.openAI_apiKey)}","0")
            
            if "modelParameter" in weaviate_jsondata and weaviate_jsondata["modelParameter"] != None:
                self.modelParameter = json.loads(weaviate_jsondata['modelParameter'])

            if "index_name" in self.modelParameter and (self.modelParameter["index_name"]).strip() != None:
                self.schema_name = (self.modelParameter["index_name"]).capitalize().replace("-","_").strip()
                logger.log(f"\ntrain_Weaviate Hybrid index_name:::\t{self.schema_name} \t{type(self.schema_name)}","0")

            if "entity_type" in self.modelParameter and (self.modelParameter["entity_type"]).strip() != None:
                self.entity_type = (self.modelParameter['entity_type']).lower().strip()
                logger.log(f'\n Tranin Weaviate vector entity_type veraible value :::  \t{self.entity_type} \t{type(self.entity_type)}')
            
            if "data_limit" in self.modelParameter and (self.modelParameter["data_limit"]).strip() != None and (self.modelParameter["data_limit"]).strip() != "":
                self.group_size = int(self.modelParameter['data_limit'])
                logger.log(f'\n Tranin Weaviate vector data_limit veraible value :::  \t{self.group_size} \t{type(self.group_size)}')

            if "modelScope" in weaviate_jsondata and weaviate_jsondata["modelScope"] != None:
                self.modelScope = weaviate_jsondata["modelScope"]
                logger.log(f"\ntrain_Weaviate class TrainData modelScope:::\t{self.modelScope} \t{type(self.modelScope)}","0")

            if "enterprise" in weaviate_jsondata and weaviate_jsondata["enterprise"] != None:
                self.enterpriseName = weaviate_jsondata["enterprise"]
                logger.log(f"\nWeaviate Hybrid class TrainData enterprise:::\t{self.enterpriseName} \t{type(self.enterpriseName)}","0")

            if "modelJsonData" in weaviate_jsondata and weaviate_jsondata["modelJsonData"] != None:
                self.dfJson = weaviate_jsondata["modelJsonData"]
                logger.log(f"\ntrain_Weaviate Hybrid dfJson:::\t{self.dfJson} \t{type(self.dfJson)}","0")
                if type(self.dfJson) == str :
                    parsed_json = json.loads(self.dfJson)

            if "server_url" in weaviate_jsondata and weaviate_jsondata["server_url"] != None:
                self.server_url = weaviate_jsondata["server_url"]
                logger.log(f"\nWeaviate Hybrid class TrainData server_url:::\t{self.server_url} \t{type(self.server_url)}","0")

            # Connection code with Weaviate
            client = weaviate.Client(self.server_url,additional_headers={"X-OpenAI-Api-Key": self.openAI_apiKey})

            logger.log(f'Connection is establish : {client.is_ready()}')

            if self.modelScope == "G" :
                self.enterpriseName = ""
                
            # Schema Class parameter

            class_obj = {
                    "class": self.schema_name,
                    "vectorizer": "text2vec-openai",
                    "moduleConfig": {
                        "text2vec-openai": {},
                        "generative-openai": {}
                                    }
                        }

            # if schema is present then process should not create new one need to update
            for s,i in enumerate(client.schema.get()["classes"]):
                schemaClasslist.append(client.schema.get()["classes"][s]['class'])

            if not self.schema_name in schemaClasslist:
                client.schema.create_class(class_obj) # Schema Class Creation

            if self.schema_name == 'Document':
                copydict = parsed_json.copy()
                parsed_json = {"id" : 'String', "description" : 'String'}
                parsed_json.update(copydict)

            columnnamelist=list(val for val in parsed_json[0])
            logger.log(f'\n Tranin Weaviate vector data_limit veraible value :::  \t{self.group_size} \t{type(self.group_size)}')
            num_groups = len(parsed_json[1:]) // self.group_size + (len(parsed_json[1:]) % self.group_size > 0)

            groups = []
            for i in range(num_groups):
                start_idx = i * self.group_size
                end_idx = (i + 1) * self.group_size if i < num_groups - 1 else len(parsed_json[1:])
                group_indices = list(range(start_idx, end_idx))
                groups.append(group_indices)

            logger.log(f'\n Print Weaviate Traning start time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")

            for val in groups:
                with client.batch.configure(batch_size=1000) as batch:
                    logger.log(f'\n Print Weaviate Group Traning start time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")    
                    for indexvalue in val:          #  for each element of the list
                        if not indexvalue == 0:
                            properties = {
                                "answer": parsed_json[indexvalue][columnnamelist[0]],
                                "description": parsed_json[indexvalue][columnnamelist[1]],
                                "organization": str(self.enterpriseName) +"_"+ str(self.entity_type),
                            }
                            if len(columnnamelist) > 2:
                                for j,valuedata in enumerate(columnnamelist[2:]):
                                    if valuedata not in parsed_json[indexvalue]:
                                        parsed_json[indexvalue][valuedata]=""
                                    else:
                                        properties[valuedata] = parsed_json[indexvalue][valuedata]
                            client.batch.add_data_object(
                                properties,
                                self.schema_name,
                            )
                    logger.log(f'\n Print Weaviate Group Traning END time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")    

            logger.log(f" {self.schema_name} Index Creation SUCCESSFUL for Enterprise: '{self.enterpriseName}'. ","0")
            result = f" {self.schema_name} Index Creation SUCCESSFUL for Enterprise: '{self.enterpriseName}'. "
            logger.log(f'\n Print Weaviate END time for traning : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            return result
        except Exception as e:
            logger.log(f" {self.schema_name} Index Creation FAILED for Enterprise: '{self.enterpriseName}'. ","0")
            logger.log(f"{self.schema_name} class trainData() Issue::: \n{e}","0")
            trace = traceback.format_exc()
            descr = str(e)
            errorXml = common.getErrorXml(descr, trace)
            logger.log(f'\n {self.schema_name} class trainData() errorXml::: \n{errorXml}', "0")
            return str(errorXml)
        
    def getLookupData(self):
        entity_type     =    ""
        try:
            logger.log(f'\n Print Weaviate start time for getLookupData : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            logger.log("inside Weaviate Hybrid class LookUpData()","0")
            finalResultJson={}
            id_list = []

            weaviate_json =  request.get_data('jsonData', None)
            weaviate_json = json.loads(weaviate_json[9:])
            logger.log(f"\nWeaviate hybrid class getLookupData() pineCone_json:::\t{weaviate_json} \t{type(weaviate_json)}","0")

            if "openAI_apiKey" in weaviate_json and weaviate_json["openAI_apiKey"] != None:
                self.openAI_apiKey = weaviate_json["openAI_apiKey"]          
                logger.log(f"\nWeaviate hybrid class LookUpData() openAI_apiKey:::\t{self.openAI_apiKey} \t{type(self.openAI_apiKey)}","0")              
            
            if "queryJson" in weaviate_json and weaviate_json["queryJson"] != None:
                queryJson = weaviate_json["queryJson"]
                logger.log(f"\nWeaviate hybrid class LookUpData() queryJson:::\t{queryJson} has length ::: '{len(queryJson)}'\t{type(queryJson)}","0")
            
            if "index_name" in weaviate_json and weaviate_json["index_name"] != None:
                self.schema_name = (weaviate_json["index_name"]).capitalize().replace("-","_")
                logger.log(f"\nWeaviate hybrid class LookUpData() schema_name:::\t{self.schema_name} \t{type(self.schema_name)}","0")

            if "enterprise" in weaviate_json and weaviate_json["enterprise"] != None:
                self.enterpriseName = weaviate_json["enterprise"]
                logger.log(f"\nWeaviate hybrid class LookUpData() enterprise:::\t{self.enterpriseName} \t{type(self.enterpriseName)}","0")

            if "server_url" in weaviate_json and weaviate_json["server_url"] != None:
                self.server_url = weaviate_json["server_url"]
                logger.log(f"\nWeaviate Hybrid class TrainData server_url:::\t{self.server_url} \t{type(self.server_url)}","0")

            if "entity_type" in weaviate_json and weaviate_json["entity_type"] != None:
                self.entity_type = (weaviate_json['entity_type']).lower()
                logger.log(f'\n Tranin Weaviate vector entity_type veraible value :::  \t{self.entity_type} \t{type(self.entity_type)}')

            if "modelScope" in weaviate_json and weaviate_json["modelScope"] != None:
                self.modelScope = weaviate_json["modelScope"]
                logger.log(f"\nWeaviate hybrid class LookUpData() modelScope:::\t{self.modelScope} \t{type(self.modelScope)}","0")

            if self.modelScope == "G":
                self.enterpriseName = ""

            # Connection code with weaviate 
            client = weaviate.Client(self.server_url,additional_headers={"X-OpenAI-Api-Key": self.openAI_apiKey})
            logger.log(f'Connection is establish : {client.is_ready()}')

            where_filter = {
                "path": ["organization"],
                "operator": "Equal",
                "valueText": str(self.enterpriseName) +"_"+ str(self.entity_type)
                            }
            
            if not self.schema_name == 'Document':
                for key in queryJson:
                    if len(queryJson[key]) > 0 and queryJson[key].strip() != "":
                        response = (
                                client.query
                                .get(self.schema_name, ["description", "answer", "organization"])
                                .with_where(where_filter)
                                .with_hybrid(
                                alpha=0.1,
                                query=queryJson[key]
                                )
                                .with_additional('score')
                                .with_limit(1)
                                .do()
                                )
                        if response != {}:
                            finalResultJson[key]= {"material_description": response['data']['Get'][self.schema_name][0]['description'], 
                                                                "id": response['data']['Get'][self.schema_name][0]['answer']} 
                
                logger.log(f"\n\nfinalResultJson:::{finalResultJson} has length ::: '{len(finalResultJson)}' \t {type(finalResultJson)}\n")
                finalResult = str(finalResultJson)
                
            elif self.schema_name == 'Document':
                for key in queryJson:
                    if len(queryJson[key]) > 0 and queryJson[key].strip() != "":
                        response = (
                                client.query
                                .get(self.schema_name, ["description", "answer", "organization"])
                                .with_where(where_filter)
                                .with_hybrid(
                                alpha=1,
                                query=queryJson[key]
                                )
                                .with_additional('score')
                                .do()
                                )
                        if response != {}:
                            for i in response['data']['Get']['Document']:
                                if i["_additional"]['score'] > '0.016':
                                    id_list.append(i['answer'])

                logger.log(f"\n\n id_list:::{id_list} has length :::'{len(id_list)}' \t {type(id_list)}\n")
                finalResult = str(id_list)
            
            logger.log(f'\n Print Weaviate END time for getLookupData : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            return finalResult
        except Exception as e:
            logger.log(f"Weaviate Hybrid class getLookUP() Issue::: \n{e}","0")
            trace = traceback.format_exc()
            descr = str(e)
            errorXml = common.getErrorXml(descr, trace)
            logger.log(f'\n Weaviate hybrid class getLookUP() errorXml::: \n{errorXml}', "0")
            return str(errorXml)



        
