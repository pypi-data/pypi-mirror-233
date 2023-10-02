import numpy as np
import enum
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, DateTime, Enum, Identity, JSON
from sqlalchemy import inspect
from typing import Union, Tuple
import datetime as dt
import copy
import dataclasses

from sunpeek.components import iam_methods
from sunpeek.components.iam_methods import IAM_Method
from sunpeek.common import unit_uncertainty as uu
from sunpeek.common.unit_uncertainty import Q
from sunpeek.common.errors import CollectorDefinitionError
from sunpeek.components.helpers import ORMBase, AttrSetterMixin, ComponentParam


@dataclasses.dataclass
class SensorType:
    name: str
    compatible_unit_str: str
    description: str
    lower_replace_min: Union[Q, None] = None
    lower_replace_max: Union[Q, None] = None
    lower_replace_value: Union[Q, None] = None
    upper_replace_min: Union[Q, None] = None
    upper_replace_max: Union[Q, None] = None
    upper_replace_value: Union[Q, None] = None
    # equation: Union[str, None] = None
    max_fill_period: Union[dt.timedelta, None] = None
    sensor_hangs_period: Union[dt.timedelta, None] = None
    info_checks: Union[dict, None] = None
    common_units: Union[list, None] = None

    @property
    def info_checks(self):
        if getattr(self, '_info_checks', None) is not None:
            return self._info_checks
        else:
            return {}

    @info_checks.setter
    def info_checks(self, val):
        self._info_checks = val


class CollectorTypes(str, enum.Enum):
    flat_plate = "flat_plate"
    concentrating = "concentrating"


