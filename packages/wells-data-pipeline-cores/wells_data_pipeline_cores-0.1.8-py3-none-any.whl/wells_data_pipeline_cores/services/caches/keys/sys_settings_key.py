import logging
from abc import ABC, abstractmethod

from enum import auto, IntEnum
from strenum import LowercaseStrEnum

from wells_data_pipeline_cores.services.caches.keys.key_info import KeyInfoEnum, GroupKeyValue

from wells_data_pipeline_cores.services.caches.keys.dataset_key_info import AbstractDatasetKeyInfo, DatasetKeyInfoEnum, DefaultDatasetKey

class AssetTypeEnum(LowercaseStrEnum):
    PARTITION_KEY = auto()
    WITSML = auto()
    DATASOURCE = auto()
    OTHERS = auto()

class SysSettingsKey(AbstractDatasetKeyInfo):
    DATASET_TYPE:str = "sys_config"
    DATASET_NAME:str = "settings"

    def __init__(self, group:GroupKeyValue=None, key:str=None, asset:str=None, uid:str=None):
        super().__init__(group=group, key=key, dataset_name=self.DATASET_NAME)

        self.set_type(dtype=self.DATASET_TYPE)

        self.set_asset_id(asset_id=asset)
        self.set_uid(uid=uid)

    def get_dtype(self) -> str:
        """
        Get Key Type
        :return:
        """
        return self.DATASET_TYPE

    @staticmethod
    def new_settings_key(asset_type:AssetTypeEnum, data_type:str, group:GroupKeyValue=GroupKeyValue.DATA):
        """ 
        /// Partition key: type=sys_config:group=data:dataset=settings:asset=partition_key:uid={master_data_type}
        /// Active Partition key: type=sys_config:group=active:dataset=settings:asset=partition_key:uid={master_data_type}
        /// Wits Configuration key: type=sys_config:group=data:dataset=settings:asset=witsml:uid={wits_provider}
        /// - Datasource Configuration key: type=sys_config:group=data:dataset=settings:asset=datasource:uid={datasource_name}
        ///     - Corva datasource: type=sys_config:group=data:dataset=settings:asset=datasource:uid=corva
        ///     - Coldbore datasource: type=sys_config:group=data:dataset=settings:asset=datasource:uid=coldbore
        """
        return SysSettingsKey(group=group, asset=asset_type, uid=data_type)

    @staticmethod
    def new_partition_settings_key(masterDataType:str):
        """
        Partition key: type=sys_config:group=data:dataset=settings:asset=partition_key:uid={master_data_type}
        """
        return SysSettingsKey.new_settings_key(asset_type=AssetTypeEnum.PARTITION_KEY, data_type=masterDataType, group=GroupKeyValue.DATA)

    @staticmethod
    def new_active_partition_settings_key(masterDataType:str):
        """
        Active Partition key: type=sys_config:group=active:dataset=settings:asset=partition_key:uid={master_data_type}
        """
        return SysSettingsKey.new_settings_key(asset_type=AssetTypeEnum.PARTITION_KEY, data_type=masterDataType, group=GroupKeyValue.ACTIVE)

    @staticmethod
    def new_witsml_settings_key(witsmlProvider:str):
        """
        Wits Configuration key: type=sys_config:group=data:dataset=settings:asset=witsml:uid={wits_provider}
        """
        return SysSettingsKey.new_settings_key(asset_type=AssetTypeEnum.WITSML, data_type=witsmlProvider, group=GroupKeyValue.DATA)

    def new_datasource_settings_key(datasourceName:str):
        """
        /// - Datasource Configuration key: type=sys_config:group=data:dataset=settings:asset=datasource:uid={datasource_name}
        ///     - Corva datasource: type=sys_config:group=data:dataset=settings:asset=datasource:uid=corva
        ///     - Coldbore datasource: type=sys_config:group=data:dataset=settings:asset=datasource:uid=coldbore
        """
        return SysSettingsKey.new_settings_key(asset_type=AssetTypeEnum.DATASOURCE, data_type=datasourceName, group=GroupKeyValue.DATA)

    @staticmethod
    def new_others_settings_key(name:str):
        """
        Other setting key: type=sys_config:group=data:dataset=settings:asset=others:uid={name}
        """
        return SysSettingsKey.new_settings_key(asset_type=AssetTypeEnum.OTHERS, data_type=name, group=GroupKeyValue.DATA)