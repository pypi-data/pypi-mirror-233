# pylint: disable=W0622
"""cubicweb-compound application packaging information"""

distname = "cubicweb-compound"
modname = "cubicweb_coumpound"

numversion = (1, 0, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Library cube to handle assemblies of composite entities"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {
    "cubicweb": ">= 4.0.0, < 5.0.0",
    "cubicweb_web": ">= 1.0.0, < 2.0.0",
}

__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
