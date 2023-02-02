
#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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
#
"""Developer comments."""

# pylint: disable=E1101


# ISSUE WITH HSPY DEFAULTS FOR MISSING VENDOR DOCS CAUSING NON-REPRODUCIBLE tSTAMPS
# already the example with Adrien Teutrie's *.emd file shows
# that the intended start_time and end_time as required by the appdef
# are practically not reliable because, tested for hyperspy==1.7.1,
# the times which are injected into the hyperspy metainfo object by the emd
# i/o routine are substantially relying on default rules. An example:
# First hyperspy asks FEI for an AcquisitionStartDatetime
# which is what intuitively one would consider as the relevant time
# however, if this metadata key is not included in the *.emd file,
# hyperspy just adds for "convenience" the local system time!
# however, this retrieval of the local system time depends heavily on
# which version of the underlying libraries and operation system is used !
# in a nutshell, what we ideally want is, to phrase it with python's
# datetime package "time-zone-aware" objects to interact with and convert
# times properly into one another
# https://www.bloomberg.com/company/stories/work-dates-time-python/
# but this is not what we face unfortunately, so consequently the parser
# should leave the field marked with a note that the relevant time
# was not reliably retrievable to avoid a potential proliferation of
# mistakes down the analysis pipeline

# this makes clear that to interpret and reproduce the content which
# an emd reader creates on a given emd file, the results will be different
# on different computers simply already because of these silent defaults
# so strictly speaking one would have to run the parser inside a
# container in the nomad oasis and not on the local host machine as if
# one would do usually with somebody having a local instance of an oasis
# and thus this local oasis would be used the local operating system and
# installation to retrieve the start time and end time data from

# from datetime import datetime
# import pytz
# timezone = pytz.timezone(dct["General"]['time_zone'])
# from dateutil import tz
# from dateutil.tz import *
# from datetime import *
# tz.tzlocal().tzname(datetime.today())
# see KabulTz example here https://docs.python.org/3/library/datetime.html


# ISSUES WITH ROUTING RAW and PROCESSED (META)DATA to SPECIFIC tSTAMPED HIERARCHIES
# ##MK::the key question is how parsable content
# (clss instances) from a hyperspy run stand in relation?
# for instance if we load a vendor file and hspy spits out
# it contains a HAADF, a sum EDS spectrum, and a EDS spectrum stack
# can we safely assume that these images have been taken
# in the same event? i.e. can we consider that the microscope
# was able enough when the HAADF was taken and thereafter
# the user acquired the spectrum/(a)? In general we cannot assume
# that this is the case. However, hyperspy implies that
# this is the case, given that hspy can in many cases simply
# also not build on or even parse timestamps and interpret them
# consequently, all we get is a specific view of the experiment and
# some key steps and metadata to its processing
# in summary, NXem is much more general than what is commonly
# available via interoperability improving tools like hyperspy

# These points substantiate that two key ingredients are missing
# a proper time(stamp) tracking of actions on the microscope and a
# agreed upon documented! format how to understand these time stamps
#   of course eventually anonymized wrt to who was the user
#   but at least a clear statement when these were taken
# a proper and much more detailed documentation of the
#   vendor file formats and their relation to the software library
#   which and when in which context the tool was running
#   so that hspy devlopers can extract
#   these time stamps and use them to route the data
#   into more useful interoperable respective places.
