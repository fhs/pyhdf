# $Id: parse_odl.py,v 1.1 2008-06-30 02:41:45 gosselin_a Exp $
# $Log: not supported by cvs2svn $
#
#
""" Tools for parsing the Object Description Language (ODL) used to provide
metadata in many HDF formats.

Maintainer:     Enthough, Inc.
                Austin, TX
                enthought-dev@mail.enthought.com
"""

import datetime
import pprint

import pyparsing as p

__all__ = ['parse_odl']

strptime = datetime.datetime.strptime
keywords = """object_kw begin_object begin_group end_object group end_group
end""".upper().split()

class Bunch(dict):
    """ Provide convenient attribute access to dictionaries with string keys.
    """
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    #def __repr__(self):
    #    return '%s(%s)' % (self.__class__.__name__, pprint.pformat(self.copy()))

class UnittedValue(object):
    """ Represent a numeric value with units.

    This does no interpretation or unit algebra, it simply keeps the two pieces
    of data together.
    """
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __repr__(self):
        name = self.__class__.__name__
        return '%s(%r, %r)' % (name, self.value, self.unit)

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, other):
        if not hasattr(other, 'key'):
            return False
        else:
            return self.key() == other.key()

    def __ne__(self, other):
        return not (self == other)

    def key(self):
        return (self.__class__.__name__, self.value, self.unit)

    @classmethod
    def possibly_unitted(cls, value, unit=None):
        if unit is None:
            return value
        else:
            return cls(value, unit)

# TODO: other-bases
#I think the thing is just that this only
uint = p.Word(p.nums)
sign = p.oneOf('+ -')
integer = p.Optional(sign) + uint
unscaled_real = p.Combine(p.Optional(p.Word(p.nums)) + '.' + p.Word(p.nums))
exponent = p.CaselessLiteral('E') + integer
scaled_real = p.Combine(unscaled_real + p.Optional(exponent))
real = p.Combine(p.Optional(sign) + (scaled_real | unscaled_real))

def myint(toks):
    return int(toks[0])
def myfloat(toks):
    return float(toks[0])

# Dates.
year_month_day = p.Combine(uint+'-'+uint+'-'+uint).setParseAction(
    lambda t: strptime(t[0], '%Y-%m-%d').date())
year_doy = p.Combine(uint+'-'+uint).setParseAction(
    lambda t: strptime(t[0], '%Y-%j').date())
date = year_month_day | year_doy

# Times.  In Coordinated Universal Time (UTC time)
second = unscaled_real | uint
zone_offset = p.Combine(sign + uint + ':' + uint)
hour_min_sec = (
    uint.setParseAction(myint) +
    p.Suppress(':') +
    uint.setParseAction(myint) +
    p.Optional(p.Suppress(':') + uint.setParseAction(myint))
)
# TODO: non-UTC time.
utc_time = (hour_min_sec + p.Suppress('Z')).setParseAction(lambda t: datetime.time(*t))
#zoned_time = p.Combine(hour_min_sec + zone_offset)
#local_time = hour_min_sec
time = utc_time
date_time = (date + 'T' + time).setParseAction(lambda t: datetime.datetime.combine(t[0], t[1]))

# Text.
# TODO: technically, we should allow newlines in quoted_text, but I don't see
# any examples of such in the ASTER data.
object_kw = p.CaselessKeyword('object')
begin_object = p.CaselessKeyword('begin_object')
begin_group = p.CaselessKeyword('begin_group')
end_object = p.CaselessKeyword('end_object')
group = p.CaselessKeyword('group')
end_group = p.CaselessKeyword('end_group')
end = p.CaselessKeyword('end')
quoted_text = p.dblQuotedString.setParseAction(lambda t: t[0][1:-1].decode('string-escape'))
symbol = p.sglQuotedString.setParseAction(lambda t: t[0][1:-1].decode('string-escape'))

def validate_identifier(t):
    if t[0] in keywords:
        raise p.ParseException("%r is a keyword" % t[0])

identifier = p.Word(p.alphas, '_'+p.alphanums).setParseAction(
    p.upcaseTokens, validate_identifier)

# Values.
units_factor = p.Combine(identifier + p.Optional('**' + integer))
units_expression = p.Combine(p.Suppress('<') + units_factor
    + p.ZeroOrMore(p.oneOf('* /') + units_factor) + p.Suppress('>'))