class Collector(AttrSetterMixin, ORMBase):
    """
    Implements a specific collector (product of some manufacturer), including all performance data acc. to data sheet.

    Stores two different collector type parameters, referring to the two test procedures defined in `ISO 9806`_,
    either quasi-dynamic or steady-state test. The type of test procedure is available from the standard collector
    data sheet / Solar Keymark certificate and must be specified in `test_type`.

    Test parameters may refer to either gross or aperture area. This must be specified in `test_reference_area`. The
    collector parameters stored in Collector _always_ refer to gross area.

    IAM (incidence angle modifier) information may be given as an instance of the IAM_Method class. This holds
    several implementations where the IAM information can be given in either of these ways:
    - If only IAM information at an aoi of 50 degrees is given, use `IAM_K50(k50)`. Internally, this uses the ASHRAE equation.
    - To use the ASHRAE IAM equation with a known parameter `b`, use `IAM_ASHRAE(b)`.
    - To use the Ambrosetti IAM equation with a known parameter `kappa`, use `IAM_Ambrosetti(kappa)`.
    - To use an IAM with given / known IAM values at given aoi angles, use `IAM_Interpolated()`. This requires a list
    of reference aoi's, and either a) 1 list of IAM values or b) 2 lists with transversal and longitudinal IAM
    values.

    Attributes
    ----------
    name : str
        Name of collector type. Must be unique within HarvestIT 'collector' database.
    manufacturer_name : str, optional
        Manufacturer name. Example: "GREENoneTEC Solarindustrie GmbH"
    product_name : str, optional
        Product name. Example: "GK 3133"

    licence_number : str, optional
        Licence number (often also known as Registration number) of the Solar Keymark certificate.
    test_report_id : str, optional
        "Test Report(s)" field on Solar Keymark certificate.
    certificate_date_issued : datetime, optional
        "Date issued" field on Solar Keymark certificate.
    certificate_lab : str, optional
        Laboratory / testing institution that issued the collector test certificate.
    certificate_details : str, optional
        Details concerning the official collector test / Solar Keymark certificate, such as testing institution etc.
    collector_type : CollectorTypes or str
        Construction type of the collector, as defined in Solar Keymark / ISO 9806.
        Main distinction is between flat plate and concentrating collectors.
    test_type : str
        Type of collector test, according to `ISO 9806`_. Valid values: 'QDT' | 'dynamic' | 'SST' | 'static'
    test_reference_area : str
        Collector area to which the test data refer. Valid values: 'area_ap | 'aperture' | 'area_gr' | 'gross'.
    area_gr : pint Quantity, optional
        Gross collector area. Mandatory if `test_reference_area`=='aperture', optional otherwise.
    area_ap : pint Quantity, optional
        Gross collector area. Mandatory if `test_reference_area`=='aperture', optional otherwise.

    gross_length : pint Quantity
        Gross length of one collector (collector side pointing upwards). Typical value around Q(2, 'm')
    gross_width : pint Quantity
        Gross width of one collector (normal to gross_length, i.e. measured parallel to the ground). For large-area
        flat plate collectors, a typical value is Q(6.0, 'm').
    gross_height : pint Quantity
        Gross height ('thickness') of one collector (from cover to backside). A typical value is Q(20, 'cm').

    a1 : pint Quantity
        Linear heat loss coefficient, according to collector test data sheet of quasi dynamic
        or steady state test.
    a2 : pint Quantity
        Quadratic heat loss coefficient, according to collector test data sheet of quasi dynamic
        or steady state test.
    a5 : pint Quantity
        Effective thermal heat capacity, according to collector test data sheet of quasi dynamic
        or steady state test.
    a8 : pint Quantity
        Radiative heat loss coefficient, according to collector test data sheet of quasi dynamic
        or steady state test.
    kd : pint Quantity, optional
        Incidence angle modifier for diffuse radiation, according to collector test data sheet of quasi dynamic test.
        Mandatory if `test_type`=='dynamic'.
    eta0b : pint Quantity, optional
        Peak collector efficiency (= zero loss coefficient) based on beam irradiance, according
        to collector test data sheet of quasi dynamic test.
        Mandatory if `test_type`=='dynamic'.
    eta0hem : pint Quantity, optional
        Peak collector efficiency (= zero loss coefficient) based on hemispherical irradiance,
        according to collector test data sheet of steady state test (or calculated from quasi-dynamic test).
        Mandatory if `test_type`=='static'.
    f_prime : pint Quantity
        Collector efficiency factor, i.e. ratio of heat transfer resistances of absorber to ambient vs. fluid to ambient.
    concentration_ratio : pint Quantity
        Geometric concentration ratio: Factor by which solar irradiance is concentrated onto the collector's
        absorbing surface.
        When applying a ISO 24194 Thermal Power Check, the `concentration_ratio` is used to determine which of the
        3 formulae defined in ISO 24194 to apply.
    calculated_parameters : dictionary
        Contains information about calculated collector parameters, where specific information was not given at
        instantiation of the object, e.g. because the Solar Keymark data sheet does not include a specific parameter.
        Some parameters can be calculated based on given ones, e.g. `Kd` (diffuse IAM) can be calculated based on
        given IAM information. Dictionary keys are the names of calculated parameters (e.g. `kd`), dictionary values
        hold information concerning specific calculation details (e.g. calculation method).
    plant : None
        Not used, included for compatibility with other component types.

    .. _ISO 9806:
        https://www.iso.org/standard/67978.html
    .. _ASHRAE model:
        https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.iam.ashrae.html
    """
    __tablename__ = 'collectors'

    class t_types(str, enum.Enum):
        SST = "SST"
        static = "static"
        QDT = "QDT"
        dynamic = "dynamic"

    class ref_a_types(str, enum.Enum):
        area_gr = "area_gr"
        gross = "gross"
        area_ap = "area_ap"
        aperture = "aperture"

    VALID_TEST_TYPES = [el.name for el in t_types]
    VALID_AREA_TYPES = [el.name for el in ref_a_types]

    # Name is the PK, and is required whenever a DB store is in use.
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String, unique=True, nullable=False)
    manufacturer_name = Column(String)
    product_name = Column(String)
    licence_number = Column(String)
    test_report_id = Column(String)
    certificate_date_issued = Column(DateTime)
    certificate_lab = Column(String)
    certificate_details = Column(String)
    collector_type = Column(Enum(CollectorTypes), nullable=False)
    iam_method = relationship("IAM_Method", back_populates='collector', uselist=False, cascade="all, delete",
                              passive_deletes=True)
    test_type = Column(Enum(t_types))
    test_reference_area = Column(Enum(ref_a_types))
    calculated_parameters = Column(JSON)

    # No limit checks for these attributes to avoid code duplication with self._set_collector_parameters()
    area_gr = ComponentParam('m**2', minimum=0.1)
    area_ap = ComponentParam('m**2', minimum=0.1)
    gross_length = ComponentParam('cm', minimum=0)
    gross_width = ComponentParam('cm', minimum=0)
    gross_height = ComponentParam('cm', minimum=0)
    a1 = ComponentParam('W m**-2 K**-1')
    a2 = ComponentParam('W m**-2 K**-2')
    a5 = ComponentParam('J m**-2 K**-1')
    a8 = ComponentParam('W m**-2 K**-4')
    kd = ComponentParam('')
    eta0b = ComponentParam('')
    eta0hem = ComponentParam('')
    f_prime = ComponentParam('', minimum=0, maximum=1)
    concentration_ratio = ComponentParam('', minimum=1)

    def __init__(self, test_reference_area, test_type, gross_length, collector_type: CollectorTypes,
                 iam_method: IAM_Method = None, concentration_ratio=None,
                 name=None, manufacturer_name=None, product_name=None, test_report_id=None, licence_number=None,
                 certificate_date_issued=None, certificate_lab=None, certificate_details=None,
                 area_gr=None, area_ap=None, gross_width=None, gross_height=None,
                 a1=None, a2=None, a5=None, a8=None, kd=None, eta0b=None, eta0hem=None, f_prime=None, plant=None):

        self.test_reference_area = self._infer_test_reference_area(test_reference_area)
        self.test_type = self._infer_test_type(test_type)
        self.iam_method = iam_method

        self.name = name
        self.manufacturer_name = manufacturer_name
        self.product_name = product_name

        self.licence_number = licence_number
        self.test_report_id = test_report_id
        self.certificate_date_issued = certificate_date_issued
        self.certificate_lab = certificate_lab
        self.certificate_details = certificate_details
        self.collector_type = collector_type
        self.concentration_ratio = concentration_ratio
        # self.description = description

        if gross_length is None:
            raise CollectorDefinitionError('Collector "gross_length" is None, but must be specified.')
        self.gross_length = gross_length
        self.gross_width = gross_width
        self.gross_height = gross_height
        self.f_prime = f_prime

        self.a1 = None
        self.a2 = None
        self.a5 = None
        self.a8 = None
        self.kd = None
        self.eta0b = None
        self.eta0hem = None
        self.calculated_parameters = {}
        self._set_collector_parameters(uu.parse_quantity(area_gr), uu.parse_quantity(area_ap), uu.parse_quantity(a1),
                                       uu.parse_quantity(a2), uu.parse_quantity(a5), uu.parse_quantity(a8),
                                       uu.parse_quantity(kd),
                                       uu.parse_quantity(eta0b), uu.parse_quantity(eta0hem))

    @sqlalchemy.orm.validates('iam_method')
    def _validate_iam_method(self, _, val):
        if isinstance(val, dict):
            val = copy.copy(val)
            # because the iam methods expect Quantities, we need to convert them here in case we have dict...
            for key, value in val.items():
                if "magnitude" in value:
                    val[key] = Q(value["magnitude"], value["units"])
            return iam_methods.__dict__[val.pop('method_type')](**val)
        return val

    def _infer_test_type(self, test_type):
        """Returns test type (static, dynamic) based on user input."""
        if test_type is None:
            raise CollectorDefinitionError(
                'Collector "test_type" is None, but must be specified. Use: ' + ", ".join(self.VALID_TEST_TYPES))
        elif test_type.lower() not in [s.lower() for s in self.VALID_TEST_TYPES]:
            raise ValueError(f'Parameter "test_type" must be one of {self.VALID_TEST_TYPES}.')

        if test_type.lower() in ['sst', 'static']:
            return 'SST'
        else:
            return 'QDT'

    def _infer_test_reference_area(self, area):
        if area is None:
            raise CollectorDefinitionError(
                'Collector "test_reference_area" is None, but must be specified. Use: ' + ", ".join(
                    self.VALID_AREA_TYPES))
        if area.lower() not in [s.lower() for s in self.VALID_AREA_TYPES]:
            raise ValueError(f'Parameter "test_reference_area" must be one of {self.VALID_AREA_TYPES}.')
        if area.lower() in ['gross', 'area_gr']:
            return 'gross'
        else:
            return 'aperture'

    def _set_collector_parameters(self, area_gr, area_ap, a1, a2, a5, a8, kd, eta0b, eta0hem):
        """
        Checks and converts provided collector information. Sets instance attributes if collector definition is sane.

        Note
        ----
        Converts given collector parameters to gross area.
        Checks that we have a complete and valid Collector definition, for both self.test_type cases 'SST' | 'QDT'.

        Raises
        ------
        CollectorDefinitionException
            If definition of collector parameters is incomplete or contradictory.
        TypeError, ValueError
            May be raised by check_quantity().
        """

        # Check if required datapoints exist for specified method
        is_dynamic_test = self.test_type == 'QDT'
        if is_dynamic_test:
            if kd is None:
                raise CollectorDefinitionError("""If test_type=='dynamic', 'kd' must be provided.""")

        # Estimation / calculation of missing parameters, if needed
        if kd is None:
            kd, info = estimate_kd_Hess_and_Hanby(self.iam_method)
            self.calculated_parameters['kd'] = info
        if eta0hem is None:
            if eta0b is None:
                raise CollectorDefinitionError("""Either 'eta0b' or 'eta0hem' must be provided in the 
                collector definition, but both are missing.""")
            eta0hem, info = estimate_eta0hem(eta0b=eta0b, kd=kd)
            self.calculated_parameters['eta0hem'] = info
        if eta0b is None:
            if eta0hem is None:
                raise CollectorDefinitionError("""Either 'eta0b' or 'eta0hem' must be provided in the 
                collector definition, but both are missing.""")
            eta0b, info = estimate_eta0b(eta0hem=eta0hem, kd=kd)
            self.calculated_parameters['eta0b'] = info

        # Convert to gross area if needed
        is_aperture = self.test_reference_area == 'aperture'
        if is_aperture:
            if None in [area_gr, area_ap]:
                raise CollectorDefinitionError("""If test_reference_area=='aperture', both 'area_gr' and 'area_ap' 
                    must be provided.""")
            if area_ap > area_gr:
                raise CollectorDefinitionError("""Aperture area 'area_ap' must be smaller than gross area 'area_gr'.""")

            conversion_factor = (area_ap / area_gr)
            a1 = a1 * conversion_factor
            a2 = a2 * conversion_factor
            a5 = a5 * conversion_factor
            a8 = a8 * conversion_factor if a8 is not None else None
            eta0b = eta0b * conversion_factor if eta0b is not None else None
            eta0hem = eta0hem * conversion_factor if eta0hem is not None else None

        # Set values and check range
        self.area_gr = uu.check_quantity(area_gr, 'm**2', 0.1, none_allowed=True)
        self.area_ap = uu.check_quantity(area_ap, 'm**2', 0.1, none_allowed=True)
        self.a1 = uu.check_quantity(a1, 'W m**-2 K**-1', min_limit=0, max_limit=20)
        self.a2 = uu.check_quantity(a2, 'W m**-2 K**-2', min_limit=0, max_limit=1)
        self.a5 = uu.check_quantity(a5, 'J m**-2 K**-1', min_limit=0, max_limit=100000)
        self.a8 = uu.check_quantity(a8, 'W m**-2 K**-4', min_limit=0, max_limit=1e-5, none_allowed=True)
        self.eta0hem = uu.check_quantity(eta0hem, min_limit=0, max_limit=1)
        self.eta0b = uu.check_quantity(eta0b, min_limit=0, max_limit=1)
        self.kd = uu.check_quantity(kd, min_limit=0, max_limit=1)

        return

    def is_attrib_missing(self, attrib_name):
        # May raise AttributeError
        attrib = getattr(self, attrib_name)
        if attrib is None:
            return True
        return False

    def __eq__(self, other):
        try:
            inst = inspect(self)
            attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs if c_attr.key != 'id']

            for attr in attr_names:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True
        except AttributeError:
            return False


