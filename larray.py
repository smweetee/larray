# -*- coding: utf8 -*-
"""
Matrix class
"""
#TODO
# * set

# * reshape / reshape_like

# * allow arithmetics between arrays with different axes order

# * implement named groups in strings
#   eg "vla=A01,A02;bru=A21;wal=A55,A56"

# * implement multi group in one axis getitem:
#   lipro['P01,P02;P05'] <=> (lipro.group('P01,P02'), lipro.group('P05'))
#                        <=> (lipro['P01,P02'], lipro['P05'])

# ? age, geo, sex, lipro = la.axes_names
#   => user only use axes strings and this allows them to not have to bother
#      about incompatible axes
#   => sadly, this prevents slicing axes (time[-10:])
#   => maybe la.axes should return another class (say GenericAxis) which only
#      contain a name, and can be "indexed"/sliced. No check that the key is
#      actually valid would be done until the valueGroup is actually used on
#      a specific LArray

# discuss VG with Geert:
# I do not "expand" key (eg :) upon group creation for perf reason
# VG[:] is much faster than [A01,A02,...,A99]
# I could make that all "contiguous" ranges are conv to slices (return views)
# but that might introduce confusing differences if they update/setitem their
# arrays

# ? keepdims=True instead of/in addition to group tuples
# * implement newaxis
# * smarter str() for large arrays
# * fix str() for 1D LArray
# * int labels
# * avg on last 10 years
#     time = Axis('time', ...)
#     x = time[-10:]  # <- does not work!
    # la[time[-10:]].avg(time)
    # la.append(la.avg(time[-10:]), axis=time)
    # la.append(time=la.avg(time[-10:]))
    # la.append(time=la.avg(time='-10:'))

# * reshape

# la.append(la.avg(time[-10:]), axis=time)

# la.avg(time[-10:])

# * drop last year
#   la = la[:,:,:,:,time[:-1]]
#   la = la.filter(time[:-1]) # <- implement this !
#   (equal to "la = la.filter(time=time[:-1])")
#   la = la.filter(geo='A25,A11')
#   la = la.filter(geo['A25,A11'])

# also for __getitem__
#   la = la[time[:-1]] # <- implement this !
#
# * split unit tests


# * easily add sum column for a dimension
#   - in all cases, we will need to define a new Axis object
#   - in the examples below, we suppose a.label is 'income'
#   - best candidates (IMO)
#       - a.append(age=a.sum(age))   # label is "income.sum(age)"
#                                    # ideally, it should be just "sum(age)"
#                                    # (the label on the array stays "income"
#                                    # after all, so it is redundant to add
#                                    # it here) but that is probably harder
#                                    # to get because a.sum(age).label should
#                                    # really be "income.sum(age)", it is just
#                                    # the label/tick on the new Axis that
#                                    # should not contain "income".
#       - a.append(age=a.sum(age).label('total'))  # label is "total"
#       - a.append(a.sum(age), axis=age)
#       - a.append_total(age)     # default aggregate is sum
#                                 # default label is "total"
#       - a.append_total(age=avg) # default aggregate is sum,
#       - a.append_total(age, sex=avg) # default aggregate is sum,

# other candidates
#   - a.with_total(age=np.sum)
#   - a.with_total(age=np.sum,np.avg) # potentially several totals
#   - a.append(age=a.sum(age))
#   - a.append(age='sum')
#   - a.append(age=sum)

#   - a.append(total=a.sum(age), axis=age) # total = the name of the new label
#   - a.append(age='total=sum') # total = the name of the new label

#   - the following should work already (modulo the axis name -> axis num)
#   - all_ages = a.sum(age=(':',))
#   - np.concatenate((a, all_ages), axis=age)

#   - np.append(a, a.sum(age), axis=age)
#   - a.append(a.sum(age), axis=age)

# * check axes on arithmetics
# * but special case for length 1 (to be able to do: "H + F" or "vla / belgium")

# * reindex a dataset (ie make it conform to the index of another dataset)
#   so that you can do operations involving both (add, divide, ...)

# * reorder an axis labels
# * modify read_csv format (last_column / time)
# * test to_csv: does it consume too much mem?
#   ---> test pandas (one dimension horizontally)
# * add labels in ValueGroups.__str__
# * xlsx export workbook without overwriting some sheets (charts)

# ? allow naming "one-shot" groups? e.g:
#   regsum = bel.sum(lipro='P01,P02 = P01P02; : = all')

# * review __getitem__ vs labels
#   o integer key on a non-integer label dimension is non-ambiguous:
#     => treat them like indices
#   o int key on in int label dimension is ambiguous:
#     => treat them like indices
#     OR
#     => treat them like values to lookup (len(key) has not relation with
#        len(dim) BUT if key is a tuple (nd-key), we have
#        len(dim0) == dim(dimX)
#   o bool key on a non-bool dimension is non-ambiguous:
#     - treat them as a filter (len(key) must be == len(dim))
#   o bool key on a bool dimension is ambiguous:
#     - treat them as a filter (len(key) must be == len(dim) == 2)
#       eg [False, True], [True, False], [True, True], [False, False]
#       >>> I think this usage is unlikely to be used by users directly but...
#     - treat them like a subset of values to include in the cartesian product
#       eg, supposing we have a array of shape (bool[2], int[110], bool[2])
#       the key ([False], [1, 5, 9], [False, True]) would return an array
#       of shape [1, 3, 2]
#     OR
#     - treat them like values to lookup (len(key) has not relation with
#       len(dim) BUT if key is a tuple (nd-key), we have len(dim0) == dim(dimX)
# * evaluate the impact of label-only __getitem__: numpy/matplotlib/...
#   functions probably rely on __getitem__ with indices

