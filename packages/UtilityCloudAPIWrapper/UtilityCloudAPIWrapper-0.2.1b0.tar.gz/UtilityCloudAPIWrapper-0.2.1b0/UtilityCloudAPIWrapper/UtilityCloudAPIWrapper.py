"""
UtilityCloudAPIWrapper.py

Python wrapper for the utility cloud API

"""
from os import makedirs
from os.path import join, isfile, abspath, isdir
# noinspection SpellCheckingInspection
from json import load as jload, dump as jdump, dumps as jdumps, JSONDecodeError
from logging import Logger
from configparser import ConfigParser
import getpass

import requests

import BetterConfigAJM as BetterConfig
import PurgeSecrets

from UCAPIErr import *


class EasyReq:
    def __init__(self, logger: Logger = None, ** kwargs):
        self._kwargs = None
        self._fail_http_400s = True
        if kwargs:
            self._kwargs = kwargs
            if 'fail_http_400s' in self._kwargs:
                self._fail_http_400s = self._kwargs['fail_http_400s']
        self._valid_request_methods = ["GET", "POST"]
        if logger:
            self._logger = logger
        else:
            self._logger = Logger("Dummy_logger")

    def MakeReq(self, method, url, headers: dict, payload) -> requests.Response:
        if method.lower() not in [x.lower() for x in self._valid_request_methods]:
            raise InvalidRequestMethod(
                f"{method} is not a valid request method "
                f"(Options are: {', '.join(self._valid_request_methods)})")

        try:
            response = requests.request(method, url, headers=headers, data=payload)
        except requests.RequestException as e:
            self._logger.error(e, exc_info=True)
            raise e
        if response.ok:
            return response
        else:
            try:
                raise requests.RequestException(f"response was {response.status_code} {response.reason},"
                                                f" with the following (if any) message: "
                                                f"{response.json()['message'].split('Authorization=')[0]}")
            except JSONDecodeError as e:
                try:
                    raise requests.RequestException(f"response was {response.status_code} {response.reason},"
                                                    f" with the following (if any) message: "
                                                    f"{response.text.split('Authorization=')[0]}") from None
                except requests.RequestException as e:
                    self._logger.error(e, exc_info=True)
                    if not self._fail_http_400s:
                        if response.status_code == 403 or response.status_code == 401:
                            self._logger.warning(f"response code {response.status_code} returned. "
                                                 f"Returning response for further processing")
                            return response
                        else:
                            raise e
                    else:
                        raise e
            except requests.RequestException as e:
                self._logger.error(e, exc_info=True)
                if not self._fail_http_400s:
                    if response.status_code == 403 or response.status_code == 401:
                        self._logger.warning(f"response code {response.status_code} returned. "
                                             f"Returning response for further processing")
                        return response
                    else:
                        raise e
                else:
                    raise e


