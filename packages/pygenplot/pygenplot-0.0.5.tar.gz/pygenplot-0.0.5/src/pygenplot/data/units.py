import copy
import math
import numbers
import os
from typing import Dict, List, Optional, Tuple

import yaml

from ..kernel.logger import log
from ..utils.numeric import get_trailing_digits


class UnitError(Exception):
    pass


process_tag = yaml.emitter.Emitter.process_tag


class UnitsManager:

    _UNITS = {}

    _EQUIVALENCES = {}

    _DEFAULT_DATABASE = os.path.join(os.path.dirname(__file__), "units.yml")

    _USER_DATABASE = os.path.join(os.path.expanduser("~"), ".pygenplot", "units.yml")

    UNAMES = ['kg', 'm', 's', 'K', 'mol', 'A', 'cd', 'rad', 'sr']

    PREFIXES = {'y': 1e-24,  # yocto
                'z': 1e-21,  # zepto
                'a': 1e-18,  # atto
                'f': 1e-15,  # femto
                'p': 1e-12,  # pico
                'n': 1e-9,   # nano
                'u': 1e-6,   # micro
                'm': 1e-3,   # milli
                'c': 1e-2,   # centi
                'd': 1e-1,   # deci
                'da':1e1,    # deca
                'h': 1e2,    # hecto
                'k': 1e3,    # kilo
                'M': 1e6,    # mega
                'G': 1e9,    # giga
                'T': 1e12,   # tera
                'P': 1e15,   # peta
                'E': 1e18,   # exa
                'Z': 1e21,   # zetta
                'Y': 1e24,   # yotta
            }

    class Unit:

        def __init__(self, uname: str, factor: float = 1.0, kg: int = 0, m: int = 0, s: int = 0,
                     k: int = 0, mol: int = 0, a: int = 0, cd: int = 0, rad: int = 0, sr: int = 0):
            """Constructor.

            Args:
                uname: the name of the unit
                factor: the factor of the unit
                m: the power for the length dimension
                s: the power for the time dimension
                k: the power for the temperature dimension
                mol: the power for the matter quantity dimension
                a: the power for the intensity dimension
                cd: the power for the light intensity dimension
                rad: the power for the angle dimension
                sr: the power for the solid angle dimension
            """
            self._factor = factor
            
            self._dimension = [kg, m, s, k, mol, a, cd, rad, sr]
            
            self._format = 'g'

            self._uname = uname

            self._ounit = None

            self._out_factor = None

            self._equivalent = False

        def __add__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Adds this unit to another one.

            Args:
                other: the unit to add

            Returns:
                the unit resulting from the addition            
            """

            u = copy.deepcopy(self)

            if u.is_analog(other):
                u._factor += other.factor
                return u
            elif self._equivalent:
                equivalence_factor = u.get_equivalence_factor(other)
                if equivalence_factor is not None:
                    u._factor += other.factor/equivalence_factor
                    return u
                else:
                    raise UnitError('The units are not equivalent')                
            else:
                raise UnitError('Incompatible units')

        def __div__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Divides this unit by another one.

            Args:
                other: the unit to add

            Returns:
                the unit resulting from the division
            """
            u = copy.deepcopy(self)
            if isinstance(other, numbers.Number):
                u._factor /= other
                return u
            elif isinstance(other, UnitsManager.Unit):
                u._div_by(other)
                return u
            else:
                raise UnitError('Invalid operand')

        __itruediv__ = __div__

        def __float__(self) -> float:
            """Returns the value of this unit coerced to float.

            Returns:
                the value of the unit coerced to float
            """    
            return float(self.toval())

        def __floordiv__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Divides and floors this unit by another one.

            Args:
                other: the unit to floor with

            Returns:
                the unit resulting from the floor div
            """
            u = copy.deepcopy(self)
            u._div_by(other)
            u._factor = math.floor(u._factor)

            return u

        def __iadd__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Adds this unit to another one.
            
            Args:
                other: the unit to add

            Returns:
                the unit resulting from the addition
            """
            if self.is_analog(other):
                self._factor += other.factor
                return self
            elif self._equivalent:
                equivalence_factor = self.get_equivalence_factor(other)
                if equivalence_factor is not None:
                    self._factor += other.factor/equivalence_factor
                    return self
                else:
                    raise UnitError('The units are not equivalent')                
            else:
                raise UnitError('Incompatible units')

        def __idiv__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Divides this unit by another one.
            
            Args:
                other: the unit to divide with

            Returns:
                the unit resulting from the division
            """
            if isinstance(other, numbers.Number):
                self._factor /= other
                return self
            elif isinstance(other, UnitsManager.Unit):
                self._div_by(other)
                return self
            else:
                raise UnitError('Invalid operand')

        def __ifloordiv__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Divides and floors the value of this unit by another one.

            Args:
                other: the unit to floor with

            Returns:
                the divided and floored unit
            """
            self._div_by(other)
            self._factor = math.floor(self._factor)
            return self

        def __imul__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Multiplies this unit by another one.
            
            Args:
                other: the unit to multiply with

            Returns:
                the unit resulting from the multiplication
            """

            if isinstance(other, numbers.Number):
                self._factor *= other
                return self
            elif isinstance(other, UnitsManager.Unit):
                self._mult_by(other)
                return self
            else:
                raise UnitError('Invalid operand')

        def __int__(self) -> int:
            """Returns the value of this unit coerced to integer.

            Returns:
                the results of the coerced unit to an int
            """
        
            return int(self.toval())

        def __ipow__(self, n: int) -> "UnitsManager.Unit":
            """Returns the unit powerized to n.

            Args:
                n: the power

            Returns:
                the powerized unit
            """
            self._factor = pow(self._factor, n)
            for i in range(len(self._dimension)):
                self._dimension[i] *= n

            self._ounit = None
            self._out_factor = None

            return self

        def __isub__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Subtracts this unit by another one.
            
            Args:
                other: the unit to subtract with

            Returns:
                the unit resulting from the subtraction
            """
            if self.is_analog(other):
                self._factor -= other.factor
                return self
            elif self._equivalent:
                equivalence_factor = self.get_equivalence_factor(other)
                if equivalence_factor is not None:
                    self._factor -= other.factor/equivalence_factor
                    return self
                else:
                    raise UnitError('The units are not equivalent')                
            else:
                raise UnitError('Incompatible units')

        def __mul__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Multiplies this unit by another one.

            Args:
                other: the unit to multiply with
            
            Returns:
                the unit resulting from the multiplication        
            """
            u = copy.deepcopy(self)
            if isinstance(other,numbers.Number):
                u._factor *= other
                return u
            elif isinstance(other,UnitsManager.Unit):
                u._mult_by(other)
                return u
            else:
                raise UnitError('Invalid operand')

        def __pow__(self, n: int) -> "UnitsManager.Unit":
            """Returns the unit powerized to n.

            Args:
                n: the power

            Returns:
                the powerized unit
            """
            output_unit = copy.copy(self)
            output_unit._ounit = None
            output_unit._out_factor = None
            output_unit._factor = pow(output_unit._factor, n)
            for i in range(len(output_unit._dimension)):
                output_unit._dimension[i] *= n

            return output_unit

        def __radd__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Adds another unit to this one.

            Args:
                other: the unit to add with

            Returns:
                the unit resulting from the addition        
            """
            return self.__add__(other)

        def __rdiv__(self, other):
            """Divides this unit by another one.

            Args:
                other: the unit to add with

            Returns:
                the unit resulting from the addition        
            """
            u = copy.deepcopy(self)
            if isinstance(other, numbers.Number):
                u._factor /= other
                return u
            elif isinstance(other, UnitsManager.Unit):
                u._div_by(other)
                return u
            else:
                raise UnitError('Invalid operand')

        def __rmul__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Multiplies this unit by another one.

            Args:
                other: the unit to multiply with
            
            Returns:
                the unit resulting from the multiplication        
            """
            u = copy.deepcopy(self)
            if isinstance(other, numbers.Number):
                u._factor *= other
                return u
            elif isinstance(other,UnitsManager.Unit):
                u._mult_by(other)
                return u
            else:
                raise UnitError('Invalid operand')

        def __rsub__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Subtracts another unit to this unit.

            Args:
                other: the unit to be subtracted with
            
            Returns:
                the unit resulting from the subtraction
            """
            return other.__sub__(self)

        def __sub__(self, other: "UnitsManager.Unit") -> "UnitsManager.Unit":
            """Subtracts another unit to this unit.

            Args:
                other: the unit to be subtracted with
            
            Returns:
                the unit resulting from the subtraction
            """
            u = copy.deepcopy(self)

            if u.is_analog(other):
                u._factor -= other.factor
                return u
            elif u._equivalent:
                equivalence_factor = u.get_equivalence_factor(other)
                if equivalence_factor is not None:
                    u._factor -= other.factor/equivalence_factor
                    return u
                else:
                    raise UnitError('The units are not equivalent')                
            else:
                raise UnitError('Incompatible units')

        def __str__(self) -> str:
            """Returns a string representation of this unit.

            Returns:
                the stringified unit
            """
            unit = copy.copy(self)

            fmt = '{:%s}' % self._format

            if self._ounit is None:

                s = fmt.format(unit._factor)

                positive_units = []
                negative_units = []
                for uname, uval in zip(UnitsManager.UNAMES, unit._dimension):
                    if uval == 0:
                        continue
                    elif uval > 0:
                        if uval == 1:
                            positive_units.append("{:s}".format(uname))
                        else:
                            if uval.is_integer():
                                positive_units.append("{:s}{:d}".format(uname,int(uval)))
                            else:
                                positive_units.append("{:s}{}".format(uname,uval))
                    elif uval < 0:
                        if uval == -1:
                            negative_units.append("{:s}".format(uname))
                        else:
                            if uval.is_integer():
                                negative_units.append("{:s}{:d}".format(uname,int(-uval)))
                            else:
                                negative_units.append("{:s}{}".format(uname,-uval))

                positive_units_str = ''                
                if positive_units:
                    positive_units_str = ' '.join(positive_units)
                
                negative_units_str = ''                
                if negative_units:
                    negative_units_str = ' '.join(negative_units)

                if positive_units_str:
                    s += ' {:s}'.format(positive_units_str)
                    
                if negative_units_str:
                    if not positive_units_str:
                        s += ' 1' 
                    s += ' / {}'.format(negative_units_str)
                        
            else:

                u = copy.deepcopy(self)
                u._div_by(self._out_factor)

                s = fmt.format(u._factor)
                s += ' {}'.format(self._ounit)

            return s

        def _div_by(self, other: "UnitsManager.Unit"):
            """Divides this unit by another one.

            Args:
                other: the unit to divide with
            """
            if self.is_analog(other):
                self._factor /= other.factor
                self._dimension = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            elif self._equivalent:
                equivalence_factor = self.get_equivalence_factor(other)
                if equivalence_factor is not None:
                    self._factor /= other.factor/equivalence_factor
                    self._dimension = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                else:
                    raise UnitError('The units are not equivalent')
            else:
                self._factor /= other.factor
                for i in range(len(self._dimension)):
                    self._dimension[i] = self._dimension[i] - other.dimension[i]

            self._ounit = None
            self._out_factor = None

        def _mult_by(self, other: "UnitsManager.Unit"):
            """Multiplies this unit by another one.

            Args:
                other: the unit to multiply with
            """
            if self.is_analog(other):
                self._factor *= other.factor
                for i in range(len(self._dimension)):
                    self._dimension[i] = 2.0*self._dimension[i]
            elif self._equivalent:
                equivalence_factor = self.get_equivalence_factor(other)
                if equivalence_factor is not None:
                    self._factor *= other.factor/equivalence_factor
                    for i in range(len(self._dimension)):
                        self._dimension[i] = 2*self._dimension[i]
                    return
                else:
                    raise UnitError('The units are not equivalent')
            else:
                self._factor *= other.factor
                for i in range(len(self._dimension)):
                    self._dimension[i] = self._dimension[i] + other.dimension[i]

            self._ounit = None
            self._out_factor = None

        def ceil(self) -> "UnitsManager.Unit":
            """Ceils this in canonical units.

            Returns:
                the ceiled unit
            """
            r = copy.deepcopy(self)

            if r._ounit is not None:
                val = math.ceil(r.toval(r._ounit))
                newu = UnitsManager.Unit('au',val)
                newu *= UnitsManager._str_to_unit(r._ounit)
                return newu.ounit(r._ounit)
            else:
                r._factor = math.ceil(r._factor)
                return r

        @property
        def dimension(self) -> List[int]:
            """Returns the dimension of the unit. Returns a copy.

            Returns:
                the dimension of the unit
            """
            return copy.copy(self._dimension)

        @dimension.setter
        def dimension(self, dimension: List[int]):
            """Sets the dimension of the unit.

            Args:
                dimension: the dimension
            """
            self._dimension = dimension

        @property
        def equivalent(self) -> bool:
            """Returns whether the unit is an equivalent unit.

            Returns:
                whether the unit is an equivalent unit
            """
            return self._equivalent

        @equivalent.setter
        def equivalent(self, equivalent: bool):
            """Sets whether the unit is an equivalent unit.

            Args:
                equivalent: whether the unit is an equivalent unit
            """

            self._equivalent = equivalent

        @property
        def factor(self) -> float:
            """Returns the factor of the unit.

            Returns:
                the factor of the unit
            """
            return self._factor

        @factor.setter
        def factor(self, factor: float):
            """Sets the factor of the units.

            Args:
                factor: the factor
            """
            self._factor = factor

        def floor(self) -> "UnitsManager.Unit":
            """Floors the unit in canonical units.

            Returns:
                the floored unit
            """
            r = copy.deepcopy(self)

            if r._ounit is not None:
                val = math.floor(r.toval(r._ounit))
                newu = UnitsManager.Unit('au',val)
                newu *= UnitsManager._str_to_unit(r._ounit)
                return newu.ounit(r._ounit)
            else:
                r._factor = math.floor(r._factor)
                return r

        def get_equivalence_factor(self,other: "UnitsManager.Unit") -> Optional[float]:
            """Returns the equivalence factor if the other unit is equivalent to this unit. Equivalent units are units
            whose dimension are related through a constant (e.g. energy and mass, or frequency and temperature).

            Args:
                other: the other unit to compute the equivalence factor with

            Returns:
                the equivalence factor
            """
            _, upower = get_trailing_digits(self._uname)
            dimension = tuple([d/upower for d in self._dimension])        
            if dimension not in UnitsManager._EQUIVALENCES:
                return None

            powerized_equivalences = {}
            for k, v in UnitsManager._EQUIVALENCES[dimension].items():
                pk = tuple([d*upower for d in k])
                powerized_equivalences[pk] = pow(v,upower)
            
            odimension = tuple(other.dimension)
            if odimension in powerized_equivalences:
                return powerized_equivalences[odimension]
            else:
                return None

        def is_analog(self, other: "UnitsManager.Unit") -> bool:
            """Returns whether the other unit is analog to this unit. Analog units are units whose dimension vector
            exactly matches.

            Args:
                other: the unit to check for analogy
            """
            return self._dimension == other.dimension

        def ounit(self, ounit: str) -> "UnitsManager.Unit":
            """Sets the preferred unit for output.

            Args:
                ounit: the output unit

            Returns:
                the converted unit 
            """
            out_factor = UnitsManager._str_to_unit(ounit)

            if self.is_analog(out_factor):
                self._ounit = ounit
                self._out_factor = out_factor
                return self
            elif self._equivalent:
                if self.get_equivalence_factor(out_factor) is not None:
                    self._ounit = ounit
                    self._out_factor = out_factor
                    return self
                else:
                    raise UnitError('The units are not equivalents')
            else:
                raise UnitError('The units are not compatible')

        def round(self) -> "UnitsManager.Unit":
            """Rounds of this unit in canonical units.

            Returns:
                the rounded unit
            """
            r = copy.deepcopy(self)

            if r._ounit is not None:
                val = round(r.toval(r._ounit))
                newu = UnitsManager.Unit('au',val)
                newu *= UnitsManager._str_to_unit(r._ounit)
                return newu.ounit(r._ounit)
            else:
                r._factor = round(r._factor)
                return r

        def toval(self, ounit: str = '') -> float:
            """Returns the numeric value of a unit. The value is given in ounit or in the default output unit.

            Args:
                ounit: the output unit

            Returns:
                the numeric value of the unit
            """
            newu = copy.deepcopy(self)
            if not ounit:
                ounit = self._ounit

            if ounit is not None:
                out_factor = UnitsManager._str_to_unit(ounit)

                if newu.is_analog(out_factor):
                    newu._div_by(out_factor)
                    return newu._factor
                elif newu._equivalent:
                    if newu.get_equivalence_factor(out_factor) is not None:
                        newu._div_by(out_factor)
                        return newu._factor
                    else:
                        raise UnitError('The units are not equivalents')
                else:
                    raise UnitError('The units are not compatible')
            else:
                return newu._factor

    @classmethod
    def _parse_unit(cls, iunit: str) -> Unit:
        """Parses a unit.

        Args:
            iunit: the unit to parse

        Returns:
            the parsed unit
        """
        
        max_prefix_length = 0
        for p in UnitsManager.PREFIXES:
            max_prefix_length = max(max_prefix_length,len(p))

        iunit = iunit.strip()

        iunit,upower = get_trailing_digits(iunit)
        if not iunit:
            raise UnitError('Invalid unit')

        for i in range(len(iunit)):
            if cls.has_unit(iunit[i:]):
                prefix = iunit[:i]
                iunit = iunit[i:]
                break
        else:
            raise UnitError('The unit {} is unknown'.format(iunit))

        if prefix:
            if prefix not in UnitsManager.PREFIXES:
                raise UnitError('The prefix {} is unknown'.format(prefix))
            prefix = UnitsManager.PREFIXES[prefix]
        else:
            prefix = 1.0
        
        unit = cls.get_unit(iunit)

        unit = UnitsManager.Unit(iunit,prefix*unit.factor, *unit.dimension)
        
        unit **= upower
            
        return unit

    @classmethod
    def _str_to_unit(cls, s: str) -> Unit:
        """Convert a str to its corresponding Unit.

        Args:
            s: the unit to convert

        Returns:
            the unit
        """
        if cls.has_unit(s):
            unit = cls.get_unit(s)
            return copy.deepcopy(unit)

        else:

            unit = UnitsManager.Unit('au', 1.0)

            splitted_units = s.split('/')
            
            if len(splitted_units) == 1:        
                units = splitted_units[0].strip().split()
                for u in units:
                    u = u.strip()
                    unit *= cls._parse_unit(u)
                unit._uname = s
                                    
                return unit
                
            elif len(splitted_units) == 2:
                numerator = splitted_units[0].strip()
                if numerator != '1':
                    numerator = numerator.split()
                    for u in numerator:
                        u = u.strip()
                        unit *= cls._parse_unit(u)

                denominator = splitted_units[1].strip().split()
                for u in denominator:
                    u = u.strip()
                    den_unit = cls._parse_unit(u)
                    unit /= den_unit

                unit._uname = s

                return unit
                
            else:
                raise UnitError('Invalid unit: {}'.format(s))

    @classmethod
    def add_equivalence(cls, dim1: Tuple[int, int, int, int, int, int, int, int, int],
                        dim2: Tuple[int, int, int, int, int, int, int, int, int], factor: float):
        """Adds a new equivalence to the manager.

        Args:
            dim1: the first dimension
            dim2: the equivalent dimension
            factor: the equivalence factor
        """

        cls._EQUIVALENCES.setdefault(dim1, {}).__setitem__(dim2, factor)
        cls._EQUIVALENCES.setdefault(dim2, {}).__setitem__(dim1, 1.0/factor)

    @classmethod
    def add_unit(cls, uname: str, factor: float = 1.0, kg: int = 0, m: int = 0, s: int = 0, k: int = 0, mol: int = 0,
                 a: int = 0, cd: int = 0, rad: int = 0, sr: int = 0):
        """Adds a unit to the manager.

        Args:
            uname: the name of the unit
            factor: the factor of the unit
            kg: the power for the mass dimension
            m: the power for the length dimension
            s: the power for the time dimension
            k: the power for the temperature dimension
            mol: the power for the matter quantity dimension
            a: the power for the intensity dimension
            cd: the power for the light intensity dimension
            rad: the power for the angle dimension
            sr: the power for the solid angle dimension        
        """
        cls._UNITS[uname] = UnitsManager.Unit(uname,factor, kg, m, s, k, mol, a, cd, rad, sr)

    @classmethod
    def delete_unit(cls, uname: str):
        """Deletes a unit from the manager.

        Args:
            uname: the unit to delete
        """
        if uname in cls._UNITS:
            del cls._UNITS[uname]

    @classmethod
    def get_unit(cls, uname: str) -> Optional[Unit]:
        """Gets a unit from the manager.
        
        Returns:
            the unit
        """
        return cls._UNITS.get(uname, None)

    @classmethod
    def get_units(cls) -> Dict[str, Unit]:
        """Returns the units stored in the units manager.

        Returns:
            the units stored in the manager
        """
        return cls._UNITS

    @classmethod
    def has_unit(cls, uname: str) -> bool:
        """Returns whether the manager has a unit with the given unit name.

        Args:
            uname: the unit to search for

        Returns:
            whether the manager has the unit
        """
        return uname in cls._UNITS

    @classmethod
    def load(cls, default_database: Optional[str] = None, user_database: Optional[str] = None):
        """Loads the units to the manager from the YAML file.

        Args:
            default_database: the default database path
            user_database: the user database path
        """
        if default_database is None:
            default_database = cls._DEFAULT_DATABASE

        # If user_database is not None, this will be path used for further saving of the database
        if user_database is not None:
            cls._USER_DATABASE = user_database

        cls._UNITS.clear()

        yaml_units = {}
        with open(default_database, 'r') as fin:
            yaml_units.update(yaml.safe_load(fin))
        log(f"Loaded successfully default units database from {default_database}",
            ["main"], "info")

        try:
            with open(cls._USER_DATABASE, 'r') as fin:
                yaml_units.update(yaml.safe_load(fin))
        except Exception:
            log(f"Can not load user units database from {cls._USER_DATABASE}", ["main"], "warning")
        else:
            log(f"Loaded successfully user units database from {cls._USER_DATABASE}",
                ["main"], "info")
        finally:
            for uname, udict in yaml_units.items():
                factor = udict.get('factor', 1.0)
                dim = udict.get('dimension', [0, 0, 0, 0, 0, 0, 0, 0, 0])
                cls._UNITS[uname] = UnitsManager.Unit(uname, factor, *dim)

    @classmethod
    def measure(cls, val: float, iunit: str = 'au', ounit: str = '', equivalent: bool = False) -> Unit:
        """Computes and returns a unit.

        Args:
            val: the value
            iunit: the input unit string
            ounit: the output unit
            equivalent: whether the unit has equivalences

        Returns:
            the unit
        """

        if iunit:
            unit = cls._str_to_unit(iunit)
            unit *= val
        else:
            unit = UnitsManager.Unit('au',val)

        unit.equivalent = equivalent

        if not ounit:
            ounit = iunit

        unit.ounit(ounit)

        return unit

    @classmethod
    def save(cls, user_database: Optional[str] = None):
        """Saves all the units stored in the manager to a YAML file.

        Args:
            user_database: the user database path
        """
        if user_database is None:
            user_database = cls._USER_DATABASE

        user_database_dir = os.path.dirname(user_database)
        if not os.path.exists(user_database_dir):
            try:
                os.makedirs(user_database_dir)
            except OSError:
                log("Can not create user settings directory", ["main"], "error")
                return

        yaml.emitter.Emitter.process_tag = noop

        try:
            with open(user_database, 'w') as fout:
                yaml.dump(cls._UNITS, fout, default_flow_style=None)
        except OSError:
            log(f"Can not save units database in {user_database}", ["main"], "error")
        else:
            log(f"Units database saved successfully in {user_database}", ["main"], "error")
        finally:
            yaml.emitter.Emitter.process_tag = process_tag

    @classmethod
    def set_units(cls, units: Dict[str, Unit]):
        """Sets units of the units manager.

        Args:
            the units
        """
        cls._UNITS = units


