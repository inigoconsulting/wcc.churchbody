from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import wcc.churchbody


WCC_CHURCHBODY = PloneWithPackageLayer(
    zcml_package=wcc.churchbody,
    zcml_filename='testing.zcml',
    gs_profile_id='wcc.churchbody:testing',
    name="WCC_CHURCHBODY")

WCC_CHURCHBODY_INTEGRATION = IntegrationTesting(
    bases=(WCC_CHURCHBODY, ),
    name="WCC_CHURCHBODY_INTEGRATION")

WCC_CHURCHBODY_FUNCTIONAL = FunctionalTesting(
    bases=(WCC_CHURCHBODY, ),
    name="WCC_CHURCHBODY_FUNCTIONAL")
