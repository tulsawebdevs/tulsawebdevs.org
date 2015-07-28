The different bits of Information Architecture and their mapping to models

# Event
There are different types of events, these types have different purposes and therefore different types of related data. Most often used to indicate to those interested what's occurring at it.

Events are representations of humans meeting at a common location for some purpose that recur.
These events are used to represent the duplicatable structure of a group's event.

## Attributes
* type - ( like category )
* date-time
* duration
* location
* description
* contact


# Type

Types are related to events and help users differentiate them

## Attributes
* name

## Initial stored types:
* Meeting ( can have different group relations )
* Hack Night
* Hangout ( online, or IRL )
* Co-working
* Conference ( internal or external conferences, members going to or hosting )


# Meeting Occurrences

An event instance/occurrence is created when the previous instance has passed. It's used the represent an actual event.
Contains many duplicate fields imprinted from the related event so they are changeable per instance.

Connected to the Meeting type

Meeting events can have relations to:

* Event
* Talks
* Speakers
* Sub-groups (Sub groups could be a separate model and added to talks as an indicator of group participation in an event.)

over-writable data from event

* location
* agenda
* canceled


# HackNight Occurrences

Share base event attributes


# Content Categories
Can have relations to Events, Talks

describe the type of content an object can have. used in the interface to show all events that contain these categories.


# Talk
can be independent of any relationship so they can get backlogged and voted on at meetings or during the the run up to any meeting.


# Speaker
The person actually giving the talk and their contact details. To be used on the site for those interested in contacting a speaker after their given talk.


# Locations

Hold information about common event locations

## Attributes
* name
* address
* lat/lng
* parking details ( what are good places to park )
* entry info ( how to get to the event )
