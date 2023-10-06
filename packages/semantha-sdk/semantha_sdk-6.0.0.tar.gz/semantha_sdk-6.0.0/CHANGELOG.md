# Changelog for the Python SDK for the semantha platform
## [6.0.0] 2023-10-04
### Fixed
- GET of files with different mimetype than application/json (e.g. get_as_docx)

## [5.11.1] 2023-09-21
### Removed
- **/model/domains/{domainname}/extractortables** has been removed
- **/model/domains/{domainname}/extractortables/{id}** has been removed

### Fixed
- fixed serialization on post of bulk endpoints with list of objects

## [5.11.0]
### Changed
- **/api/domains/{domainname}/summarizations** returns an object now instead of string.
- renamed class Metadata to ModelMetadata

## [5.10.0]
Improved Use Case SDK

## [5.9.0]
### Removed
- **/api/domains/{domainname}/referencedocuments/{documentid}/paragraphs/{id}/links**

## [5.8.0]
### Added
- **/api/domains/{domainname}/documentclasses/{id}/documentclasses**
- **/api/domains/{domainname}/documentclasses/{id}/referencedocuments**
- **/api/domains/{domainname}/referencedocuments/{documentid}/paragraphs/{id}/links**
- **/api/model/domains/{domainname}/backups**

SDK covers now 193/197 services.

## [5.7.0]
Added new endpoints in:
- **/api/domains/{domainname}/documenttypes/*** 
- **/api/domains/{domainname}/documentclasses/{id}/customfields**
- **/api/model/domains/{domainname}/classes/***

SDK covers now 184/197 services.


## [5.6.0]
Added most endpoints in **/api/models/* **
SDK covers now 158/180 services.

## [5.5.0]
Removed language parameter on **/api/domains/{domainname}/references**
Fixed bug on serialization of **/api/domains/{domainname}/modelinstances** response.
Fixed return of binary responses of bulk services.

## [5.4.0]
Added **new** service: 
- **/api/domains/{domainname}/summarizations** which generations a summarization for a given list of texts and a given topic.

Added support for **existing** services: 
- /api/model/domains/{domainname}/boostwords/{id}
- /api/model/domains/{domainname}/namedentities
- /api/model/domains/{domainname}/namedentities/{id}
- /api/model/domains/{domainname}/stopwords
- /api/model/domains/{domainname}/stopwords/{id}
- /api/model/domains/{domainname}/synonyms/{id}

## [5.3.0]

Added new service: **/api/domains/{domainid}/answers** with retrieval augemented answer generation based on your library entries.
Added new parameter on /modelinstances

## [5.2.0]

The SDK is now automatically generated from our openapi.json specification. It covers 71/169 (=42%) of all available services. Many class names and package names have been changed.

## [4.5.0]
Major restructuring of the SDK.
All sub-resources are directly accessible (instead of invoking getters).
That also means that (except for a few) all functions are plain get/post/delete/put/patch.
For example, in Versions < 4.5.0 a domain resource was fetched using `semantha_sdk.domains.get_one("domain_name")`.
Starting with 4.5.0 it is `semantha_sdk.domains("domain_name")`.
That also means that get/post/put/patch functions return semantha model objects (and never resources), which makes usage more consistent.
