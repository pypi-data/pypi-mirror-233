import logging
from abc import ABC, abstractmethod

from enum import auto, IntEnum
from strenum import LowercaseStrEnum

from wells_data_pipeline_cores.services.caches.keys.key_info import AbstractKeyInfo, KeyInfoEnum, GroupKeyValue

class DatasetKeyInfoEnum(LowercaseStrEnum):
    DATASET = auto()
    ASSET = auto()

class AbstractDatasetKeyInfo(AbstractKeyInfo):
    """
    /// Corva Master Assets Data: type=corva_master:group=data:dataset=assets:uid={asset_id}
    /// Corva Dataset: type=corva_data:group=data:dataset={dataset_name}:asset={asset_id}:uid={dataset_id}
    /// ExxomMobil Dataset: type=corva_xom:group=data:dataset={dataset_name}:asset={asset_id}:uid={dataset_id}
    /// 
    /// Master Assets Active Key: type=corva_master:group=active:dataset={assets}:uid={well_id}
    """

    """
    Dataset key pattern: type=corva_data:group=data:dataset={dataset_name}:asset={asset_id}:uid={dataset_id}
    """
    ORDERED_APP_KEY_NAMES:list[str] = [
        DatasetKeyInfoEnum.DATASET,
        DatasetKeyInfoEnum.ASSET
    ]

    """
    Cosmops Primary Key pattern: type={type}:group={group}:dataset={dataset_name}
    """
    ORDERED_COSMOS_PRIMARY_KEY_NAMES:list[str] = [
        KeyInfoEnum.TYPE,
        KeyInfoEnum.GROUP,
        DatasetKeyInfoEnum.DATASET
    ]

    def __init__(self, group:GroupKeyValue=None, key:str=None, dataset_name:str=None):
        super().__init__(group=group, key=key)
        self.set_dataset_name(dataset_name=dataset_name)
        
    def get_dataset_name(self) -> str:
        return self.get_prop(key=DatasetKeyInfoEnum.DATASET)

    def set_dataset_name(self, dataset_name:str):
        if dataset_name is not None:
            self.add_prop(
                key=DatasetKeyInfoEnum.DATASET, 
                value=self.to_value(value=dataset_name, defaultValue="")
            )

    def get_asset_id(self) -> str:
        return self.get_prop(key=DatasetKeyInfoEnum.ASSET)

    def set_asset_id(self, asset_id:str):
        if asset_id is not None:
            self.add_prop(
                key=DatasetKeyInfoEnum.ASSET, 
                value=self.to_value(value=asset_id, defaultValue="")
            )

    def post_parser_key(self):
        """
        Process parser key
        :return:
        """
        pass

    def get_app_keys(self) -> list[str]:
        """
        Get app keys (ordered key) to build key
        """
        return self.ORDERED_APP_KEY_NAMES

    def get_partion_key_names(self) -> list[str]:
        """
        GProvide list ordered key name to build Cosmos's primaryKey
        e,g: type={type}:group={group}:wits={provider}
        """
        return self.ORDERED_COSMOS_PRIMARY_KEY_NAMES

    @abstractmethod
    def get_dtype(self) -> str:
        """
        Get Key Type
        :return:
        """
        pass

class DefaultDatasetKey(AbstractDatasetKeyInfo):
    """
    /// DefaultDatasetKey is used to decode and get dataset key info
    /// type=sys_config:group=data:dataset=settings:asset=partition_key:uid={master_data_type}
    """

    def __init__(self, data_type:str=None, group:GroupKeyValue=None, key:str=None, dataset_name:str=None, asset:str=None, uid:str=None):
        super().__init__(group=group, key=key, dataset_name=dataset_name)

        self.set_type(dtype=data_type)        
        self.set_asset_id(asset_id=asset)
        self.set_uid(uid=uid)

    def get_dtype(self) -> str:
        """
        Get Key Type
        :return:
        """
        return self.get_type()

    @staticmethod
    def new_dataset_data_key(data_type:str, dataset_name:str,  asset:str=None, uid:str=None) -> AbstractDatasetKeyInfo:
        return DefaultDatasetKey.new_dataset_key(data_type=data_type, group=GroupKeyValue.DATA,  dataset_name=dataset_name, asset=asset, uid=uid)

    @staticmethod
    def new_dataset_active_key(data_type:str, dataset_name:str,  asset:str=None, uid:str=None) -> AbstractDatasetKeyInfo:
        return DefaultDatasetKey.new_dataset_key(data_type=data_type, group=GroupKeyValue.ACTIVE,  dataset_name=dataset_name, asset=asset, uid=uid)

    @staticmethod
    def new_dataset_sync_key(data_type:str, dataset_name:str,  asset:str=None, uid:str=None) -> AbstractDatasetKeyInfo:
        return DefaultDatasetKey.new_dataset_key(data_type=data_type, group=GroupKeyValue.SYNC,  dataset_name=dataset_name, asset=asset, uid=uid)

    @staticmethod
    def new_dataset_error_key(data_type:str, dataset_name:str,  asset:str=None, uid:str=None) -> AbstractDatasetKeyInfo:
        return DefaultDatasetKey.new_dataset_key(data_type=data_type, group=GroupKeyValue.ERROR,  dataset_name=dataset_name, asset=asset, uid=uid)

    @staticmethod
    def new_dataset_key(data_type:str, group:GroupKeyValue,dataset_name:str,  asset:str=None, uid:str=None) -> AbstractDatasetKeyInfo:
        if asset is None:
            asset = DefaultDatasetKey.ID_DEFAULT_VALUE

        if uid is None:
            uid = DefaultDatasetKey.ID_DEFAULT_VALUE

        return DefaultDatasetKey(data_type=data_type, group=group,  dataset_name=dataset_name, asset=asset, uid=uid)

    @staticmethod
    def new_dataset_key_by_keyinfo(key:str=None) -> AbstractDatasetKeyInfo:
        return DefaultDatasetKey(key=key)