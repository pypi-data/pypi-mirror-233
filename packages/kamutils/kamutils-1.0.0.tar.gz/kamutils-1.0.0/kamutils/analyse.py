# Analyse and data handling module
# see docs. in Readme.md

#-----------------------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------------------

from collections import OrderedDict

class RangeSet:
    __slots__ = ('ranges')
    
    class Range:
        # ex_upper_bound : exclusive upper bound
        # upper_bound : inclusive upper bound
        __slots__ = ('lower_bound', 'upper_bound', 'ex_upper_bound', 'label')
        
        def __init__(self, lower_bound = None, upper_bound = None, ex_upper_bound = None, label = None):
            self.lower_bound = lower_bound
            self.upper_bound = upper_bound
            self.ex_upper_bound = ex_upper_bound
            self.label = label
            
        def  __repr__(self):
            return self.label
    
    def __init__(self,*args):
        key = 0
        # OrderedDict preserves the order in which the keys are inserted
        # OrderedDict allows to get ranges in ascending order with a simple loop over the keys
        self.ranges = OrderedDict()
        prev_upper_bound = None
        for arg in args:
            # Each argument can be :
            # - A single value which represents the upper bound of the interval
            # - A tuple or a list that contains the interval lower and upper bounds
            lower_bound = None
            upper_bound = None
            try:
                bound_idx = 0
                for value in arg:
                    if bound_idx == 0:
                        lower_bound = value
                    elif bound_idx == 1:
                        upper_bound = value
                        if (upper_bound < lower_bound):
                            raise Exception(f"{arg} : lower bound is greater than the upper bound")
                    else:
                        break # values beyond the second element are ignored
                    bound_idx += 1
                if bound_idx == 1:
                    # if there is only one bound defined, this is by default the upper bound
                    upper_bound = lower_bound
                    lower_bound = None
            except TypeError:
                # If the argument is not iterable, it's considered to be the interval upper bound
                upper_bound = arg
            if upper_bound is None:
                raise Exception(f"{arg} : upper bound is not defined")
            if (prev_upper_bound is not None) and (prev_upper_bound >= upper_bound):
                raise Exception(f"{arg} : upper bound should be greater than the previous range upper bound")
            if lower_bound is None:
                if prev_upper_bound is None:
                    label = f"<= {upper_bound}"
                else:
                    label = f"{prev_upper_bound}]..{upper_bound}]"
            else:
                if (prev_upper_bound is not None) and (prev_upper_bound > lower_bound):
                    raise Exception(f"{arg} : lower bound should be greater than or equal to the previous range upper bound")
                elif (prev_upper_bound is not None) and (prev_upper_bound == lower_bound):
                    # If this interval lower bound is equal to the previous interval upper bound, the lower bound is
                    # considered as exclusive because a value equal to it will be classified in the previous
                    # interval. This is equivalent to lower_bound == None
                    label = f"{lower_bound}]..{upper_bound}]"
                    lower_bound = None
                else:
                    # When the lower bound is defined, a previous interval is generated :
                    # - Either from - infinite to the lower bound if it's the first range
                    # - Or from the preceding interval upper bound to the lower bound
                    create_previous_range = True
                    if key == 0:
                        label = f"< {lower_bound}"
                    else:
                        # We dont create an intermediate interval like 'n]..[n' because n value will always 
                        # belong to the previous range
                        if self.ranges[key-1].upper_bound == lower_bound: 
                            create_previous_range = False
                        else:
                            label = f"{self.ranges[key-1].upper_bound}]..[{lower_bound}"
                    if create_previous_range:
                        self.ranges[key] = RangeSet.Range(None,None,lower_bound,label)
                        key += 1
                    label = f"[{lower_bound}..{upper_bound}]"
            self.ranges[key] = RangeSet.Range(lower_bound,upper_bound,None,label)
            prev_upper_bound = upper_bound
            key += 1
        if prev_upper_bound is None:
            raise Exception(f"{args} : empty RangeSet is not allowed")
        # Cration of an extra interval from upper bound to +infinity
        self.ranges[key] = RangeSet.Range(None,None,None,f"> {prev_upper_bound}")
        
    def  __repr__(self):
        r = ''
        for k,v in self.ranges.items():
            if len(r) > 0:
                r = f"{r}\n{k}:{v}"
            else:
                r = f"{k}:{v}"
        return r
    
    def label(self,level):
        return self.ranges[level].label

    def first_level(self):
        return 0
        
    def last_level(self):
        # next(reversed(odict)) returns the last (key, value) pair
        return next(reversed(self.ranges.items()))[0]
        
    def level(self,value):
        for key, range in self.ranges.items():
            if (range.upper_bound is not None) and (value <= range.upper_bound) and ((range.lower_bound is None) or (value >= range.lower_bound)):
                return key
            elif (range.ex_upper_bound is not None) and (value < range.ex_upper_bound) and ((range.lower_bound is None) or (value >= range.lower_bound)):
                return key
        # next(reversed(odict)) returns the last (key, value) pair
        return next(reversed(self.ranges.items()))[0]