# noinspection SpellCheckingInspection
class _UtilityCloudAuth:
    def __init__(self, logger: Logger = None, key_dirpath=None, chosen_keyfile_format=None, **kwargs):
        self.auth = None
        self.auto_auth = None
        self.auth_initialized = False
        self.config = None
        self.use_config = False
        self._auth_runtype_default = None
        self._auth_credentials = None
        self._config_suffixes = ['cfg', 'config', 'ini']
        self._make_key_dirpath = True
        self.user_email_suffix = None
        self.check_purge = False
        self.purge_all = False
        self._key_dirpath = key_dirpath
        self._key_filename = 'auth_key'
        self._valid_key_filetypes = ['json', 'config']
        self._default_key_format = self._valid_key_filetypes[0]
        self._chosen_keyfile_format = chosen_keyfile_format
        self._auth_base_url = "https://wc.ucld.us/"

        if self._chosen_keyfile_format:
            pass
        else:
            self._chosen_keyfile_format = self._default_key_format

        if logger:
            self._logger = logger
        else:
            self._logger = Logger("DUMMY_LOGGER")

        self.ER = EasyReq(logger=self._logger, fail_http_400s=True)

        if kwargs:
            self._logger.info("__init__ kwargs detected")
            self._kwargs = kwargs
            if 'make_key_dirpath' in self._kwargs:
                self._make_key_dirpath = self._kwargs['make_key_dirpath']
            if 'auth_runtype_default' in self._kwargs:
                self._auth_runtype_default = self._kwargs['auth_runtype_default']
            if 'auth_credentials' in self._kwargs:
                self._auth_credentials = self._kwargs['auth_credentials']
            if 'config' in self._kwargs:
                self.config = self._validate_config()
            if 'use_config' in self._kwargs:
                self.use_config = self._kwargs['use_config']
            if 'user_email_suffix' in self._kwargs:
                self.user_email_suffix = self._kwargs['user_email_suffix']
            if 'auto_auth' in self._kwargs:
                self.auto_auth = self._kwargs['auto_auth']
            if 'check_purge' in self._kwargs:
                self.check_purge = self._kwargs['check_purge']
            if 'purge_all' in self._kwargs:
                self.purge_all = self._kwargs['purge_all']

        if self.config and self.use_config:
            try:
                self._auth_runtype_default = self.config['AUTH']['auth_runtype_default']
                self.user_email_suffix = self.config['AUTH']['user_email_suffix']
            except KeyError as e:
                self.config.add_section("AUTH")
                self.config["AUTH"]["user"] = ""
                self.RunAuth()
                #self._get_uc_login(override_config_to_edit=True)
                """try:
                    raise InvalidConfigError(f"self.config is invalid. section {e} does not exist") from None
                except InvalidConfigError as e:
                    self._logger.error(e, exc_info=True)
                    raise e"""

        if self.config and self.use_config and self._key_dirpath is None:
            try:
                self._key_dirpath = self.config["AUTH"]["key_dirpath"]
            except KeyError as e:
                self._logger.warning("config['AUTH']['key_dirpath'] does not exist, creating it with a blank value")
                self.config["AUTH"]["key_dirpath"] = ""
                self._key_dirpath = key_dirpath
                pass
        elif self._key_dirpath is not None:
            self._key_dirpath = key_dirpath
        else:
            try:
                raise InvalidConfigError("Either self.use_config is false AND key_dirpath is None,"
                                         " or self.config is invalid AND key_dirpath is None")
            except InvalidConfigError as e:
                self._logger.error(e, exc_info=True)
                raise e

        self._key_dirpath_check()

        if self.auto_auth:
            self._logger.debug("auto_auth is true")
            self.auth, self.auth_initialized = self.RunAuth()
        else:
            self._logger.info("self.RunAuth() needs to be run manually, or auto_auth arg needs to be True.")

    def RunAuth(self):
        self._logger.info("Attempting to intialize Auth...")
        if self._auth_runtype_default:
            if self._auth_credentials:
                self.auth = self._InitAuth(runtype=self._auth_runtype_default, credentials=self._auth_credentials)
            else:
                self.auth = self._InitAuth(runtype=self._auth_runtype_default)
        else:
            self.auth = self._InitAuth()

        if self.auth:
            self._logger.info("self.Auth initialized successfully")
            self.auth_initialized = True
        return self.auth, self.auth_initialized

    # noinspection PyProtectedMember
    def _validate_config(self):
        if issubclass(self._kwargs['config'].__class__, BetterConfig):
            self.config = self._kwargs['config'].GetConfig()
            self._logger.info("Config Validated - BetterConfig Used")
            return self.config
        elif issubclass(self._kwargs['config'].__class__, ConfigParser):
            self.config = self._kwargs['config']
            self._logger.info("Config Validated - ConfigParser Used")
            return self.config
        else:
            try:
                raise InvalidConfigError(
                    "config must be an instance of ConfigParser or BetterConfig (my own edits to ConfigParser)")
            except InvalidConfigError as e:
                self._logger.error(e, exc_info=True)
                raise e

    def _get_uc_login(self, **kwargs):
        def _email_check(candidate):
            import re
            email_pattern = re.compile('^[\w-]+@([\w-]+\.)+[\w-]{2,4}$')
            res = re.fullmatch(email_pattern, candidate)
            return res

        def _get_user_loop():
            while True:
                user = input("UC Username: ")
                if user:
                    if self.user_email_suffix:
                        if not user.endswith(self.user_email_suffix):
                            user = user + self.user_email_suffix
                            return user
                    elif not self.user_email_suffix and not _email_check(user):
                        try:
                            raise InvalidUtilityCloudUserName("Invalid username format, please use your full email!")
                        except InvalidUtilityCloudUserName as e:
                            print(e)
                            self._logger.warning(e, exc_info=True)
                    if _email_check(user):
                        return user

        def _get_pass_loop():
            print(f"username: {user}")
            while True:
                password = getpass.getpass("Password: ")
                if password:
                    return password

        user = None
        password = None
        override_config_to_edit = False

        if kwargs:
            self._logger.debug("kwargs used in _get_uc_login.")
            if 'override_config_to_edit' in kwargs:
                override_config_to_edit = kwargs['override_config_to_edit']

        if not self.use_config or not self.config["AUTH"]["user"]:
            user = _get_user_loop()

        # if not self.use_config OR IF OVERRIDE_CONFIG_TO_EDIT IS TRUE
        if not self.use_config or override_config_to_edit:
            if not user:
                user = self.config['AUTH']["user"]
            else:
                self.config["AUTH"]["user"] = user
            password = _get_pass_loop()
            if password:
                if self.use_config:
                    self.config['AUTH']["password"] = password
                    user = self.config['AUTH']["user"]
                    if hasattr(self.config, "config_location"):
                        with open(self.config.config_location, 'w') as f:
                            self.config.write(f)
                    else:
                        self._logger.warning("Config could not be written to "
                                             "since there is no config.config_location parameter.")

        if self.use_config and not override_config_to_edit:
            if self.config and self.use_config:
                if not user:
                    user = self.config['AUTH']["user"]
                self.config["AUTH"]['user'] = user
                if self.user_email_suffix is not None and self.config['AUTH']["user"].endswith(self.user_email_suffix):
                    pass
                else:
                    if not user:
                        user = self.config['AUTH']["user"] + self.user_email_suffix
                try:
                    if not self.config['AUTH']["password"] or self.config['AUTH']["password"] == '':
                        self._get_uc_login(override_config_to_edit=True)
                    password = self.config['AUTH']["password"]
                except KeyError as e:
                    self._get_uc_login(override_config_to_edit=True)
                    password = self.config['AUTH']["password"]



            else:
                try:
                    raise MissingConfigError("self.Config must be set in order to use config file.")
                except MissingConfigError as e:
                    self._logger.error(e, exc_info=True)
                    raise e

        if user and password:
            return user, password
        else:
            try:
                raise AttributeError("Both user and password cannot be None.")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e

    def _InitAuth(self, **kwargs):
        def _runtype_read_logic():
            self._logger.info("attempting to read auth key")
            if (self.full_keypath.endswith("json") or
                    [x for x in self._config_suffixes if self._full_keypath.endswith(x)]):
                if isfile(self.full_keypath):
                    self._logger.info(f"{self.full_keypath} detected, reading.")
                    self.auth = self.ReadAuth(self._full_keypath)
                else:
                    self._logger.info(f"{self.full_keypath} not detected, attempting to request new auth.")
                    user, password = self._get_uc_login(use_config=self.use_config)
                    self.auth = self.ReqNewAuth(username=user, password=password)
            else:
                try:
                    raise FileNotFoundError(f"{self.full_keypath} could not be found.")
                except FileNotFoundError as e:
                    self._logger.error(e, exc_info=True)
                    raise e
            return self.auth

        def _runtype_req_logic():
            self._logger.info("requesting new auth key")
            if 'username' in credentials.keys() and 'password' in credentials.keys():
                self._logger.info("logging in with credentials")
                self.auth = self.ReqNewAuth(credentials['username'], credentials['password'])
            else:
                self._logger.info("logging in with credentials")
                user, password = self._get_uc_login(use_config=self.use_config)
                self.auth = self.ReqNewAuth(user, password)
            return self.auth

        runtype = None
        credentials = None
        if kwargs:
            if 'runtype' in kwargs or runtype is not None:
                runtype = kwargs['runtype']
                if runtype not in ['read', 'req_new']:
                    try:
                        raise AttributeError('runtype attribute not recognized')
                    except AttributeError as e:
                        self._logger.error(e, exc_info=True)
                        raise e
            else:
                try:
                    raise AttributeError('runtype attribute not given!')
                except AttributeError as e:
                    self._logger.error(e, exc_info=True)
                    raise e

            if 'credentials' in kwargs and isinstance(kwargs['credentials'], dict):
                credentials = kwargs['credentials']
            else:
                if runtype == 'read':
                    pass
                else:
                    try:
                        raise AttributeError(f'Credentials needed for runtype {runtype}')
                    except AttributeError as e:
                        self._logger.error(e, exc_info=True)
                        raise e

        self._logger.info(f"runtype detected as {runtype or 'runtype is None'}")

        if runtype == 'read':
            self.auth = _runtype_read_logic()

        elif runtype == 'req_new':
            self.auth = _runtype_req_logic()

        elif not runtype:
            self._logger.info("no runtype detected, defaulting to \'read\' mode.")
            self.auth = _runtype_read_logic()
        return self.auth

    def _key_dirpath_check(self):
        try:
            if not isdir(self._key_dirpath) and self._make_key_dirpath:
                makedirs(self._key_dirpath)
                self._logger.info(f"{self._key_dirpath} created.")
            elif isdir(self._key_dirpath):
                self._logger.info(f"{self._key_dirpath} detected.")
                pass
            else:
                try:
                    raise NotADirectoryError(f"{self._key_dirpath} does not exist, "
                                             f"and self._make_key_dirpath kwarg is set to false")
                except NotADirectoryError as e:
                    self._logger.error(e, exc_info=True)
                    raise e
        except TypeError as e:
            try:
                raise ValueError(f"_key_dirpath is {self._key_dirpath}, this folder cannot be created. "
                                 f"Please use the key_dirpath attribute if key_dirpath "
                                 f"is not part of your config file.") from None
            except ValueError as e:
                self._logger.error(e, exc_info=True)
                raise e

    @property
    def valid_key_filetypes(self):
        return self._valid_key_filetypes

    @valid_key_filetypes.getter
    def valid_key_filetypes(self):
        return self._valid_key_filetypes

    @valid_key_filetypes.setter
    def valid_key_filetypes(self, value):
        self._valid_key_filetypes = value

    @property
    def key_dirpath(self):
        return self._key_dirpath

    @key_dirpath.getter
    def key_dirpath(self):
        return self._key_dirpath

    @key_dirpath.setter
    def key_dirpath(self, value):
        self._key_dirpath = value

    @property
    def full_keypath(self):
        self._full_keypath = (join(self.key_dirpath, self._key_filename).replace("\\", "/")
                              + '.' + self._chosen_keyfile_format)
        return self._full_keypath

    def ReadAuth(self, key_path=None):
        def _load_auth(f_obj):
            if abspath(f_obj.name).split('.')[-1].lower() == 'json':
                loaded = jload(fp=f_obj)
                l_auth = eval(jdumps(loaded, indent=4))
                l_auth = l_auth['auth']
            elif abspath(f_obj.name).split('.')[-1].lower() in self._config_suffixes:
                # TODO: implement this
                try:
                    raise NotImplementedError("config is not implemented yet.")
                except NotImplementedError as e:
                    self._logger.error(e, exc_info=True)
                    raise e
            else:
                l_auth = f_obj.read()
            return l_auth

        if key_path:
            if isfile(key_path):
                with open(key_path) as f:
                    auth = _load_auth(f)
            else:
                user, password = self._get_uc_login(use_config=self.use_config)
                auth = self.ReqNewAuth(username=user, password=password)

        else:
            if isfile(self.full_keypath):
                if (not abspath(self.full_keypath).split('.')[-1]
                        or abspath(self.full_keypath).split('.')[-1] not in self.valid_key_filetypes):
                    with open(self.full_keypath) as f:
                        auth = _load_auth(f)
                else:
                    with open(self.full_keypath) as f:
                        auth = _load_auth(f)
            else:
                try:
                    raise FileNotFoundError("keypath file not found, try running ReqNewAuth method.")
                except FileNotFoundError as e:
                    self._logger.error(e, exc_info=True)
                    raise e
        return auth

    def ReqNewAuth(self, username: str, password: str, ):
        self._logger.info("Getting authentication token...")
        auth_url = join(self._auth_base_url, "api/authentication").replace("\\", "/")

        payload = jdumps({
            "UserName": username,
            "Password": password
        })
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json'
        }

        res = self.ER.MakeReq("POST", auth_url, headers, payload)

        auth = res.text

        self._WriteAuthToFile(file_type=self._chosen_keyfile_format, auth=auth)
        self._logger.info("Auth received, returning auth.")
        return auth

    def _WriteAuthToFile(self, file_type: str, auth: str = None, **kwargs):
        pw = None
        user = None

        if kwargs:
            if 'password' in kwargs:
                pw = kwargs['password']
            if 'username' in kwargs:
                user = kwargs['username']

        if file_type not in self.valid_key_filetypes:
            try:
                raise AttributeError(f"File type is not valid, use {self.valid_key_filetypes}")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e
        if auth:
            if self.full_keypath:
                pass
            with open(self.full_keypath, 'w') as f:
                if file_type == 'json':
                    auth_dict = {'auth': auth}
                    # this is where the auth file is written
                    jdump(obj=auth_dict, fp=f, indent=4)
                elif file_type == 'config':
                    try:
                        raise NotImplementedError("config portion is still in progress.")
                    except NotImplementedError as e:
                        self._logger.error(e, exc_info=True)
                        raise e
        else:
            if user and pw:
                auth = self.ReqNewAuth(password=pw, username=user)
                self._WriteAuthToFile('json', auth=auth)
            else:
                try:
                    raise AttributeError("User and password are required  if no auth is supplied.")
                except AttributeError as e:
                    self._logger.error(e, exc_info=True)
                    raise e

    def PurgeAuthkey(self, purge_age_minutes: int = 30):
        PS = PurgeSecrets(logger=self._logger, purge_age_minutes=purge_age_minutes)
        if PS.IsExpired(filepath=self._full_keypath):
            PS.PurgeFile()

    def PurgeAll(self, config_section_to_purge='AUTH',
                 config_fields_to_purge: list or None = None,
                 purge_age_minutes: int = 30):
        if config_fields_to_purge is None:
            config_fields_to_purge = ['user', 'password']
        PS = PurgeSecrets(logger=self._logger, purge_age_minutes=purge_age_minutes)
        PS.TotalPurge(self.config, self.config.config_location,
                      config_section_to_purge, config_fields_to_purge, filepath=self._full_keypath)


