import logging
from abc import ABC, abstractmethod

from enum import auto, IntEnum
from strenum import LowercaseStrEnum

class GroupKeyValue(LowercaseStrEnum):
    DATA = auto()
    ACTIVE = auto()
    ERROR = auto()
    SYNC = auto()

class KeyInfoEnum(LowercaseStrEnum):
    TYPE = auto()
    GROUP = auto()
    UID = auto()

class AbstractKeyInfo(ABC):
    """
    /// Well Data Key: type=well:group=data:wits={provider_name}:uid={well_id}
    /// Well Active Key: type=well:group=active:wits={provider_name}:uid={well_id}
    /// 
    /// Wellbore Data Key: type=wellbore:group=data:wits={provider_name}:well={well_id}:uid={wellbore_id}
    /// 
    /// Log Data Key: type=log:group=data:wits={provider_name}:well={well_id}:wellbore={wellbore_id}:uid={log_id}
    /// 
    /// Log Data Key: type=synclog:group=data:wits={provider_name}:well={well_id}:wellbore={wellbore_id}:uid={log_id}
    """

    ID_DEFAULT_VALUE = "-99999"
    APP_KEY_NAMES_PLACEHOLDER = "_app_key_names_"

    # Key format: type=[type_valye]:group=[data|active|error]:{_app_keys_}:uid=[id]
    ORDERED_KEY_NAMES_TEMPLATE = [
        KeyInfoEnum.TYPE,
        KeyInfoEnum.GROUP,
        APP_KEY_NAMES_PLACEHOLDER,
        KeyInfoEnum.UID
    ]

    def __init__(self, group:GroupKeyValue=None, key:str=None):
        # keep properties of keyinfo
        self._props:dict[str,str] = {}
        self._ordered_key_names:list[str] = []

        # process key first
        if key is not None and len(key) > 0:
            self.parser_key(key=key)

        # add group
        if group is not None:
            self.set_group(group=group)
        
        # add default type
        self.set_type(dtype=self.get_dtype())

    def add_prop(self, key:str, value:str):
        if key is not None and value is not None:
            key = key.lower()
            self._props.update({key : value})

    def get_prop(self, key:str, defaultValue:str=None) -> str:
        if key is not None:
            return self._props.get(key, defaultValue)
        
        return defaultValue

    def get_prop_keys(self) -> list[str]:
        return list(self._props.keys)

    def get_keys_ordered(self) -> list[str]:
        if self._ordered_key_names is None:
            self._ordered_key_names = []
        
        if len(self._ordered_key_names) == 0:
            for key in self.ORDERED_KEY_NAMES_TEMPLATE:
                if key == self.APP_KEY_NAMES_PLACEHOLDER:
                    app_keys = self.get_app_keys()
                    if app_keys is not None and len(app_keys) > 0:
                        self._ordered_key_names.extend(app_keys);
                else:
                    self._ordered_key_names.append(key)
        
        return self._ordered_key_names

    def set_group(self, group:GroupKeyValue | str):
        self.add_prop(key=KeyInfoEnum.GROUP, value=group)

    def get_group(self) -> str:
        return self.get_prop(key=KeyInfoEnum.GROUP)

    def is_group(self, group:GroupKeyValue | str) -> bool:
        return group == self.get_group()
    
    def get_properties(self) -> dict[str, str]:
        return self._props
    
    def set_uid(self, uid:str):
        self.add_prop(key=KeyInfoEnum.UID, value=uid)
    
    def get_uid(self) -> str:
        return self.get_prop(key=KeyInfoEnum.UID)
    
    def set_type(self, dtype: str):
        self.add_prop(key=KeyInfoEnum.TYPE, value=dtype)

    def get_type(self) -> str:
        return self.get_prop(key=KeyInfoEnum.TYPE)

    def is_type(self, dtype: str) -> bool:
        return dtype == self.get_type()

    def to_str_key(self) -> str:
        return AbstractKeyInfo.to_key(props=self._props, ordered_keys=self.get_keys_ordered())

    def to_str_search_key(self) -> str:
        return AbstractKeyInfo.to_search_key(props=self._props, ordered_keys=self.get_keys_ordered())
    
    def to_str_partition_key(self) -> str:
        """
        Build Cosmos's primaryKey
        """
        return AbstractKeyInfo.to_key(props=self._props, ordered_keys=self.get_partion_key_names())

    def to_value(self, value:str, defaultValue:str) -> str:
        return AbstractKeyInfo.to_value(value=value, defaultValue=defaultValue)

    @staticmethod
    def to_key(props:dict[str,str], ordered_keys:list[str]) -> str:
        """
        /// Well Data Key: type=well:group=data:wits={provider_name}:uid={well_id}
        /// Well Active Key: type=well:group=active:wits={provider_name}:uid={well_id}
        /// 
        /// Wellbore Data Key: type=wellbore:group=data:wits={provider_name}:well={well_id}:uid={wellbore_id}
        /// 
        /// Log Data Key: type=log:group=data:wits={provider_name}:well={well_id}:wellbore={wellbore_id}:uid={log_id}
        """
        if props is None or ordered_keys is None or len(ordered_keys) == 0:
            return ""

        _str_keys: list[str] = []

        for key in ordered_keys:
            value = props.get(key, None)
            if value is not None:
                _str_keys.append(f"{key}={AbstractKeyInfo.to_value(value=value, defaultValue='')}")
            else:
                # check key is Type or Group
                if key == KeyInfoEnum.TYPE:
                    _str_keys.append(f"{key}=")
                elif key == KeyInfoEnum.GROUP:
                    _str_keys.append(f"{key}={GroupKeyValue.DATA}")
 
        return ":".join(_str_keys)

    @staticmethod
    def to_search_key(props:dict[str,str], ordered_keys:list[str]) -> str:
        """
        Well Active Search Key: type=well:group=active:wits=*:uid=*
        """
        if props is None or ordered_keys is None:
            return "*"
        
        _str_search_keys: list[str] = []

        for key in ordered_keys:
            value = props.get(key, None)
            if value is not None:
                _str_search_keys.append(f"{key}={AbstractKeyInfo.to_value(value=value, defaultValue='*')}")
            else:
                # check key is Type or Group
                if key == KeyInfoEnum.TYPE or key == KeyInfoEnum.GROUP:
                    _str_search_keys.append(f"{key}=*")

        return ":".join(_str_search_keys)

    @staticmethod
    def is_valid_key(check_type:str, key:str) -> bool:
        if check_type is None or len(check_type) == 0:
            return False
        if key is None or len(key) == 0:
            return False
        
        return (f"{KeyInfoEnum.TYPE}={check_type}" in key)

    @staticmethod
    def to_value(value:str, defaultValue:str) -> str:
        if value is not None:
            if type(value) is str:
                return value.strip()
            else:
                return value

        return defaultValue
    
    @staticmethod
    def is_wildcard_search(values: list[str]) -> bool:
        if values is None or len(values) == 0:
            return True
        
        for value in values:
            if value is None or "*" in value:
                return True

        return False

    def parser_key(self, key:str) -> bool:
        """
        Convert key: type=well:group=data:wits={provider_name}:uid={well_id} to KeyInfo
        """

        if key is None or len(key) == 0:
            return False

        key_pairs = key.split(sep=":")
        for key_pair in key_pairs:
            try:
                key_value = key_pair.split("=")
                if len(key_value) == 1:
                    self.add_prop(key=key_value[0], value="")
                elif len(key_value) > 1:
                    self.add_prop(key=key_value[0], value=key_value[1])

            except Exception as ex:
                logging.debug("parser_key() - key_pair: %s, error: %s", key_pair, ex) 
            
        return True

    @abstractmethod
    def post_parser_key(self):
        """
        Process parser key
        :return:
        """
        pass

    @abstractmethod
    def get_dtype(self) -> str:
        """
        Get Key Type
        :return:
        """
        pass

    @abstractmethod
    def get_app_keys(self) -> list[str]:
        """
        Get app keys (ordered key) to build key
        """
        pass

    @abstractmethod
    def get_partion_key_names(self) -> list[str]:
        """
        GProvide list ordered key name to build Cosmos's primaryKey
        e,g: type={type}:group={group}:wits={provider}
        """
        pass