# * docstring for all methods
# * choose between subset and group. Having both is just confusing, I think.
# * check whether we could use np.array_repr/array_str (and
#   np.set_printoptions) instead of our own as_table/table2str
# * IO functions: csv/hdf/excel?/...?
#   >> needs discussion of the formats (users involved in the discussion?)
#      + check pandas dialects
# * better info()
#   ? make info a property?
#   * only display X label ticks by default (with an argument to display all)
#     eg 'A11' ... 'A93'
# * __setitem__
# * plotting (see plot.py)
#   >> check pandas API
# * implement iloc
# * implement more Axis functions:
#   - arithmetic operations: + -
#   - regexp functions: geo.group('A3*')
#   - sequence?: geo.seq('A31', 'A38')
#     this NOT exactly equivalent to geo['A31':'A38'] because the later
#     can contain A22 if it is defined between A31 and A38
# * re-implement row_totals/col_totals? or what do we do with them?
# * all the other TODO/XXX in the code
# * time specific API so that we know if we go for a subclass or not
# * check Collapse: is this needed? can't we generalize it?
# * data alignment in arithmetic methods (or at least check that axes are
#   compatible and raise an exception if they are not)
# * test structured arrays
# * review all method & argument names
# * implement ValueGroup.__getitem__
# ? allow __getitem__ with ValueGroups at any position since we know
#   which axis the ValueGroup correspond to. ie: allow bel[vla] even though
#   geo is not the first dimension of bel.
# ? move "utils" to its own project (so that it is not duplicated between
#   larray and liam2)
#   OR
#   include utils only in larray project and make larray a dependency of liam2
#   (and potentially rename it to reflect the broader scope)
# ? move "excelcom" to its own project (so that it is not duplicated between
#   potential projects using it)

# ? make pywin32 optional?
# ? implement dict-like behavior for LArray.axes (to be able to do stuff like
#   la.axes['sex'].labels
#

from itertools import product, chain, groupby
import string
import sys

import numpy as np
import pandas as pd

import tables

from utils import (prod, table2str, table2csv, table2iode, timed, unique,
                   array_equal, csv_open)

#TODO: return a generator, not a list
def srange(*args):
    return list(map(str, range(*args)))


def slice_to_str(key):
    """
    converts a slice to a string
    >>> slice_to_str(slice(None))
    ':'
    >>> slice_to_str(slice(24))
    ':24'
    >>> slice_to_str(slice(25, None))
    '25:'
    >>> slice_to_str(slice(5, 10))
    '5:10'
    >>> slice_to_str(slice(None, 5, 2))
    ':5:2'
    """
    # examples of result: ":24" "25:" ":" ":5:2"
    start = key.start if key.start is not None else ''
    stop = key.stop if key.stop is not None else ''
    step = (":" + str(key.step)) if key.step is not None else ''
    return '%s:%s%s' % (start, stop, step)


def to_label(v):
    """
    make it a string
    """
    #XXX: return the same string for list and tuples?
    if isinstance(v, slice):
        return slice_to_str(v)
    elif isinstance(v, list):
        if len(v) == 1:
            return str(v) + ','
        else:
            return ','.join(str(k) for k in v)
    else:
        return str(v)


def to_tick(e):
    """
    make it hashable, and acceptable as an ndarray element
    scalar & VG -> not modif
    slice -> 'start:stop'
    list -> 'v1,v2,v3'
    tuple -> '(v1, v2, v3)'
    other -> str(v)
    """
    # we need to either make all collections to ValueGroup (and keep VG as is)
    # or transform it to string, be we can't use to_tick(e.key) because that
    # can result in a tuple of value and array(['H', ('H', 'F')]) does not work
    if np.isscalar(e) or isinstance(e, ValueGroup):
        return e
    else:
        return to_label(e)


def to_labels(s):
    """
    Makes a (list of) value(s) usable as the collection of labels for an
    Axis (ie hashable). Strip strings, split them on ',' and translate
    "range strings" to real ranges **including the end point** !
    >>> to_labels('H , F')
    ['H', 'F']

    #XXX: we might want to return real int instead, because if we ever
    # want to have more complex queries, such as:
    # arr.filter(age > 10 and age < 20)
    # this would break for string values (because '10' < '2')
    >>> to_labels(':3')
    ['0', '1', '2', '3']
    """
    if isinstance(s, ValueGroup):
        # a single ValueGroup used for all ticks of an Axis
        raise NotImplemented("not sure what to do with it yet")
    elif isinstance(s, np.ndarray):
        #XXX: we assume it has already been translated. Is it a safe assumption?
        return s
    elif isinstance(s, (list, tuple)):
        return [to_tick(e) for e in s]
    elif sys.version >= '3' and isinstance(s, range):
        return list(s)

    numcolons = s.count(':')
    if numcolons:
        assert numcolons <= 2
        fullstr = s + ':1' if numcolons == 1 else s
        start, stop, step = [int(a) if a else None for a in fullstr.split(':')]
        if start is None:
            start = 0
        if stop is None:
            raise ValueError("no stop bound provided in range: %s" % s)
        stop += 1
        return srange(start, stop, step)
    else:
        return [v.strip() for v in s.split(',')]


def to_key(v):
    """
    Converts a value to a key usable for indexing (slice object, list of values,
    ...). Strings are split on ',' and stripped. Colons (:) are interpreted
    as slices. "int strings" are not converted to int.
    >>> to_key('a:c')
    slice('a', 'c', None)
    >>> to_key('a, b,c ,')
    ['a', 'b', 'c']
    >>> to_key('a,')
    ['a']
    >>> to_key(' a ')
    'a'
    >>> to_key(10)
    10
    """
    if isinstance(v, tuple):
        return list(v)
    elif not isinstance(v, str):
        return v

    numcolons = v.count(':')
    if numcolons:
        assert numcolons <= 2
        # can be of len 2 or 3 (if step is provided)
        bounds = [a if a else None for a in v.split(':')]
        return slice(*bounds)
    else:
        if ',' in v:
            # strip extremity commas to avoid empty string keys
            v = v.strip(',')
            return [v.strip() for v in v.split(',')]
        else:
            return v.strip()


