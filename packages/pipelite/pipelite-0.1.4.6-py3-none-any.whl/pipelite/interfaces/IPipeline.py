__author__ = "datacorner.fr"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import pipelite.constants as C
from pipelite.dpObject import dpObject
from abc import abstractmethod
from pipelite.objConfig import objConfig
from pipelite.etlDatasets import etlDatasets

""" Pipeline Management rules:
    1) a pipeline can have 
        * Many Extractors
        * Many Transformers
        * Many Loaders
"""
class IPipeline(dpObject):
    def __init__(self, config, log):
        super().__init__(config, log)
        # ETL objects does not contain any data, just the pipeline specifications
        self.extractors = []    # dpObject list with all extractors
        self.loaders = []       # dpObject list with all loaders
        self.transformers = []  # dpObject list with all transformers
        self.dsStack = etlDatasets()    # data set stack (contains the data)

    def __initETLObjects(self, paramJSONPath) -> list:
        """ Initialize an set of similar etl object (can be a extractor, loader or transformer)
        Args:
            etlObjParams (JSON): "$.extractors"
            Parameters for the etl Object. Look like something like this (below)
                [{
                    "name": "...",
                    "classname": "pipelines.datasources.ObjClassExample",
                    "parameters": {
                        "separator": ",",
                        "filename": "test2.csv",
                        "path": "/tests/data/",
                        "encoding": "utf-8"
                }, { ... } ]
        Returns:
            list: list of etl objects initialized
        """
        objectList = []
        try:
            etlObjParams = self.config.getParameter(paramJSONPath, C.EMPTY)
            # DS or TR to init
            self.log.info("There is/are {} [{}] objects(es)".format(len(etlObjParams), paramJSONPath))
            if (len(etlObjParams) < 1):
                raise Exception("At least one Object is needed for processing the pipeline!")
            self.log.debug("Intantiate needs and configured objects ...")
            # Initialize the Extractors/transformers
            for ObjItem in etlObjParams:
                dpConfig = objConfig(self.config, self.log, paramJSONPath, ObjItem)
                self.log.debug("Validate and initialize Object...")
                if not dpConfig.validate():
                    raise Exception("Impossible to validate the object configuration")
                if not dpConfig.initialize():
                    raise Exception("Impossible to initialize the object")
                # instantiate & Init the object
                self.log.info("Instantiate Object: {}".format(dpConfig.className))
                dsObj = dpObject.instantiate(dpConfig.className, self.config, self.log)
                self.log.debug("Initialize Object: {}".format(dpConfig.className))
                # Check the parameter (json) structure against the json scheme provided (if any, otherwise try to get the one by default)
                valFileCfg = dpConfig.validation if dpConfig.validation != None else dsObj.parametersValidationFile
                if (not self.validateParametersCfg(valFileCfg, dpConfig.parameters)):
                    raise Exception("The {} parameters are not configured properly, check out the configuration file.".format(dsObj['name']))
                # some init considering the object
                if (paramJSONPath == C.PLJSONCFG_TRANSFORMER):
                    # Only for transformers ...
                    self.log.debug("Transformer {} initialized successfully".format(dpConfig.className))
                    dsObj.dsInputs = dpConfig.inputs
                    dsObj.dsOutputs = dpConfig.outputs
                if (dsObj.initialize(dpConfig)):
                    # Add the object in the list
                    self.log.debug("Data Source {} initialized successfully".format(dpConfig.className))
                    dsObj.name = dpConfig.name
                    dsObj.objtype = paramJSONPath
                    objectList.append(dsObj)
                else:
                    raise Exception("Object {} cannot be initialized properly".format(dpConfig.className))
            return objectList
        except Exception as e:
            self.log.error("{}".format(e))
            return objectList
    
    def __initAllETLObjects(self) -> bool:
        """Initialize the pipeline object by gathering the Pipeline infos and initializing the etl objects
        Returns:
            bool: False if error
        """
        try:
            self.log.info("*** Starting pipeline processing ***")
            # 1) init Extractors
            self.log.info("Initializing Extractor(s) ...")
            self.extractors = self.__initETLObjects(C.PLJSONCFG_EXTRACTOR)
            if (len(self.extractors) == 0):
                raise Exception("Extractor(s) has/have not been initialized properly")
            self.log.info("There is/are {} extractor(s)".format(len(self.extractors)))
            # 2) init Loaders
            self.log.info("Initializing Loaders(s) ...")
            self.loaders = self.__initETLObjects(C.PLJSONCFG_LOADER)
            if (len(self.loaders) == 0):
                raise Exception("Loader(s) has/have not been initialized properly")
            self.log.info("There is/are {} loader(s)".format(len(self.loaders)))
            # 3) init Transformers
            self.log.info("Initializing Transformer(s) ...")
            self.transformers = self.__initETLObjects(C.PLJSONCFG_TRANSFORMER)

            self.log.info("There is/are {} Transformers(s)".format(len(self.transformers)))
            return True
        except Exception as e:
            self.log.error("{}".format(e))
            return False

    def initialize(self) -> bool:
        """Initialize the pipeline object by gathering the Pipeline infos and initializing the etl objects
        Returns:
            bool: False if error
        """
        try:
            if not(self.__initAllETLObjects()):
                raise Exception ("All the pipeline objects could not be configured and initialized properly")
            # TO DO CHECKS here ...
            #   Check if No Inputs or No outputs
            #   Warning if Loaders & Extractors have same names

            return True
        except Exception as e:
            self.log.error("{}".format(e))
            return False

    def terminate(self) -> bool:
        # For surcharge
        self.log.info("*** End of Job treatment ***")
        return True
    
    @abstractmethod
    def extract(self) -> int: 
        """This method must be surchaged and aims to collect the data from the datasources to provides the corresponding datasets
        Returns:
            int: Total Number of read rows
        """
        return 0
        
    @abstractmethod
    def transform(self) -> int: 
        """ Make some modifications in the Dataset(s) after gathering the data and before loading
        Returns:
            etlDataset: Output dataset
            int: Total Number of transformed rows
        """
        return 0
    
    @abstractmethod
    def load(self) -> int:
        """ Load the dataset transformed in one or more loaders.
            Only load the datasets which are referenced as Data Source Load and are in the Stack.
            Be Careful: the loaders are not in the stack by default (because they don't still have data)
            so To load, 2 options:
                1) Use a name which exists in the extractors
                2) Use a Tranformer to create a new dataset
        Args:
            dfDataset (etlDataset): dataset with the Data to load in one or several data sources
        Returns:
            bool: False if error
        """
        return 0