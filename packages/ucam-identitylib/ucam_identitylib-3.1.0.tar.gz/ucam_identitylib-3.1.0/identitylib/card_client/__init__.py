# coding: utf-8

# flake8: noqa

"""
    University Card API

     ## Introduction  The Card API allows access to information about University Cards.  The API broadly follows the principles of REST and strives to provide an interface that can be easily consumed by downstream systems.  ### Stability  This release of the Card API is a `beta` offering: a service we are moving towards live but which requires wider testing with a broader group of users. We consider the Card API as being at least as stable as the legacy card system which it aims to replace, so we encourage users to make use of the Card API rather than relying on the legacy card system.  ### Versioning  The Card API is versioned using url path prefixes in the format: `/v1beta1/cards`. This follows the pattern established by the [GCP API](https://cloud.google.com/apis/design/versioning). Breaking changes will not be made without a change in API major version, however non-breaking changes will be introduced without changes to the version path prefix. All changes will be documented in the project's [CHANGELOG](https://gitlab.developers.cam.ac.uk/uis/devops/iam/card-database/card-api/-/blob/master/CHANGELOG.md).  The available versions of the API are listed at the API's root.  ### Domain  The Card API has been designed to only expose information about University Cards and the identifiers which link a Card to a person. The API does not expose information about cardholders or the institutions that a cardholder belongs to. This is in order to combat domain crossover and to ensure the Card API does not duplicate information which is held and managed within systems such as Lookup, CamSIS or CHRIS.  It is expected that the Card API should be used alongside APIs such as Lookup which allow personal and institutional membership information to be retrieved. A tool has been written in order to allow efficient querying of the Card API using information contained within, CamSIS or CHRIS. [Usage and installation instructions for this tool can be found here](https://gitlab.developers.cam.ac.uk/uis/devops/iam/card-database/card-client).  ### Data source  The data exposed in the Card API is currently a mirror of data contained within the [Card Database](https://webservices.admin.cam.ac.uk/uc/). With data being synced from the Card Database to the Card API hourly.  In future, card data will be updated and created directly using the Card API so changes will be reflected in the Card API 'live' without this hourly sync.  ## Core entities  ### The `Card` Entity  The `Card` entity is a representation of a physical University Card. The entity contains fields indicating the status of the card and when the card has moved between different statuses. Cards held by individuals (such as students or staff) and temporary cards managed by institutions are both represented by the `Card` entity, with the former having a `cardType` of `MIFARE_PERSONAL` and the latter having a `cardType` of `MIFARE_TEMPORARY`.  Each card should have a set of `CardIdentifiers` which allow the card to be linked to an entity in another system (e.g. a person in Lookup), or record information about identifiers held within the card, such as Mifare ID.  The full `Card` entity contains a `cardNotes` field which holds a set of notes made by administrator users related to the card, as well as an `attributes` field which holds the data that is present on the physical presentation of a card. Operations which list many cards return `CardSummary` entities which omit these fields for brevity.  ### The `CardIdentifier` Entity  The `CardIdentifier` entity holds the `value` and `scheme` of a given identifier. The `value` field of a `CardIdentifier` is a simple ID string - e.g. `wgd23` or `000001`. The `scheme` field of a `CardIdentifier` indicates what system this identifier relates to or was issued by. This allows many identifiers which relate to different systems to be recorded against a single `Card`.  The supported schemes are: * `v1.person.identifiers.cam.ac.uk`: The CRSid of the person who holds this card * `person.v1.student-records.university.identifiers.cam.ac.uk`: The CamSIS identifier (USN) of the person who holds this card * `person.v1.human-resources.university.identifiers.cam.ac.uk`: The CHRIS identifier (staff number) of the person who holds this card * `person.v1.board-of-graduate-studies.university.identifiers.cam.ac.uk`: The Board of Graduate Studies identifier of the person who holds this card * `person.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy card holder ID for the person who holds this card * `mifare-identifier.v1.card.university.identifiers.cam.ac.uk`: The Mifare ID which is embedded in this card (this     identifier uniquely identifies a single card) * `mifare-number.v1.card.university.identifiers.cam.ac.uk`: The Mifare Number which is embedded in this card     (this identifier is a digest of card's legacy cardholder ID and issue number, so is not     guaranteed to be unique) * `card.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy card ID from the card database * `temporary-card.v1.card.university.identifiers.cam.ac.uk`: The temporary card ID from the card database * `photo.v1.photo.university.identifiers.cam.ac.uk`: The ID of the photo printed on this card * `barcode.v1.card.university.identifiers.cam.ac.uk`: The barcode printed on this card * `institution.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy institution ID from the card database (only populated on temporary cards)   ## Using the API  ### Auth  To authenticate against the Card API, an application must be registered within the API Service and granted access to the `University Card` product. Details of how to register an application and grant access to products can be found in the [API Service Getting Started Guide](https://developer.api.apps.cam.ac.uk/start-using-an-api).  #### Principal  Throughout this specification the term `principal` is used to describe the user or service who is making use of the API. When authenticating using the OAuth2 client credentials flow the principal shall be the application registered within the API Gateway. When authenticating using the authorization code flow, e.g. via a Single Page Application, the principal shall be the user who has authenticated and consented to give the application access to the data contained within this API - identified by their CRSid.  This specification references permissions which can be granted to any principal - please contact the API maintainers to grant a principal a specific permission.  ### Content Type  The Card API responds with JSON data. The `Content-Type` request header should be omitted or set to `application/json`. If an invalid `Content-Type` header is sent the API will respond with `415 Unsupported Media Type`.  ### Pagination  For all operations where multiple entities will be returned, the API will return a paginated result. This is to account for too many entities needing to be returned within a single response. A Paginated response has the structure:  ```json {   \"next\": \"https://<gateway_host>/card/v1beta1/cards/?cursor=cD0yMDIxLTAxL   \"previous\": null,   \"results\": [       ... the data for the current page   ] }  ```  The `next` field holds the url of the next page of results, containing a cursor which indicates to the API which page of results to return. If the `next` field is `null` no further results are available. The `previous` field can be used to navigate backwards through pages of results.  The `page_size` query parameter can be used to control the number of results to return. This defaults to 200 but can be set to a maximum of 500, if set to greater than this no error will be returned but only 500 results will be given in the response.  

    The version of the OpenAPI document: v1beta1
    Contact: devops+cardapi@uis.cam.ac.uk
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


__version__ = "1.0.0"

# import apis into sdk package
from identitylib.card_client.api.api_versions_api import APIVersionsApi
from identitylib.card_client.api.permissions_api import PermissionsApi
from identitylib.card_client.api.v1beta1_api import V1beta1Api

# import ApiClient
from identitylib.card_client.api_response import ApiResponse
from identitylib.card_client.api_client import ApiClient
from identitylib.card_client.configuration import Configuration
from identitylib.card_client.exceptions import OpenApiException
from identitylib.card_client.exceptions import ApiTypeError
from identitylib.card_client.exceptions import ApiValueError
from identitylib.card_client.exceptions import ApiKeyError
from identitylib.card_client.exceptions import ApiAttributeError
from identitylib.card_client.exceptions import ApiException

# import models into sdk package
from identitylib.card_client.models.api_versions import APIVersions
from identitylib.card_client.models.available_barcode import AvailableBarcode
from identitylib.card_client.models.available_barcode_batch_invalid import AvailableBarcodeBatchInvalid
from identitylib.card_client.models.available_barcode_batch_request import AvailableBarcodeBatchRequest
from identitylib.card_client.models.available_barcode_batch_response_type import AvailableBarcodeBatchResponseType
from identitylib.card_client.models.available_barcode_request import AvailableBarcodeRequest
from identitylib.card_client.models.bad_request import BadRequest
from identitylib.card_client.models.card import Card
from identitylib.card_client.models.card_bulk_update_element_request import CardBulkUpdateElementRequest
from identitylib.card_client.models.card_bulk_update_request import CardBulkUpdateRequest
from identitylib.card_client.models.card_bulk_update_response_type import CardBulkUpdateResponseType
from identitylib.card_client.models.card_filter_request import CardFilterRequest
from identitylib.card_client.models.card_identifier import CardIdentifier
from identitylib.card_client.models.card_identifier_allowed_actions import CardIdentifierAllowedActions
from identitylib.card_client.models.card_identifier_bulk_update_details import CardIdentifierBulkUpdateDetails
from identitylib.card_client.models.card_identifier_bulk_update_element_request import CardIdentifierBulkUpdateElementRequest
from identitylib.card_client.models.card_identifier_bulk_update_request import CardIdentifierBulkUpdateRequest
from identitylib.card_client.models.card_identifier_bulk_update_response_type import CardIdentifierBulkUpdateResponseType
from identitylib.card_client.models.card_identifier_destroy_response_type import CardIdentifierDestroyResponseType
from identitylib.card_client.models.card_identifier_summary import CardIdentifierSummary
from identitylib.card_client.models.card_identifier_summary_request import CardIdentifierSummaryRequest
from identitylib.card_client.models.card_identifier_update_request import CardIdentifierUpdateRequest
from identitylib.card_client.models.card_identifier_update_response_type import CardIdentifierUpdateResponseType
from identitylib.card_client.models.card_logo import CardLogo
from identitylib.card_client.models.card_note import CardNote
from identitylib.card_client.models.card_note_create_request_type_request import CardNoteCreateRequestTypeRequest
from identitylib.card_client.models.card_note_destroy_response_type import CardNoteDestroyResponseType
from identitylib.card_client.models.card_rfid_config_list_response_type import CardRFIDConfigListResponseType
from identitylib.card_client.models.card_request import CardRequest
from identitylib.card_client.models.card_request_bulk_update_details import CardRequestBulkUpdateDetails
from identitylib.card_client.models.card_request_bulk_update_element_request import CardRequestBulkUpdateElementRequest
from identitylib.card_client.models.card_request_bulk_update_request import CardRequestBulkUpdateRequest
from identitylib.card_client.models.card_request_bulk_update_response_type import CardRequestBulkUpdateResponseType
from identitylib.card_client.models.card_request_create_type_request import CardRequestCreateTypeRequest
from identitylib.card_client.models.card_request_distinct_values import CardRequestDistinctValues
from identitylib.card_client.models.card_request_summary import CardRequestSummary
from identitylib.card_client.models.card_request_update_request import CardRequestUpdateRequest
from identitylib.card_client.models.card_request_update_response_type import CardRequestUpdateResponseType
from identitylib.card_client.models.card_request_update_update_request import CardRequestUpdateUpdateRequest
from identitylib.card_client.models.card_summary import CardSummary
from identitylib.card_client.models.card_update_request import CardUpdateRequest
from identitylib.card_client.models.card_update_response_type import CardUpdateResponseType
from identitylib.card_client.models.college_instituions_ids_list_response_type import CollegeInstituionsIdsListResponseType
from identitylib.card_client.models.forbidden import Forbidden
from identitylib.card_client.models.internal_server_error import InternalServerError
from identitylib.card_client.models.not_found import NotFound
from identitylib.card_client.models.paginated_available_barcode_list import PaginatedAvailableBarcodeList
from identitylib.card_client.models.paginated_card_identifier_summary_list import PaginatedCardIdentifierSummaryList
from identitylib.card_client.models.paginated_card_logo_list import PaginatedCardLogoList
from identitylib.card_client.models.paginated_card_note_list import PaginatedCardNoteList
from identitylib.card_client.models.paginated_card_request_summary_list import PaginatedCardRequestSummaryList
from identitylib.card_client.models.paginated_card_summary_list import PaginatedCardSummaryList
from identitylib.card_client.models.permissions import Permissions
from identitylib.card_client.models.rfid_configuration import RFIDConfiguration
from identitylib.card_client.models.unauthorized import Unauthorized
