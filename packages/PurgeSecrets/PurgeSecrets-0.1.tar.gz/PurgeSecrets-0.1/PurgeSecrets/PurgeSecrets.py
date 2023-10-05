"""
PurgeSecrets.py

Easy deletion of INI/key etc files

"""

from datetime import timedelta, datetime
from logging import Logger
from os import stat, system, remove
from os.path import isfile
from time import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from configparser import ConfigParser


class FilepathNotDefined(Exception):
    ...


class PurgeSecrets:
    def __init__(self, logger: Logger = None, **kwargs):
        self._purge_age_minutes: int or None = None
        self._purge_age_hours: int or None = None
        self._purge_age_days: int or None = None
        self.filepath = None
        self._fail_silent = None

        if logger:
            self._logger = logger
        else:
            self._logger = Logger("DUMMY_LOGGER")

        if kwargs:
            self._kwargs = kwargs
            try:
                if 'purge_age_days' in self._kwargs:
                    self._purge_age_days: int = int(self._kwargs['purge_age_days'])
                if 'purge_age_hours' in self._kwargs:
                    self._purge_age_hours: int = int(self._kwargs['purge_age_hours'])
                if 'purge_age_minutes' in self._kwargs:
                    self._purge_age_minutes: int = int(self._kwargs['purge_age_minutes'])
                if 'fail_silent' in self._kwargs:
                    self._fail_silent = self._kwargs['fail_silent']
            except ValueError as e:
                self._logger.error(e, exc_info=True)
                raise e
        if any([self._purge_age_minutes, self._purge_age_hours, self._purge_age_days]):
            self._purge_age_minutes = self._ConvertAgeToMinutes()

    @staticmethod
    def _yn(question):
        while True:
            q = input(f"{question} (y/n/q): ").lower()
            if q == 'y':
                return True
            elif q == 'n':
                return False
            elif q == 'q':
                print("Ok Quitting!")
                system("pause")
                exit()
            else:
                pass

    def IsExpired(self, filepath):
        age_val = [x for x in self._kwargs if x.startswith('purge_age')]
        self._logger.debug('Checking for necessary arguments...')
        if age_val:
            self._logger.debug("argument found")
            pass
        else:
            try:
                raise AttributeError("At least one of the 'purge_age' instance attributes "
                                     "must be set in order to check for expiration.")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e
        self.filepath = filepath
        self._logger.info(f"Checking to see if {self.filepath} is expired.")

        file_age = self._GetFileAge()
        if file_age:
            if file_age >= self._purge_age_minutes:
                self._logger.info(f"{self.filepath} is expired")
                return True
            else:
                self._logger.info(f"{self.filepath} is NOT expired")
                return False
        else:
            self._logger.warning("no file_age available.")
            return False

    def _GetFileAge(self):

        if isfile(self.filepath):
            self._logger.info("Attempting to calculate file age.")
            # creation time in seconds
            c_time = datetime.fromtimestamp(stat(self.filepath).st_ctime).timestamp()
            # current time in seconds
            timestamp_now = datetime.fromtimestamp(time()).timestamp()
            # timedelta type file age (prints pretty)
            f_age = timedelta(seconds=(timestamp_now - c_time))
            # timedelta seconds divided into minutes
            f_age_minutes = f_age.seconds / 60
            return f_age_minutes
        else:
            try:
                raise FileNotFoundError(f"{self.filepath} does not exist")
            except FileNotFoundError as e:
                if self._fail_silent:
                    self._logger.warning(e)
                else:
                    self._logger.error(e, exc_info=True)
                    raise e

    def _ConvertAgeToMinutes(self):
        self._logger.debug("Converting given purge age to minutes")
        if self._purge_age_minutes:
            pass
        elif self._purge_age_hours:
            self._purge_age_minutes = self._purge_age_hours * 60
            self._logger.debug(f"converted {self._purge_age_hours} hours into {self._purge_age_minutes} minutes.")
        elif self._purge_age_days:
            self._purge_age_minutes = (self._purge_age_days * 24) * 60
            self._logger.debug(f"converted {self._purge_age_days} days into {self._purge_age_minutes} minutes.")
        else:
            try:
                raise AttributeError("all purge options cannot be None.")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e

        self._logger.debug(f"given purge age was converted to {self._purge_age_minutes} minutes.")
        return self._purge_age_minutes

    def _final_file_check(self):
        if self.filepath:
            final_file_check_text = f"Are you sure you want to purge {self.filepath}? (y/n/q): "
            purge = self._yn(final_file_check_text)
            return purge
        else:
            try:
                raise FilepathNotDefined("self.filepath is not defined. "
                                         "Expiration not determined (run self.IsExpired)")
            except FilepathNotDefined as e:
                self._logger.error(e, exc_info=True)
                raise e

    def PurgeFile(self):
        self._logger.info("Running final checks before file purge.")
        purge = self._final_file_check()
        if purge:
            try:
                remove(self.filepath)
                self._logger.info(f"{self.filepath} deleted.")
            except FileNotFoundError as e:
                if self._fail_silent:
                    self._logger.warning(e)
                    self._logger.warning(f"{self.filepath} was NOT PURGED")

                else:
                    self._logger.warning(f"{self.filepath} was NOT PURGED")
                    self._logger.error(e, exc_info=True)
                    raise e
        else:
            self._logger.warning(f"{self.filepath} was NOT PURGED")

    def PurgeINIValue(self, config: 'ConfigParser', config_path: str,
                      secrets_section: str, secrets_items: list):
        self._logger.info(f"attempting to purge [{secrets_section}]{secrets_items} from {config_path.split('/')[-1]}")
        for s in secrets_items:
            if config[secrets_section][s]:
                config[secrets_section][s] = ''
        final_config_text = (f"Are you sure you want to purge {secrets_section}, {secrets_items} items "
                             f"from {config_path.split('/')[-1]}?")
        purge = self._yn(final_config_text)
        if purge:
            with open(config_path, 'w') as f:
                config.write(f)
                self._logger.info(f"config file {secrets_section} section has been blanked.")
        else:
            self._logger.warning(f"config file {secrets_section} section has NOT been blanked.")

    def TotalPurge(self, config: 'ConfigParser', config_path: str,
                   secrets_section: str, secrets_items: list):
        if self._purge_age_minutes:
            self.PurgeFile()
        else:
            try:
                raise AttributeError("any purge age instance value must be supplied for TotalPurge to function.")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e
        self.PurgeINIValue(config, config_path, secrets_section, secrets_items)
        self._logger.info("self.TotalPurge complete.")
