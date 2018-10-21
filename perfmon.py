# Author: Travis Sun
# From: https://www.cac.cornell.edu/wiki/index.php?title=Performance_Data_Helper_in_Python_with_win32pdh
# ##### Concepts #####
# To use this library, you construct a query, to which you add counters. There are many counters available. You specify a counter with a path:

# #object# - These are registered with the operating system. Examples are 'Process', and 'System'.
# #counter# - An object contains several counters which can be monitored. For the Process object, this includes "% User Time" and "Working Set." (Note there are two uses of the word counter, one an object you add to a query, and another a string to specify part of the path.)
# #instance# - A Process object provides counters for all processes running on the system: csrss, lsass, wininit, cmd. Each of these processes is an example of an instance.
# #instance index# - Because instances are listed under a counter by their name, not PID, the instance index distinguishes among several instances with the same name.
# The full path of a counter includes the object, instance, index, and counter name: \Process(svchost#1)\IO Other Bytes/sec

from time import sleep
from win32pdh import *
##

class Counter(object):
    # The dwType field from GetCounterInfo returns the following, or'ed.
    # These come from WinPerf.h
    PERF_SIZE_DWORD         = 0x00000000
    PERF_SIZE_LARGE         = 0x00000100
    PERF_SIZE_ZERO          = 0x00000200  # for Zero Length fields
    PERF_SIZE_VARIABLE_LEN  = 0x00000300  # length is in CounterLength field
                                          #  of Counter Definition struct
    #
    #  select one of the following values to indicate the counter field usage
    #
    PERF_TYPE_NUMBER        = 0x00000000  # a number (not a counter)
    PERF_TYPE_COUNTER       = 0x00000400  # an increasing numeric value
    PERF_TYPE_TEXT          = 0x00000800  # a text field
    PERF_TYPE_ZERO          = 0x00000C00  # displays a zero
    #
    #  If the PERF_TYPE_NUMBER field was selected, then select one of the
    #  following to describe the Number
    #
    PERF_NUMBER_HEX         = 0x00000000  # display as HEX value
    PERF_NUMBER_DECIMAL     = 0x00010000  # display as a decimal integer
    PERF_NUMBER_DEC_1000    = 0x00020000  # display as a decimal/1000
    #
    #  If the PERF_TYPE_COUNTER value was selected then select one of the
    #  following to indicate the type of counter
    #
    PERF_COUNTER_VALUE      = 0x00000000  # display counter value
    PERF_COUNTER_RATE       = 0x00010000  # divide ctr / delta time
    PERF_COUNTER_FRACTION   = 0x00020000  # divide ctr / base
    PERF_COUNTER_BASE       = 0x00030000  # base value used in fractions
    PERF_COUNTER_ELAPSED    = 0x00040000  # subtract counter from current time
    PERF_COUNTER_QUEUELEN   = 0x00050000  # Use Queuelen processing func.
    PERF_COUNTER_HISTOGRAM  = 0x00060000  # Counter begins or ends a histogram
    #
    #  If the PERF_TYPE_TEXT value was selected, then select one of the
    #  following to indicate the type of TEXT data.
    #
    PERF_TEXT_UNICODE       = 0x00000000  # type of text in text field
    PERF_TEXT_ASCII         = 0x00010000  # ASCII using the CodePage field
    #
    #  Timer SubTypes
    #
    PERF_TIMER_TICK         = 0x00000000  # use system perf. freq for base
    PERF_TIMER_100NS        = 0x00100000  # use 100 NS timer time base units
    PERF_OBJECT_TIMER       = 0x00200000  # use the object timer freq
    #
    #  Any types that have calculations performed can use one or more of
    #  the following calculation modification flags listed here
    #
    PERF_DELTA_COUNTER      = 0x00400000  # compute difference first
    PERF_DELTA_BASE         = 0x00800000  # compute base diff as well
    PERF_INVERSE_COUNTER    = 0x01000000  # show as 1.00-value (assumes:
    PERF_MULTI_COUNTER      = 0x02000000  # sum of multiple instances
    #
    #  Select one of the following values to indicate the display suffix (if any)
    #
    PERF_DISPLAY_NO_SUFFIX  = 0x00000000  # no suffix
    PERF_DISPLAY_PER_SEC    = 0x10000000  # "/sec"
    PERF_DISPLAY_PERCENT    = 0x20000000  # "%"
    PERF_DISPLAY_SECONDS    = 0x30000000  # "secs"
    PERF_DISPLAY_NOSHOW     = 0x40000000  # value is not displayed

    def BuildCounter(obj, instance, instance_index, counter):
        path=MakeCounterPath((None,obj,instance,None,instance_index,counter),0)
        if ValidatePath(path) is 0:
            return Counter(path,obj,instance, instance_index, counter)
        return None
    BuildCounter = staticmethod(BuildCounter)
    
    def __init__(self,path, obj, instance, index, counter):
        self.__path = path
        self.__obj = obj
        self.__instance = instance
        self.__index = index
        self.__counter = counter
        self.__handle = None
        self.__info = None
        self.__type = None

    def addToQuery(self,query):
        self.__handle = AddCounter(query,self.__path)

    def getInfo(self):
        '''GetCounterInfo sometimes crashes in the wrapper code. Fewer crashes if 
        this is called after sampling data.'''
        if not self.__info:
            ci = GetCounterInfo( self.__handle, 0 )
            self.__info = {}
            self.__info['type']=ci[0]
            self.__info['version']=ci[1]
            self.__info['scale']=ci[2]
            self.__info['defaultScale']=ci[3]
            self.__info['userData']=ci[4]
            self.__info['queryUserData']=ci[5]
            self.__info['fullPath']=ci[6]
            self.__info['machineName']=ci[7][0]
            self.__info['objectName']=ci[7][1]
            self.__info['instanceName']=ci[7][2]
            self.__info['parentInstance']=ci[7][3]
            self.__info['instanceIndex']=ci[7][4]
            self.__info['counterName']=ci[7][5]
            self.__info['explainText']=ci[8]
        return self.__info
        
    def value(self):
        (counter_type, value) = GetFormattedCounterValue(self.__handle, PDH_FMT_DOUBLE)
        self.__type = counter_type
        return value

    def typeString(self):
        '''This string shows which bits are set in the dwType from PdhGetInfo.
        It can be used to format the counter.'''
        type=self.__getInfo()['type']
        type_list = []
        type_list.append(str(type))
        for member in self.____class__.__dict__.keys():
            if member.startswith("PERF_"):
                bit = getattr(self,member)
                if bit and bit&type:
                    type_list.append(member[5:])
        return " ".join(type_list)
        
    def __str__(self):
        return self.__path

