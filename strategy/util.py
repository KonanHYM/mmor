# PyAlgoTrade
#
# Copyright 2011-2018 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import abc
import datetime

import six

from pyalgotrade.utils import dt
from pyalgotrade.utils import csvutils
from pyalgotrade.feed import memfeed


# Interface for csv row parsers.
@six.add_metaclass(abc.ABCMeta)
class RowParser(object):

    # Parses a row and returns a tuple with with two elements:
    # 1: datetime.datetime.
    # 2: dictionary or dict-like object.
    @abc.abstractmethod
    def parseRow(self, csvRowDict):
        raise NotImplementedError()

    # Returns a list of field names. If None, then the first row in the CSV should have the field names.
    @abc.abstractmethod
    def getFieldNames(self):
        raise NotImplementedError()

    # Returns the delimiter.
    @abc.abstractmethod
    def getDelimiter(self):
        raise NotImplementedError()


# Interface for bar filters.
@six.add_metaclass(abc.ABCMeta)
class RowFilter(object):

    @abc.abstractmethod
    def includeRow(self, dateTime, values):
        raise NotImplementedError()


class DateRangeFilter(RowFilter):
    def __init__(self, fromDate=None, toDate=None):
        self.__fromDate = fromDate
        self.__toDate = toDate

    def includeRow(self, dateTime, values):
        if self.__toDate and dateTime > self.__toDate:
            return False
        if self.__fromDate and dateTime < self.__fromDate:
            return False
        return True


class BaseFeed(memfeed.MemFeed):
    def __init__(self, rowParser, maxLen=None):
        super(BaseFeed, self).__init__(maxLen)

        self.__rowParser = rowParser
        self.__rowFilter = None

    def setRowFilter(self, rowFilter):
        self.__rowFilter = rowFilter

    def addValuesFromCSV(self, path):
        # Load the values from the csv file
        values = []
        reader = csvutils.FastDictReader(open(path, "r"), fieldnames=self.__rowParser.getFieldNames(), delimiter=self.__rowParser.getDelimiter())
        for row in reader:
            dateTime, rowValues = self.__rowParser.parseRow(row)
            if dateTime is not None and (self.__rowFilter is None or self.__rowFilter.includeRow(dateTime, rowValues)):
                values.append((dateTime, rowValues))

        self.addValues(values)


# This row parser doesn't support CSV files that have date and time in different columns.
class BasicRowParser(RowParser):
    def __init__(self, dateTimeColumn, dateTimeFormat, converter, delimiter=",", timezone=None):
        self.__dateTimeColumn = dateTimeColumn
        self.__dateTimeFormat = dateTimeFormat
        self.__converter = converter
        self.__delimiter = delimiter
        self.__timezone = timezone
        self.__timeDelta = None

    def parseRow(self, csvRowDict):
        dateTime = datetime.datetime.strptime(csvRowDict[self.__dateTimeColumn], self.__dateTimeFormat)
        # Localize the datetime if a timezone was given.
        if self.__timezone is not None:
            if self.__timeDelta is not None:
                dateTime += self.__timeDelta
            dateTime = dt.localize(dateTime, self.__timezone)
        # Convert the values
        values = {}
        for key, value in csvRowDict.items():
            if key != self.__dateTimeColumn:
                values[key] = self.__converter(key, value)
        return (dateTime, values)

    def getFieldNames(self):
        return None

    def getDelimiter(self):
        return self.__delimiter

    def setTimeDelta(self, timeDelta):
        self.__timeDelta = timeDelta


def float_or_string(column, value):
    return csvutils.float_or_string(value)
