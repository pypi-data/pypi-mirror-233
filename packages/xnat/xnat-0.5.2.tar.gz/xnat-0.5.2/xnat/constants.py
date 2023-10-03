# Copyright 2011-2015 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Optional, Dict, List, Set

TYPE_HINTS: Dict[str, Optional[str]] = {
    'demographics': 'xnat:demographicData',
    'investigator': 'xnat:investigatorData',
    'metadata': 'xnat:subjectMetadata',
    'pi': 'xnat:investigatorData',
    'studyprotocol': 'xnat:studyProtocol',
    'validation': 'xnat:validationData',
    'baseimage': 'xnat:abstractResource',
    'projects': 'xnat:projectData',
    'subjects': 'xnat:subjectData',
    'experiments': None,  # Can be many types, need to check each time
    'scans': None,  # Can be many types, need to check each time
    'resources': None,  # Can be many types, need to check each time
    'assessors': None,   # Can be many types, need to check each time
    'reconstructions': None,  # Can be many types, need to check each time
    'files': 'xnat:fileData',
}

FIELD_HINTS: Dict[str, str] = {
    'xnat:projectData': 'projects',
    'xnat:subjectData': 'subjects',
    'xnat:experimentData': 'experiments',
    'xnat:imageScanData': 'scans',
    'xnat:reconstructedImageData': 'reconstructions',
    'xnat:imageAssessorData': 'assessors',
    'xnat:abstractResource': 'resources',
    'xnat:fileData': 'files',
    'addParam': 'parameters/addParam',
}

DATA_FIELD_HINTS: Dict[str, str] = {
    'addParam': 'addField'
}

# The following xsi_types are objects with their own REST paths, the
# other are nested in the xml of their parent.
CORE_REST_OBJECTS: Set[str] = {
    'xnat:projectData',
    'xnat:subjectData',
    'xnat:experimentData',
    'xnat:reconstructedImageData',
    'xnat:imageAssessorData',
    'xnat:imageScanData',
    'xnat:abstractResource',
    'xnat:fileData',
}

# Override base class for some types
OVERRIDE_BASE = {
#    'xnat:demographicData': 'XNATNestedObjectMixin',
}

# These are additions to the DisplayIdentifier set in the xsd files
SECONDARY_LOOKUP_FIELDS: Dict[str, str] = {
    'xnat:projectData': 'name',
    'xnat:imageScanData': 'type',
    'xnat:fileData': 'name',
}

# DEFAULT SCHEMAS IN XNAT 1.7
DEFAULT_SCHEMAS: List[str] = [
    "security",
    "xnat",
    "assessments",
    "screening/screeningAssessment",
    "pipeline/build",
    "pipeline/repository",
    "pipeline/workflow",
    "birn/birnprov",
    "catalog",
    "project",
    "validation/protocolValidation",
    "xdat/display",
    "xdat",
    "xdat/instance",
    "xdat/PlexiViewer"
]


TIMEZONES_STRING = """-12 Y
-11 X NUT SST
-10 W CKT HAST HST TAHT TKT
-9 V AKST GAMT GIT HADT HNY
-8 U AKDT CIST HAY HNP PST PT
-7 T HAP HNR MST PDT
-6 S CST EAST GALT HAR HNC MDT
-5 R CDT COT EASST ECT EST ET HAC HNE PET
-4 Q AST BOT CLT COST EDT FKT GYT HAE HNA PYT
-3 P ADT ART BRT CLST FKST GFT HAA PMST PYST SRT UYT WGT
-2 O BRST FNT PMDT UYST WGST
-1 N AZOT CVT EGT
0 Z EGST GMT UTC WET WT
1 A CET DFT WAT WEDT WEST
2 B CAT CEDT CEST EET SAST WAST
3 C EAT EEDT EEST IDT MSK
4 D AMT AZT GET GST KUYT MSD MUT RET SAMT SCT
5 E AMST AQTT AZST HMT MAWT MVT PKT TFT TJT TMT UZT YEKT
6 F ALMT BIOT BTT IOT KGT NOVT OMST YEKST
7 G CXT DAVT HOVT ICT KRAT NOVST OMSST THA WIB
8 H ACT AWST BDT BNT CAST HKT IRKT KRAST MYT PHT SGT ULAT WITA WST
9 I AWDT IRKST JST KST PWT TLT WDT WIT YAKT
10 K AEST ChST PGT VLAT YAKST YAPT
11 L AEDT LHDT MAGT NCT PONT SBT VLAST VUT
12 M ANAST ANAT FJT GILT MAGST MHT NZST PETST PETT TVT WFT
13 FJST NZDT
11.5 NFT
10.5 ACDT LHST
9.5 ACST
6.5 CCT MMT
5.75 NPT
5.5 SLT
4.5 AFT IRDT
3.5 IRST
-2.5 HAT NDT
-3.5 HNT NST NT
-4.5 HLV VET
-9.5 MART MIT"""


# Convert the string into a dictionary to be used by dateutil.parser.parse,
# see https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse
TIMEZONES_DICT = {}
for _timezone in TIMEZONES_STRING.split('\n'):
    _timezone = _timezone.split()
    _offset = int(float(_timezone[0]) * 3600)
    for _code in _timezone[1:]:
        TIMEZONES_DICT[_code] = _offset