class Query:
    def __init__(self):
        self.__query = OpenQuery()
        self.__counters = []

    def close_query(self):
        CloseQuery(self.__query)

    def add_counters(self, object_counter_list, instance_list):
        for (obj, counter_string) in object_counter_list:
            for instance in instance_list:
                instance_index = 0
                counter = Counter.BuildCounter(obj,instance,instance_index,counter_string)
                if counter:
                    # log
                    self.__counters.append(counter)
                    counter.addToQuery(self.__query)
                else:
                    # log
                    pass
    def ready_start(self):
        CollectQueryData(self.__query)

    def get_value(self):
        CollectQueryData(self.__query)
        return self.__counters

def get_obj_all_counters(obj):
    (counters, instances) = EnumObjectItems(None, None, obj, -1, 0)
    print('counters', counters)
    print('instances', instances)

if __name__ == '__main__':
    # get_obj_all_counters('Process')
    q1 = Query()
    q1.add_counters([('Process', '% Processor Time'), ('Process', 'Handle Count')], ['Moxy32', 'sqlservr'])
    q1.add_counters([('LogicalDisk','% Free Space')], ['C:',])

    q1.ready_start()
    sleep(2)
    counters = q1.get_value()
    for counter in counters:
        print (counter)
        print (counter.value())

    
