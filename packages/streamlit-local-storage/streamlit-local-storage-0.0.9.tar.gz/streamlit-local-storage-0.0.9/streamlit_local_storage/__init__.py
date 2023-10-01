import os
from typing import Literal, Optional, Union
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _st_local_storage = components.declare_component(

        "st_local_storage",

        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _st_local_storage = components.declare_component("st_local_storage", path=build_dir)


class LocalStorage:
    """
    Component to help manager local storage for streamlit apps
    """

    def __init__(self, key="init"):
        self.localStorageManager = _st_local_storage
        self.storedItems = self.localStorageManager(method="getAll", key=key, default={})

    def setList(self, items:list = None, key:str="setList"):
        """
        Set a list of items to local storage. Send a list and its contents will be sent to local storage.

        Args:
            items: list of dictionaries -
                - dict args:
                    - key: name of the key used to identify the item being stored
                    - toStore: list of items (strings, bool, dictionaries, numbers) to be stored to local storage
                    - example:
                        [
                            {"key": "item to store", "toStore": [1,2,3,4]},
                            {"key": "another item to store", "toStore": [{"username":"name here"}]},
                        ]
            key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
        
            if items is `None` or emtpy list, function will not run
        """
        if items is None or items == "" or len(items) == 0:
            return
        
        try:
            self.localStorageManager(method="setList", items=items, key=key)
            [self.storedItems.update({d["key"]: d["toStore"]}) for d in items]

            return True
        except:
            return False
    
    def setItem(self, itemKey:str=None, itemValue:Union[str, int, float, bool]=None, key:str="set"):
        """
        Set individual items to local storage with a given name (itemKey) and value (itemValue)

        Args:
            itemKey: Name of the item to set
            itemValue: The value to save. Can be string, int, float, bool, dict, json but will be stored as a string
        """

        if (itemKey is None or itemKey == "") or (itemValue is None or itemValue == ""):
            return
        
        try:
            self.localStorageManager(method="setItem", itemKey=itemKey, itemValue=itemValue, key=key)
            self.storedItems[itemKey] = itemValue
            return True
        except:
            return False
    
    # def getList(self, items:list=None, key:str="getList"):
    #     """
    #     Get a list of saved items from local storage.

    #     Args:
    #         items: list of dictionaries -
    #             - dict args: 
    #                 - key: keys to get from local storage
    #                 - example:
    #                     [
    #                         {"key": "get this"},
    #                         {"key": "get that too"}
    #                     ]
    #         key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
    #     """

    #     if items is None or items == "" or len(items) == 0:
    #         return
        
    #     try:
    #         saved_list = self.localStorageManager(method="getList", items=items, key=key) 
    #         return saved_list
    #     except:
    #         return False

    def getList(self, items:list=None):
        """
        Get a list of saved items from local storage.

        Args:
            items: list of keys to get 
                - example:
                    [
                        "key1", "key2"
                    ]
            key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
        """

        if items is None or items == "" or len(items) == 0:
            return
        
        data_to_return = dict((k, self.storedItems[k]) for k in items if k in self.storedItems)
        return data_to_return
    
    
    # def getItemRender(self, itemKey:str=None, key:str="get"):
    #     """
    #     Get individual items stored in local storage.

    #     Args:
    #         itemKey: name of item to get from local storage
    #     """

    #     if itemKey is None or itemKey == "":
    #         return
       
    #     try:
    #         saved_key = self.localStorageManager(method="getItem", itemKey=itemKey, key=key) 
    #         return saved_key
    #     except:
    #         return False
    
    def getItem(self, itemKey:str=None):

        if itemKey is None or itemKey == "":
            return

        return {"item":itemKey, "data": self.storedItems.get(itemKey)}
    
    def deleteList(self, items:list=None, key:str="deleteList"): 
        """
        Delete a list of items from local storage

        Args:
            items: list of keys to get 
                - example:
                    [
                        "key1", "key2"
                    ]
            key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
        """

        if items is None or items == "" or len(items) == 0:
            return
        
        try:
            saved_key = self.localStorageManager(method="deleteList", items=items, key=key) 
            self.storedItems = {k: v for k, v in self.storedItems.items() if k not in items}
            return saved_key
        except:
            return False

    def deleteItem(self, itemKey:str, key:str="deleteItem"): 
        """
        Delete individual item from local storage

        Args:
            itemKey: item key to delete from local storage
            key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
        """

        if itemKey is None or itemKey == "":
            return
        
        try:
            saved_key = self.localStorageManager(method="deleteItem", itemKey=itemKey, key=key) 
            self.storedItems.pop(itemKey)
            return saved_key
        except:
            return False
    
    def deleteAll(self, key:str="deleteAll"):
        """
        Delete all items you saved on local storage

        Args:
            key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
        """

        try:
            saved_key = self.localStorageManager(method="deleteAll", key=key) 
            return saved_key
        except:
            return False
        
    def getAll(self, key:str="getAll"):
        """
        Get all items saved on local storage.

        Args:
            key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
        """

        try:
            saved_key = self.localStorageManager(method="getAll", key=key) 
            return saved_key
        except:
            return False
        


