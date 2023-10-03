# coding: utf-8

"""
    University Card API

     ## Introduction  The Card API allows access to information about University Cards.  The API broadly follows the principles of REST and strives to provide an interface that can be easily consumed by downstream systems.  ### Stability  This release of the Card API is a `beta` offering: a service we are moving towards live but which requires wider testing with a broader group of users. We consider the Card API as being at least as stable as the legacy card system which it aims to replace, so we encourage users to make use of the Card API rather than relying on the legacy card system.  ### Versioning  The Card API is versioned using url path prefixes in the format: `/v1beta1/cards`. This follows the pattern established by the [GCP API](https://cloud.google.com/apis/design/versioning). Breaking changes will not be made without a change in API major version, however non-breaking changes will be introduced without changes to the version path prefix. All changes will be documented in the project's [CHANGELOG](https://gitlab.developers.cam.ac.uk/uis/devops/iam/card-database/card-api/-/blob/master/CHANGELOG.md).  The available versions of the API are listed at the API's root.  ### Domain  The Card API has been designed to only expose information about University Cards and the identifiers which link a Card to a person. The API does not expose information about cardholders or the institutions that a cardholder belongs to. This is in order to combat domain crossover and to ensure the Card API does not duplicate information which is held and managed within systems such as Lookup, CamSIS or CHRIS.  It is expected that the Card API should be used alongside APIs such as Lookup which allow personal and institutional membership information to be retrieved. A tool has been written in order to allow efficient querying of the Card API using information contained within, CamSIS or CHRIS. [Usage and installation instructions for this tool can be found here](https://gitlab.developers.cam.ac.uk/uis/devops/iam/card-database/card-client).  ### Data source  The data exposed in the Card API is currently a mirror of data contained within the [Card Database](https://webservices.admin.cam.ac.uk/uc/). With data being synced from the Card Database to the Card API hourly.  In future, card data will be updated and created directly using the Card API so changes will be reflected in the Card API 'live' without this hourly sync.  ## Core entities  ### The `Card` Entity  The `Card` entity is a representation of a physical University Card. The entity contains fields indicating the status of the card and when the card has moved between different statuses. Cards held by individuals (such as students or staff) and temporary cards managed by institutions are both represented by the `Card` entity, with the former having a `cardType` of `MIFARE_PERSONAL` and the latter having a `cardType` of `MIFARE_TEMPORARY`.  Each card should have a set of `CardIdentifiers` which allow the card to be linked to an entity in another system (e.g. a person in Lookup), or record information about identifiers held within the card, such as Mifare ID.  The full `Card` entity contains a `cardNotes` field which holds a set of notes made by administrator users related to the card, as well as an `attributes` field which holds the data that is present on the physical presentation of a card. Operations which list many cards return `CardSummary` entities which omit these fields for brevity.  ### The `CardIdentifier` Entity  The `CardIdentifier` entity holds the `value` and `scheme` of a given identifier. The `value` field of a `CardIdentifier` is a simple ID string - e.g. `wgd23` or `000001`. The `scheme` field of a `CardIdentifier` indicates what system this identifier relates to or was issued by. This allows many identifiers which relate to different systems to be recorded against a single `Card`.  The supported schemes are: * `v1.person.identifiers.cam.ac.uk`: The CRSid of the person who holds this card * `person.v1.student-records.university.identifiers.cam.ac.uk`: The CamSIS identifier (USN) of the person who holds this card * `person.v1.human-resources.university.identifiers.cam.ac.uk`: The CHRIS identifier (staff number) of the person who holds this card * `person.v1.board-of-graduate-studies.university.identifiers.cam.ac.uk`: The Board of Graduate Studies identifier of the person who holds this card * `person.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy card holder ID for the person who holds this card * `mifare-identifier.v1.card.university.identifiers.cam.ac.uk`: The Mifare ID which is embedded in this card (this     identifier uniquely identifies a single card) * `mifare-number.v1.card.university.identifiers.cam.ac.uk`: The Mifare Number which is embedded in this card     (this identifier is a digest of card's legacy cardholder ID and issue number, so is not     guaranteed to be unique) * `card.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy card ID from the card database * `temporary-card.v1.card.university.identifiers.cam.ac.uk`: The temporary card ID from the card database * `photo.v1.photo.university.identifiers.cam.ac.uk`: The ID of the photo printed on this card * `barcode.v1.card.university.identifiers.cam.ac.uk`: The barcode printed on this card * `institution.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy institution ID from the card database (only populated on temporary cards)   ## Using the API  ### Auth  To authenticate against the Card API, an application must be registered within the API Service and granted access to the `University Card` product. Details of how to register an application and grant access to products can be found in the [API Service Getting Started Guide](https://developer.api.apps.cam.ac.uk/start-using-an-api).  #### Principal  Throughout this specification the term `principal` is used to describe the user or service who is making use of the API. When authenticating using the OAuth2 client credentials flow the principal shall be the application registered within the API Gateway. When authenticating using the authorization code flow, e.g. via a Single Page Application, the principal shall be the user who has authenticated and consented to give the application access to the data contained within this API - identified by their CRSid.  This specification references permissions which can be granted to any principal - please contact the API maintainers to grant a principal a specific permission.  ### Content Type  The Card API responds with JSON data. The `Content-Type` request header should be omitted or set to `application/json`. If an invalid `Content-Type` header is sent the API will respond with `415 Unsupported Media Type`.  ### Pagination  For all operations where multiple entities will be returned, the API will return a paginated result. This is to account for too many entities needing to be returned within a single response. A Paginated response has the structure:  ```json {   \"next\": \"https://<gateway_host>/card/v1beta1/cards/?cursor=cD0yMDIxLTAxL   \"previous\": null,   \"results\": [       ... the data for the current page   ] }  ```  The `next` field holds the url of the next page of results, containing a cursor which indicates to the API which page of results to return. If the `next` field is `null` no further results are available. The `previous` field can be used to navigate backwards through pages of results.  The `page_size` query parameter can be used to control the number of results to return. This defaults to 200 but can be set to a maximum of 500, if set to greater than this no error will be returned but only 500 results will be given in the response.  

    The version of the OpenAPI document: v1beta1
    Contact: devops+cardapi@uis.cam.ac.uk
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist, constr, validator
from identitylib.card_client.models.card_identifier_allowed_actions import CardIdentifierAllowedActions
from identitylib.card_client.models.card_identifier_summary import CardIdentifierSummary

class CardIdentifier(BaseModel):
    """
    The V1Beta1CardIdentifierSummarySerializer is the same as the V1Alpha1 version, but with the identifiers not being mapped to their deprecated forms.
    """
    allowed_actions: CardIdentifierAllowedActions = Field(..., alias="allowedActions")
    card_requests: conlist(StrictStr) = Field(..., alias="cardRequests", description="Card requests identified by this identifier")
    cards: conlist(StrictStr) = Field(..., description="Cards identified by this identifier")
    deleted_at: Optional[datetime] = Field(None, alias="deletedAt")
    id: constr(strict=True) = Field(...)
    is_deleted: Optional[StrictBool] = Field(None, alias="isDeleted")
    is_highest_primary_identifier: Optional[StrictBool] = Field(None, alias="isHighestPrimaryIdentifier", description="Card identifier is highest primary identifier")
    related_identifiers: conlist(CardIdentifierSummary) = Field(..., alias="relatedIdentifiers")
    retain_until: Optional[datetime] = Field(None, alias="retainUntil", description="If non-NULL, the minimum period the record should be retained")
    scheme: StrictStr = Field(..., description="The identifier's scheme  * `v1.person.identifiers.cam.ac.uk` - CRSID of the Card Holder * `person.v1.student-records.university.identifiers.cam.ac.uk` - CamSIS Identifier of the Card Holder * `person.v1.human-resources.university.identifiers.cam.ac.uk` - CHRIS Identifier of the Card Holder * `person.v1.board-of-graduate-studies.university.identifiers.cam.ac.uk` - Board of Graduate Studies Identifier of the Card Holder * `person.v1.legacy-card.university.identifiers.cam.ac.uk` - Legacy Card DB Card Holder Identifier * `mifare-identifier.v1.card.university.identifiers.cam.ac.uk` - Physical Card's native Identifier * `mifare-number.v1.card.university.identifiers.cam.ac.uk` - Our Identifier on the Physical Card * `card.v1.legacy-card.university.identifiers.cam.ac.uk` - Legacy Card DB Card Identifier * `temporary-card.v1.card.university.identifiers.cam.ac.uk` - Legacy Card DB Card Identifier for Temporary Cards * `photo.v1.photo.university.identifiers.cam.ac.uk` - Photo Identifier for the Photo Printed on the Physical Card * `barcode.v1.card.university.identifiers.cam.ac.uk` - Library Identifier Printed as the Barcode on the Physical Card * `institution.v1.legacy-card.university.identifiers.cam.ac.uk` - Legacy Card DB Institution Id for Temporary Cards")
    value: StrictStr = Field(..., description="The identifier's value")
    __properties = ["allowedActions", "cardRequests", "cards", "deletedAt", "id", "isDeleted", "isHighestPrimaryIdentifier", "relatedIdentifiers", "retainUntil", "scheme", "value"]

    @validator('id')
    def id_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", value):
            raise ValueError(r"must validate the regular expression /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/")
        return value

    @validator('scheme')
    def scheme_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('v1.person.identifiers.cam.ac.uk', 'person.v1.student-records.university.identifiers.cam.ac.uk', 'person.v1.human-resources.university.identifiers.cam.ac.uk', 'person.v1.board-of-graduate-studies.university.identifiers.cam.ac.uk', 'person.v1.legacy-card.university.identifiers.cam.ac.uk', 'mifare-identifier.v1.card.university.identifiers.cam.ac.uk', 'mifare-number.v1.card.university.identifiers.cam.ac.uk', 'card.v1.legacy-card.university.identifiers.cam.ac.uk', 'temporary-card.v1.card.university.identifiers.cam.ac.uk', 'photo.v1.photo.university.identifiers.cam.ac.uk', 'barcode.v1.card.university.identifiers.cam.ac.uk', 'institution.v1.legacy-card.university.identifiers.cam.ac.uk'):
            raise ValueError("must be one of enum values ('v1.person.identifiers.cam.ac.uk', 'person.v1.student-records.university.identifiers.cam.ac.uk', 'person.v1.human-resources.university.identifiers.cam.ac.uk', 'person.v1.board-of-graduate-studies.university.identifiers.cam.ac.uk', 'person.v1.legacy-card.university.identifiers.cam.ac.uk', 'mifare-identifier.v1.card.university.identifiers.cam.ac.uk', 'mifare-number.v1.card.university.identifiers.cam.ac.uk', 'card.v1.legacy-card.university.identifiers.cam.ac.uk', 'temporary-card.v1.card.university.identifiers.cam.ac.uk', 'photo.v1.photo.university.identifiers.cam.ac.uk', 'barcode.v1.card.university.identifiers.cam.ac.uk', 'institution.v1.legacy-card.university.identifiers.cam.ac.uk')")
        return value

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> CardIdentifier:
        """Create an instance of CardIdentifier from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "allowed_actions",
                            "id",
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of allowed_actions
        if self.allowed_actions:
            _dict['allowedActions'] = self.allowed_actions.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in related_identifiers (list)
        _items = []
        if self.related_identifiers:
            for _item in self.related_identifiers:
                if _item:
                    _items.append(_item.to_dict())
            _dict['relatedIdentifiers'] = _items
        # set to None if deleted_at (nullable) is None
        # and __fields_set__ contains the field
        if self.deleted_at is None and "deleted_at" in self.__fields_set__:
            _dict['deletedAt'] = None

        # set to None if retain_until (nullable) is None
        # and __fields_set__ contains the field
        if self.retain_until is None and "retain_until" in self.__fields_set__:
            _dict['retainUntil'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CardIdentifier:
        """Create an instance of CardIdentifier from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CardIdentifier.parse_obj(obj)

        _obj = CardIdentifier.parse_obj({
            "allowed_actions": CardIdentifierAllowedActions.from_dict(obj.get("allowedActions")) if obj.get("allowedActions") is not None else None,
            "card_requests": obj.get("cardRequests"),
            "cards": obj.get("cards"),
            "deleted_at": obj.get("deletedAt"),
            "id": obj.get("id"),
            "is_deleted": obj.get("isDeleted"),
            "is_highest_primary_identifier": obj.get("isHighestPrimaryIdentifier"),
            "related_identifiers": [CardIdentifierSummary.from_dict(_item) for _item in obj.get("relatedIdentifiers")] if obj.get("relatedIdentifiers") is not None else None,
            "retain_until": obj.get("retainUntil"),
            "scheme": obj.get("scheme"),
            "value": obj.get("value")
        })
        return _obj