def noop(self, *args, **kw):
    pass


def represent_unit(dumper: yaml.Dumper, unit: UnitsManager.Unit):
    """Represents a Unit when dumping in YAML.

    Args:
        dumper: the dumper
        unit: the unit to dump
    """
    return dumper.represent_mapping("", dict(factor=unit.factor, dimension=unit.dimension))


yaml.add_representer(UnitsManager.Unit, represent_unit)

# au --> au
UnitsManager.add_equivalence((0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0),1.0)
# 1J --> 1Hz
UnitsManager.add_equivalence((1, 2, -2, 0, 0, 0, 0, 0, 0),
                             (0, 0, -1, 0, 0, 0, 0, 0, 0),1.50919031167677e+33)
# 1J --> 1K
UnitsManager.add_equivalence((1, 2, -2, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 1, 0, 0, 0, 0, 0),7.242971666663e+22)
# 1J --> 1kg
UnitsManager.add_equivalence((1, 2, -2, 0, 0, 0, 0, 0, 0),
                             (1, 0, 0, 0, 0, 0, 0, 0, 0),1.112650055999e-17)
# 1J --> 1/m
UnitsManager.add_equivalence((1, 2, -2, 0, 0, 0, 0, 0, 0),
                             (0, -1, 0, 0, 0, 0, 0, 0, 0),5.034117012218e+24)
