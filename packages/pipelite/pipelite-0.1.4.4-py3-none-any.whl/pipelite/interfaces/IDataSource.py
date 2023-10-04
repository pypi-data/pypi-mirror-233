__author__ = "datacorner.fr"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from pipelite.dpObject import dpObject
from pipelite.etlDataset import etlDataset
from abc import abstractmethod

class IDataSource(dpObject):
    def __init__(self, config, log):
        super().__init__(config, log)

    @property
    def count(self):
        """Returns the number of rows
        Returns:
            int: rows count
        """
        try:
            return self.content.count
        except:
            return 0

    @abstractmethod
    def initialize(self, cfg) -> bool:
        """ Initialize and makes some checks (params) for that datasource
        Args:
            cfg (objConfig): parameters
        Returns:
            bool: False if error
        """
        return True

    @abstractmethod
    def extract(self) -> etlDataset:
        """ MUST BE OVERRIDED !
            Returns all the data in a DataFrame format
        Returns:
            etlDataset: Number of data read
        """
        self.log.error("DataSource.extract() -> This Data sources does not support reading/extracting")
        return etlDataset()

    @abstractmethod
    def load(self, etlDataset) -> int:
        """ MUST BE OVERRIDED !
            write the dataset in the datasource
        Returns:
            int: Number of data rows loaded
        """
        self.log.error("DataSource.load() -> This Data sources does not support writing/loading")
        return 0