def to_keys(s):
    # FIXME: fix doc: it does not accept only strings
    """
    converts a "family string" to its corresponding structure.
    It is only used for .sum(axis=xxx)
    'label' or ['l1', 'l2'] or [['l1', 'l2'], ['l3']]
    >>> to_keys('P01,P02')  # <-- one group => collapse dimension
    ['P01', 'P02']
    >>> to_keys(('P01,P02',))  # <-- do not collapse dimension
    (['P01', 'P02'],)
    >>> to_keys('P01;P02;:')
    ('P01', 'P02', slice(None, None, None))

    # >>> to_keys('P01,P02,:') # <-- INVALID !
    # it should have an explicit failure

    # we allow this, even though it is a dubious syntax
    >>> to_keys(('P01', 'P02', ':'))
    ('P01', 'P02', slice(None, None, None))

    # it is better to use explicit groups
    >>> to_keys(('P01,', 'P02,', ':'))
    (['P01'], ['P02'], slice(None, None, None))

    # or even the ugly duck...
    >>> to_keys((('P01',), ('P02',), ':'))
    (['P01'], ['P02'], slice(None, None, None))
    """
    if isinstance(s, str):
        if ';' in s:
            return tuple([to_key(group) for group in s.split(';')])
        else:
            # a single group => collapse dimension
            return to_key(s)
    elif isinstance(s, ValueGroup):
        return s
    elif isinstance(s, list):
        return to_key(s)
    else:
        assert isinstance(s, tuple)
        return tuple([to_key(group) for group in s])


def union(*args):
    #TODO: add support for ValueGroup and lists
    """
    returns the union of several "value strings" as a list
    """
    if args:
        return list(unique(chain(*(to_labels(arg) for arg in args))))
    else:
        return []


def range_to_slice(seq):
    """
    seq is a sequence-like (list, tuple or ndarray (*)) of integers
    returns a slice if possible (including for sequences of 1 element)
    otherwise returns the input sequence itself

    (*) isinstance(ndarray, Sequence) is False but it behaves like one
    """
    if len(seq) < 1:
        return seq
    first = seq[0]
    if len(seq) == 1:
        return slice(first, first + 1)
    second = seq[1]
    step = second - first
    prev_value = second
    for value in seq[2:]:
        if value != prev_value + step:
            return seq
        prev_value = value
    return slice(first, prev_value + step, step)


def larray_equal(first, other):
    return (first.axes == other.axes and
            np.array_equal(np.asarray(first), np.asarray(other)))


class Axis(object):
    # ticks instead of labels?
    #XXX: make name and labels optional?
    def __init__(self, name, labels):
        """
        labels should be an array-like (convertible to an ndarray)
        """
        self.name = name
        labels = to_labels(labels)

        #TODO: move this to to_labels????
        # we convert to an ndarray to save memory (for scalar ticks, for
        # ValueGroup ticks, it does not make a difference since a list of VG
        # and an ndarray of VG are both arrays of pointers)
        self.labels = np.asarray(labels)

        self._mapping = {label: i for i, label in enumerate(labels)}
        # we have no choice but to do that!
        # otherwise we could not make geo['Brussels'] work efficiently
        # (we could have to traverse the whole mapping checking for each name,
        # which is not an option)
        self._mapping.update({label.name: i for i, label in enumerate(labels)
                              if isinstance(label, ValueGroup)})

    #XXX: not sure I should offer an *args version. We should probably kill
    # this one and rename subset to group
    def group(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        if kwargs:
            raise ValueError("invalid keyword argument(s): %s"
                             % list(kwargs.keys()))
        key = args[0] if len(args) == 1 else args
        return self.subset(key, name)

    def subset(self, key, name=None):
        """
        key is label-based (slice and fancy indexing are supported)
        returns a ValueGroup usable in .sum or .filter
        """
        if isinstance(key, ValueGroup):
            if key.axis != self:
                raise ValueError("cannot subset an axis with a ValueGroup of "
                                 "an incompatible axis")
            return key
        return ValueGroup(key, name, self)

    def all(self, name=None):
        return self.subset(slice(None),
                           name=name if name is not None else "all")

    def subaxis(self, key, name=None):
        """
        key is label-based (slice and fancy indexing are supported)
        returns an Axis for a sub-array
        """
        if (isinstance(key, slice) and
                key.start is None and key.stop is None and key.step is None):
            return self
        # we must NOT modify the axis name, even though this creates a new axis
        # that is independent from the original one because the original
        # name is probably what users will want to use to filter
        if name is None:
            name = self.name
        return Axis(name, self.labels[self.translate(key)])

    def subaxis2(self, key, name=None):
        """
        key is index-based (slice and fancy indexing are supported)
        returns an Axis for a sub-array
        """
        if (isinstance(key, slice) and
                    key.start is None and key.stop is None and key.step is None):
            return self
        # we must NOT modify the axis name, even though this creates a new axis
        # that is independent from the original one because the original
        # name is probably what users will want to use to filter
        if name is None:
            name = self.name
        return Axis(name, self.labels[key])

    def __eq__(self, other):
        return (isinstance(other, Axis) and self.name == other.name and
                array_equal(self.labels, other.labels))

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, key):
        """
        key is a label-based key (slice and fancy indexing are supported)
        """
        return self.subset(key)

    def __contains__(self, key):
        return to_tick(key) in self._mapping

    def __hash__(self):
        return id(self)

    def translate(self, key):
        """
        translates a label key to its numerical index counterpart
        fancy index with boolean vectors are passed through unmodified
        """
        mapping = self._mapping

        # first, try the key as-is
        try:
            return mapping[key]
        except (KeyError, TypeError):
            pass

        if isinstance(key, ValueGroup):
            # return the index of all the elements in the group
            # the check made it fail
            # self is the aggregated axis, key.axis is the "original" geo axis
            key = key.key
            # if key.axis == self:
            #     key = key.key
            # else:
            #     raise ValueError("group %r cannot be used on axis %s"
            #                      % (key, self))

        # try again, before we munge the string
        # to support targeting a string-based aggregate with a VG
        # reg = x.sum(geo=(vla_str, wal_str, bru_str, belgium))
        # vla = geo.group(vla_str)
        # reg.filter(geo=vla)
        try:
            return mapping[key]
        except (KeyError, TypeError):
            pass

        if isinstance(key, str):
            key = to_key(key)

        if isinstance(key, slice):
            start = mapping[key.start] if key.start is not None else None
            # stop is inclusive in the input key and exclusive in the output !
            stop = mapping[key.stop] + 1 if key.stop is not None else None
            return slice(start, stop, key.step)
        elif isinstance(key, np.ndarray) and key.dtype.kind is 'b':
            return key
        elif isinstance(key, (tuple, list, np.ndarray)):
            # handle fancy indexing with a sequence of labels
            #TODO: the result should be cached
            res = np.empty(len(key), int)
            for i, label in enumerate(key):
                res[i] = mapping[label]
            return res
        else:
            assert np.isscalar(key), "%s (%s) is not scalar" % (key, type(key))
            # key is scalar (integer, float, string, ...)
            return mapping[key]

    def __str__(self):
        return self.name if self.name is not None else 'Unnamed axis'

    def __repr__(self):
        return 'Axis(%r, %r)' % (self.name, self.labels.tolist())