# TODO: based integers.
numeric = (((real.setParseAction(myfloat)|integer.setParseAction(myint)).setResultsName('value')
    + p.Optional(units_expression).setResultsName('unit'))).setParseAction(
        lambda t: UnittedValue.possibly_unitted(*t))
symbolic = identifier | symbol
scalar = date_time | numeric | quoted_text | symbolic
sequence_1d = p.Group(p.Suppress('(') + p.delimitedList(scalar)
    + p.Suppress(')')).setParseAction(lambda t: t.asList())
sequence_2d = p.Group(p.Suppress('(') + p.OneOrMore(sequence_1d) + p.Suppress(')')).setParseAction(lambda t: t.asList())
set_value = (p.Suppress('{') + p.delimitedList(scalar) + p.Suppress('}')).setParseAction(lambda t: set(t.asList()))
value = set_value | sequence_2d | sequence_1d | scalar

# Statements.
statement = p.Forward()
label = p.ZeroOrMore(statement) + end
attribute = p.Combine(identifier + ':' + identifier) | identifier
assignment_stmt = p.Group(attribute.setResultsName('name') +
                          p.Suppress('=') +
                          value.setResultsName('value'))

class Namespace(dict):
    """ Namespace.

    Subclassing allows us to decorate the dictionary with attributes that we can
    use to recognize it during parsing.
    """

    @classmethod
    def validate_object_stanza(cls, t):
        if t.end_object_name and t.end_object_name != t.object_name:
            raise p.ParseException("Object names do not match (%r != %r')" % 
                (t.object_name, t.end_object_name))

    @classmethod
    def fromparseresults(cls, t):
        if t.object_name:
            ns = cls()
            ns.object_name = t.object_name
        else:
            ns = Bunch()
        for statement in t.statements:
            if getattr(statement, 'name', ''):
                # Assignment.
                ns[statement.name] = statement.value
            elif getattr(statement, 'object_name', ''):
                # OBJECT or GROUP.
                ns[statement.object_name] = Bunch(statement)
        return ns

    def __repr__(self):
        s = '<%s : %s>' % (self.object_name, pprint.pformat(self.copy()))
        return s

object_stmt = ((object_kw|begin_object|group|begin_group).suppress()
    + p.Suppress('=')
    + identifier.setResultsName('object_name')
    + p.Group(p.ZeroOrMore(statement)).setResultsName('statements')
    + (end_object|end_group).suppress() + 
        p.Optional(p.Suppress('=') + identifier.setResultsName('end_object_name'))).setParseAction(
                Namespace.validate_object_stanza, Namespace.fromparseresults)

statement << (object_stmt | assignment_stmt)
label = (p.Group(p.ZeroOrMore(statement)).setResultsName('statements') + end).ignore(p.cStyleComment).setParseAction(Namespace.fromparseresults)

def parse_odl(odl):
    """ Parse ODL into a set of nested dictionaries.

    Each assignment becomes a dictionary entry mapping the identifier key to the
    value. Each GROUP or OBJECT becomes a dictionary entry mapping the name to
    another dictionary containing the contents of the GROUP/OBJECT. GROUPs and
    OBJECTs are not distinguished.
    
    Integers become ints. Reals become floats. 1D sequences become lists. 2D
    sequences become lists of lists. Sets become Python sets. Date-times become
    datetime objects. Quoted strings and identifiers become strs. Unitted
    numerical values become `UnittedValue` instances.

    This parser is not a complete implementation of the full ODL grammar. In
    particular, we lack the following features: non-decimal integer bases,
    non-UTC date-times, \\v string formatting character, pointers. Furthermore,
    we do not reject some invalid constructs, e.g.::

        BEGIN_OBJECT = FOO
        END_GROUP = FOO

    Parameters
    ----------
    odl : str
        The ODL text. Trailing NULs are removed before parsing. They sometimes
        appear as padding because HDF imposes limits on resizing.

    Returns
    -------
    ns : dict
        A nested dictionary.

    Raises
    ------
    ParseException if there is a syntax error or if the ODL text contains an
    unimplemented feature of the grammar.
    """
    pr = label.parseString(odl.rstrip('\0'))
    return pr[0]