# noinspection SpellCheckingInspection
class UtilityCloudAPIWrapper(_UtilityCloudAuth):
    def __init__(self, base_url: str, **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url

        if self.config:
            self.config['DEFAULT']['base_url'] = self.base_url
            self._logger.info("Attempting to write base_url to config...")
            if hasattr(self.config, "config_location"):
                with open(self.config.config_location, 'w') as f:
                    self._logger.debug(f"Writing Config to {self.config.config_location}")
                    self.config.write(fp=f)
            else:
                self._logger.warning("Config could not be written to "
                                     "since there is no config.config_location parameter.")

        self.base_headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Authorization': self.auth
        }
        self.base_query = {
            "page": 1,
            "itemCount": "10",
            "Search": "",
            "SearchFacets": "",
            "orderby": None,
            "isAdvanced": True,
            "filters": None,
            "isactive": True,
            "facets": ""
        }

        self.account_id_dict = self._GetAssignedAccounts()
        self.valid_asset_search_facets = self._GetAssetBasicFilterSearchFacetsList()

    def _check_auth(self):
        if not self.auth_initialized:
            try:
                raise AuthenticationError("self.RunAuth must be run before making requests.")
            except AuthenticationError as e:
                self._logger.error(e, exc_info=True)
                raise e
        else:
            self.base_headers['Authorization'] = self.auth
            return

    def GetWorkOrderDetails(self, **kwargs):
        def _GetIDLoop():
            while True:
                wo_id = input("Please enter workorder ID: ")
                if wo_id.isnumeric():
                    return wo_id
                else:
                    pass

        self._check_auth()
        # TODO: generalize this down to else: work_order_id - _GetIDLoop()
        print_response = False
        payload = {}
        if kwargs:
            if 'workorderid' in kwargs:
                if isinstance(kwargs['workorderid'], int) or kwargs['workorderid'].isnumeric():
                    work_order_id = kwargs['workorderid']
                else:
                    try:
                        raise AttributeError("Work Order ID can contain numbers only.")
                    except AttributeError as e:
                        self._logger.error(e, exc_info=True)
                        raise e
            else:
                work_order_id = _GetIDLoop()

            if 'print_response' in kwargs:
                print_response = kwargs['print_response']
        else:
            work_order_id = _GetIDLoop()

        if work_order_id:
            wod_url = f"workorder?workorderid={work_order_id}"
            url = self.base_url + wod_url
            res = self.ER.MakeReq("GET", url, headers=self.base_headers, payload=payload)
            if print_response:
                print(jdumps(res.json(), indent=4))
        else:
            try:
                raise AttributeError("work_order_id cannot be None")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e

    def QueryWorkOrders(self, search_query: str = '', **kwargs):
        try:
            raise NotImplementedError("non functional, see TODOs/fixmes")
        except NotImplementedError as e:
            self._logger.error(e, exc_info=True)
            raise e
        self._check_auth()
        print_response = False
        query_url = self.base_url + "workorder/getworkorders"
        if kwargs:
            if 'query_dict' in kwargs:
                query_dict = kwargs['query_dict']
            else:
                query_dict = self.base_query
            if 'print_response' in kwargs:
                print_response = kwargs['print_response']
        else:
            query_dict = self.base_query
        # TODO: figure out how this works
        query_dict['Search'] = search_query
        # TODO: figure out why this times out. maybe needs a search query?
        query_dict['itemCount'] = '1'
        res = self.ER.MakeReq(method="post", url=query_url, headers=self.base_headers, payload=jdumps(query_dict))
        if print_response:
            print(jdumps(res.json(), indent=4))
        return res.json()

    def GetAssetsSearch(self, search_string: str, ** kwargs):
        self._check_auth()

        print_results = False
        item_count = None
        page = None

        if kwargs:
            if 'print_results' in kwargs:
                print_results = kwargs['print_results']
            if 'item_count' in kwargs:
                item_count = kwargs['item_count']
            if 'page' in kwargs:
                page = kwargs['page']

        search_url = self.base_url + "asset/getassets"

        self.base_query['SearchFacets'] = search_string

        if item_count:
            self.base_query['itemCount'] = str(item_count)
        if page:
            self.base_query['page'] = page

        res = self.ER.MakeReq("POST", search_url, headers=self.base_headers, payload=jdumps(self.base_query))

        if print_results:
            print(jdumps(res.json(), indent=4))
        return res.json()

    def _GetAssetBasicFilterSearchFacetsList(self, ** kwargs):
        self._check_auth()

        print_response = False
        payload = {}
        if kwargs:
            if 'print_response' in kwargs:
                print_response = kwargs['print_response']
        url = self.base_url + "asset/basicfilters"
        res = self.ER.MakeReq("get", url, self.base_headers, payload)
        if res.text == '' or res.text == {}:
            res = None
            return res
        if print_response:
            print(jdumps(res.json(), indent=4))
        return res.json()

    def GetAssetByID(self, **kwargs):
        def _GetIDLoop():
            while True:
                asset_id = input("Please enter Asset ID: ")
                if asset_id:#.isnumeric():
                    return asset_id
                else:
                    pass
        try:
            raise NotImplementedError("non functional, see TODOs/fixmes")
        except NotImplementedError as e:
            self._logger.error(e, exc_info=True)
            raise e
        self._check_auth()

        print_response = False
        payload = {}
        if kwargs:
            if 'assetid' in kwargs:
                if isinstance(kwargs['assetid'], int) or kwargs['assetid'].isnumeric():
                    asset_id = kwargs['assetid']
                else:
                    try:
                        raise AttributeError("Asset ID can contain numbers only.")
                    except AttributeError as e:
                        self._logger.error(e, exc_info=True)
                        raise e
            else:
                asset_id = _GetIDLoop()

            if 'print_response' in kwargs:
                print_response = kwargs['print_response']
        else:
            asset_id = _GetIDLoop()
        if asset_id:
            asset_url = f"api/asset/getassetbyid?assetid={asset_id}"
            url = self.base_url + asset_url
            # FIXME: this still doesnt seem to work
            get_asset_headers = {** self.base_headers, ** {'Credential': '', 'Signature': '',
                                                           'SignedHeaders': '', 'Date': ''}}
            res = self.ER.MakeReq("GET", url, get_asset_headers, payload=payload)
            if print_response:
                try:
                    print(jdumps(res.json(), indent=4))
                except requests.exceptions.JSONDecodeError as e:
                    self._logger.warning(e)
                    print(res.text)
        else:
            try:
                raise AttributeError("asset_id cannot be None")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e
        return res.json()

    def _GetAssignedAccounts(self, ** kwargs):
        self._check_auth()

        print_response = False
        payload = {}
        if kwargs:
            if 'print_response' in kwargs:
                print_response = kwargs['print_response']

        url = self.base_url + 'account/getaccounts'
        res = self.ER.MakeReq("GET", url, self.base_headers, payload)
        if res.text == '' or res.text == {}:
            res = None
            return res
        if print_response:
            print(jdumps(res.json(), indent=4))
        return res.json()

    def GetAssetClassByAccount(self, ** kwargs):
        def _GetIDLoop():
            while True:
                acc_id = input("Please enter Account ID: ")
                if acc_id:
                    return acc_id
                else:
                    pass

        self._check_auth()
        print_response = False
        payload = {}
        if kwargs:
            if 'accountid' in kwargs:
                account_id = kwargs['accountid']
            else:
                account_id = _GetIDLoop()

            if 'print_results' in kwargs:
                print_response = kwargs['print_results']
        else:
            account_id = _GetIDLoop()

        account_url = self.base_url + f'assetclass/getassetclassbyaccount?accountkey={account_id}'
        res = self.ER.MakeReq("get", account_url, self.base_headers, payload)

        if print_response:
            print(jdumps(res.json(), indent=4))
        return res.json()