# We need a separate class for ValueGroup and cannot simply create a
# new Axis with a subset of values/ticks/labels: the subset of
# ticks/labels of the ValueGroup need to correspond to its *Axis*
# indices
class ValueGroup(object):
    def __init__(self, key, name=None, axis=None):
        """
        key should be either a sequence of labels, a slice with label bounds
        or a string
        axis, is only used to check the key and later to cache the translated
        key
        """
        self.key = key
        # we do NOT assign a name in all cases because that makes it
        # impossible to know whether a name was explicitly given or computed
        self.name = name

        #TODO: for performance reasons, we should cache the result. This will
        # need to be invalidated correctly
        # check the key is valid
        if axis is not None:
            axis.translate(key)
        self.axis = axis

    def __hash__(self):
        # to_tick & to_key are partially opposite operations but this
        # standardize on a single notation so that they can all target each
        # other. eg, this removes spaces in "list strings", instead of
        # hashing them directly
        #XXX: but we might want to include that normalization feature in
        # to_tick directly, instead of using to_key explicitly here
        return hash(to_tick(to_key(self.key)))

    def __eq__(self, other):
        # different name or axis compare equal !
        other_key = other.key if isinstance(other, ValueGroup) else other
        return to_tick(to_key(self.key)) == to_tick(to_key(other_key))

    def __str__(self):
        return to_label(self.key) if self.name is None else self.name

    def __repr__(self):
        name = ", %r" % self.name if self.name is not None else ''
        return "ValueGroup(%r%s)" % (self.key, name)