class UninitialisedCollector(Collector):
    def __init__(self, collector_name, parent, attribute):
        self.name = collector_name
        self.parent = parent
        self.attribute = attribute


def estimate_eta0hem(eta0b: Q, kd: Q) -> Tuple[Q, str]:
    """
    Calculates the hemispherical peak collector efficiency 'eta_0hem'
    based on the QDT-SST conversion formulas in EN ISO 9806 ANNEX B.

    Parameters
    ----------
    eta0b: beam peak collector efficiency based on QDT test
    kd:  diffuse incidence angle

    Returns
    -------
    eta0hem: Quantity, estimated hemispherical peak collector efficiency based on SST test
    info: string, information on calculation method used
    """
    eta0hem = eta0b * (0.85 + 0.15 * kd)
    info = 'Parameter "eta0hem" (hemispherical peak collector efficiency) calculated based on "eta0b" and diffuse ' \
           'incidence angle modifier "Kd" using the formula: eta0hem = eta0b * (0.85 + 0.15 * Kd)'
    return eta0hem, info


def estimate_eta0b(eta0hem: Q, kd: Q) -> Tuple[Q, str]:
    """
    Calculates the beam peak collector efficiency 'eta_0b'
    based on the SST-QDT conversion formulas in EN ISO 9806 ANNEX B.

    Parameters
    ----------
    eta0hem: hemispherical peak collector efficiency based on SST test
    kd:  diffuse incidence angle

    Returns
    -------
    eta0hem: Quantity, estimated hemispherical peak collector efficiency based on QDT test
    info: string, information on calculation method used
    """
    eta0b = eta0hem / (0.85 + 0.15 * kd)
    info = 'Parameter "eta0b" (beam peak collector efficiency) calculated based on "eta0hem" and diffuse incidence ' \
           'angle modifier "Kd" using the formula: eta0b = eta0hem / (0.85 + 0.15 * Kd)'
    return eta0b, info


