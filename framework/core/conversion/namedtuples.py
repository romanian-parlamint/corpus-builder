"""Defines named tuples."""
from collections import namedtuple

Event = namedtuple('Event', ['org_id', 'event_id', 'start_date', 'end_date'])

NameCorrection = namedtuple('NameCorrection', ['written_name', 'actual_name'])

PersonalInformation = namedtuple(
    'PersonalInformation', ["first_name", "last_name", "sex", "profile_image"])

LegislativeTerm = namedtuple(
    'LegislativeTerm',
    ['term_id', 'number', 'start_date', 'end_date', 'description'])

ParliamentaryGroup = namedtuple('ParliamentaryGroup', ['Acronym', 'Name'])