class LArray(np.ndarray):
    def __new__(cls, data, axes=None):
        obj = np.asarray(data).view(cls)
        ndim = obj.ndim
        if axes is not None:
            if len(axes) != ndim:
                raise ValueError("number of axes (%d) does not match "
                                 "number of dimensions of data (%d)"
                                 % (len(axes), ndim))
            shape = tuple(len(axis) for axis in axes)
            if shape != obj.shape:
                raise ValueError("length of axes %s does not match "
                                 "data shape %s" % (shape, obj.shape))

        if axes is not None and not isinstance(axes, list):
            axes = list(axes)
        obj.axes = axes
        return obj
    
    def as_dataframe(self):
        axes_labels = [a.labels.tolist() for a in self.axes[:-1]]
        axes_names = [a.name for a in self.axes[:-1]]
        axes_names[-1] = axes_names[-1] + '\\' + self.axes[-1].name
        columns = self.axes[-1].labels.tolist()
        full_index = list(product(*axes_labels))
        index = pd.MultiIndex.from_tuples(full_index, names=axes_names)
        return pd.DataFrame(self.reshape(len(full_index), len(columns)),
                            index, columns)

    def as_series(self):
        index = pd.MultiIndex.from_product([axis.labels for axis in self.axes],
                                           names=self.axes_names)
        return pd.Series(np.asarray(self).reshape(self.size), index)

    #noinspection PyAttributeOutsideInit
    def __array_finalize__(self, obj):
        # We are in the middle of the LabeledArray.__new__ constructor,
        # and our special attributes will be set when we return to that
        # constructor, so we do not need to set them here.
        if obj is None:
            return

        # obj is our "template" object (on which we have asked a view on).
        if isinstance(obj, LArray) and self.shape == obj.shape:
            # obj.view(LArray)
            # larr[:3]
            self.axes = obj.axes
        else:
            self.axes = None
            #self.row_totals = None
            #self.col_totals = None

    @property
    def axes_names(self):
        return [axis.name for axis in self.axes]

    def full_key(self, key):
        """
        Returns a full nd-key from a key in any of the following forms:
        a) a single value b) a tuple of values c) an {axis_name: value} dict
        """
        if isinstance(key, dict):
            axes_names = set(self.axes_names)
            for axis_name in key:
                if axis_name not in axes_names:
                    raise KeyError("{} is not an axis name".format(axis_name))
            key = tuple(key[axis.name] if axis.name in key else slice(None)
                        for axis in self.axes)
        elif not isinstance(key, tuple):
            # convert scalar keys to 1D keys
            key = (key,)

        # convert xD keys to ND keys
        if len(key) < self.ndim:
            key += (slice(None),) * (self.ndim - len(key))

        return key

    #XXX: we only need axes length, so we might want to move this out of the
    # class
    def cross_key(self, key, collapse_slices=False):
        """
        :param key: a complete (contains all dimensions) index-based key
        :param collapse_slices: convert contiguous ranges to slices
        :return: a key for indexing the cross product
        """
        # isinstance(ndarray, collections.Sequence) is False but it
        # behaves like one
        sequence = (tuple, list, np.ndarray)
        if collapse_slices:
            key = [range_to_slice(axis_key)
                   if isinstance(axis_key, sequence)
                   else axis_key
                   for axis_key in key]

        # count number of indexing arrays (ie non scalar/slices) in tuple
        num_ix_arrays = sum(isinstance(axis_key, sequence) for axis_key in key)
        num_scalars = sum(np.isscalar(axis_key) for axis_key in key)
        num_slices = sum(isinstance(axis_key, slice) for axis_key in key)
        assert len(key) == num_ix_arrays + num_scalars + num_slices

        # handle advanced indexing with more than one indexing array:
        # basic indexing (only integer and slices) and advanced indexing
        # with only one indexing array are handled fine by numpy
        if num_ix_arrays > 1 or (num_ix_arrays > 0 and num_scalars):
            # np.ix_ wants only lists so:

            # 1) transform scalar-key to lists of 1 element. In that case,
            #    ndarray.__getitem__ leaves length 1 dimensions instead of
            #    dropping them like we would like so we will need to drop
            #    them later ourselves (via reshape)
            noscalar_key = [[axis_key] if np.isscalar(axis_key) else axis_key
                            for axis_key in key]

            # 2) expand slices to lists (ranges)
            #TODO: cache the range in the axis?
            listkey = tuple(np.arange(*axis_key.indices(len(axis)))
                            if isinstance(axis_key, slice)
                            else axis_key
                            for axis_key, axis in zip(noscalar_key, self.axes))
            # np.ix_ computes the cross product of all lists
            return np.ix_(*listkey)
        else:
            return key

    def translated_key(self, key):
        return tuple(axis.translate(axis_key)
                     for axis, axis_key in zip(self.axes, key))

    def __getitem__(self, key, collapse_slices=False):
        data = np.asarray(self)

        translated_key = self.translated_key(self.full_key(key))

        axes = [axis.subaxis2(axis_key)
                for axis, axis_key in zip(self.axes, translated_key)
                if not np.isscalar(axis_key)]

        cross_key = self.cross_key(translated_key, collapse_slices)
        data = data[cross_key]
        # drop length 1 dimensions created by scalar keys
        data = data.reshape(tuple(len(axis) for axis in axes))
        return LArray(data, axes)

    def set(self, value, **kwargs):
        data = np.asarray(self)
        # expand string keys with commas
        #XXX: is it the right place to do this?
        key = tuple(to_key(axis_key) for axis_key in self.full_key(kwargs))
        translated_key = self.translated_key(key)
        cross_key = self.cross_key(translated_key, collapse_slices=True)
        data[cross_key] = value

    # deprecated since Python 2.0 but we need to define it to catch "simple"
    # slices (with integer bounds !) because ndarray is a "builtin" type
    def __getslice__(self, i, j):
        return self[slice(i, j)]

    def __str__(self):
        # return str(self.shape)
        if not self.ndim:
            return str(np.asscalar(self))
        else:
            return '\n' + table2str(self.as_table(), 'nan', True) + '\n'
    __repr__ = __str__

    def as_table(self):
        if not self.ndim:
            return []

        # ert    | unit | geo\time | 2012   | 2011   | 2010
        # NEER27 | I05  | AT       | 101.41 | 101.63 | 101.63
        # NEER27 | I05  | AU       | 134.86 | 125.29 | 117.08

        width = self.shape[-1]
        height = prod(self.shape[:-1])
        if self.axes is not None:
            axes_names = self.axes_names
            if len(axes_names) > 1:
                axes_names[-2] = '\\'.join(axes_names[-2:])
                axes_names.pop()
                
            axes_labels = [axis.labels for axis in self.axes]
        else:
            axes_names = None
            axes_labels = None

        if axes_names is not None:
            result = [axes_names + list(axes_labels[-1])]
            #if self.row_totals is not None:
            #    result[0].append('')
            #    result[1].append('total')
        else:
            result = []
        data = np.asarray(self).ravel()
        if axes_labels is not None:
            categ_values = list(product(*axes_labels[:-1]))
        else:
            categ_values = [[] for y in range(height)]
        #row_totals = self.row_totals
        for y in range(height):
            line = list(categ_values[y]) + \
                   list(data[y * width:(y + 1) * width])
            #if row_totals is not None:
            #    line.append(row_totals[y])
            result.append(line)
        #if self.col_totals is not None and self.ndim > 1:
        #    result.append([''] * (self.ndim - 2) + ['total'] + self.col_totals)
        return result

    #XXX: should filter(geo=['W']) return a view by default? (collapse=True)
    # I think it would be dangerous to make it the default
    # behavior, because that would introduce a subtle difference between
    # filter(dim=[a, b]) and filter(dim=[a]) even though it would be faster
    # and uses less memory. Maybe I should have a "view" argument which
    # defaults to 'auto' (ie collapse by default), can be set to False to
    # force a copy and to True to raise an exception if a view is not possible.
    def filter(self, collapse=False, **kwargs):
        """
        filters the array along the axes given as keyword arguments.
        The *collapse* argument determines whether consecutive ranges should
        be collapsed to slices, which is more efficient and returns a view
        (and not a copy) if possible (if all ranges are consecutive).
        Only use this argument if you do not intent to modify the resulting
        array, or if you know what you are doing.
        It is similar to np.take but works with several axes at once.
        """
        return self.__getitem__(kwargs, collapse)

    def _axis_aggregate(self, op, axes=()):
        """
        op is an aggregate function: func(arr, axis=(0, 1))
        axes is a tuple of axes (Axis objects or integers)
        """
        src_data = np.asarray(self)
        if not axes:
            # scalars don't need to be wrapped in LArray
            return op(src_data)

        axes_indices = tuple(self.get_axis_idx(a) for a in axes)
        res_data = op(src_data, axis=axes_indices)
        axes_tokill = set(axes_indices)
        res_axes = [axis for axis_num, axis in enumerate(self.axes)
                    if axis_num not in axes_tokill]
        return LArray(res_data, res_axes)

    def get_axis_idx(self, axis):
        """
        returns the index of an axis

        axis can be a name or an Axis object (or an index)
        if the Axis object is from another LArray, get_axis_idx will return the
        index of the local axis with the same name, whether it is compatible
        (has the same ticks) or not.
        """
        name_or_idx = axis.name if isinstance(axis, Axis) else axis
        axis_names = [a.name for a in self.axes]
        return axis_names.index(name_or_idx) \
            if isinstance(name_or_idx, str) \
            else name_or_idx

    def get_axis(self, axis, idx=False):
        """
        axis can be an index, a name or an Axis object
        if the Axis object is from another LArray, get_axis will return the
        local axis with the same name, **whether it is compatible (has the
        same ticks) or not**.
        """
        axis_idx = self.get_axis_idx(axis)
        axis = self.axes[axis_idx]
        return (axis, axis_idx) if idx else axis

    def _group_aggregate(self, op, items):
        res = self
        #TODO: when working with several "axes" at the same times, we should
        # not produce the intermediary result at all. It should be faster and
        # consume a bit less memory.
        for axis, groups in items:
            groups = to_keys(groups)

            axis, axis_idx = res.get_axis(axis, idx=True)
            res_axes = res.axes[:]
            res_shape = list(res.shape)

            if not isinstance(groups, tuple):
                # groups is in fact a single group
                assert isinstance(groups, (str, slice, list,
                                           ValueGroup)), type(groups)
                if isinstance(groups, list):
                    assert len(groups) > 0

                    # Make sure this is actually a single group, not multiple
                    # mistakenly given as a list instead of a tuple
                    assert all(not isinstance(g, (tuple, list)) for g in groups)

                groups = (groups,)
                del res_axes[axis_idx]

                # it is easier to kill the axis after the fact
                killaxis = True
            else:
                # convert all value groups to strings
                # groups = tuple(str(g) if isinstance(g, ValueGroup) else g
                #                for g in groups)
                # grx = tuple(g.key if isinstance(g, ValueGroup) else g
                #             for g in groups)

                # We do NOT modify the axis name (eg append "_agg" or "*") even
                # though this creates a new axis that is independent from the
                # original one because the original name is what users will
                # want to use to access that axis (eg in .filter kwargs)
                res_axes[axis_idx] = Axis(axis.name, groups)
                killaxis = False

            res_shape[axis_idx] = len(groups)
            res_data = np.empty(res_shape, dtype=res.dtype)

            group_idx = [slice(None) for _ in res_shape]
            for i, group in enumerate(groups):
                group_idx[axis_idx] = i

                # we need only lists of ticks, not single ticks, otherwise the
                # dimension is discarded too early (in filter instead of in the
                # aggregate func)
                group = [group] if group in axis else group

                arr = res.filter(collapse=True, **{axis.name: group})
                arr = np.asarray(arr)
                op(arr, axis=axis_idx, out=res_data[group_idx])
                del arr
            if killaxis:
                assert group_idx[axis_idx] == 0
                res_data = res_data[group_idx]
            res = LArray(res_data, res_axes)
        return res

    def _aggregate(self, op, args, kwargs, commutative=False):
        if not commutative and len(kwargs) > 1:
            raise ValueError("grouping aggregates on multiple axes at the same "
                             "time using keyword arguments is not supported "
                             "for '%s' (because it is not a commutative"
                             "operation and keyword arguments are *not* "
                             "ordered in Python)" % op.__name__)

        # Sort kwargs by axis name so that we have consistent results
        # between runs because otherwise rounding errors could lead to
        # slightly different results even for commutative operations.

        #XXX: transform kwargs to ValueGroups? ("geo", [1, 2]) -> geo[[1, 2]]
        operations = list(args) + sorted(kwargs.items())
        if not operations:
            # op() without args is equal to op(all_axes)
            return self._axis_aggregate(op)

        def isaxis(a):
            return isinstance(a, (int, str, Axis))

        res = self
        # group consecutive same-type (group vs axis aggregates) operations
        for are_axes, axes in groupby(operations, isaxis):
            func = res._axis_aggregate if are_axes else res._group_aggregate
            res = func(op, axes)
        return res

    def copy(self):
        return LArray(np.ndarray.copy(self), axes=self.axes[:])
    
    def zeros_like(self):
        return LArray(np.zeros_like(np.asarray(self)), axes=self.axes[:])
    
    def info(self):
        def shorten(l):
            return l if len(l) < 7 else l[:3] + ['...'] + list(l[-3:])
        axes_labels = [' '.join(shorten([repr(l) for l in axis.labels]))
                       for axis in self.axes]
        lines = [" %s [%d]: %s" % (axis.name, len(axis), labels)
                 for axis, labels in zip(self.axes, axes_labels)]
        shape = " x ".join(str(s) for s in self.shape)
        return '\n'.join([shape] + lines)

    def ratio(self, *axes):
        if not axes:
            axes = self.axes
        return np.nan_to_num(self / self.sum(*axes))

    # aggregate method factory
    def agg_method(npfunc, name=None, commutative=False):
        def method(self, *args, **kwargs):
            return self._aggregate(npfunc, args, kwargs,
                                   commutative=commutative)
        if name is None:
            name = npfunc.__name__
        method.__name__ = name
        return method

    all = agg_method(np.all, commutative=True)
    any = agg_method(np.any, commutative=True)
    # commutative modulo float precision errors
    sum = agg_method(np.sum, commutative=True)
    prod = agg_method(np.prod, commutative=True)
    cumsum = agg_method(np.cumsum, commutative=True)
    cumprod = agg_method(np.cumprod, commutative=True)
    min = agg_method(np.min, commutative=True)
    max = agg_method(np.max, commutative=True)
    mean = agg_method(np.mean, commutative=True)
    # not commutative
    ptp = agg_method(np.ptp)
    var = agg_method(np.var)
    std = agg_method(np.std)

    def append(self, **kwargs):
        label = kwargs.pop('label', None)
        # It does not make sense to accept multiple axes at once, as "values"
        # will not have the correct shape for all axes after the first one.
        #XXX: Knowing that, it might be better to use a required (non kw) axis
        # argument, but it would be inconsistent with filter and sum.
        # It would look like: la.append(lipro, la.sum(lipro), label='sum')
        if len(kwargs) > 1:
            raise ValueError("Cannot append to several axes at the same time")
        axis_name, values = list(kwargs.items())[0]
        axis, axis_idx = self.get_axis(axis_name, idx=True)
        shape = self.shape
        values = np.asarray(values)
        if values.shape == shape[:axis_idx] + shape[axis_idx+1:]:
            # adding a dimension of size one if it is missing
            new_shape = shape[:axis_idx] + (1,) + shape[axis_idx+1:]
            values = values.reshape(new_shape)
        data = np.append(np.asarray(self), values, axis=axis_idx)
        new_axes = self.axes[:]
        new_axes[axis_idx] = Axis(axis.name, np.append(axis.labels, label))
        return LArray(data, axes=new_axes)

    def extend(self, axis, other):
        axis, axis_idx = self.get_axis(axis, idx=True)
        # Get axis by name, so that we do *NOT* check they are "compatible",
        # because it makes sense to append axes of different length
        other_axis = other.get_axis(axis)

        data = np.append(np.asarray(self), np.asarray(other), axis=axis_idx)
        new_axes = self.axes[:]
        new_axes[axis_idx] = Axis(axis.name,
                                  np.append(axis.labels, other_axis.labels))
        return LArray(data, axes=new_axes)

    #XXX: sep argument does not seem very useful
    #XXX: use pandas function instead?
    def to_excel(self, filename, sep=None):
        # Why xlsxwriter? Because it is faster than openpyxl and xlwt
        # currently does not .xlsx (only .xls).
        # PyExcelerate seem like a decent alternative too
        import xlsxwriter as xl

        if sep is None:
            sep = '_'
            #sep = self.sep
        workbook = xl.Workbook(filename)
        if self.ndim > 2:
            for key in product(*[axis.labels for axis in self.axes[:-2]]):
                sheetname = sep.join(str(k) for k in key)
                # sheet names must not:
                # * contain any of the following characters: : \ / ? * [ ]
                #XXX: this will NOT work for unicode strings !
                sheetname = sheetname.translate(string.maketrans('[:]', '(-)'),
                                                r'\/?*') # chars to delete
                # * exceed 31 characters
                # sheetname = sheetname[:31]
                # * be blank
                assert sheetname, "sheet name cannot be blank"
                worksheet = workbook.add_worksheet(sheetname)
                worksheet.write_row(0, 1, self.axes[-1].labels) 
                worksheet.write_column(1, 0, self.axes[-2].labels)                    
                for row, data in enumerate(np.asarray(self[key])):
                    worksheet.write_row(1+row, 1, data)                    
                     
        else:
            worksheet = workbook.add_worksheet('Sheet1')
            worksheet.write_row(0, 1, self.axes[-1].labels) 
            if self.ndim == 2:
                worksheet.write_column(1, 0, self.axes[-2].labels)
            for row, data in enumerate(np.asarray(self)):
                worksheet.write_row(1+row, 1, data)                    

    def transpose(self, *args):
        axes = [self.get_axis(a) for a in args]
        axes_names = set(axis.name for axis in axes)
        missing_axes = [axis for axis in self.axes
                        if axis.name not in axes_names]
        res_axes = axes + missing_axes
        axes_indices = [self.get_axis_idx(axis) for axis in res_axes]
        src_data = np.asarray(self)
        res_data = src_data.transpose(axes_indices)
        return LArray(res_data, res_axes)
    #XXX: is this necessary?
    reorder = transpose

    def ToCsv(self, filename):
        res = table2csv(self.as_table(), ',', 'nan')
        f = open(filename, "w")
        f.write(res)

    def Collapse(self, filename):
        res = table2csv(self.as_table(), ',', 'nan', self.dimcount)
        f = open(filename, "w")
        f.write(res)

    def ToAv(self, filename):
        res = table2iode(self.as_table(), self.samplestr, self.dimcount, '_',
                         'nan')
        f = open(filename, "w")
        f.write(res)
        
    def plot(self):
        self.as_dataframe().plot()


