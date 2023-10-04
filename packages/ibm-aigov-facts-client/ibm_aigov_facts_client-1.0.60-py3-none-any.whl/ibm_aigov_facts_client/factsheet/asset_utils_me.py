import logging
import os
import json
import collections
import ibm_aigov_facts_client._wrappers.requests as requests

from typing import BinaryIO, Dict, List, TextIO, Union,Any
from ibm_aigov_facts_client.factsheet import assets 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator,CloudPakForDataAuthenticator
from ibm_aigov_facts_client.utils.enums import AssetContainerSpaceMap, AssetContainerSpaceMapExternal,ContainerType, FactsType, RenderingHints,ModelEntryContainerType, AllowedDefinitionType,FormatType
from ibm_aigov_facts_client.utils.utils import validate_enum,validate_type
from ibm_aigov_facts_client.utils.cell_facts import CellFactsMagic

from ibm_aigov_facts_client.utils.config import *
from ibm_aigov_facts_client.utils.client_errors import *
from ibm_aigov_facts_client.utils.constants import *

from ibm_aigov_facts_client.factsheet.approaches import ApproachUtilities
from ibm_aigov_facts_client.factsheet.html_parser import FactHTMLParser

_logger = logging.getLogger(__name__) 


class ModelUsecaseUtilities:

    """
        Model use case utilities. Running `client.assets.model_usecase()` makes all methods in ModelUsecaseUtilities object available to use.
    
    """
   
    def __init__(self,assets_client:'assets.Assets',model_id:str=None, model_usecase_id: str=None, container_type: str=None, container_id: str=None,facts_type: str=None) -> None:

        """
        Initialize a ModelUsecaseUtilities object.
        
        """

        self._asset_id = model_usecase_id
        self._container_type=container_type
        self._container_id=container_id
        self._facts_type=facts_type

        self._assets_client=assets_client

        self._facts_client=assets_client._facts_client
        self._is_cp4d=assets_client._is_cp4d
        self._external_model=assets_client._external_model
        
        if self._is_cp4d:
            self._cpd_configs=assets_client._cpd_configs
            self._cp4d_version=assets_client._cp4d_version

        self._facts_definitions=self._get_fact_definitions()

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ModelUsecaseUtilities':
        """Initialize a ModelUsecaseUtilities object from a json dictionary."""
        args = {}
        if '_asset_id' in _dict:
            args['asset_id'] = _dict.get('_asset_id')
       
        if '_container_type' in _dict:
            args['container_type'] = _dict.get('_container_type') #[convert_model(x) for x in metrics]
        else:
            raise ValueError('Required property \'container_type\' not present in AssetProps JSON')
        
        if '_container_id' in _dict:
            args['container_id'] = _dict.get('_container_id') #[convert_model(x) for x in metrics]
        else:
            raise ValueError('Required property \'container_id\' not present in AssetProps JSON')
        
        if '_facts_type' in _dict:
            args['facts_type'] = _dict.get('_facts_type') #[convert_model(x) for x in metrics]
        else:
            raise ValueError('Required property \'facts_type\' not present in AssetProps JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        return cls.from_dict(_dict)


    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, '_asset_id') and self._asset_id is not None:
            _dict['model_usecase_id'] = self._asset_id
        if hasattr(self, '_container_type') and self._container_type is not None:
            _dict['container_type'] = self._container_type
        if hasattr(self, '_container_id') and self._container_id is not None:
            _dict['catalog_id'] = self._container_id
        if hasattr(self, '_facts_type') and self._facts_type is not None:
            _dict['facts_type'] = self._facts_type
        
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()
    
    def __str__(self) -> str:
        """Return a `str` version of this ModelUsecaseUtilities object."""
        return json.dumps(self.to_dict(), indent=2)

    def __repr__(self):
        """Return a `repr` version of this ModelUsecaseUtilities object."""
        return json.dumps(self.to_dict(), indent=2)

    def _get_fact_definitions(self)->Dict:

        """
            Get all facts definitions

            :rtype: dict

            A way you might use me is:

            >>> model_usecase.get_fact_definitions()

        """

        if(self._facts_type != None):
            if self._is_cp4d:
                url = self._cpd_configs["url"] + \
                        "/v2/asset_types/" + self._facts_type + "?" + self._container_type + "_id=" + self._container_id
            else:
                if get_env() == 'dev':
                    url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                        "/v2/asset_types/" + self._facts_type + "?" + self._container_type + "_id=" + self._container_id
                elif get_env() == 'test':
                    url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                        "/v2/asset_types/" + self._facts_type + "?" + self._container_type + "_id=" + self._container_id
                else:
                    url = prod_config["DEFAULT_SERVICE_URL"] + \
                        "/v2/asset_types/" + self._facts_type + "?" + self._container_type + "_id=" + self._container_id

            response = requests.get(url, headers=self._get_headers())
            if not response.ok:
                raise ClientError("User facts definitions not found. ERROR {}. {}".format(response.status_code,response.text))
            else:
                return response.json()

    def get_info(self,verbose=False)-> Dict:
        """Get model use case details

        :param verbose: If True, returns additional model details. Defaults to False
        :type verbose: bool, optional
        :rtype: dict

        The way to use me is:
        
        >>> get_model_usecase.get_info()
        >>> get_model_usecase.get_info(verbose=True)

        """
        if verbose:
            url=self._get_assets_url(self._asset_id,self._container_type,self._container_id)
            response = requests.get(url, headers=self._get_headers())
            if response.status_code==200:
                cur_metadata=self._to_dict()
                additional_data={}

                model_name=response.json()["metadata"].get("name")
                asset_type=response.json()["metadata"].get("asset_type")
                desc=response.json()["metadata"].get("description")
                if self._is_cp4d:
                    url=MODEL_USECASE_PATH.format(self._cpd_configs["url"],self._container_id,self._asset_id)
                else:
                    url=MODEL_USECASE_PATH.format(CLOUD_URL,self._container_id,self._asset_id)

                additional_data["name"]=model_name
                if desc:
                    additional_data["description"]=desc
                additional_data["asset_type"]=asset_type
                additional_data["url"]=url
                additional_data.update(cur_metadata)
                return additional_data
            else:
                raise ClientError("Failed to get additional model use case information. ERROR {}. {}".format(response.status_code,response.text))
        else:
            return self._to_dict()
    
    
    def get_tracked_models(self)->list:
        """
        Get models tracked in model use case

        :return: physical model details for all models in model use case
        :rtype: list[dict]
        """
        get_assets_url=self._get_assets_url(self._asset_id,self._container_type,self._container_id)
        assets_data=requests.get(get_assets_url, headers=self._get_headers())
        if assets_data:
            get_facts_global=assets_data.json()['entity'].get('modelfacts_global')
            get_models=get_facts_global.get('physical_models')
            return get_models
        else:
            raise ClientError("Failed to get tracked models. ERROR {}. {}".format(assets_data.status_code,assets_data.text))


    def set_custom_fact(self, fact_id: str, value: Any)->None:

        """
            Set custom fact by given id.

            :param str fact_id: Custom fact id.
            :param any value: Value of custom fact. It can be string, integer, date. if custom fact definition attribute `is_array` is set to `True`, value can be a string or list of strings.

            A way you might use me is:

            >>> model_usecase.set_custom_fact(fact_id="custom_int",value=50)
            >>> model_usecase.set_custom_fact(fact_id="custom_string",value="test")
            >>> model_usecase.set_custom_fact(fact_id="custom_string",value=["test","test2"]) # allowed if attribute property `is_array` is true.

        """
        
        if not value or value=='':
            raise ClientError("Value can not be empty")
        
        url=self._get_url_by_factstype_container()

        attr_is_array=self._get_fact_definition_properties(fact_id).get("is_array")
        value_type_array=(type(value) is not str and isinstance(value, collections.abc.Sequence))
        
        if isinstance(value, list) and any(isinstance(x, dict) for x in value ):
            raise ClientError("Value should be a list of Strings but found Dict")

        self._type_check_by_id(fact_id,value)
        
        path= "/" + fact_id
        op = ADD

     
        if (attr_is_array and value_type_array) or value_type_array:
            body = [
                {
                    "op": op, 
                    "path": path,
                    "value": "[]"
                }
            ]
            response = requests.patch(url, data=json.dumps(body), headers=self._get_headers())
            
            if not response.status_code==200:
                raise ClientError("Patching array type values failed. ERROR {}. {}".format(response.status_code,response.text))
            
            op=REPLACE

        body = [
                {
                    "op": op, 
                    "path": path,
                    "value": value
                }
            ]

        
        response = requests.patch(url, data=json.dumps(body), headers=self._get_headers())
        
        if response.status_code==200:
            _logger.info("Custom fact {} successfully set to new value {}".format(fact_id,value))

        elif response.status_code==404:
            url=self._get_assets_attributes_url()

            body =  {
                        "name": self._facts_type,
                        "entity": {fact_id: value}
                        }

            response = requests.post(url,data=json.dumps(body), headers=self._get_headers())
            
            if response.status_code==201:
                _logger.info("Custom fact {} successfully set to new value {}".format(fact_id,value))
            else:
                _logger.error("Something went wrong. ERROR {}.{}".format(response.status_code,response.text))
        else:
            raise ClientError("Failed to add custom fact {}. ERROR: {}. {}".format(fact_id,response.status_code,response.text))
    
    def set_custom_facts(self, facts_dict: Dict[str, Any])->None:

        
        """
            Set multiple custom facts.

            :param dict facts_dict: Multiple custom facts. Example: {id: value, id1: value1, ...}

            A way you might use me is:

            >>> model_usecase.set_custom_facts({"fact_1": 2, "fact_2": "test", "fact_3":["data1","data2"]})

        """
        
        url=self._get_url_by_factstype_container()

        body=[]

        for key, val in facts_dict.items() : 
            
            attr_is_array=self._get_fact_definition_properties(key).get("is_array")
            value_type_array=(type(val) is not str and isinstance(val, collections.abc.Sequence))
            
            self._type_check_by_id(key,val)

            path= "/" + key
            op = ADD

            
            if (attr_is_array and value_type_array) or value_type_array:
                
                tmp_body = {
                        "op": op, 
                        "path": path,
                        "value": "[]"
                    }
                
                body.append(tmp_body)
                op=REPLACE

            v = {
                "op": op, #"replace",
                "path": path,
                "value": val
            }

            body.append(v)

       
        response = requests.patch(url, data=json.dumps(body), headers=self._get_headers())
        if response.status_code==200:
                _logger.info("Custom facts {} successfully set to values {}".format(list(facts_dict.keys()),list(facts_dict.values())))
        
        
        elif response.status_code==404:

            url=self._get_assets_attributes_url()

            body =  {
                        "name": self._facts_type,
                        "entity": facts_dict
                        }

            response = requests.post(url,data=json.dumps(body), headers=self._get_headers())
            if response.status_code==201:
                 _logger.info("Custom facts {} successfully set to values {}".format(list(facts_dict.keys()),list(facts_dict.values())))
            else:
                _logger.error("Something went wrong. ERROR {}.{}".format(response.status_code,response.text))

        else:
            raise ClientError("Failed to add custom facts. ERROR: {}-{}".format(response.status_code,response.text))
    
    
    def get_custom_fact_by_id(self, fact_id: str):

        """
            Get custom fact value/s by id

            :param str fact_id: Custom fact id to retrieve.

            A way you might use me is:

            >>> model_usecase.get_custom_fact_by_id(fact_id="fact_id")

        """

        url=self._get_url_by_factstype_container()
        
        response = requests.get(url, headers=self._get_headers())

        if response.status_code==200:
            fact_details = response.json().get(self._facts_type)
            id_val=fact_details.get(fact_id)
            if not id_val:
                raise ClientError("Could not find value of fact_id {}".format(fact_id))
            else:
                return id_val

    def get_custom_facts(self)->Dict:

        """
            Get all defined custom facts for model_entry_user fact type.

            :rtype: dict

            A way you might use me is:

            >>> model_usecase.get_custom_facts()

        """
        
        url=self._get_url_by_factstype_container()
        
        response = requests.get(url, headers=self._get_headers())

        if response.status_code==200:
            user_facts = response.json().get(self._facts_type)
            return user_facts
        else:
            raise ClientError("Failed to get facts. ERROR. {}. {}".format(response.status_code,response.text))


    
    def get_all_facts(self)->Dict:

        """
            Get all facts related to asset.
            
            :rtype: dict

            A way you might use me is:

            >>> model_usecase.get_all_facts()

        """
        
        url=self._get_assets_url(self._asset_id,self._container_type,self._container_id)
        response = requests.get(url, headers=self._get_headers())
        if response.status_code==200:
             return response.json() 
        else:
            raise ClientError("Failed to get facts. ERROR. {}. {}".format(response.status_code,response.text))


    def get_facts_by_type(self,facts_type:str=None)-> Dict:
        
        """
            Get custom facts by asset type.

            :param str facts_type: (Optional) Custom facts asset type.
            :rtype: dict

            A way you might use me is:

            >>> model_usecase.get_facts_by_type(facts_type=<type name>)
            >>> model_usecase.get_facts_by_type() # default to model_entry_user type

        """

        if not facts_type:
            facts_type=self._facts_type
        
        get_all_first=self.get_all_facts()
        all_resources=get_all_first.get("entity")
        if all_resources and all_resources.get(facts_type)!=None:
            return all_resources.get(facts_type)
        else:
            raise ClientError("Could not find custom facts for type {}".format(facts_type)) 


    def remove_custom_fact(self, fact_id: str)->None:

        """
            Remove custom fact by id

            :param str fact_id: Custom fact id value/s to remove.

            A way you might use me is:

            >>> model_usecase.remove_custom_fact(fact_id=<fact_id>)

        """
        
        url=self._get_url_by_factstype_container()
        
        response = requests.get(url, headers=self._get_headers())

        if response.status_code==200:
            fact_details = response.json().get(self._facts_type)
            check_val_exists_for_id=fact_details.get(fact_id)
        if not check_val_exists_for_id:
            raise ClientError("Fact id {} is invalid or have no associated value to remove".format(fact_id))

        url=self._get_url_by_factstype_container()

        body = [
            {
                "op": "remove",  # "replace",
                "path": "/" + fact_id,
            }
        ]

        response = requests.patch(url, data=json.dumps(body), headers=self._get_headers())
        if response.status_code==200:
            _logger.info(" Value of Fact id {} removed successfully".format(fact_id))
        else:
            raise ClientError("Could not delete the fact_id {}. ERROR. {}. {}".format(fact_id,response.status_code,response.text))
            

    def remove_custom_facts(self, fact_ids:List[str])->None:

        """
            Remove multiple custom facts ids

            :param list fact_ids: Custom fact ids to remove.

            A way you might use me is:

            >>> model_usecase.remove_custom_facts(fact_ids=["id1","id2"])

        """
        
        url=self._get_url_by_factstype_container()
        
        response = requests.get(url, headers=self._get_headers())

        if response.status_code==200:
            fact_details = response.json().get(self._facts_type)
        
        final_list=[]
        for fact_id in fact_ids:
            check_val_exists=fact_details.get(fact_id)
            if check_val_exists:
                final_list.append(fact_id)
            else:
                _logger.info("Escaping fact_id {} as either it is invalid or have no value to remove".format(fact_id))
        
        body=[]
        
        if final_list:
            for val in final_list : 
                val = {
                    "op": "remove", #"replace",
                    "path": "/" + val
                }
                body.append(val)
            
            response = requests.patch(url, data=json.dumps(body), headers=self._get_headers())
            if response.status_code==200:
                _logger.info("Values of Fact ids {} removed successfully".format(final_list))
            else:
                raise ClientError("Could not delete the fact_ids. ERROR. {}. {}".format(response.status_code,response.text))
        else:
            raise ClientError("Please use valid id with values to remove")
        
    
    def set_attachment_fact(self, 
                        file_to_upload,
                        description:str,
                        fact_id:str,
                        html_rendering_hint:str=None
                        )->None:
    
        """
            Set attachment fact for given model use case. Supported for CPD version >=4.6.5
            
            :param str file_to_upload: Attachment file path to upload
            :param str description: Description about the attachment file
            :param str fact_id: Fact id for the attachment
            :param str html_rendering_hint: (Optional) html rendering hint. Available options are in :func:`~ibm_aigov_facts_client.utils.enums.RenderingHints`

            A way to use me is:

            >>> model_usecase.set_attachment_fact(file_to_upload="./artifacts/image.png",description=<file description>,fact_id=<custom fact id>)
            >>> model_usecase.set_attachment_fact(file_to_upload="./artifacts/image.png",description=<file description>,fact_id=<custom fact id>,html_rendering_hint=<render hint>)

        """
        
        if self._is_cp4d and self._cp4d_version < "4.6.5":
            raise ClientError("Version mismatch: Attachment functionality is only supported in CP4D version 4.6.5 or higher. Current version of CP4D is "+self._cp4d_version)

        model_asset_id=self._asset_id
        model_container_type= self._container_type
        model_container_id= self._container_id

        if os.path.exists(file_to_upload):
            file_size=os.stat(file_to_upload).st_size
            #<500MB
            if file_size>MAX_SIZE:
                raise ClientError("Maximum file size allowed is 500 MB")
        else:
            raise ClientError("Invalid file path provided")

        if html_rendering_hint:
            validate_enum(html_rendering_hint,"html_rendering_hint", RenderingHints, False)

        # check if have attachment for given fact id. only one attachment allowed per fact_id.
        get_factid_attachment=self.list_attachments(filter_by_factid=fact_id)

        if get_factid_attachment:
            raise ClientError("Fact id {} already have an attachment set and only allowed to have one. You can remove and set new attachment if needed".format(fact_id))
        
        else:
            #create attachment

            mimetype=self._get_mime(file_to_upload)

            attachment_url=self._get_url_attachments(model_asset_id,model_container_type,model_container_id)

            base_filename = os.path.basename(file_to_upload)

            if html_rendering_hint==RenderingHints.INLINE_HTML:
                htmlparser = FactHTMLParser()
                html_file = open(file_to_upload, 'r')
                html_content = html_file.read()
                htmlparser.feed(html_content)
                htmlparser.close()
                restricted_tags = "style istyle css"
                # checking if any of the above restricted_tags values in html tags
                contains_restricted_tag = any(item in restricted_tags for item in htmlparser.start_tags)
                if contains_restricted_tag:
                    raise ClientError("Invalid inline HTML content: Attachments content to be rendered as inline_html is NOT allowed to contain any of the following HTML tags: {}".format(list(restricted_tags.split(" "))))

            # convert png to jpeg
            flag=False
            if mimetype=="image/png":
                from PIL import Image

                ima=Image.open(file_to_upload)
                rgb_im = ima.convert('RGB')
                rgb_im.save(os.path.splitext(file_to_upload)[0]+".jpg", format='JPEG')
                mimetype="image/jpg"
                base_filename=os.path.splitext(file_to_upload)[0]+".jpg"
                file_to_upload=base_filename
                flag=True

            
            attachment_data = {}

            if fact_id: 
                attachment_data["fact_id"] = fact_id
            if html_rendering_hint: 
                attachment_data["html_rendering_hint"] = html_rendering_hint

            body = "{ \"asset_type\": \""+self._facts_type+"\" \
                    , \"name\": \"" + base_filename + "\",\"mime\": \"" + mimetype \
                    + "\",\"data_partitions\" : 0,\"private_url\": \"false\",\"is_partitioned\": \"false\",\"description\": \"" \
                    + description + "\",\"user_data\": " + json.dumps(attachment_data) + "}"
            

            create_attachment_response = requests.post(attachment_url, data=body, headers=self._get_headers())

            if create_attachment_response.status_code==400:
                url=self._get_assets_attributes_url()

                body =  {
                            "name": self._facts_type,
                            "entity": {}
                            }

                response = requests.post(url,data=json.dumps(body), headers=self._get_headers())
            
                if response.status_code==201:
                   create_attachment_response = requests.post(attachment_url, data=body, headers=self._get_headers())
                else:
                    raise ClientError("Failed to initiate {} attribute. ERROR {}. {}".format(self._facts_type,response.status_code,response.text))
            
            if create_attachment_response.status_code==201:
                get_upload_uri=create_attachment_response.json().get("url1")
                if not get_upload_uri:
                    raise ClientError("Upload url not found")
            else:
                raise ClientError("Failed to create attachment URL. ERROR {}. {}".format(create_attachment_response.status_code,create_attachment_response.text))

            if self._is_cp4d:
                get_upload_uri = self._cpd_configs["url"] + get_upload_uri
            
            attachment_id=create_attachment_response.json()["attachment_id"]

            # upload file

            if self._is_cp4d:
                files= {'file': (file_to_upload, open(file_to_upload, 'rb').read(),mimetype)}
                response_update = requests.put(get_upload_uri, files=files)

            else:
                # headers=self._get_headers()
                with open(file_to_upload, 'rb') as f:
                    data=f.read()
                    response_update=requests.put(get_upload_uri,data=data)

            if response_update.status_code==201 or response_update.status_code==200:

                #complete attachment
                completion_url=self._get_url_attachments(model_asset_id,model_container_type,model_container_id,attachment_id,action="complete")
                completion_response=requests.post(completion_url,headers=self._get_headers())
                

                if completion_response.status_code==200:
                    
                    #get attachment info
                    get_attachmentUrl=self._get_url_attachments(model_asset_id,model_container_type,model_container_id,attachment_id,mimetype,action="get")
                    
                    if (mimetype.startswith("image/") or mimetype.startswith("application/pdf")
                            or mimetype.startswith("text/html")):
                        get_attachmentUrl += '&response-content-disposition=inline;filename=' + file_to_upload

                    else: 
                        get_attachmentUrl += '&response-content-disposition=attachment;filename=' + file_to_upload

                    response_get=requests.get(get_attachmentUrl,headers=self._get_headers())

                    if response_get.status_code==200:
                        if self._is_cp4d:
                            url= self._cpd_configs["url"] + response_get.json().get("url")
                            _logger.info("Attachment uploaded successfully and access url (15min valid) is - {}".format(url))
                        else:
                            _logger.info("Attachment uploaded successfully and access url (15min valid) is - {}".format(response_get.json().get("url")))
                        if flag:
                            os.remove(file_to_upload)
                    else:
                        raise ClientError("Could not fetch attachment url. ERROR {}. {}".format(response_get.status_code,response_get.text))  

                else:
                    raise ClientError("Failed to mark attachment as complete. ERROR {}. {} ".format(completion_response.status_code,completion_response.text))

            else:
                raise ClientError("Failed to upload file using URI {}. ERROR {}. {}".format(get_upload_uri ,response_update.status_code,response_update.text))


    def set_cell_attachment_fact(self, 
                        description:str,
                        fact_id:str
                        )->None:
    
        """
            Set attachment fact using captured cell output. Supported for CPD version >=4.6.5.
            
            :param str description: Description about the cell facts attachment file
            :param str fact_id: Fact id for the attachment

            A way to use me is:

            >>> model_usecase.set_cell_attachment_fact(description=<file description>,fact_id=<custom fact id>)

        """
        
        if self._is_cp4d and self._cp4d_version < "4.6.5":
            raise ClientError("Version mismatch: Attachment functionality is only supported in CP4D version 4.6.5 or higher. Current version of CP4D is "+self._cp4d_version)

        model_asset_id=self._asset_id
        model_container_type= self._container_type
        model_container_id= self._container_id

        file_to_upload="{}/{}/{}".format(os.getcwd(),CELL_FACTS_TMP_DIR,CellFactsMagic._fname)
        
        if not os.path.exists(file_to_upload):
            raise ClientError("Invalid file path. Failed to find {}".format(CellFactsMagic._fname))

        # check if have attachment for given fact id. only one attachment allowed per fact_id.
        get_factid_attachment=self.list_attachments(filter_by_factid=fact_id)

        if get_factid_attachment:
            raise ClientError("Fact id {} already have an attachment set and only allowed to have one. You can remove and set new attachment if needed".format(fact_id))
        
        else:
            #create attachment

            mimetype=self._get_mime(file_to_upload)

            attachment_url=self._get_url_attachments(model_asset_id,model_container_type,model_container_id)

            base_filename = os.path.basename(file_to_upload)

            
            attachment_data = {}

            if fact_id: 
                attachment_data["fact_id"] = fact_id
            attachment_data["html_rendering_hint"] = "inline_html"

            body = "{ \"asset_type\": \""+self._facts_type+"\" \
                    , \"name\": \"" + base_filename + "\",\"mime\": \"" + mimetype \
                    + "\",\"data_partitions\" : 0,\"private_url\": \"false\",\"is_partitioned\": \"false\",\"description\": \"" \
                    + description + "\",\"user_data\": " + json.dumps(attachment_data) + "}"
            

            create_attachment_response = requests.post(attachment_url, data=body, headers=self._get_headers())

            if create_attachment_response.status_code==400:
                url=self._get_assets_attributes_url()

                body =  {
                            "name": self._facts_type,
                            "entity": {}
                            }

                response = requests.post(url,data=json.dumps(body), headers=self._get_headers())
            
                if response.status_code==201:
                   create_attachment_response = requests.post(attachment_url, data=body, headers=self._get_headers())
                else:
                    raise ClientError("Failed to initiate {} attribute. ERROR {}. {}".format(self._facts_type,response.status_code,response.text))
            
            if create_attachment_response.status_code==201:
                get_upload_uri=create_attachment_response.json().get("url1")
                if not get_upload_uri:
                    raise ClientError("Upload url not found")
            else:
                raise ClientError("Failed to create attachment URL. ERROR {}. {}".format(create_attachment_response.status_code,create_attachment_response.text))

            if self._is_cp4d:
                get_upload_uri = self._cpd_configs["url"] + get_upload_uri
            
            attachment_id=create_attachment_response.json()["attachment_id"]

            # upload file

            if self._is_cp4d:
                files= {'file': (file_to_upload, open(file_to_upload, 'rb').read(),mimetype)}
                response_update = requests.put(get_upload_uri, files=files)

            else:
                # headers=self._get_headers()
                with open(file_to_upload, 'rb') as f:
                    data=f.read()
                    response_update=requests.put(get_upload_uri,data=data)

            if response_update.status_code==201 or response_update.status_code==200:

                #complete attachment
                completion_url=self._get_url_attachments(model_asset_id,model_container_type,model_container_id,attachment_id,action="complete")
                completion_response=requests.post(completion_url,headers=self._get_headers())
                

                if completion_response.status_code==200:
                    
                    #get attachment info
                    get_attachmentUrl=self._get_url_attachments(model_asset_id,model_container_type,model_container_id,attachment_id,mimetype,action="get")
                    
                    get_attachmentUrl += '&response-content-disposition=inline;filename=' + file_to_upload

                    response_get=requests.get(get_attachmentUrl,headers=self._get_headers())

                    if response_get.status_code==200:
                        if self._is_cp4d:
                            url= self._cpd_configs["url"] + response_get.json().get("url")
                            _logger.info("Cell facts attachment uploaded successfully and access url (15min valid) is - {}".format(url))
                        else:
                            _logger.info("Cell facts attachment uploaded successfully and access url (15min valid) is - {}".format(response_get.json().get("url")))
                        
                        os.remove(file_to_upload)
                    else:
                        raise ClientError("Could not fetch attachment url. ERROR {}. {}".format(response_get.status_code,response_get.text))  

                else:
                    raise ClientError("Failed to mark attachment as complete. ERROR {}. {} ".format(completion_response.status_code,completion_response.text))

            else:
                raise ClientError("Failed to upload file using URI {}. ERROR {}. {}".format(get_upload_uri ,response_update.status_code,response_update.text))
            
    def has_attachment(self,fact_id:str=None)-> bool:
        """ Check if attachment/s exist. Supported for CPD version >=4.6.5

        :param fact_id: Id of attachment fact 
        :type fact_id: str, optional

        :rtype: bool

        The way to use me is :

        >>> model_usecase.has_attachment()
        >>> model_usecase.has_attachment(fact_id=<fact id>)

        """

        if self._is_cp4d and self._cp4d_version < "4.6.5":
            raise ClientError("Version mismatch: Attachment functionality is only supported in CP4D version 4.6.5 or higher. Current version of CP4D is "+self._cp4d_version)

        url=self._get_assets_url(self._asset_id,self._container_type,self._container_id)
        response=requests.get(url,headers=self._get_headers())
        all_attachments=response.json().get(ATTACHMENT_TAG)
        if all_attachments:
            attachments=[ i for i in all_attachments if i.get('asset_type')==self._facts_type and (fact_id==None or fact_id==i.get("user_data").get("fact_id"))]
            if attachments:
                return True
            else:
                return False
    
    
    def list_attachments(self,filter_by_factid:str=None, format:str=FormatType.DICT):

        """
            List available attachments facts. Supported for CPD version >=4.6.5
            
            :param str filter_by_factid: (Optional) Fact id for the attachment to filter by
            :param str format: Result output format (dict or str). Default to dict.

            A way to use me is:


            >>> model_usecase.list_attachments(format="str") # use this format if using output for `set_custom_fact()`
            >>> model_usecase.list_attachments() # get all attachment facts
            >>> model_usecase.list_attachments(filter_by_factid=<"fact_id_1">) # filter by associated fact_id_1

        """

        if self._is_cp4d and self._cp4d_version < "4.6.5":
            raise ClientError("Version mismatch: Attachment functionality is only supported in CP4D version 4.6.5 or higher. Current version of CP4D is "+self._cp4d_version)

        model_asset_id=self._asset_id
        model_container_type=self._container_type
        model_container_id= self._container_id

        url=self._get_assets_url(model_asset_id,model_container_type,model_container_id)

       
        response=requests.get(url,headers=self._get_headers())
        all_attachments=response.json().get(ATTACHMENT_TAG)
        results=[]
        if all_attachments:
            attachments=[ i for i in all_attachments if i.get('asset_type')==self._facts_type and (filter_by_factid==None or filter_by_factid==i.get("user_data").get("fact_id"))]

            for a in attachments:
                if format==FormatType.STR:
                    get_url=self._get_attachment_download_url(model_asset_id, model_container_type, model_container_id, a.get("id"), a.get("mime"), a.get("name"))
                    if self._is_cp4d and get_url:
                        get_url=self._cpd_configs["url"] + get_url
                    output_fmt = "{} - {} {}".format(a.get("name"),a.get("mime"),get_url) 
                    results.append(output_fmt)

                else:
                    attachment_dict={}
                    attachment_dict["attachment_id"]=a.get("id")
                    attachment_dict["description"]=a.get("description")
                    attachment_dict["name"]=a.get("name")
                    attachment_dict["mime"]=a.get("mime")
                    if a.get("user_data"):
                        if a.get("user_data").get("fact_id"):
                            attachment_dict["fact_id"]=a.get("user_data").get("fact_id")
                        if a.get("user_data").get("html_rendering_hint"):
                            attachment_dict["html_rendering_hint"]=a.get("user_data").get("html_rendering_hint")
                    
                    get_url=self._get_attachment_download_url(model_asset_id, model_container_type, model_container_id, a.get("id"), a.get("mime"), a.get("name"))
                    if self._is_cp4d and get_url:
                        get_url=self._cpd_configs["url"] + get_url
                    attachment_dict["url"]=get_url
                    results.append(attachment_dict)
            return results
        
        else:
            return results

        

    def remove_attachment(self,fact_id:str):

        """
            Remove available attachments facts for given id. Supported for CPD version >=4.6.5
            
            :param str fact_id:  Fact id of the attachment

            A way to use me is:

            >>> model_usecase.remove_attachment(fact_id=<fact id of attachment>)


        """

        if self._is_cp4d and self._cp4d_version < "4.6.5":
            raise ClientError("Version mismatch: Attachment functionality is only supported in CP4D version 4.6.5 or higher. Current version of CP4D is "+self._cp4d_version)

        model_asset_id=self._asset_id
        model_container_type=self._container_type
        model_container_id= self._container_id

        get_attachment=self.list_attachments(filter_by_factid=fact_id)
        
        if get_attachment:
            get_id=get_attachment[0].get("attachment_id")
            del_url=self._get_url_attachments(model_asset_id,model_container_type,model_container_id,get_id,action="del")
            response=requests.delete(del_url,headers=self._get_headers())
            if response.status_code==204:
                _logger.info("Deleted attachment for fact id: {} successfully".format(fact_id))
            else:
                _logger.error("Failed to delete attachment for fact id: {}. ERROR {}. {}".format(fact_id,response.status_code,response.text))
        else:
            raise ClientError("No valid attachment found related to fact id {}".format(fact_id))


    def remove_all_attachments(self): 

        """
            Remove all attachments facts for given asset. Supported for CPD version >=4.6.5


            A way to use me is:

            >>> model_usecase.remove_all_attachments()


        """
    
        if self._is_cp4d and self._cp4d_version < "4.6.5":
            raise ClientError("Version mismatch: Attachment functionality is only supported in CP4D version 4.6.5 or higher. Current version of CP4D is "+self._cp4d_version)

        model_asset_id=self._asset_id
        model_container_type=self._container_type
        model_container_id=self._container_id
        
        url=self._get_assets_url(model_asset_id,model_container_type,model_container_id)

        get_assets=requests.get(url,headers=self._get_headers())
        all_attachments=get_assets.json().get(ATTACHMENT_TAG)
        if all_attachments == None:
            raise ClientError("No attachments available to remove")
        filtered_attachment_ids=[ i.get('id') for i in all_attachments if i.get(ASSET_TYPE_TAG)==self._facts_type]
        if not filtered_attachment_ids:
            raise ClientError("No attachments available to remove")
        else:
            for id in filtered_attachment_ids:
                del_url=self._get_url_attachments(model_asset_id,model_container_type,model_container_id,id,action="del")
                response=requests.delete(del_url,headers=self._get_headers())
                if response.status_code==204:
                    _logger.info("Deleted attachment id {} successfully".format(id))
                else:
                    _logger.error("Could not delete attachment id {}. ERROR {}. {}".format(id,response.status_code,response.text))
            _logger.info("All attachments deleted successfully")
    
    #====================================utils==========================================
    def _get_headers(self):
        token =  self._facts_client._authenticator.token_manager.get_token() if  ( isinstance(self._facts_client._authenticator, IAMAuthenticator) or (isinstance(self._facts_client._authenticator, CloudPakForDataAuthenticator))) else self._facts_client._authenticator.bearer_token
        iam_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % token
        }
        return iam_headers 

    def _check_if_op_enabled(self):
        url=self._cpd_configs["url"] + "/v1/aigov/model_inventory/grc/config"
        response = requests.get(url,
                    headers=self._get_headers()
                    )
        return response.json().get("grc_integration")
    
    def _get_assets_url(self,asset_id:str=None,container_type:str=None,container_id:str=None):

        if self._is_cp4d:
            url = self._cpd_configs["url"] + \
                '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
        return url

    
    
    def _get_fact_definition_properties(self,fact_id):
        
        if self._facts_definitions:
            props=self._facts_definitions.get(PROPERTIES)
            props_by_id=props.get(fact_id)
        else:
            data=self._get_fact_definitions()
            props=data.get(PROPERTIES)
            props_by_id=props.get(fact_id)

        if not props_by_id:
            raise ClientError("Could not find properties for fact id {} ".format(fact_id))

        return props_by_id

    
    def _type_check_by_id(self,id,val):
        cur_type=self._get_fact_definition_properties(id).get("type")
        is_arr=self._get_fact_definition_properties(id).get("is_array")

        if cur_type=="integer" and not isinstance(val, int):
            raise ClientError("Invalid value used for type of Integer")
        elif cur_type=="string" and not isinstance(val, str) and not is_arr:
            raise ClientError("Invalid value used for type of String")
        elif (cur_type=="string" and is_arr) and (not isinstance(val, str) and not isinstance(val, list)) :
            raise ClientError("Invalid value used for type of String. Value should be either a string or list of strings")

    def _trigger_container_move(self,asset_id:str,container_type:str=None,container_id:str=None):
        
        asset_id=asset_id or self._asset_id
        container_type= container_type or self._container_type
        container_id= container_id or self._container_id

        try:
            get_assets_url=self._get_assets_url(asset_id,container_type,container_id)
            assets_data=requests.get(get_assets_url, headers=self._get_headers())
            get_desc=assets_data.json()["metadata"].get("description")
            get_name=assets_data.json()["metadata"].get("name")
        except:
            raise ClientError("Asset details not found for asset id {}".format(asset_id))

        if get_desc:
            body= [
                {
                    "op": "add",
                    "path": "/metadata/description",
                    "value": get_desc +' '
                }
                ]
        else:
            body= [
                {
                    "op": "add",
                    "path": "/metadata/description",
                    "value": get_name
                }
                ]
        response = requests.patch(get_assets_url,data=json.dumps(body), headers=self._get_headers())
        
        if response.status_code ==200:
           _logger.info("Asset container updated successfully")
        else:
            raise ClientError("Could not update asset container. ERROR {}. {}".format(response.status_code,response.text))


    
    def _get_mime(self,file):
        # pip install python-magic
        # On a Mac you may also have to run a "brew install libmagic"
        import magic
        mime = magic.Magic(mime=True)
        magic_mimetype_result = mime.from_file(file) 
        # sometimes we need to post-correct where the magic result is just not
        if file.endswith(".csv") and not magic_mimetype_result.endswith("/csv"): 
            return "text/csv"
        if file.endswith(".html") and not magic_mimetype_result.endswith("/html"): 
            return "text/html"
        return magic_mimetype_result
    
    
    def _get_assets_attributes_url(self):

            if self._is_cp4d:
                url = self._cpd_configs["url"] + \
                    '/v2/assets/' + self._asset_id + "/attributes?" + self._container_type + "_id=" + self._container_id
            else:
                if get_env() == 'dev':
                    url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                        '/v2/assets/' + self._asset_id + "/attributes?" + self._container_type + "_id=" + self._container_id
                elif get_env() == 'test':
                    url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                        '/v2/assets/' + self._asset_id + "/attributes?" + self._container_type + "_id=" + self._container_id
                else:
                    url = prod_config["DEFAULT_SERVICE_URL"] + \
                        '/v2/assets/'+ self._asset_id + "/attributes?" + self._container_type + "_id=" + self._container_id

            return url

    def _get_url_by_factstype_container(self):
        
        if self._is_cp4d:
           
           url = self._cpd_configs["url"] + \
                '/v2/assets/' + self._asset_id + "/attributes/" + \
            self._facts_type + "?" + self._container_type + "_id=" + self._container_id
        
        else:

            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                    '/v2/assets/' + self._asset_id + "/attributes/" + \
                self._facts_type + "?" + self._container_type + "_id=" + self._container_id
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    '/v2/assets/' + self._asset_id + "/attributes/" + \
                self._facts_type + "?" + self._container_type + "_id=" + self._container_id
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v2/assets/'+ self._asset_id + "/attributes/" + \
                self._facts_type + "?" + self._container_type + "_id=" + self._container_id
        
        return url

    def _get_url_sysfacts_container(self,asset_id:str=None, container_type:str=None, container_id: str=None,key:str=FactsType.MODEL_FACTS_SYSTEM):

        asset_id=asset_id or self._asset_id
        container_type=container_type or self._container_type
        container_id=container_id or self._container_id
        
        if self._is_cp4d:
                url = self._cpd_configs["url"] + \
                    '/v2/assets/' + asset_id + "/attributes/" + \
                key + "?" + container_type + "_id=" + container_id

        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + "/attributes/" + \
                key + "?" + container_type + "_id=" + container_id
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + "/attributes/" + \
                key + "?" + container_type + "_id=" + container_id
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v2/assets/'+ asset_id + "/attributes/" + \
                key + "?" + container_type + "_id=" + container_id
        
        return url
    
    def _get_url_space(self,space_id:str):
        
        if self._is_cp4d:
                url = self._cpd_configs["url"] + \
                    '/v2/spaces/' + space_id 
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                    '/v2/spaces/' + space_id 
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    '/v2/spaces/' + space_id 
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v2/spaces/' + space_id 
        return url

    def _get_url_attachments(self,asset_id:str,container_type:str, container_id:str,attachment_id:str=None,mimetype:str=None,action:str=None):

        if action=="del":
            if self._is_cp4d:
                    url = self._cpd_configs["url"] + \
                        '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '?'+ container_type + '_id=' + container_id
            else:
                if get_env() == 'dev':
                    url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                        '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '?'+ container_type + '_id=' + container_id 
                elif get_env() == 'test':
                    url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                        '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '?'+ container_type + '_id=' + container_id 
                else:
                    url = prod_config["DEFAULT_SERVICE_URL"] + \
                        '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '?'+ container_type + '_id=' + container_id 


        elif attachment_id and mimetype and action=="get":
            if self._is_cp4d:
                    url = self._cpd_configs["url"] + \
                        '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '?'+ container_type + '_id=' + container_id + '&response-content-type=' + mimetype
            else:
                if get_env() == 'dev':
                    url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                        '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '?'+ container_type + '_id=' + container_id + '&response-content-type=' + mimetype
                elif get_env() == 'test':
                    url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                        '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '?'+ container_type + '_id=' + container_id + '&response-content-type=' + mimetype
                else:
                    url = prod_config["DEFAULT_SERVICE_URL"] + \
                        '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '?'+ container_type + '_id=' + container_id + '&response-content-type=' + mimetype

        
        elif attachment_id and action=="complete":
            if self._is_cp4d:
                    url = self._cpd_configs["url"] + \
                        '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '/complete?'+ container_type + '_id=' + container_id
            else:
                if get_env() == 'dev':
                    url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                        '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '/complete?'+ container_type + '_id=' + container_id
                elif get_env() == 'test':
                    url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                         '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '/complete?'+ container_type + '_id=' + container_id
                else:
                    url = prod_config["DEFAULT_SERVICE_URL"] + \
                         '/v2/assets/' + asset_id + '/attachments/' + attachment_id + '/complete?'+ container_type + '_id=' + container_id
        
        else:
            if self._is_cp4d:
                    url = self._cpd_configs["url"] + \
                        '/v2/assets/' + asset_id + '/attachments?'+ container_type + '_id=' + container_id 
            else:
                if get_env() == 'dev':
                    url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                        '/v2/assets/' + asset_id + '/attachments?'+ container_type + '_id=' + container_id
                elif get_env() == 'test':
                    url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                        '/v2/assets/' + asset_id + '/attachments?'+ container_type + '_id=' + container_id
                else:
                    url = prod_config["DEFAULT_SERVICE_URL"] + \
                        '/v2/assets/' + asset_id + '/attachments?'+ container_type + '_id=' + container_id
        return url

    def _get_assets_url(self,asset_id:str=None,container_type:str=None,container_id:str=None):
       

        asset_id=asset_id or self._asset_id
        container_type=container_type or self._container_type
        container_id= container_id or self._container_id

        if self._is_cp4d:
            url = self._cpd_configs["url"] + \
                '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
        return url

    def _get_attachment_download_url(self, asset_id, container_type, container_id, attachment_id, mimetype, filename):
        
        url = self._get_url_attachments(asset_id,container_type,container_id,attachment_id,mimetype,action="get")
        if mimetype.startswith("image/") or mimetype.startswith("application/pdf") or mimetype.startswith("text/html") :
            url += "&response-content-disposition=inline;filename=" + filename

        else :
            url += "&response-content-disposition=attachment;filename=" + filename

        response=requests.get(url, headers=self._get_headers())
        download_url = response.json().get("url")
        return download_url


    ########   Commenting below 2 methods based on this defect  https://github.ibm.com/wdp-gov/tracker/issues/126147

    # def modify_approach_or_version_of_model(self,approach_id:str=None,version_number:str=None,target_approach_id:str=None,target_version_number:str=None,target_version_comment:str=None):

    #     """
    #         Returns WKC Model usecase updated approach. Supported for CPD version >=4.7.0
            
    #         :param str approach_id: Name of approach
    #         :param str version_number: Version number of the model
    #         :param str target_approach_id: Target approach ID
    #         :param str target_version_number: Target version number
    #         :param str target_version_comment: Target version comment

    #         :rtype: None

    #         :return: WKC Model usecase approache is modified
            
    #         Example:
    #         >>> client.assets.model_usecase.modify_approach_or_version_of_model(approach_id=<approach_id>,version_number=<version_number>,target_approach_id=<target_approach_id>,target_version_number=<target_version_number>,target_version_comment=<target_version_comment>)
    #     """

    #     if self._is_cp4d and self._cp4d_version < "4.7.0":
    #         raise ClientError("Version mismatch: Model usecase, modify approach or version of model functionality is only supported in CP4D version 4.7.0 or higher. Current version of CP4D is "+self._cp4d_version)

    #     if (approach_id is None or approach_id == ""):
    #         raise MissingValue("approach_id", "approach ID is missing")
    #     if (version_number is None or version_number == ""):
    #         raise MissingValue("version_number", "version number is missing")
    #     if (target_approach_id is None or target_approach_id == ""):
    #         raise MissingValue("target_approach_id", "target approach ID is missing")
    #     if (target_version_number is None or target_version_number == ""):
    #         raise MissingValue("target_version_number", "target version number is missing")

    #     model_asset_id=self._asset_id
    #     model_container_id= self._container_id

    #     if target_approach_id:
    #         body= {
    #                 "target_approach_id": target_approach_id,
    #                 "target_version_number": target_version_number,
    #                 "target_version_comment": target_version_comment
    #             }
    #     else:
    #         raise ClientError("Provide target approach ID")
       
    #     url=self._get_approach_url(model_asset_id,model_container_id,approach_id,version_number,operation="put")

    #     response = requests.put(url,data=json.dumps(body), headers=self._get_headers())
        
    #     if response.status_code ==200:
    #         _logger.info("Approach or version of model updated successfully")
    #         return response
    #     else:
    #         raise ClientError("Failed while updating an approach or version of model. ERROR {}. {}".format(response.status_code,response.text))
    


    # def update_approach(self,approach_id:str=None,new_approach_name:str=None,new_approach_description:str=None):

    #     """
    #         Returns WKC Model usecase updated approach. Supported for CPD version >=4.7.0
            
    #         :param str approach_id: Name of approach
    #         :param str new_approach_name: New name for approach
    #         :param str new_approach_description: New description for approach
            
    #         :rtype: None

    #         :return: WKC Model usecase approache is updated
            
    #         Example:
    #         >>> client.assets.model_usecase.remove_approach(approach_id=<approach_id>,new_approach_name=<new_approach_name>,new_approach_description=<new_approach_description>)
    #     """

    #     if self._is_cp4d and self._cp4d_version < "4.7.0":
    #         raise ClientError("Version mismatch: Model usecase, update approach functionality is only supported in CP4D version 4.7.0 or higher. Current version of CP4D is "+self._cp4d_version)

    #     if (approach_id is None or approach_id == ""):
    #         raise MissingValue("approach_id", "approach ID is missing")
    #     if (new_approach_name is None or new_approach_name == ""):
    #         raise MissingValue("new_approach_name", "New approach name is missing")
    #     if (new_approach_description is None or new_approach_description == ""):
    #         raise MissingValue("new_approach_description", "New approach description is missing")

    #     model_asset_id=self._asset_id
    #     model_container_id= self._container_id

    #     if new_approach_name:
    #         body= [
    #             {
    #                 "op": "add",
    #                 "path": "/name",
    #                 "value": new_approach_name
    #             },
    #             {
    #                 "op": "add",
    #                 "path": "/description",
    #                 "value": new_approach_description
    #             }
    #             ]
    #     else:
    #         raise ClientError("Provide approach name")

    #     url=self._get_approach_url(model_asset_id,model_container_id,approach_id,operation="patch")

    #     response = requests.patch(url,data=json.dumps(body), headers=self._get_headers())
        
    #     if response.status_code ==200:
    #         _logger.info("Approach updated successfully")
    #         return response.json()
    #     else:
    #         raise ClientError("Failed while updating an approach. ERROR {}. {}".format(response.status_code,response.text))
    

    def remove_approach(self,approach:ApproachUtilities=None):

        """
            Returns WKC Model usecase removed approache. Supported for CPD version >=4.7.0
            
            :param ApproachUtilities approach: Object or instance of ApproachUtilities
            
            :rtype: None

            :return: WKC Model usecase approache is removed
            
            Example:
            >>> client.assets.model_usecase.remove_approach(approach=ApproachUtilities)
        """

        if self._is_cp4d and self._cp4d_version < "4.7.0":
            raise ClientError("Version mismatch: Model usecase, remove approach functionality is only supported in CP4D version 4.7.0 or higher. Current version of CP4D is "+self._cp4d_version)


        if (approach is None or approach == ""):
            raise MissingValue("approach", "ApproachUtilities object or instance is missing")
        
        if ( not isinstance(approach, ApproachUtilities)):
            raise ClientError("Provide ApproachUtilities object for approach")

        approach_id = approach.get_id()
        if (approach_id == "00000000-0000-0000-0000-000000000000"):
            _logger.info("Can't delete default approach ")
        else:
            model_asset_id=self._asset_id
            model_container_id= self._container_id

            url=self._get_approach_url(model_asset_id,model_container_id,approach_id,operation="delete")

        
            response=requests.delete(url,headers=self._get_headers())

            if response.status_code ==204:
                _logger.info("Approach removed successfully")
            else:
                raise ClientError("Failed in removing an approache. ERROR {}. {}".format(response.status_code,response.text))


    def create_approach(self,name:str=None,description:str=None)->ApproachUtilities:

        """
            Returns WKC Model usecase approache. Supported for CPD version >=4.7.0
            
            :param str name: Name of approach
            :param str description: (Optional) Description of approach
            :rtype: ApproachUtilities

            :return: WKC Model usecase approache
            
            Example:
            >>> client.assets.model_usecase.create_approach(name=<approach name>,description=<approach description>)
            >>> client.assets.model_usecase.create_approach(name=<approach name>)

        """

        if self._is_cp4d and self._cp4d_version < "4.7.0":
            raise ClientError("Version mismatch: Model usecase, create approach functionality is only supported in CP4D version 4.7.0 or higher. Current version of CP4D is "+self._cp4d_version)

        model_asset_id=self._asset_id
        model_container_type= self._container_type
        model_container_id= self._container_id

        if (name is None or name == ""):
            raise MissingValue("name", "approach name is missing")
        
        if name:
            body={
                    "name": name,
                    "description": description,
                    "icon": "Packages",
                    "icon_color": "Gray"
                }
        else:
            raise ClientError("Provide approach name")

        url=self._get_approach_url(model_asset_id,model_container_id,operation="post")
        response = requests.post(url,data=json.dumps(body), headers=self._get_headers())
        
        if response.status_code ==200:
            _logger.info("Approach created successfully")
            ret_create_approach = response.json()
            return ApproachUtilities(self,approach_id=ret_create_approach.get('id'),approach_name=ret_create_approach.get('name'),approach_desc=ret_create_approach.get('description'),approach_icon=ret_create_approach.get('icon'),approach_icon_color=ret_create_approach.get('icon_color'),model_asset_id=model_asset_id,model_container_type=model_container_type,model_container_id=model_container_id)
            #return response.json()
        else:
            raise ClientError("Failed while creating an approach. ERROR {}. {}".format(response.status_code,response.text))


    def get_approaches(self)->list:

        """
            Returns list of WKC Model usecase approaches. Supported for CPD version >=4.7.0
            
            :return: All WKC Model usecase approaches
            :rtype: list(ApproachUtilities)

            Example:
            >>> client.assets.model_usecase.get_approaches()

        """

        if self._is_cp4d and self._cp4d_version < "4.7.0":
            raise ClientError("Version mismatch: Model usecase, retrieve approaches functionality is only supported in CP4D version 4.7.0 or higher. Current version of CP4D is "+self._cp4d_version)

        model_asset_id=self._asset_id
        model_container_type= self._container_type
        model_container_id= self._container_id

        url=self._get_approach_url(model_asset_id,model_container_id,operation="get")
        response=requests.get(url,headers=self._get_headers())

        if response.status_code ==200:
            _logger.info("Approaches retrieved successfully")
            approaches_list = response.json()["approaches"]
            approach_list_values = []
            for approach in approaches_list:
                approach_list_values.append(ApproachUtilities(self,approach_id=approach.get('id'),approach_name=approach.get('name'),approach_desc=approach.get('description'),approach_icon=approach.get('icon'),approach_icon_color=approach.get('icon_color'),versions=approach.get('versions'),model_asset_id=model_asset_id,model_container_type=model_container_type,model_container_id=model_container_id))
            return approach_list_values
        else:
            raise ClientError("Failed in retrieving an approache. ERROR {}. {}".format(response.status_code,response.text))

    def get_approach(self,approach_id:str=None)->ApproachUtilities:

        """
            Returns WKC Model usecase approaches. Supported for CPD version >=4.7.0
            
            :param str approach_id: Approach ID

            :rtype: ApproachUtilities

            :return:  Specific WKC Model usecase approache
            

            Example:
            >>> client.assets.model_usecase.get_approach(approach_id=<approach_id>)

        """

        if self._is_cp4d and self._cp4d_version < "4.7.0":
            raise ClientError("Version mismatch: Model usecase, retrieve approach functionality is only supported in CP4D version 4.7.0 or higher. Current version of CP4D is "+self._cp4d_version)

        if (approach_id is None or approach_id == ""):
            raise MissingValue("approach_id", "approach ID is missing")

        model_asset_id=self._asset_id
        model_container_type= self._container_type
        model_container_id= self._container_id

        url=self._get_approach_url(model_asset_id,model_container_id,operation="get")
        response=requests.get(url,headers=self._get_headers())

        if response.status_code ==200:
            approaches_list = response.json()["approaches"]
            _is_approach_exists = False
            for approach in approaches_list:
                if approach.get('id') == approach_id:
                    _is_approach_exists = True
                    _logger.info("Approach retrieved successfully")
                    return ApproachUtilities(self,approach_id=approach.get('id'),approach_name=approach.get('name'),approach_desc=approach.get('description'),approach_icon=approach.get('icon'),approach_icon_color=approach.get('icon_color'),versions=approach.get('versions'),model_asset_id=model_asset_id,model_container_type=model_container_type,model_container_id=model_container_id)
            if not _is_approach_exists:
                raise ClientError("Approach "+approach_id+" is not available.")
        else:
            raise ClientError("Failed in retrieving an approache. ERROR {}. {}".format(response.status_code,response.text))


    def _get_approach_url(self,model_usecase_asset_id:str=None,catalog_id:str=None,approach_id:str=None,version_number:str=None,operation:str=None):
        
        if operation == 'post':
            append_url = '/v1/aigov/model_inventory/model_usecases/' + model_usecase_asset_id + '/version_approach?catalog_id='+ catalog_id
        elif operation == 'get':
            append_url = '/v1/aigov/model_inventory/model_usecases/' + model_usecase_asset_id + '/tracked_model_versions?catalog_id='+ catalog_id
        elif operation == 'delete' or operation == 'patch':
            append_url = '/v1/aigov/model_inventory/model_usecases/' + model_usecase_asset_id + '/version_approach/' + approach_id + '?catalog_id='+ catalog_id
        elif operation == 'put':
            append_url = '/v1/aigov/model_inventory/model_usecases/' + model_usecase_asset_id + '/version_approach/' + approach_id + '/versions/'+ version_number +'?catalog_id='+ catalog_id
        else:
            append_url = ""
        
        if self._is_cp4d:
            url = self._cpd_configs["url"] + append_url
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + append_url
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + append_url
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + append_url

        return url


    def get_grc_models(self)->list:

        """
            Returns list of WKC Models associated with Openpages for a particular model usecase
            
            :return: All WKC Models associated with Openpages for a particular model usecase
            :rtype: list()

            Example:
            >>> client.assets.model_usecase.get_grc_models()

        """

        modelusecase_asset_id=self._asset_id
        model_container_type= self._container_type
        modelusecase_catalog_id= self._container_id

        #if self._is_cp4d and self._cp4d_version < "4.7.0":
        #    raise ClientError("Version mismatch: models associated for a particular Model usecase in Openpages functionality is only supported in CP4D version 4.7.0 or higher. Current version of CP4D is "+self._cp4d_version)

        if (modelusecase_asset_id is None or modelusecase_asset_id == ""):
            raise MissingValue("modelusecase_asset_id", "model usecase asset ID is missing")
        if (modelusecase_catalog_id is None or modelusecase_catalog_id == ""):
            raise MissingValue("modelusecase_catalog_id", "model usecase catalog ID is missing")

        url=self._get_grc_url(modelusecase_asset_id,modelusecase_catalog_id)
        response=requests.get(url,headers=self._get_headers())

        if response.status_code ==200:
            _logger.info("GRC models retrieved successfully")
            grc_model_list = response.json()["models"]
            grc_model_list_values = []
            for grc_model in grc_model_list:
                grc_model_list_values.append({'GrcModel': {'id': grc_model.get('model_id'), 'name': grc_model.get('model_name'), 'description': grc_model.get('model_description'), 'status': grc_model.get('model_status')}})
            return grc_model_list_values
        else:
            raise ClientError("Failed in retrieving GRC models. ERROR {}. {}".format(response.status_code,response.text))


    def get_grc_model(self,id: str=None):

        """
            Returns list WKC Model associated with Openpages for a particular model usecase
            
            :return: WKC Model associated with Openpages for a particular model usecase
            :rtype: dictionary

            Example:
            >>> client.assets.model_usecase.get_grc_model(id=<grc_model_id>)

        """

        modelusecase_asset_id=self._asset_id
        model_container_type= self._container_type
        modelusecase_catalog_id= self._container_id

        #if self._is_cp4d and self._cp4d_version < "4.7.0":
        #    raise ClientError("Version mismatch: models associated for a particular Model usecase in Openpages functionality is only supported in CP4D version 4.7.0 or higher. Current version of CP4D is "+self._cp4d_version)

        if (modelusecase_asset_id is None or modelusecase_asset_id == ""):
            raise MissingValue("modelusecase_asset_id", "model usecase asset ID is missing")
        if (modelusecase_catalog_id is None or modelusecase_catalog_id == ""):
            raise MissingValue("modelusecase_catalog_id", "model usecase catalog ID is missing")

        url=self._get_grc_url(modelusecase_asset_id,modelusecase_catalog_id)
        response=requests.get(url,headers=self._get_headers())

        if response.status_code ==200:
            _logger.info("GRC models retrieved successfully")
            grc_model_list = response.json()["models"]
            _is_grc_model_exists = False
            for grc_model in grc_model_list:
                if grc_model.get('model_id') == id:
                    _is_grc_model_exists = True
                    _logger.info("GRC model retrieved successfully")
                    return {'GrcModel': {'id': grc_model.get('model_id'), 'name': grc_model.get('model_name'), 'description': grc_model.get('model_description'), 'status': grc_model.get('model_status')}}
            if not _is_grc_model_exists:
                raise ClientError("GRC Model ID "+id+" is not available.")
        else:
            raise ClientError("Failed in retrieving GRC models. ERROR {}. {}".format(response.status_code,response.text))


    def _get_grc_url(self,model_usecase_asset_id:str=None,catalog_id:str=None):
        
        
        append_url = '/v1/aigov/model_inventory/grc/model_entries/' + model_usecase_asset_id + '/models?catalog_id='+ catalog_id
        
        if self._is_cp4d:
            url = self._cpd_configs["url"] + append_url
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + append_url
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + append_url
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + append_url

        return url


    def get_name(self)->str:

        """
            Returns model usecase name
            
            :return: Model usecase name
            :rtype: str

            Example:
            >>> client.assets.model_usecase.get_name()

        """

        return self.get_info(True).get("name")
    
    def get_id(self)->str:

        """
            Returns model usecase asset ID 
            
            :return: Model usecase asset ID
            :rtype: str

            Example:
            >>> client.assets.model_usecase.get_id()

        """

        return self.get_info(True).get("model_usecase_id")

    def get_container_id(self)->str:

        """
            Returns model usecase container ID 
            
            :return: Model usecase container ID
            :rtype: str

            Example:
            >>> client.assets.model_usecase.get_container_id()

        """

        return self.get_info(True).get("catalog_id")
    
    def get_container_type(self)->str:

        """
            Returns model usecase container type
            
            :return: Model usecase container type
            :rtype: str

            Example:
            >>> client.assets.model_usecase.get_container_type()

        """

        return self.get_info(True).get("container_type")

    def get_description(self)->str:

        """
            Returns model usecase description
            
            :return: Model usecase description
            :rtype: str

            Example:
            >>> client.assets.model_usecase.get_description()

        """

        return self.get_info(True).get("description")

    def relate_models(self,reference_model_asset_id: str=None, model_asset_id: str=None):

        """
            Returns Update master_id for a model
            
            :return: Update master_id for a model, now both models will be in same row.
            :rtype: None

            Example:
            >>> client.assets.model_usecase.get_grc_model(id=<grc_model_id>)

        """

        if (reference_model_asset_id is None or reference_model_asset_id == ""):
            raise MissingValue("reference_model_asset_id", "Reference model asset ID is missing")
        
        if (model_asset_id is None or model_asset_id == ""):
            raise MissingValue("model_asset_id", "Model asset ID is missing")
        
        modelusecase_asset_id=self._asset_id
        model_container_type= self._container_type
        modelusecase_catalog_id= self._container_id

        #if self._is_cp4d and self._cp4d_version < "4.7.0":
        #    raise ClientError("Version mismatch: relate models functionality is only supported in CP4D version 4.7.0 or higher. Current version of CP4D is "+self._cp4d_version)

        if (modelusecase_asset_id is None or modelusecase_asset_id == ""):
            raise MissingValue("modelusecase_asset_id", "model usecase asset ID is missing")
        if (modelusecase_catalog_id is None or modelusecase_catalog_id == ""):
            raise MissingValue("modelusecase_catalog_id", "model usecase catalog ID is missing")

        url=self._get_relatemodels_url(modelusecase_asset_id,modelusecase_catalog_id)

        body = [
                {
                    "reference_model_id": reference_model_asset_id, 
                    "model_id": model_asset_id
                }
            ]
        response = requests.patch(url, data=json.dumps(body), headers=self._get_headers())
        
        if response.status_code ==200:
            _logger.info("Models are related successfully")
        else:
            raise ClientError("Failed in relating models. ERROR {}. {}".format(response.status_code,response.text))


    def _get_relatemodels_url(self,model_usecase_asset_id:str=None,catalog_id:str=None):
        
        
        append_url = '/v1/aigov/model_inventory/grc/model_entries/' + model_usecase_asset_id + '/relatemodels?catalog_id='+ catalog_id
        
        if self._is_cp4d:
            url = self._cpd_configs["url"] + append_url
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + append_url
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + append_url
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + append_url

        return url