# 1J --> 1J/mol
UnitsManager.add_equivalence((1, 2, -2, 0, 0, 0, 0, 0, 0),
                             (1, 2, -2, 0, -1, 0, 0, 0, 0),6.02214076e+23)
# 1J --> 1rad/s
UnitsManager.add_equivalence((1, 2, -2, 0, 0, 0, 0, 0, 0),
                             (0, 0, -1, 0, 0, 0, 0, 1, 0),9.482522392065263e+33)
# 1Hz --> 1K
UnitsManager.add_equivalence((0, 0, -1, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 1, 0, 0, 0, 0, 0),4.79924341590788e-11)
# 1Hz --> 1kg
UnitsManager.add_equivalence((0, 0, -1, 0, 0, 0, 0, 0, 0),
                             (1, 0, 0, 0, 0, 0, 0, 0, 0),7.37249667845648e-51)
# 1Hz --> 1/m
UnitsManager.add_equivalence((0, 0, -1, 0, 0, 0, 0, 0, 0),
                             (0, -1, 0, 0, 0, 0, 0, 0, 0),3.33564095480276e-09)
# 1Hz --> 1J/mol
UnitsManager.add_equivalence((0, 0, -1, 0, 0, 0, 0, 0, 0),
                             (1, 2, -2, 0, -1, 0, 0, 0, 0),3.9903124e-10)