def parse(s):
    #parameters can be strings or numbers
    if isinstance(s, str):
        s = s.lower()
        if s in ('0', '1', 'false', 'true'):
            return s in ('1', 'true')
        elif s.isdigit():
            return int(s)
        else:
            try:
                return float(s)
            except ValueError:
                return s
    else:
        return s


def df_aslarray(df, na=np.nan):
    if isinstance(df.index, pd.core.index.MultiIndex):
        axes_labels = [list(unique(level[labels]))
                       for level, labels
                       in zip(df.index.levels, df.index.labels)]
        axes_names = list(df.index.names)
        laxis = axes_names[-1].split('\\')
        if len(laxis) > 0:
            axes_names[-1] = laxis[0]
        axes = [Axis(name, labels)
                for name, labels in zip(axes_names, axes_labels)]
        # pandas treats the "time" labels as column names (strings) so we need
        # to convert them to values
        if len(laxis) > 0:
            axes_names[-1] = laxis[0]
            axes.append(Axis(laxis[1],
                             [parse(cell) for cell in df.columns.values]))
        else:
            axes.append(Axis('time',
                             [parse(cell) for cell in df.columns.values]))
        sdf = df.reindex([i for i in product(*axes_labels)], df.columns.values)
        if na != np.nan:
            sdf.fillna(na,inplace=True)
        data = sdf.values.reshape([len(axis.labels) for axis in axes])    
        return LArray(data, axes) 
    elif isinstance(df.index, pd.core.index.Index):        
        labels = [l for l in df.index]
        axes_names = list(df.index.names)
        laxis = axes_names[-1].split('\\')                                                       
        if len(laxis) > 0:
            axes_names[-1] = laxis[0]        
        axes = [Axis(axes_names[0], labels)]
        # pandas treats the "time" labels as column names (strings) so we need to
        # convert them to values
        if len(laxis) > 0:
            axes.append(Axis(laxis[1],
                             [parse(cell) for cell in df.columns.values]))
        else:
            axes.append(Axis('time',
                             [parse(cell) for cell in df.columns.values]))