def estimate_kd_Hess_and_Hanby(iam_method: IAM_Method) -> Tuple[Q, str]:
    """
    Estimates the diffuse IAM (incidence angle modifier) ``Kd`` by integrating the IAM values for beam irradiation
    over the hemispherical plane. Assumes isotropic diffuse radiation (which typically underestimates the derived ``Kd``
    values).

    Parameters
    ----------
    iam_method : IAM_Method
        instance based on a _IAM_Method class with a method ``get_iam(aoi, azimuth_diff)`` to calculate the iam based
        on the angle of incidence ``aoi`` and the solar azimuth angle ``phi``

    Returns
    -------
    kd: Quantity, estimated diffuse radiation incidence angle modifier
    info: string, information on calculation method used

    References
    ----------
    S. Hess and V. I. Hanby, “Collector Simulation Model with Dynamic Incidence Angle Modifier for Anisotropic Diffuse
    Irradiance,” Energy Procedia, vol. 48, pp. 87–96, 2014, doi: 10.1016/j.egypro.2014.02.011.
    https://repositorio.lneg.pt/bitstream/10400.9/1063/1/SOLARTHRMAL.pdf
    """

    n_range = 180
    min_angle = 0
    max_angle = 90
    theta_range = np.linspace(min_angle, max_angle, n_range, endpoint=False)
    phi_range = np.linspace(-max_angle, max_angle, n_range, endpoint=False)
    ai_theta = (max_angle - min_angle) / n_range
    ai_phi = 2 * ai_theta

    angles = np.array(np.meshgrid(theta_range, phi_range)).T.reshape(-1, 2)
    theta_angles = angles[:, [0]].flatten() + 0.5 * ai_theta
    theta_angles = Q(theta_angles, 'deg')
    phi_angles = angles[:, [1]].flatten() + 0.5 * ai_phi
    phi_angles = Q(phi_angles, 'deg')

    iam = iam_method.get_iam(aoi=theta_angles, azimuth_diff=phi_angles)

    v = np.sin(np.deg2rad(theta_angles)) * np.cos(np.deg2rad(theta_angles))
    W = v.sum()
    kd = np.multiply(v, iam).sum() / W

    info = 'Parameter "Kd" (incidence angle modifier for diffuse radiation) calculated based on integration of the ' \
           'beam IAM values over the hemispherical plane (Hess & Hanby method), as described in ' \
           'doi: 10.1016/j.egypro.2014.02.011'
    return kd, info