# 1Hz --> 1rad/s
UnitsManager.add_equivalence((0, 0, -1, 0, 0, 0, 0, 0, 0),
                             (0, 0, -1, 0, 0, 0, 0, 1, 0),6.283185307179586)
# 1K --> 1kg
UnitsManager.add_equivalence((0, 0, 0, 1, 0, 0, 0, 0, 0),
                             (1, 0, 0, 0, 0, 0, 0, 0, 0), 1.53617894312656e-40)
# 1K --> 1/m
UnitsManager.add_equivalence((0, 0, 0, 1, 0, 0, 0, 0, 0),
                             (0, -1, 0, 0, 0, 0, 0, 0, 0), 6.95034751466497e+01)
# 1K --> 1J/mol
UnitsManager.add_equivalence((0, 0, 0, 1, 0, 0, 0, 0, 0),
                             (1, 2, -2, 0, -1, 0, 0, 0, 0), 8.31435)
# 1K --> 1rad/s
UnitsManager.add_equivalence((0, 0, 0, 1, 0, 0, 0, 0, 0),
                             (0, 0, -1, 0, 0, 0, 0, 1, 0), 130920329782.73508)
# 1kg --> 1/m
UnitsManager.add_equivalence((1, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, -1, 0, 0, 0, 0, 0, 0, 0), 4.52443873532014e+41)
# 1kg --> 1J/mol
UnitsManager.add_equivalence((1, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, -1, 0, 0, 0, 0, 0, 0, 0), 5.412430195397762e+40)
# 1kg --> 1rad/s
UnitsManager.add_equivalence((1, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, -1, 0, 0, 0, 0, 1, 0), 8.522466107774846e+50)
# 1/m --> 1J/mol
UnitsManager.add_equivalence((0, -1, 0, 0, 0, 0, 0, 0, 0),
                             (1, 2, -2, 0, -1, 0, 0, 0, 0), 0.000119627)
# 1/m --> 1rad/s
UnitsManager.add_equivalence((0, -1, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, -1, 0, 0, 0, 0, 1, 0), 1883651565.7166505)
# 1J/mol --> 1rad/s
UnitsManager.add_equivalence((1, 2, -2, 0, -1, 0, 0, 0, 0),
                             (0, 0, -1, 0, 0, 0, 0, 1, 0), 15746098887.375164)