#        sdf = df.reindex([i for i in product(*axes_labels)], df.columns.values)
#        if na != np.nan:
#            sdf.fillna(na,inplace=True)
#        data = sdf.values.reshape([len(axis.labels) for axis in axes])    
        data = df.values
        return LArray(data, axes) 
    else:
        return None


# CSV functions
def read_csv(filepath, nb_index=0, index_col=[], sep=',', na=np.nan):  
    import csv
    """
    reads csv file and returns an Larray with the contents
        nb_index: number of leading index columns (ex. 4)
    or 
        index_col : list of columns for the index (ex. [0, 1, 2, 3])
    
    format csv file:
    arr,ages,sex,nat\time,1991,1992,1993
    A1,BI,H,BE,1,0,0
    A1,BI,H,FO,2,0,0
    A1,BI,F,BE,0,0,1
    A1,BI,F,FO,0,0,0
    A1,A0,H,BE,0,0,0

    """    
    # read the first line to determine how many axes (time excluded) we have
    with csv_open(filepath) as f:
        reader = csv.reader(f, delimiter=sep)
        header = [parse(cell) for cell in next(reader)]
        axes_names = [cell for cell in header if isinstance(cell, str)]

    if len(index_col) == 0 and nb_index == 0:
        nb_index = len(axes_names)

    if len(index_col) > 0:
        nb_index = len(index_col)
    else:
        index_col = list(range(nb_index))

    # force str for dimensions
    dtype = {}
    for axis in axes_names[:nb_index]:
        dtype[axis] = np.str
    df = pd.read_csv(filepath, index_col=index_col, sep=sep, dtype=dtype)
    return df_aslarray(df.reindex_axis(sorted(df.columns), axis=1), na)


def save_csv(l_array, filepath, sep=',', na_rep='', transpose=True):
    """
    saves an LArray to a csv file
    """
    if transpose:
        df = l_array.as_dataframe()
        df.to_csv(filepath, sep=sep, na_rep=na_rep)
    else:
        s = l_array.as_series()
        s.to_csv(filepath, sep=sep, na_rep=na_rep, header=True)


# HDF5 functions
def save_h5(l_array, name, filepath):
    """
    save a l_array to a h5-store using the specified name
    """
    df = l_array.as_dataframe()
    store = pd.HDFStore(filepath)
    store.put(name, df)
    store.close()    
    

def read_h5(name, filepath):
    """
    read a l_array from a h5-store with the specified name
    """
    store = pd.HDFStore(filepath)
    df = store.get(name)
    store.close()
    return df_aslarray(df)


def SaveMatrices(h5_filename):
    try:
        h5file = tables.openFile(h5_filename, mode="w", title="IodeMatrix")
        matnode = h5file.createGroup("/", "matrices", "IodeMatrices")
        d = sys._getframe(1).f_locals
        for k, v in d.items():
            if isinstance(v, LArray):
                # print "storing %s %s" % (k, v.info())
                disk_array = h5file.createArray(matnode, k, v.matdata, k)
                attrs = disk_array.attrs
                attrs._dimensions = np.array(v.dimnames)
                attrs._sep = v.sep
                attrs._sample = np.array(v.samplestr)
                attrs._t = np.array(v.samplelist)
                attrs.shape = np.array(v.matrixshape())
                for i, dimlist in enumerate(v.dimlist):
                    setattr(attrs, '%s' %v.dimnames[i], np.array(v.dimlist[i]))
    finally:
        h5file.close()


def ListMatrices(h5_filename):
    try:
        h5file = tables.openFile(h5_filename, mode="r")
        h5root = h5file.root
        if 'matrices' not in h5root:
            raise Exception('could not find any matrices in the input data file')
        matnames = [mat.name for mat in h5root.matrices]
    finally:
        h5file.close()
        return matnames


def LoadMatrix(h5_filename, matname):
    try:
        h5file = tables.openFile(h5_filename, mode="r")
        h5root = h5file.root
        if 'matrices' not in h5root:
            #raise Exception('could not find any matrices in the input data file')
            # print 'could not find any matrices in the input data file'
            return None
        if matname not in [mat.name for mat in h5root.matrices]:
            #raise Exception('could not find %s in the input data file' % matname)
            # print 'could not find %s in the input data file' % matname
            return None
        mat = getattr(h5root.matrices, matname)
        dimnames = list(mat.attrs._dimensions)
        dimlist = [list(mat.getAttr('%s' % name)) for name in dimnames]
        axes = [Axis(name, labels) for name, labels in zip(dimnames, dimlist)]
        axes.append(Axis('time', list(mat.attrs._t)))
        data = timed(mat.read)
        return LArray(data, axes)
    finally:
        h5file.close()


# EXCEL functions
def save_excel(l_array, name, filepath):
    """
    saves an LArray to the sheet name in the file: filepath
    """
    df = l_array.as_dataframe()
    writer = pd.ExcelWriter(filepath)
    df.to_excel(writer, name)
    writer.save()


def read_excel(name, filepath, nb_index=0, index_col=[]):
    """
    reads excel file from sheet name and returns an Larray with the contents
        nb_index: number of leading index columns (ex. 4)
    or 
        index_col : list of columns for the index (ex. [0, 1, 2, 3])    
    """    
    if len(index_col) > 0:
        df = pd.read_excel(filepath, name, index_col=index_col)
    else:
        df = pd.read_excel(filepath, name, index_col=list(range(nb_index)))
    return df_aslarray(df.reindex_axis(sorted(df.columns), axis=1))     


def zeros(axes):
    s = tuple(len(axis) for axis in axes)
    return LArray(np.zeros(s), axes)  


# def ArrayAssign(larray, larray_new, **kwargs):
#     data, full_key = fullkey(larray, full_idx)
#     #DIFFERENT SHAPE BUT SAME SIZE
#     if (data[full_key].shape != larray_new.shape) and \
#             (data[full_key].size == larray_new.size):
#         data[full_key] = np.asarray(larray_new).reshape(data[full_key].shape)
#         return
#
#     #DIFFERENT SHAPE BUT ONLY ONE OR MORE MISSING DIMENSION(S)
#     if len(data[full_key].shape) != len(larray_new.shape):
#         bshape = broadcastshape(larray_new.shape, data[full_key].shape)
#         if bshape is not None:
#             data[full_key] = np.asarray(larray_new).reshape(bshape)
#         return
#
#     # SAME DIMENSIONS
#     data[full_key] = np.asarray(larray_new)


def broadcastshape(oshape, nshape):
    bshape = list(nshape)
    dshape = set(nshape).difference(set(oshape))
    if len(dshape) == len(nshape)-len(oshape):
        for i in range(len(bshape)):
            if bshape[i] in dshape:
                bshape[i] = 1        
        return tuple(bshape)
    else:
        return None    
