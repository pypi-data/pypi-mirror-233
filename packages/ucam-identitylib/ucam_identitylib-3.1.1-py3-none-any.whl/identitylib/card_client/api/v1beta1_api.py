# coding: utf-8

"""
    University Card API

     ## Introduction  The Card API allows access to information about University Cards.  The API broadly follows the principles of REST and strives to provide an interface that can be easily consumed by downstream systems.  ### Stability  This release of the Card API is a `beta` offering: a service we are moving towards live but which requires wider testing with a broader group of users. We consider the Card API as being at least as stable as the legacy card system which it aims to replace, so we encourage users to make use of the Card API rather than relying on the legacy card system.  ### Versioning  The Card API is versioned using url path prefixes in the format: `/v1beta1/cards`. This follows the pattern established by the [GCP API](https://cloud.google.com/apis/design/versioning). Breaking changes will not be made without a change in API major version, however non-breaking changes will be introduced without changes to the version path prefix. All changes will be documented in the project's [CHANGELOG](https://gitlab.developers.cam.ac.uk/uis/devops/iam/card-database/card-api/-/blob/master/CHANGELOG.md).  The available versions of the API are listed at the API's root.  ### Domain  The Card API has been designed to only expose information about University Cards and the identifiers which link a Card to a person. The API does not expose information about cardholders or the institutions that a cardholder belongs to. This is in order to combat domain crossover and to ensure the Card API does not duplicate information which is held and managed within systems such as Lookup, CamSIS or CHRIS.  It is expected that the Card API should be used alongside APIs such as Lookup which allow personal and institutional membership information to be retrieved. A tool has been written in order to allow efficient querying of the Card API using information contained within, CamSIS or CHRIS. [Usage and installation instructions for this tool can be found here](https://gitlab.developers.cam.ac.uk/uis/devops/iam/card-database/card-client).  ### Data source  The data exposed in the Card API is currently a mirror of data contained within the [Card Database](https://webservices.admin.cam.ac.uk/uc/). With data being synced from the Card Database to the Card API hourly.  In future, card data will be updated and created directly using the Card API so changes will be reflected in the Card API 'live' without this hourly sync.  ## Core entities  ### The `Card` Entity  The `Card` entity is a representation of a physical University Card. The entity contains fields indicating the status of the card and when the card has moved between different statuses. Cards held by individuals (such as students or staff) and temporary cards managed by institutions are both represented by the `Card` entity, with the former having a `cardType` of `MIFARE_PERSONAL` and the latter having a `cardType` of `MIFARE_TEMPORARY`.  Each card should have a set of `CardIdentifiers` which allow the card to be linked to an entity in another system (e.g. a person in Lookup), or record information about identifiers held within the card, such as Mifare ID.  The full `Card` entity contains a `cardNotes` field which holds a set of notes made by administrator users related to the card, as well as an `attributes` field which holds the data that is present on the physical presentation of a card. Operations which list many cards return `CardSummary` entities which omit these fields for brevity.  ### The `CardIdentifier` Entity  The `CardIdentifier` entity holds the `value` and `scheme` of a given identifier. The `value` field of a `CardIdentifier` is a simple ID string - e.g. `wgd23` or `000001`. The `scheme` field of a `CardIdentifier` indicates what system this identifier relates to or was issued by. This allows many identifiers which relate to different systems to be recorded against a single `Card`.  The supported schemes are: * `v1.person.identifiers.cam.ac.uk`: The CRSid of the person who holds this card * `person.v1.student-records.university.identifiers.cam.ac.uk`: The CamSIS identifier (USN) of the person who holds this card * `person.v1.human-resources.university.identifiers.cam.ac.uk`: The CHRIS identifier (staff number) of the person who holds this card * `person.v1.board-of-graduate-studies.university.identifiers.cam.ac.uk`: The Board of Graduate Studies identifier of the person who holds this card * `person.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy card holder ID for the person who holds this card * `mifare-identifier.v1.card.university.identifiers.cam.ac.uk`: The Mifare ID which is embedded in this card (this     identifier uniquely identifies a single card) * `mifare-number.v1.card.university.identifiers.cam.ac.uk`: The Mifare Number which is embedded in this card     (this identifier is a digest of card's legacy cardholder ID and issue number, so is not     guaranteed to be unique) * `card.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy card ID from the card database * `temporary-card.v1.card.university.identifiers.cam.ac.uk`: The temporary card ID from the card database * `photo.v1.photo.university.identifiers.cam.ac.uk`: The ID of the photo printed on this card * `barcode.v1.card.university.identifiers.cam.ac.uk`: The barcode printed on this card * `institution.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy institution ID from the card database (only populated on temporary cards)   ## Using the API  ### Auth  To authenticate against the Card API, an application must be registered within the API Service and granted access to the `University Card` product. Details of how to register an application and grant access to products can be found in the [API Service Getting Started Guide](https://developer.api.apps.cam.ac.uk/start-using-an-api).  #### Principal  Throughout this specification the term `principal` is used to describe the user or service who is making use of the API. When authenticating using the OAuth2 client credentials flow the principal shall be the application registered within the API Gateway. When authenticating using the authorization code flow, e.g. via a Single Page Application, the principal shall be the user who has authenticated and consented to give the application access to the data contained within this API - identified by their CRSid.  This specification references permissions which can be granted to any principal - please contact the API maintainers to grant a principal a specific permission.  ### Content Type  The Card API responds with JSON data. The `Content-Type` request header should be omitted or set to `application/json`. If an invalid `Content-Type` header is sent the API will respond with `415 Unsupported Media Type`.  ### Pagination  For all operations where multiple entities will be returned, the API will return a paginated result. This is to account for too many entities needing to be returned within a single response. A Paginated response has the structure:  ```json {   \"next\": \"https://<gateway_host>/card/v1beta1/cards/?cursor=cD0yMDIxLTAxL   \"previous\": null,   \"results\": [       ... the data for the current page   ] }  ```  The `next` field holds the url of the next page of results, containing a cursor which indicates to the API which page of results to return. If the `next` field is `null` no further results are available. The `previous` field can be used to navigate backwards through pages of results.  The `page_size` query parameter can be used to control the number of results to return. This defaults to 200 but can be set to a maximum of 500, if set to greater than this no error will be returned but only 500 results will be given in the response.  

    The version of the OpenAPI document: v1beta1
    Contact: devops+cardapi@uis.cam.ac.uk
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import re  # noqa: F401
import io
import warnings

from pydantic import validate_arguments, ValidationError
from typing_extensions import Annotated

from datetime import datetime

from pydantic import Field, StrictBool, StrictInt, StrictStr, conlist, constr, validator

from typing import Optional, Union

from identitylib.card_client.models.available_barcode import AvailableBarcode
from identitylib.card_client.models.available_barcode_batch_request import AvailableBarcodeBatchRequest
from identitylib.card_client.models.available_barcode_batch_response_type import AvailableBarcodeBatchResponseType
from identitylib.card_client.models.available_barcode_request import AvailableBarcodeRequest
from identitylib.card_client.models.card import Card
from identitylib.card_client.models.card_bulk_update_request import CardBulkUpdateRequest
from identitylib.card_client.models.card_bulk_update_response_type import CardBulkUpdateResponseType
from identitylib.card_client.models.card_filter_request import CardFilterRequest
from identitylib.card_client.models.card_identifier import CardIdentifier
from identitylib.card_client.models.card_identifier_bulk_update_request import CardIdentifierBulkUpdateRequest
from identitylib.card_client.models.card_identifier_bulk_update_response_type import CardIdentifierBulkUpdateResponseType
from identitylib.card_client.models.card_identifier_destroy_response_type import CardIdentifierDestroyResponseType
from identitylib.card_client.models.card_identifier_update_request import CardIdentifierUpdateRequest
from identitylib.card_client.models.card_identifier_update_response_type import CardIdentifierUpdateResponseType
from identitylib.card_client.models.card_logo import CardLogo
from identitylib.card_client.models.card_note import CardNote
from identitylib.card_client.models.card_note_create_request_type_request import CardNoteCreateRequestTypeRequest
from identitylib.card_client.models.card_note_destroy_response_type import CardNoteDestroyResponseType
from identitylib.card_client.models.card_rfid_config_list_response_type import CardRFIDConfigListResponseType
from identitylib.card_client.models.card_request import CardRequest
from identitylib.card_client.models.card_request_bulk_update_request import CardRequestBulkUpdateRequest
from identitylib.card_client.models.card_request_bulk_update_response_type import CardRequestBulkUpdateResponseType
from identitylib.card_client.models.card_request_create_type_request import CardRequestCreateTypeRequest
from identitylib.card_client.models.card_request_distinct_values import CardRequestDistinctValues
from identitylib.card_client.models.card_request_update_request import CardRequestUpdateRequest
from identitylib.card_client.models.card_request_update_response_type import CardRequestUpdateResponseType
from identitylib.card_client.models.card_update_request import CardUpdateRequest
from identitylib.card_client.models.card_update_response_type import CardUpdateResponseType
from identitylib.card_client.models.college_instituions_ids_list_response_type import CollegeInstituionsIdsListResponseType
from identitylib.card_client.models.metrics_list_response_type import MetricsListResponseType
from identitylib.card_client.models.paginated_available_barcode_list import PaginatedAvailableBarcodeList
from identitylib.card_client.models.paginated_card_identifier_summary_list import PaginatedCardIdentifierSummaryList
from identitylib.card_client.models.paginated_card_logo_list import PaginatedCardLogoList
from identitylib.card_client.models.paginated_card_note_list import PaginatedCardNoteList
from identitylib.card_client.models.paginated_card_request_summary_list import PaginatedCardRequestSummaryList
from identitylib.card_client.models.paginated_card_summary_list import PaginatedCardSummaryList

from identitylib.card_client.api_client import ApiClient
from identitylib.card_client.api_response import ApiResponse
from identitylib.card_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class V1beta1Api(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def v1beta1_available_barcodes_batch_create(self, available_barcode_batch_request : AvailableBarcodeBatchRequest, **kwargs) -> AvailableBarcodeBatchResponseType:  # noqa: E501
        """Create multiple available barcodes  # noqa: E501

         ## Create multiple available barcode in a batch  This method allows the client to create multiple available barcode at once. The response includes the details on which barcodes were created and which already exist.  ### Permissions  Only Principals with the `CARD_REQUEST_UPDATER` permission will be able to create available barcodes.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_available_barcodes_batch_create(available_barcode_batch_request, async_req=True)
        >>> result = thread.get()

        :param available_barcode_batch_request: (required)
        :type available_barcode_batch_request: AvailableBarcodeBatchRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AvailableBarcodeBatchResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_available_barcodes_batch_create_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_available_barcodes_batch_create_with_http_info(available_barcode_batch_request, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_available_barcodes_batch_create_with_http_info(self, available_barcode_batch_request : AvailableBarcodeBatchRequest, **kwargs) -> ApiResponse:  # noqa: E501
        """Create multiple available barcodes  # noqa: E501

         ## Create multiple available barcode in a batch  This method allows the client to create multiple available barcode at once. The response includes the details on which barcodes were created and which already exist.  ### Permissions  Only Principals with the `CARD_REQUEST_UPDATER` permission will be able to create available barcodes.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_available_barcodes_batch_create_with_http_info(available_barcode_batch_request, async_req=True)
        >>> result = thread.get()

        :param available_barcode_batch_request: (required)
        :type available_barcode_batch_request: AvailableBarcodeBatchRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(AvailableBarcodeBatchResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'available_barcode_batch_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_available_barcodes_batch_create" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['available_barcode_batch_request'] is not None:
            _body_params = _params['available_barcode_batch_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "AvailableBarcodeBatchResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/available-barcodes/batch', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_available_barcodes_create(self, available_barcode_request : AvailableBarcodeRequest, **kwargs) -> AvailableBarcode:  # noqa: E501
        """Creates a single available barcode  # noqa: E501

         ## Create an available barcode  This method allows the client to create a single available barcode. Typically, the batch creation endpoint would be used to import a batch of barcodes all at once, rather than multiple calls to this endpoint.  ### Permissions  Only Principals with the `CARD_REQUEST_UPDATER` permission will be able to create available barcodes.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_available_barcodes_create(available_barcode_request, async_req=True)
        >>> result = thread.get()

        :param available_barcode_request: (required)
        :type available_barcode_request: AvailableBarcodeRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AvailableBarcode
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_available_barcodes_create_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_available_barcodes_create_with_http_info(available_barcode_request, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_available_barcodes_create_with_http_info(self, available_barcode_request : AvailableBarcodeRequest, **kwargs) -> ApiResponse:  # noqa: E501
        """Creates a single available barcode  # noqa: E501

         ## Create an available barcode  This method allows the client to create a single available barcode. Typically, the batch creation endpoint would be used to import a batch of barcodes all at once, rather than multiple calls to this endpoint.  ### Permissions  Only Principals with the `CARD_REQUEST_UPDATER` permission will be able to create available barcodes.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_available_barcodes_create_with_http_info(available_barcode_request, async_req=True)
        >>> result = thread.get()

        :param available_barcode_request: (required)
        :type available_barcode_request: AvailableBarcodeRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(AvailableBarcode, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'available_barcode_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_available_barcodes_create" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['available_barcode_request'] is not None:
            _body_params = _params['available_barcode_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '201': "AvailableBarcode",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/available-barcodes', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_available_barcodes_list(self, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, **kwargs) -> PaginatedAvailableBarcodeList:  # noqa: E501
        """List available barcodes  # noqa: E501

         ## List Available Barcodes  Returns a list of barcodes which are available to be used by a new University Card.  ### Permissions  Only principals with the `CARD_DATA_READERS` permission are able to list available barcodes.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_available_barcodes_list(cursor, page_size, async_req=True)
        >>> result = thread.get()

        :param cursor: The pagination cursor value.
        :type cursor: str
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PaginatedAvailableBarcodeList
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_available_barcodes_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_available_barcodes_list_with_http_info(cursor, page_size, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_available_barcodes_list_with_http_info(self, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """List available barcodes  # noqa: E501

         ## List Available Barcodes  Returns a list of barcodes which are available to be used by a new University Card.  ### Permissions  Only principals with the `CARD_DATA_READERS` permission are able to list available barcodes.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_available_barcodes_list_with_http_info(cursor, page_size, async_req=True)
        >>> result = thread.get()

        :param cursor: The pagination cursor value.
        :type cursor: str
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PaginatedAvailableBarcodeList, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'cursor',
            'page_size'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_available_barcodes_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('cursor') is not None:  # noqa: E501
            _query_params.append(('cursor', _params['cursor']))

        if _params.get('page_size') is not None:  # noqa: E501
            _query_params.append(('page_size', _params['page_size']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "PaginatedAvailableBarcodeList",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/available-barcodes', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_available_barcodes_retrieve(self, barcode : Annotated[StrictStr, Field(..., description="A unique value identifying this available barcode.")], **kwargs) -> AvailableBarcode:  # noqa: E501
        """Get available barcode detail  # noqa: E501

        Returns a single Available Barcode by ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_available_barcodes_retrieve(barcode, async_req=True)
        >>> result = thread.get()

        :param barcode: A unique value identifying this available barcode. (required)
        :type barcode: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AvailableBarcode
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_available_barcodes_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_available_barcodes_retrieve_with_http_info(barcode, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_available_barcodes_retrieve_with_http_info(self, barcode : Annotated[StrictStr, Field(..., description="A unique value identifying this available barcode.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Get available barcode detail  # noqa: E501

        Returns a single Available Barcode by ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_available_barcodes_retrieve_with_http_info(barcode, async_req=True)
        >>> result = thread.get()

        :param barcode: A unique value identifying this available barcode. (required)
        :type barcode: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(AvailableBarcode, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'barcode'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_available_barcodes_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['barcode']:
            _path_params['barcode'] = _params['barcode']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "AvailableBarcode",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/available-barcodes/{barcode}', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_identifiers_destroy(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card identifier.")], **kwargs) -> CardIdentifierDestroyResponseType:  # noqa: E501
        """Get card identifier detail  # noqa: E501

         ## Remove card identifier  This method allows a client to remove a card identifier and in the process delete all associated identifiers, cards, card notes and card requests.  This method only operates on the primary identifiers: - `person.v1.legacy-card.university.identifiers.cam.ac.uk` the CRSid identifier of the cardholder - `person.v1.legacy-card.university.identifiers.cam.ac.uk` the legacy identifier of the cardholder  ### Permissions  Principals with the `CARD_ADMIN` permission are able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_identifiers_destroy(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card identifier. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardIdentifierDestroyResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_identifiers_destroy_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_identifiers_destroy_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_identifiers_destroy_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card identifier.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Get card identifier detail  # noqa: E501

         ## Remove card identifier  This method allows a client to remove a card identifier and in the process delete all associated identifiers, cards, card notes and card requests.  This method only operates on the primary identifiers: - `person.v1.legacy-card.university.identifiers.cam.ac.uk` the CRSid identifier of the cardholder - `person.v1.legacy-card.university.identifiers.cam.ac.uk` the legacy identifier of the cardholder  ### Permissions  Principals with the `CARD_ADMIN` permission are able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_identifiers_destroy_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card identifier. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardIdentifierDestroyResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_identifiers_destroy" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardIdentifierDestroyResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-identifiers/{id}', 'DELETE',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_identifiers_list(self, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, deleted_at__gte : Optional[datetime] = None, deleted_at__isnull : Optional[StrictBool] = None, deleted_at__lte : Optional[datetime] = None, identifier : Annotated[Optional[StrictStr], Field(description="Email-formatted identifier")] = None, is_deleted : Optional[StrictBool] = None, is_highest_primary_identifier : Optional[StrictBool] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, retain_until__gte : Optional[datetime] = None, retain_until__isnull : Optional[StrictBool] = None, retain_until__lte : Optional[datetime] = None, scheme : Annotated[Optional[StrictStr], Field(description="Identifier scheme")] = None, **kwargs) -> PaginatedCardIdentifierSummaryList:  # noqa: E501
        """List card identifiers  # noqa: E501

         ## List card identifiers  Returns a list of card identifiers associated with the cards and card requests.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view card identifiers contained within the card system.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_identifiers_list(cursor, deleted_at__gte, deleted_at__isnull, deleted_at__lte, identifier, is_deleted, is_highest_primary_identifier, page_size, retain_until__gte, retain_until__isnull, retain_until__lte, scheme, async_req=True)
        >>> result = thread.get()

        :param cursor: The pagination cursor value.
        :type cursor: str
        :param deleted_at__gte:
        :type deleted_at__gte: datetime
        :param deleted_at__isnull:
        :type deleted_at__isnull: bool
        :param deleted_at__lte:
        :type deleted_at__lte: datetime
        :param identifier: Email-formatted identifier
        :type identifier: str
        :param is_deleted:
        :type is_deleted: bool
        :param is_highest_primary_identifier:
        :type is_highest_primary_identifier: bool
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param retain_until__gte:
        :type retain_until__gte: datetime
        :param retain_until__isnull:
        :type retain_until__isnull: bool
        :param retain_until__lte:
        :type retain_until__lte: datetime
        :param scheme: Identifier scheme
        :type scheme: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PaginatedCardIdentifierSummaryList
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_identifiers_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_identifiers_list_with_http_info(cursor, deleted_at__gte, deleted_at__isnull, deleted_at__lte, identifier, is_deleted, is_highest_primary_identifier, page_size, retain_until__gte, retain_until__isnull, retain_until__lte, scheme, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_identifiers_list_with_http_info(self, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, deleted_at__gte : Optional[datetime] = None, deleted_at__isnull : Optional[StrictBool] = None, deleted_at__lte : Optional[datetime] = None, identifier : Annotated[Optional[StrictStr], Field(description="Email-formatted identifier")] = None, is_deleted : Optional[StrictBool] = None, is_highest_primary_identifier : Optional[StrictBool] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, retain_until__gte : Optional[datetime] = None, retain_until__isnull : Optional[StrictBool] = None, retain_until__lte : Optional[datetime] = None, scheme : Annotated[Optional[StrictStr], Field(description="Identifier scheme")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """List card identifiers  # noqa: E501

         ## List card identifiers  Returns a list of card identifiers associated with the cards and card requests.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view card identifiers contained within the card system.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_identifiers_list_with_http_info(cursor, deleted_at__gte, deleted_at__isnull, deleted_at__lte, identifier, is_deleted, is_highest_primary_identifier, page_size, retain_until__gte, retain_until__isnull, retain_until__lte, scheme, async_req=True)
        >>> result = thread.get()

        :param cursor: The pagination cursor value.
        :type cursor: str
        :param deleted_at__gte:
        :type deleted_at__gte: datetime
        :param deleted_at__isnull:
        :type deleted_at__isnull: bool
        :param deleted_at__lte:
        :type deleted_at__lte: datetime
        :param identifier: Email-formatted identifier
        :type identifier: str
        :param is_deleted:
        :type is_deleted: bool
        :param is_highest_primary_identifier:
        :type is_highest_primary_identifier: bool
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param retain_until__gte:
        :type retain_until__gte: datetime
        :param retain_until__isnull:
        :type retain_until__isnull: bool
        :param retain_until__lte:
        :type retain_until__lte: datetime
        :param scheme: Identifier scheme
        :type scheme: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PaginatedCardIdentifierSummaryList, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'cursor',
            'deleted_at__gte',
            'deleted_at__isnull',
            'deleted_at__lte',
            'identifier',
            'is_deleted',
            'is_highest_primary_identifier',
            'page_size',
            'retain_until__gte',
            'retain_until__isnull',
            'retain_until__lte',
            'scheme'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_identifiers_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('cursor') is not None:  # noqa: E501
            _query_params.append(('cursor', _params['cursor']))

        if _params.get('deleted_at__gte') is not None:  # noqa: E501
            if isinstance(_params['deleted_at__gte'], datetime):
                _query_params.append(('deleted_at__gte', _params['deleted_at__gte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('deleted_at__gte', _params['deleted_at__gte']))

        if _params.get('deleted_at__isnull') is not None:  # noqa: E501
            _query_params.append(('deleted_at__isnull', _params['deleted_at__isnull']))

        if _params.get('deleted_at__lte') is not None:  # noqa: E501
            if isinstance(_params['deleted_at__lte'], datetime):
                _query_params.append(('deleted_at__lte', _params['deleted_at__lte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('deleted_at__lte', _params['deleted_at__lte']))

        if _params.get('identifier') is not None:  # noqa: E501
            _query_params.append(('identifier', _params['identifier']))

        if _params.get('is_deleted') is not None:  # noqa: E501
            _query_params.append(('is_deleted', _params['is_deleted']))

        if _params.get('is_highest_primary_identifier') is not None:  # noqa: E501
            _query_params.append(('is_highest_primary_identifier', _params['is_highest_primary_identifier']))

        if _params.get('page_size') is not None:  # noqa: E501
            _query_params.append(('page_size', _params['page_size']))

        if _params.get('retain_until__gte') is not None:  # noqa: E501
            if isinstance(_params['retain_until__gte'], datetime):
                _query_params.append(('retain_until__gte', _params['retain_until__gte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('retain_until__gte', _params['retain_until__gte']))

        if _params.get('retain_until__isnull') is not None:  # noqa: E501
            _query_params.append(('retain_until__isnull', _params['retain_until__isnull']))

        if _params.get('retain_until__lte') is not None:  # noqa: E501
            if isinstance(_params['retain_until__lte'], datetime):
                _query_params.append(('retain_until__lte', _params['retain_until__lte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('retain_until__lte', _params['retain_until__lte']))

        if _params.get('scheme') is not None:  # noqa: E501
            _query_params.append(('scheme', _params['scheme']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "PaginatedCardIdentifierSummaryList",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-identifiers', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_identifiers_retrieve(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card identifier.")], **kwargs) -> CardIdentifier:  # noqa: E501
        """Get card identifier detail  # noqa: E501

         ## Get card identifier detail  Allows the detail of a single Card Identifier to be retrieved by identifier UUID. The Card Identifier entity returned contains the information as presented in the list operation above plus additional fields.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view the card identifier detail of any card identifier contained within the card system.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_identifiers_retrieve(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card identifier. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardIdentifier
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_identifiers_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_identifiers_retrieve_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_identifiers_retrieve_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card identifier.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Get card identifier detail  # noqa: E501

         ## Get card identifier detail  Allows the detail of a single Card Identifier to be retrieved by identifier UUID. The Card Identifier entity returned contains the information as presented in the list operation above plus additional fields.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view the card identifier detail of any card identifier contained within the card system.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_identifiers_retrieve_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card identifier. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardIdentifier, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_identifiers_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardIdentifier",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-identifiers/{id}', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_identifiers_update(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card identifier.")], card_identifier_update_request : CardIdentifierUpdateRequest, **kwargs) -> CardIdentifierUpdateResponseType:  # noqa: E501
        """Updates the card identifier  # noqa: E501

         ## Update the card identifier  This method allows a client to submit an action in the request body for a given card identifier. The allowed actions are `repair`, `restore`, `soft_delete` and `hard_delete`.  ### Permissions  Principals with the `CARD_ADMIN` permission will be able to affect this endpoint.     # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_identifiers_update(id, card_identifier_update_request, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card identifier. (required)
        :type id: str
        :param card_identifier_update_request: (required)
        :type card_identifier_update_request: CardIdentifierUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardIdentifierUpdateResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_identifiers_update_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_identifiers_update_with_http_info(id, card_identifier_update_request, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_identifiers_update_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card identifier.")], card_identifier_update_request : CardIdentifierUpdateRequest, **kwargs) -> ApiResponse:  # noqa: E501
        """Updates the card identifier  # noqa: E501

         ## Update the card identifier  This method allows a client to submit an action in the request body for a given card identifier. The allowed actions are `repair`, `restore`, `soft_delete` and `hard_delete`.  ### Permissions  Principals with the `CARD_ADMIN` permission will be able to affect this endpoint.     # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_identifiers_update_with_http_info(id, card_identifier_update_request, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card identifier. (required)
        :type id: str
        :param card_identifier_update_request: (required)
        :type card_identifier_update_request: CardIdentifierUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardIdentifierUpdateResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id',
            'card_identifier_update_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_identifiers_update" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['card_identifier_update_request'] is not None:
            _body_params = _params['card_identifier_update_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardIdentifierUpdateResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-identifiers/{id}', 'PUT',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_identifiers_update_update(self, card_identifier_bulk_update_request : CardIdentifierBulkUpdateRequest, **kwargs) -> CardIdentifierBulkUpdateResponseType:  # noqa: E501
        """Update multiple card identifiers  # noqa: E501

         ## Update multiple card identifiers  Allows multiple card identifiers to be updated in one call. For large number of card identifiers, this endpoint will be faster than PUT-ing each update.  Updates are processed in the order they are received. The response includes the detail of the operation, the UUID of the card identifier that was updated, and HTTP status code which would have been returned from separate PUTs. If the status code is 404, the `id` property is omitted.  ### Permissions  Principals with the `CARD_ADMIN` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_identifiers_update_update(card_identifier_bulk_update_request, async_req=True)
        >>> result = thread.get()

        :param card_identifier_bulk_update_request: (required)
        :type card_identifier_bulk_update_request: CardIdentifierBulkUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardIdentifierBulkUpdateResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_identifiers_update_update_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_identifiers_update_update_with_http_info(card_identifier_bulk_update_request, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_identifiers_update_update_with_http_info(self, card_identifier_bulk_update_request : CardIdentifierBulkUpdateRequest, **kwargs) -> ApiResponse:  # noqa: E501
        """Update multiple card identifiers  # noqa: E501

         ## Update multiple card identifiers  Allows multiple card identifiers to be updated in one call. For large number of card identifiers, this endpoint will be faster than PUT-ing each update.  Updates are processed in the order they are received. The response includes the detail of the operation, the UUID of the card identifier that was updated, and HTTP status code which would have been returned from separate PUTs. If the status code is 404, the `id` property is omitted.  ### Permissions  Principals with the `CARD_ADMIN` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_identifiers_update_update_with_http_info(card_identifier_bulk_update_request, async_req=True)
        >>> result = thread.get()

        :param card_identifier_bulk_update_request: (required)
        :type card_identifier_bulk_update_request: CardIdentifierBulkUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardIdentifierBulkUpdateResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'card_identifier_bulk_update_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_identifiers_update_update" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['card_identifier_bulk_update_request'] is not None:
            _body_params = _params['card_identifier_bulk_update_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardIdentifierBulkUpdateResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-identifiers/update', 'PUT',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_logos_content_retrieve(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card logo.")], **kwargs) -> None:  # noqa: E501
        """Get card logo image content  # noqa: E501

         ## Get Card Logo Image Content  Redirects to the image content for a given card logo. Note that this endpoint will redirect to a temporary URL provided by the storage provider. This URL will timeout after a short period of time and therefore should not be persisted.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_logos_content_retrieve(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card logo. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_logos_content_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_logos_content_retrieve_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_logos_content_retrieve_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card logo.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Get card logo image content  # noqa: E501

         ## Get Card Logo Image Content  Redirects to the image content for a given card logo. Note that this endpoint will redirect to a temporary URL provided by the storage provider. This URL will timeout after a short period of time and therefore should not be persisted.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_logos_content_retrieve_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card logo. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        _params = locals()

        _all_params = [
            'id'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_logos_content_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {}

        return self.api_client.call_api(
            '/v1beta1/card-logos/{id}/content', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_logos_list(self, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, **kwargs) -> PaginatedCardLogoList:  # noqa: E501
        """List card logos  # noqa: E501

         ## List Card Logos  Returns a list of card logo objects - representing logos which can be displayed on cards.  Each logo contains a `contentLink` which links to the image content for this logo. The rest of the object represents metadata about a logo.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_logos_list(cursor, page_size, async_req=True)
        >>> result = thread.get()

        :param cursor: The pagination cursor value.
        :type cursor: str
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PaginatedCardLogoList
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_logos_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_logos_list_with_http_info(cursor, page_size, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_logos_list_with_http_info(self, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """List card logos  # noqa: E501

         ## List Card Logos  Returns a list of card logo objects - representing logos which can be displayed on cards.  Each logo contains a `contentLink` which links to the image content for this logo. The rest of the object represents metadata about a logo.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_logos_list_with_http_info(cursor, page_size, async_req=True)
        >>> result = thread.get()

        :param cursor: The pagination cursor value.
        :type cursor: str
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PaginatedCardLogoList, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'cursor',
            'page_size'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_logos_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('cursor') is not None:  # noqa: E501
            _query_params.append(('cursor', _params['cursor']))

        if _params.get('page_size') is not None:  # noqa: E501
            _query_params.append(('page_size', _params['page_size']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "PaginatedCardLogoList",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-logos', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_logos_retrieve(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card logo.")], **kwargs) -> CardLogo:  # noqa: E501
        """Get card logo detail  # noqa: E501

         ## Get Card Logo  Returns a single card logo by UUID - containing metadata about a logo that can be present on a card.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_logos_retrieve(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card logo. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardLogo
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_logos_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_logos_retrieve_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_logos_retrieve_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card logo.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Get card logo detail  # noqa: E501

         ## Get Card Logo  Returns a single card logo by UUID - containing metadata about a logo that can be present on a card.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_logos_retrieve_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card logo. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardLogo, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_logos_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardLogo",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-logos/{id}', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_notes_create(self, card_note_create_request_type_request : CardNoteCreateRequestTypeRequest, **kwargs) -> CardNote:  # noqa: E501
        """Creates a card note  # noqa: E501

         ## Create card note  This method allows the client to create a card note for a given card.  ### Permissions  Principals with the `CARD_NOTE_CREATOR` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_notes_create(card_note_create_request_type_request, async_req=True)
        >>> result = thread.get()

        :param card_note_create_request_type_request: (required)
        :type card_note_create_request_type_request: CardNoteCreateRequestTypeRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardNote
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_notes_create_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_notes_create_with_http_info(card_note_create_request_type_request, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_notes_create_with_http_info(self, card_note_create_request_type_request : CardNoteCreateRequestTypeRequest, **kwargs) -> ApiResponse:  # noqa: E501
        """Creates a card note  # noqa: E501

         ## Create card note  This method allows the client to create a card note for a given card.  ### Permissions  Principals with the `CARD_NOTE_CREATOR` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_notes_create_with_http_info(card_note_create_request_type_request, async_req=True)
        >>> result = thread.get()

        :param card_note_create_request_type_request: (required)
        :type card_note_create_request_type_request: CardNoteCreateRequestTypeRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardNote, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'card_note_create_request_type_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_notes_create" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['card_note_create_request_type_request'] is not None:
            _body_params = _params['card_note_create_request_type_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '201': "CardNote",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-notes', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_notes_destroy(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card note.")], **kwargs) -> CardNoteDestroyResponseType:  # noqa: E501
        """Deletes a card note  # noqa: E501

         ## Delete card note  This method allows the client to delete a given card note.  ### Permissions  Principals with the `CARD_NOTE_CREATOR` permission who created the card note instance will be able to affect this endpoint.  Principals with the `CARD_NOTE_UPDATER` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_notes_destroy(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card note. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardNoteDestroyResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_notes_destroy_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_notes_destroy_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_notes_destroy_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card note.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Deletes a card note  # noqa: E501

         ## Delete card note  This method allows the client to delete a given card note.  ### Permissions  Principals with the `CARD_NOTE_CREATOR` permission who created the card note instance will be able to affect this endpoint.  Principals with the `CARD_NOTE_UPDATER` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_notes_destroy_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card note. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardNoteDestroyResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_notes_destroy" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardNoteDestroyResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-notes/{id}', 'DELETE',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_notes_list(self, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, **kwargs) -> PaginatedCardNoteList:  # noqa: E501
        """v1beta1_card_notes_list  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_notes_list(cursor, page_size, async_req=True)
        >>> result = thread.get()

        :param cursor: The pagination cursor value.
        :type cursor: str
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PaginatedCardNoteList
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_notes_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_notes_list_with_http_info(cursor, page_size, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_notes_list_with_http_info(self, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """v1beta1_card_notes_list  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_notes_list_with_http_info(cursor, page_size, async_req=True)
        >>> result = thread.get()

        :param cursor: The pagination cursor value.
        :type cursor: str
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PaginatedCardNoteList, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'cursor',
            'page_size'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_notes_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('cursor') is not None:  # noqa: E501
            _query_params.append(('cursor', _params['cursor']))

        if _params.get('page_size') is not None:  # noqa: E501
            _query_params.append(('page_size', _params['page_size']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "PaginatedCardNoteList",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-notes', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_notes_retrieve(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card note.")], **kwargs) -> CardNote:  # noqa: E501
        """v1beta1_card_notes_retrieve  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_notes_retrieve(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card note. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardNote
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_notes_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_notes_retrieve_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_notes_retrieve_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card note.")], **kwargs) -> ApiResponse:  # noqa: E501
        """v1beta1_card_notes_retrieve  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_notes_retrieve_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card note. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardNote, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_notes_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardNote",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-notes/{id}', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_requests_back_visualization_retrieve(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card request.")], format : Optional[StrictStr] = None, height : Annotated[Optional[StrictInt], Field(description="The desired height of the visualization (in pixels)")] = None, width : Annotated[Optional[StrictInt], Field(description="The desired width of the visualization (in pixels)")] = None, **kwargs) -> bytearray:  # noqa: E501
        """Returns a representation of the back of this card request  # noqa: E501

         ## Get card back visualization  Returns a visualization of the back of this card in BMP, PNG or SVG format.  Currently a placeholder is used to represent the barcode printed on the back of the card, this will be replaced with a valid barcode as a piece of follow-up work.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_back_visualization_retrieve(id, format, height, width, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card request. (required)
        :type id: str
        :param format:
        :type format: str
        :param height: The desired height of the visualization (in pixels)
        :type height: int
        :param width: The desired width of the visualization (in pixels)
        :type width: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: bytearray
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_requests_back_visualization_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_requests_back_visualization_retrieve_with_http_info(id, format, height, width, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_requests_back_visualization_retrieve_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card request.")], format : Optional[StrictStr] = None, height : Annotated[Optional[StrictInt], Field(description="The desired height of the visualization (in pixels)")] = None, width : Annotated[Optional[StrictInt], Field(description="The desired width of the visualization (in pixels)")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Returns a representation of the back of this card request  # noqa: E501

         ## Get card back visualization  Returns a visualization of the back of this card in BMP, PNG or SVG format.  Currently a placeholder is used to represent the barcode printed on the back of the card, this will be replaced with a valid barcode as a piece of follow-up work.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_back_visualization_retrieve_with_http_info(id, format, height, width, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card request. (required)
        :type id: str
        :param format:
        :type format: str
        :param height: The desired height of the visualization (in pixels)
        :type height: int
        :param width: The desired width of the visualization (in pixels)
        :type width: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(bytearray, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id',
            'format',
            'height',
            'width'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_requests_back_visualization_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        if _params.get('format') is not None:  # noqa: E501
            _query_params.append(('format', _params['format']))

        if _params.get('height') is not None:  # noqa: E501
            _query_params.append(('height', _params['height']))

        if _params.get('width') is not None:  # noqa: E501
            _query_params.append(('width', _params['width']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['image/bmp', 'image/png', 'image/svg+xml'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "bytearray",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-requests/{id}/back-visualization', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_requests_cardholder_statuses_retrieve(self, **kwargs) -> CardRequestDistinctValues:  # noqa: E501
        """Returns all cardholder statuses present on card requests  # noqa: E501

        Returns the distinct cardholder statuses present on card requests.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_cardholder_statuses_retrieve(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardRequestDistinctValues
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_requests_cardholder_statuses_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_requests_cardholder_statuses_retrieve_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_requests_cardholder_statuses_retrieve_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Returns all cardholder statuses present on card requests  # noqa: E501

        Returns the distinct cardholder statuses present on card requests.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_cardholder_statuses_retrieve_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardRequestDistinctValues, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_requests_cardholder_statuses_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardRequestDistinctValues",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-requests/cardholder-statuses', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_requests_create(self, card_request_create_type_request : CardRequestCreateTypeRequest, **kwargs) -> CardRequest:  # noqa: E501
        """Creates a card request  # noqa: E501

         ## Create a card request  This method allows the client to create a card request for a given identifier. The identifier should be provided in the format `<value>@<scheme>`.  Only the `v1.person.identifiers.cam.ac.uk` scheme is supported at present.  ### Permission  Principals with the `CARD_REQUEST_CREATOR` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_create(card_request_create_type_request, async_req=True)
        >>> result = thread.get()

        :param card_request_create_type_request: (required)
        :type card_request_create_type_request: CardRequestCreateTypeRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardRequest
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_requests_create_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_requests_create_with_http_info(card_request_create_type_request, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_requests_create_with_http_info(self, card_request_create_type_request : CardRequestCreateTypeRequest, **kwargs) -> ApiResponse:  # noqa: E501
        """Creates a card request  # noqa: E501

         ## Create a card request  This method allows the client to create a card request for a given identifier. The identifier should be provided in the format `<value>@<scheme>`.  Only the `v1.person.identifiers.cam.ac.uk` scheme is supported at present.  ### Permission  Principals with the `CARD_REQUEST_CREATOR` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_create_with_http_info(card_request_create_type_request, async_req=True)
        >>> result = thread.get()

        :param card_request_create_type_request: (required)
        :type card_request_create_type_request: CardRequestCreateTypeRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardRequest, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'card_request_create_type_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_requests_create" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['card_request_create_type_request'] is not None:
            _body_params = _params['card_request_create_type_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '201': "CardRequest",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-requests', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_requests_destinations_retrieve(self, **kwargs) -> CardRequestDistinctValues:  # noqa: E501
        """Returns the destinations of all card requests  # noqa: E501

        Returns the distinct destinations of all card requests.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_destinations_retrieve(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardRequestDistinctValues
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_requests_destinations_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_requests_destinations_retrieve_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_requests_destinations_retrieve_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Returns the destinations of all card requests  # noqa: E501

        Returns the distinct destinations of all card requests.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_destinations_retrieve_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardRequestDistinctValues, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_requests_destinations_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardRequestDistinctValues",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-requests/destinations', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_requests_front_visualization_retrieve(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card request.")], format : Optional[StrictStr] = None, height : Annotated[Optional[StrictInt], Field(description="The desired height of the visualization (in pixels)")] = None, render_placeholder : Annotated[Optional[StrictBool], Field(description="Whether to render a placeholder image when the photo associated with the card cannot be found")] = None, width : Annotated[Optional[StrictInt], Field(description="The desired width of the visualization (in pixels)")] = None, **kwargs) -> bytearray:  # noqa: E501
        """Returns a representation of the front of this card request  # noqa: E501

         ## Get card front visualization  Returns a visualization of the front of this card in BMP, PNG or SVG format. Makes use of the Photo API to fetch the photo of the cardholder used on this card. In cases where this card makes use of an out-of-date photo of the cardholder imported from the legacy card system, the Photo may not be available, in which case a placeholder is displayed unless the `render_placeholder` query parameter is set to `false`.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_front_visualization_retrieve(id, format, height, render_placeholder, width, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card request. (required)
        :type id: str
        :param format:
        :type format: str
        :param height: The desired height of the visualization (in pixels)
        :type height: int
        :param render_placeholder: Whether to render a placeholder image when the photo associated with the card cannot be found
        :type render_placeholder: bool
        :param width: The desired width of the visualization (in pixels)
        :type width: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: bytearray
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_requests_front_visualization_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_requests_front_visualization_retrieve_with_http_info(id, format, height, render_placeholder, width, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_requests_front_visualization_retrieve_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card request.")], format : Optional[StrictStr] = None, height : Annotated[Optional[StrictInt], Field(description="The desired height of the visualization (in pixels)")] = None, render_placeholder : Annotated[Optional[StrictBool], Field(description="Whether to render a placeholder image when the photo associated with the card cannot be found")] = None, width : Annotated[Optional[StrictInt], Field(description="The desired width of the visualization (in pixels)")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Returns a representation of the front of this card request  # noqa: E501

         ## Get card front visualization  Returns a visualization of the front of this card in BMP, PNG or SVG format. Makes use of the Photo API to fetch the photo of the cardholder used on this card. In cases where this card makes use of an out-of-date photo of the cardholder imported from the legacy card system, the Photo may not be available, in which case a placeholder is displayed unless the `render_placeholder` query parameter is set to `false`.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_front_visualization_retrieve_with_http_info(id, format, height, render_placeholder, width, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card request. (required)
        :type id: str
        :param format:
        :type format: str
        :param height: The desired height of the visualization (in pixels)
        :type height: int
        :param render_placeholder: Whether to render a placeholder image when the photo associated with the card cannot be found
        :type render_placeholder: bool
        :param width: The desired width of the visualization (in pixels)
        :type width: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(bytearray, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id',
            'format',
            'height',
            'render_placeholder',
            'width'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_requests_front_visualization_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        if _params.get('format') is not None:  # noqa: E501
            _query_params.append(('format', _params['format']))

        if _params.get('height') is not None:  # noqa: E501
            _query_params.append(('height', _params['height']))

        if _params.get('render_placeholder') is not None:  # noqa: E501
            _query_params.append(('render_placeholder', _params['render_placeholder']))

        if _params.get('width') is not None:  # noqa: E501
            _query_params.append(('width', _params['width']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['image/bmp', 'image/png', 'image/svg+xml'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "bytearray",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-requests/{id}/front-visualization', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_requests_list(self, card_type : Annotated[Optional[StrictStr], Field(description="Type  * `MIFARE_PERSONAL` - Personal * `MIFARE_TEMPORARY` - Temporary")] = None, cardholder_status : Optional[StrictStr] = None, created_at__gte : Optional[datetime] = None, created_at__lte : Optional[datetime] = None, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, destination : Optional[StrictStr] = None, identifier : Annotated[Optional[StrictStr], Field(description="Email-formatted identifier")] = None, ordering : Annotated[Optional[StrictStr], Field(description="Which field to use when ordering the results.")] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, requestor : Optional[StrictStr] = None, updated_at__gte : Optional[datetime] = None, updated_at__lte : Optional[datetime] = None, workflow_state : Annotated[Optional[conlist(StrictStr)], Field(description="Workflow state  * `PENDING` - Pending * `HOLD` - Hold * `CANCELLED` - Cancelled * `CREATING_TODO` - ToDo * `CREATING_INPROGRESS` - InProgress * `CREATING_INVERIFICATION` - InVerification * `CREATING_DONE` - Done * `PENDING_CRSID_REQUIRED` - PendingCRSidRequired * `PENDING_PHOTO_REQUIRED` - PendingPhotoRequired * `PENDING_DESTINATION_REQUIRED` - PendingDestinationRequired * `PENDING_EXPIRY_DATA_REQUIRED` - PendingExpiryDataRequired")] = None, **kwargs) -> PaginatedCardRequestSummaryList:  # noqa: E501
        """List card requests  # noqa: E501

         ## List Card Requests  Returns a list of card request objects - representing requests for card creation.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view all card requests contained within the card system. Without this permission only card requests owned by the authenticated principal will be returned. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_list(card_type, cardholder_status, created_at__gte, created_at__lte, cursor, destination, identifier, ordering, page_size, requestor, updated_at__gte, updated_at__lte, workflow_state, async_req=True)
        >>> result = thread.get()

        :param card_type: Type  * `MIFARE_PERSONAL` - Personal * `MIFARE_TEMPORARY` - Temporary
        :type card_type: str
        :param cardholder_status:
        :type cardholder_status: str
        :param created_at__gte:
        :type created_at__gte: datetime
        :param created_at__lte:
        :type created_at__lte: datetime
        :param cursor: The pagination cursor value.
        :type cursor: str
        :param destination:
        :type destination: str
        :param identifier: Email-formatted identifier
        :type identifier: str
        :param ordering: Which field to use when ordering the results.
        :type ordering: str
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param requestor:
        :type requestor: str
        :param updated_at__gte:
        :type updated_at__gte: datetime
        :param updated_at__lte:
        :type updated_at__lte: datetime
        :param workflow_state: Workflow state  * `PENDING` - Pending * `HOLD` - Hold * `CANCELLED` - Cancelled * `CREATING_TODO` - ToDo * `CREATING_INPROGRESS` - InProgress * `CREATING_INVERIFICATION` - InVerification * `CREATING_DONE` - Done * `PENDING_CRSID_REQUIRED` - PendingCRSidRequired * `PENDING_PHOTO_REQUIRED` - PendingPhotoRequired * `PENDING_DESTINATION_REQUIRED` - PendingDestinationRequired * `PENDING_EXPIRY_DATA_REQUIRED` - PendingExpiryDataRequired
        :type workflow_state: List[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PaginatedCardRequestSummaryList
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_requests_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_requests_list_with_http_info(card_type, cardholder_status, created_at__gte, created_at__lte, cursor, destination, identifier, ordering, page_size, requestor, updated_at__gte, updated_at__lte, workflow_state, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_requests_list_with_http_info(self, card_type : Annotated[Optional[StrictStr], Field(description="Type  * `MIFARE_PERSONAL` - Personal * `MIFARE_TEMPORARY` - Temporary")] = None, cardholder_status : Optional[StrictStr] = None, created_at__gte : Optional[datetime] = None, created_at__lte : Optional[datetime] = None, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, destination : Optional[StrictStr] = None, identifier : Annotated[Optional[StrictStr], Field(description="Email-formatted identifier")] = None, ordering : Annotated[Optional[StrictStr], Field(description="Which field to use when ordering the results.")] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, requestor : Optional[StrictStr] = None, updated_at__gte : Optional[datetime] = None, updated_at__lte : Optional[datetime] = None, workflow_state : Annotated[Optional[conlist(StrictStr)], Field(description="Workflow state  * `PENDING` - Pending * `HOLD` - Hold * `CANCELLED` - Cancelled * `CREATING_TODO` - ToDo * `CREATING_INPROGRESS` - InProgress * `CREATING_INVERIFICATION` - InVerification * `CREATING_DONE` - Done * `PENDING_CRSID_REQUIRED` - PendingCRSidRequired * `PENDING_PHOTO_REQUIRED` - PendingPhotoRequired * `PENDING_DESTINATION_REQUIRED` - PendingDestinationRequired * `PENDING_EXPIRY_DATA_REQUIRED` - PendingExpiryDataRequired")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """List card requests  # noqa: E501

         ## List Card Requests  Returns a list of card request objects - representing requests for card creation.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view all card requests contained within the card system. Without this permission only card requests owned by the authenticated principal will be returned. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_list_with_http_info(card_type, cardholder_status, created_at__gte, created_at__lte, cursor, destination, identifier, ordering, page_size, requestor, updated_at__gte, updated_at__lte, workflow_state, async_req=True)
        >>> result = thread.get()

        :param card_type: Type  * `MIFARE_PERSONAL` - Personal * `MIFARE_TEMPORARY` - Temporary
        :type card_type: str
        :param cardholder_status:
        :type cardholder_status: str
        :param created_at__gte:
        :type created_at__gte: datetime
        :param created_at__lte:
        :type created_at__lte: datetime
        :param cursor: The pagination cursor value.
        :type cursor: str
        :param destination:
        :type destination: str
        :param identifier: Email-formatted identifier
        :type identifier: str
        :param ordering: Which field to use when ordering the results.
        :type ordering: str
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param requestor:
        :type requestor: str
        :param updated_at__gte:
        :type updated_at__gte: datetime
        :param updated_at__lte:
        :type updated_at__lte: datetime
        :param workflow_state: Workflow state  * `PENDING` - Pending * `HOLD` - Hold * `CANCELLED` - Cancelled * `CREATING_TODO` - ToDo * `CREATING_INPROGRESS` - InProgress * `CREATING_INVERIFICATION` - InVerification * `CREATING_DONE` - Done * `PENDING_CRSID_REQUIRED` - PendingCRSidRequired * `PENDING_PHOTO_REQUIRED` - PendingPhotoRequired * `PENDING_DESTINATION_REQUIRED` - PendingDestinationRequired * `PENDING_EXPIRY_DATA_REQUIRED` - PendingExpiryDataRequired
        :type workflow_state: List[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PaginatedCardRequestSummaryList, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'card_type',
            'cardholder_status',
            'created_at__gte',
            'created_at__lte',
            'cursor',
            'destination',
            'identifier',
            'ordering',
            'page_size',
            'requestor',
            'updated_at__gte',
            'updated_at__lte',
            'workflow_state'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_requests_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('card_type') is not None:  # noqa: E501
            _query_params.append(('card_type', _params['card_type']))

        if _params.get('cardholder_status') is not None:  # noqa: E501
            _query_params.append(('cardholder_status', _params['cardholder_status']))

        if _params.get('created_at__gte') is not None:  # noqa: E501
            if isinstance(_params['created_at__gte'], datetime):
                _query_params.append(('created_at__gte', _params['created_at__gte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('created_at__gte', _params['created_at__gte']))

        if _params.get('created_at__lte') is not None:  # noqa: E501
            if isinstance(_params['created_at__lte'], datetime):
                _query_params.append(('created_at__lte', _params['created_at__lte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('created_at__lte', _params['created_at__lte']))

        if _params.get('cursor') is not None:  # noqa: E501
            _query_params.append(('cursor', _params['cursor']))

        if _params.get('destination') is not None:  # noqa: E501
            _query_params.append(('destination', _params['destination']))

        if _params.get('identifier') is not None:  # noqa: E501
            _query_params.append(('identifier', _params['identifier']))

        if _params.get('ordering') is not None:  # noqa: E501
            _query_params.append(('ordering', _params['ordering']))

        if _params.get('page_size') is not None:  # noqa: E501
            _query_params.append(('page_size', _params['page_size']))

        if _params.get('requestor') is not None:  # noqa: E501
            _query_params.append(('requestor', _params['requestor']))

        if _params.get('updated_at__gte') is not None:  # noqa: E501
            if isinstance(_params['updated_at__gte'], datetime):
                _query_params.append(('updated_at__gte', _params['updated_at__gte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('updated_at__gte', _params['updated_at__gte']))

        if _params.get('updated_at__lte') is not None:  # noqa: E501
            if isinstance(_params['updated_at__lte'], datetime):
                _query_params.append(('updated_at__lte', _params['updated_at__lte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('updated_at__lte', _params['updated_at__lte']))

        if _params.get('workflow_state') is not None:  # noqa: E501
            _query_params.append(('workflow_state', _params['workflow_state']))
            _collection_formats['workflow_state'] = 'multi'

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "PaginatedCardRequestSummaryList",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-requests', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_requests_requestors_retrieve(self, **kwargs) -> CardRequestDistinctValues:  # noqa: E501
        """Returns the list of people or services who have made a card request  # noqa: E501

        Returns the distinct people or services who have made a card request.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_requestors_retrieve(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardRequestDistinctValues
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_requests_requestors_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_requests_requestors_retrieve_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_requests_requestors_retrieve_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Returns the list of people or services who have made a card request  # noqa: E501

        Returns the distinct people or services who have made a card request.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_requestors_retrieve_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardRequestDistinctValues, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_requests_requestors_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardRequestDistinctValues",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-requests/requestors', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_requests_retrieve(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card request.")], **kwargs) -> CardRequest:  # noqa: E501
        """Get card request detail  # noqa: E501

         ## Get Card Request  Returns a single card request by UUID - containing metadata about a request for card creation.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view all card requests contained within the card system. Without this permission only card requests owned by the authenticated principal are visible. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_retrieve(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card request. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardRequest
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_requests_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_requests_retrieve_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_requests_retrieve_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card request.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Get card request detail  # noqa: E501

         ## Get Card Request  Returns a single card request by UUID - containing metadata about a request for card creation.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view all card requests contained within the card system. Without this permission only card requests owned by the authenticated principal are visible. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_retrieve_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card request. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardRequest, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_requests_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardRequest",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-requests/{id}', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_requests_update(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card request.")], card_request_update_request : CardRequestUpdateRequest, **kwargs) -> CardRequestUpdateResponseType:  # noqa: E501
        """Updates the card request  # noqa: E501

         ## Update the card request  This method allows a client to submit an action in the request body and optional identifier for a given card request. The available actions are `update`, `set_hold`, `release_hold`, `add`, `start`, `refresh`, `abandon`, `make`, `requeue`, `complete` and `cancel`.  For the `set_hold` action, the client can optionally append a `hold_reason` field describing the reason for holding the card request.  For the `cancel` action, the client can optionally append a `cancel_reason` field describing the reason for cancelling the card request.  For the `update` action, the client can optionally append `fields` and/or `identifiers` to be updated. An `update` action without `fields` or `identifiers` refreshes the card request by updating the card request data from the data sources.  For the `make` action, the client can also append identifiers which associates the physically created cards to the card record - for example the card UID which is  pre-encoded into the card by the manufacturer.   The `complete` action returns the UUID of the created `card` entity.  ### Permissions  Principals with the `CARD_REQUEST_UPDATER` permission will be able to affect this endpoint.  Principals with the `CARD_REQUEST_CREATOR` permission are able to affect the `update`, `set_hold`, `release_hold` and `cancel` actions for card requests created by the principal.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_update(id, card_request_update_request, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card request. (required)
        :type id: str
        :param card_request_update_request: (required)
        :type card_request_update_request: CardRequestUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardRequestUpdateResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_requests_update_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_requests_update_with_http_info(id, card_request_update_request, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_requests_update_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card request.")], card_request_update_request : CardRequestUpdateRequest, **kwargs) -> ApiResponse:  # noqa: E501
        """Updates the card request  # noqa: E501

         ## Update the card request  This method allows a client to submit an action in the request body and optional identifier for a given card request. The available actions are `update`, `set_hold`, `release_hold`, `add`, `start`, `refresh`, `abandon`, `make`, `requeue`, `complete` and `cancel`.  For the `set_hold` action, the client can optionally append a `hold_reason` field describing the reason for holding the card request.  For the `cancel` action, the client can optionally append a `cancel_reason` field describing the reason for cancelling the card request.  For the `update` action, the client can optionally append `fields` and/or `identifiers` to be updated. An `update` action without `fields` or `identifiers` refreshes the card request by updating the card request data from the data sources.  For the `make` action, the client can also append identifiers which associates the physically created cards to the card record - for example the card UID which is  pre-encoded into the card by the manufacturer.   The `complete` action returns the UUID of the created `card` entity.  ### Permissions  Principals with the `CARD_REQUEST_UPDATER` permission will be able to affect this endpoint.  Principals with the `CARD_REQUEST_CREATOR` permission are able to affect the `update`, `set_hold`, `release_hold` and `cancel` actions for card requests created by the principal.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_update_with_http_info(id, card_request_update_request, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card request. (required)
        :type id: str
        :param card_request_update_request: (required)
        :type card_request_update_request: CardRequestUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardRequestUpdateResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id',
            'card_request_update_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_requests_update" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['card_request_update_request'] is not None:
            _body_params = _params['card_request_update_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardRequestUpdateResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-requests/{id}', 'PUT',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_requests_update_update(self, card_request_bulk_update_request : CardRequestBulkUpdateRequest, **kwargs) -> CardRequestBulkUpdateResponseType:  # noqa: E501
        """Update multiple card requests  # noqa: E501

         ## Update multiple card requests.  Allows multiple card requests to be updated in one call. For large number of card requests, this endpoint will be faster than PUT-ing each update.  Updates are processed in the order they are received. The response includes the detail of the operation, the UUID of the card that was updated, and HTTP status code which would have been returned from separate PUTs. If the status code is 404, the `id` property is omitted.  ### Permissions  Principals with the `CARD_REQUEST_UPDATER` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_update_update(card_request_bulk_update_request, async_req=True)
        >>> result = thread.get()

        :param card_request_bulk_update_request: (required)
        :type card_request_bulk_update_request: CardRequestBulkUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardRequestBulkUpdateResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_requests_update_update_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_requests_update_update_with_http_info(card_request_bulk_update_request, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_requests_update_update_with_http_info(self, card_request_bulk_update_request : CardRequestBulkUpdateRequest, **kwargs) -> ApiResponse:  # noqa: E501
        """Update multiple card requests  # noqa: E501

         ## Update multiple card requests.  Allows multiple card requests to be updated in one call. For large number of card requests, this endpoint will be faster than PUT-ing each update.  Updates are processed in the order they are received. The response includes the detail of the operation, the UUID of the card that was updated, and HTTP status code which would have been returned from separate PUTs. If the status code is 404, the `id` property is omitted.  ### Permissions  Principals with the `CARD_REQUEST_UPDATER` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_update_update_with_http_info(card_request_bulk_update_request, async_req=True)
        >>> result = thread.get()

        :param card_request_bulk_update_request: (required)
        :type card_request_bulk_update_request: CardRequestBulkUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardRequestBulkUpdateResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'card_request_bulk_update_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_requests_update_update" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['card_request_bulk_update_request'] is not None:
            _body_params = _params['card_request_bulk_update_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardRequestBulkUpdateResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-requests/update', 'PUT',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_card_rfid_data_config_list(self, **kwargs) -> CardRFIDConfigListResponseType:  # noqa: E501
        """Returns the card RFID data configuration  # noqa: E501

        Returns the card RFID data configuration  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_rfid_data_config_list(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardRFIDConfigListResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_card_rfid_data_config_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_card_rfid_data_config_list_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_card_rfid_data_config_list_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Returns the card RFID data configuration  # noqa: E501

        Returns the card RFID data configuration  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_rfid_data_config_list_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardRFIDConfigListResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_card_rfid_data_config_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardRFIDConfigListResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/card-rfid-data-config', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_cards_back_visualization_retrieve(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card.")], format : Optional[StrictStr] = None, height : Annotated[Optional[StrictInt], Field(description="The desired height of the visualization (in pixels)")] = None, width : Annotated[Optional[StrictInt], Field(description="The desired width of the visualization (in pixels)")] = None, **kwargs) -> bytearray:  # noqa: E501
        """Returns a representation of the back of this card  # noqa: E501

         ## Get card back visualization  Returns a visualization of the back of this card in BMP, PNG or SVG format.  Currently a placeholder is used to represent the barcode printed on the back of the card, this will be replaced with a valid barcode as a piece of follow-up work.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_back_visualization_retrieve(id, format, height, width, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card. (required)
        :type id: str
        :param format:
        :type format: str
        :param height: The desired height of the visualization (in pixels)
        :type height: int
        :param width: The desired width of the visualization (in pixels)
        :type width: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: bytearray
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_cards_back_visualization_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_cards_back_visualization_retrieve_with_http_info(id, format, height, width, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_cards_back_visualization_retrieve_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card.")], format : Optional[StrictStr] = None, height : Annotated[Optional[StrictInt], Field(description="The desired height of the visualization (in pixels)")] = None, width : Annotated[Optional[StrictInt], Field(description="The desired width of the visualization (in pixels)")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Returns a representation of the back of this card  # noqa: E501

         ## Get card back visualization  Returns a visualization of the back of this card in BMP, PNG or SVG format.  Currently a placeholder is used to represent the barcode printed on the back of the card, this will be replaced with a valid barcode as a piece of follow-up work.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_back_visualization_retrieve_with_http_info(id, format, height, width, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card. (required)
        :type id: str
        :param format:
        :type format: str
        :param height: The desired height of the visualization (in pixels)
        :type height: int
        :param width: The desired width of the visualization (in pixels)
        :type width: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(bytearray, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id',
            'format',
            'height',
            'width'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_cards_back_visualization_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        if _params.get('format') is not None:  # noqa: E501
            _query_params.append(('format', _params['format']))

        if _params.get('height') is not None:  # noqa: E501
            _query_params.append(('height', _params['height']))

        if _params.get('width') is not None:  # noqa: E501
            _query_params.append(('width', _params['width']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['image/bmp', 'image/png', 'image/svg+xml'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "bytearray",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/cards/{id}/back-visualization', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_cards_filter_create(self, card_filter_request : CardFilterRequest, institution : Annotated[Optional[constr(strict=True, min_length=1)], Field(description="Filter by the institutions that cardholders belong to")] = None, status : Annotated[Optional[constr(strict=True, min_length=1)], Field(description="Status to filter by, if omitted cards of all statuses are returned  * `ISSUED` - Issued * `REVOKED` - Revoked * `RETURNED` - Returned * `EXPIRED` - Expired * `UNACTIVATED` - Unactivated")] = None, updated_at__gte : Annotated[Optional[datetime], Field(description="Filter updatedAt by IsoDateTime greater than")] = None, updated_at__lte : Annotated[Optional[datetime], Field(description="Filter updatedAt by IsoDateTime less than")] = None, **kwargs) -> PaginatedCardSummaryList:  # noqa: E501
        """Filter cards by identifiers  # noqa: E501

         ## Filter cards by Identifiers  Returns the cards related to the given batch of identifiers. This is useful for finding a set of cards based on a batch of entities from another system. For example, finding cards for members of a group in Lookup can be achieved by first fetching all members of the group and their crsids from Lookup and then using this endpoint to find all cards based on those crsids.  Identifiers should be provided in the format `<value>@<scheme>`, but if the scheme is not provided the scheme shall be assumed to be `person.crs.identifiers.uis.cam.ac.uk`. See above for the list of supported schemes.  __Note__: the number of identifiers which can be sent in each request is limited to 50, if more that 50 unique identifiers are sent in a single request a `400` error response will be returned. If cards need to be filtered by more than 50 identifiers, multiple request should be made with the identifiers split into batches of 50.  A `status` to filter cards can optionally be included in the body or as a query param. If not included cards of all statuses are returned.  Although this endpoint uses the `POST` method, no data is created. `POST` is used to allow the set of identifiers to be provided in the body and therefore avoid problems caused by query-string length limits.  This endpoint returns a paginated response object (as described above), but will not actually perform pagination due to the overall limit on the number of identifiers that can be queried by. Therefore the `next` and `previous` fields will always be `null` and the `page_size` and `cursor` query parameters will not be honoured.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to filter all cards contained within the card system. Without this permission only cards owned by the authenticated principal will be returned. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_filter_create(card_filter_request, institution, status, updated_at__gte, updated_at__lte, async_req=True)
        >>> result = thread.get()

        :param card_filter_request: (required)
        :type card_filter_request: CardFilterRequest
        :param institution: Filter by the institutions that cardholders belong to
        :type institution: str
        :param status: Status to filter by, if omitted cards of all statuses are returned  * `ISSUED` - Issued * `REVOKED` - Revoked * `RETURNED` - Returned * `EXPIRED` - Expired * `UNACTIVATED` - Unactivated
        :type status: str
        :param updated_at__gte: Filter updatedAt by IsoDateTime greater than
        :type updated_at__gte: datetime
        :param updated_at__lte: Filter updatedAt by IsoDateTime less than
        :type updated_at__lte: datetime
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PaginatedCardSummaryList
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_cards_filter_create_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_cards_filter_create_with_http_info(card_filter_request, institution, status, updated_at__gte, updated_at__lte, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_cards_filter_create_with_http_info(self, card_filter_request : CardFilterRequest, institution : Annotated[Optional[constr(strict=True, min_length=1)], Field(description="Filter by the institutions that cardholders belong to")] = None, status : Annotated[Optional[constr(strict=True, min_length=1)], Field(description="Status to filter by, if omitted cards of all statuses are returned  * `ISSUED` - Issued * `REVOKED` - Revoked * `RETURNED` - Returned * `EXPIRED` - Expired * `UNACTIVATED` - Unactivated")] = None, updated_at__gte : Annotated[Optional[datetime], Field(description="Filter updatedAt by IsoDateTime greater than")] = None, updated_at__lte : Annotated[Optional[datetime], Field(description="Filter updatedAt by IsoDateTime less than")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Filter cards by identifiers  # noqa: E501

         ## Filter cards by Identifiers  Returns the cards related to the given batch of identifiers. This is useful for finding a set of cards based on a batch of entities from another system. For example, finding cards for members of a group in Lookup can be achieved by first fetching all members of the group and their crsids from Lookup and then using this endpoint to find all cards based on those crsids.  Identifiers should be provided in the format `<value>@<scheme>`, but if the scheme is not provided the scheme shall be assumed to be `person.crs.identifiers.uis.cam.ac.uk`. See above for the list of supported schemes.  __Note__: the number of identifiers which can be sent in each request is limited to 50, if more that 50 unique identifiers are sent in a single request a `400` error response will be returned. If cards need to be filtered by more than 50 identifiers, multiple request should be made with the identifiers split into batches of 50.  A `status` to filter cards can optionally be included in the body or as a query param. If not included cards of all statuses are returned.  Although this endpoint uses the `POST` method, no data is created. `POST` is used to allow the set of identifiers to be provided in the body and therefore avoid problems caused by query-string length limits.  This endpoint returns a paginated response object (as described above), but will not actually perform pagination due to the overall limit on the number of identifiers that can be queried by. Therefore the `next` and `previous` fields will always be `null` and the `page_size` and `cursor` query parameters will not be honoured.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to filter all cards contained within the card system. Without this permission only cards owned by the authenticated principal will be returned. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_filter_create_with_http_info(card_filter_request, institution, status, updated_at__gte, updated_at__lte, async_req=True)
        >>> result = thread.get()

        :param card_filter_request: (required)
        :type card_filter_request: CardFilterRequest
        :param institution: Filter by the institutions that cardholders belong to
        :type institution: str
        :param status: Status to filter by, if omitted cards of all statuses are returned  * `ISSUED` - Issued * `REVOKED` - Revoked * `RETURNED` - Returned * `EXPIRED` - Expired * `UNACTIVATED` - Unactivated
        :type status: str
        :param updated_at__gte: Filter updatedAt by IsoDateTime greater than
        :type updated_at__gte: datetime
        :param updated_at__lte: Filter updatedAt by IsoDateTime less than
        :type updated_at__lte: datetime
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PaginatedCardSummaryList, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'card_filter_request',
            'institution',
            'status',
            'updated_at__gte',
            'updated_at__lte'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_cards_filter_create" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('institution') is not None:  # noqa: E501
            _query_params.append(('institution', _params['institution']))

        if _params.get('status') is not None:  # noqa: E501
            _query_params.append(('status', _params['status']))

        if _params.get('updated_at__gte') is not None:  # noqa: E501
            if isinstance(_params['updated_at__gte'], datetime):
                _query_params.append(('updated_at__gte', _params['updated_at__gte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('updated_at__gte', _params['updated_at__gte']))

        if _params.get('updated_at__lte') is not None:  # noqa: E501
            if isinstance(_params['updated_at__lte'], datetime):
                _query_params.append(('updated_at__lte', _params['updated_at__lte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('updated_at__lte', _params['updated_at__lte']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['card_filter_request'] is not None:
            _body_params = _params['card_filter_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "PaginatedCardSummaryList",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/cards/filter', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_cards_front_visualization_retrieve(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card.")], format : Optional[StrictStr] = None, height : Annotated[Optional[StrictInt], Field(description="The desired height of the visualization (in pixels)")] = None, width : Annotated[Optional[StrictInt], Field(description="The desired width of the visualization (in pixels)")] = None, **kwargs) -> bytearray:  # noqa: E501
        """Returns a representation of the front of this card  # noqa: E501

         ## Get card front visualization  Returns a visualization of the front of this card in BMP, PNG or SVG format. Makes use of the Photo API to fetch the photo of the cardholder used on this card. In cases where this card makes use of an out-of-date photo of the cardholder imported from the legacy card system, the Photo may not be available, in which case a placeholder is displayed.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_front_visualization_retrieve(id, format, height, width, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card. (required)
        :type id: str
        :param format:
        :type format: str
        :param height: The desired height of the visualization (in pixels)
        :type height: int
        :param width: The desired width of the visualization (in pixels)
        :type width: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: bytearray
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_cards_front_visualization_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_cards_front_visualization_retrieve_with_http_info(id, format, height, width, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_cards_front_visualization_retrieve_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card.")], format : Optional[StrictStr] = None, height : Annotated[Optional[StrictInt], Field(description="The desired height of the visualization (in pixels)")] = None, width : Annotated[Optional[StrictInt], Field(description="The desired width of the visualization (in pixels)")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Returns a representation of the front of this card  # noqa: E501

         ## Get card front visualization  Returns a visualization of the front of this card in BMP, PNG or SVG format. Makes use of the Photo API to fetch the photo of the cardholder used on this card. In cases where this card makes use of an out-of-date photo of the cardholder imported from the legacy card system, the Photo may not be available, in which case a placeholder is displayed.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_front_visualization_retrieve_with_http_info(id, format, height, width, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card. (required)
        :type id: str
        :param format:
        :type format: str
        :param height: The desired height of the visualization (in pixels)
        :type height: int
        :param width: The desired width of the visualization (in pixels)
        :type width: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(bytearray, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id',
            'format',
            'height',
            'width'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_cards_front_visualization_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        if _params.get('format') is not None:  # noqa: E501
            _query_params.append(('format', _params['format']))

        if _params.get('height') is not None:  # noqa: E501
            _query_params.append(('height', _params['height']))

        if _params.get('width') is not None:  # noqa: E501
            _query_params.append(('width', _params['width']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['image/bmp', 'image/png', 'image/svg+xml'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "bytearray",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/cards/{id}/front-visualization', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_cards_list(self, card_type : Annotated[Optional[StrictStr], Field(description="Filter by the type of card  * `MIFARE_PERSONAL` - Personal * `MIFARE_TEMPORARY` - Temporary")] = None, created_at__gte : Optional[datetime] = None, created_at__lte : Optional[datetime] = None, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, expires_at__gte : Optional[datetime] = None, expires_at__isnull : Optional[StrictBool] = None, expires_at__lte : Optional[datetime] = None, identifier : Annotated[Optional[StrictStr], Field(description="Filter cards by an identifier in the format {value}@{scheme}")] = None, institution : Annotated[Optional[StrictStr], Field(description="Institution id")] = None, issued_at__gte : Optional[datetime] = None, issued_at__isnull : Optional[StrictBool] = None, issued_at__lte : Optional[datetime] = None, originating_card_request : Annotated[Optional[StrictStr], Field(description="Originating CardRequest UUID")] = None, originating_card_request__isnull : Optional[StrictBool] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, search : Annotated[Optional[StrictStr], Field(description="A search term.")] = None, status : Annotated[Optional[StrictStr], Field(description="Filter cards by their current status  * `ISSUED` - Issued * `REVOKED` - Revoked * `RETURNED` - Returned * `EXPIRED` - Expired * `UNACTIVATED` - Unactivated")] = None, updated_at__gte : Optional[datetime] = None, updated_at__lte : Optional[datetime] = None, **kwargs) -> PaginatedCardSummaryList:  # noqa: E501
        """List cards  # noqa: E501

        ## List Cards  Allows current and historic University Cards to be listed.  By default (without any URL parameters included) this method will return all cards, including temporary cards and cards that have expired / been revoked.  Query parameters can be used to refine the cards that are returned. For example, to fetch cards which have been issued and are therefore currently active we can add the query parameter: `status=ISSUED`.  If we want to find Cards with a specific identifier we can specify that identifier as a query parameter as well. For example, adding the following to the query string will return all revoked cards with the mifare ID '123':  `status=REVOKED&identifier=123@<mifare id scheme>`. Identifiers should be provided in the format `<value>@<scheme>`, but if the scheme is not provided the scheme shall be assumed to be the CRSid. See above for the list of supported schemes.  In the case of querying by mifare identifier, any leading zeros within the identifier value included in the query will be ignored - so querying with `identifier=0000000123@<mifare id scheme>` and `identifier=123@<mifare id scheme>` will return the same result.  Alternately the `search` query parameter can be used to search all cards by a single identifier value regardless of the scheme of that identifier.  If cards for multiple identifiers need to be fetched, use the `/cards/filter/` endpoint documented below.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view all cards contained within the card system. Without this permission only cards owned by the authenticated principal will be returned. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_list(card_type, created_at__gte, created_at__lte, cursor, expires_at__gte, expires_at__isnull, expires_at__lte, identifier, institution, issued_at__gte, issued_at__isnull, issued_at__lte, originating_card_request, originating_card_request__isnull, page_size, search, status, updated_at__gte, updated_at__lte, async_req=True)
        >>> result = thread.get()

        :param card_type: Filter by the type of card  * `MIFARE_PERSONAL` - Personal * `MIFARE_TEMPORARY` - Temporary
        :type card_type: str
        :param created_at__gte:
        :type created_at__gte: datetime
        :param created_at__lte:
        :type created_at__lte: datetime
        :param cursor: The pagination cursor value.
        :type cursor: str
        :param expires_at__gte:
        :type expires_at__gte: datetime
        :param expires_at__isnull:
        :type expires_at__isnull: bool
        :param expires_at__lte:
        :type expires_at__lte: datetime
        :param identifier: Filter cards by an identifier in the format {value}@{scheme}
        :type identifier: str
        :param institution: Institution id
        :type institution: str
        :param issued_at__gte:
        :type issued_at__gte: datetime
        :param issued_at__isnull:
        :type issued_at__isnull: bool
        :param issued_at__lte:
        :type issued_at__lte: datetime
        :param originating_card_request: Originating CardRequest UUID
        :type originating_card_request: str
        :param originating_card_request__isnull:
        :type originating_card_request__isnull: bool
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param search: A search term.
        :type search: str
        :param status: Filter cards by their current status  * `ISSUED` - Issued * `REVOKED` - Revoked * `RETURNED` - Returned * `EXPIRED` - Expired * `UNACTIVATED` - Unactivated
        :type status: str
        :param updated_at__gte:
        :type updated_at__gte: datetime
        :param updated_at__lte:
        :type updated_at__lte: datetime
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PaginatedCardSummaryList
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_cards_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_cards_list_with_http_info(card_type, created_at__gte, created_at__lte, cursor, expires_at__gte, expires_at__isnull, expires_at__lte, identifier, institution, issued_at__gte, issued_at__isnull, issued_at__lte, originating_card_request, originating_card_request__isnull, page_size, search, status, updated_at__gte, updated_at__lte, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_cards_list_with_http_info(self, card_type : Annotated[Optional[StrictStr], Field(description="Filter by the type of card  * `MIFARE_PERSONAL` - Personal * `MIFARE_TEMPORARY` - Temporary")] = None, created_at__gte : Optional[datetime] = None, created_at__lte : Optional[datetime] = None, cursor : Annotated[Optional[StrictStr], Field(description="The pagination cursor value.")] = None, expires_at__gte : Optional[datetime] = None, expires_at__isnull : Optional[StrictBool] = None, expires_at__lte : Optional[datetime] = None, identifier : Annotated[Optional[StrictStr], Field(description="Filter cards by an identifier in the format {value}@{scheme}")] = None, institution : Annotated[Optional[StrictStr], Field(description="Institution id")] = None, issued_at__gte : Optional[datetime] = None, issued_at__isnull : Optional[StrictBool] = None, issued_at__lte : Optional[datetime] = None, originating_card_request : Annotated[Optional[StrictStr], Field(description="Originating CardRequest UUID")] = None, originating_card_request__isnull : Optional[StrictBool] = None, page_size : Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None, search : Annotated[Optional[StrictStr], Field(description="A search term.")] = None, status : Annotated[Optional[StrictStr], Field(description="Filter cards by their current status  * `ISSUED` - Issued * `REVOKED` - Revoked * `RETURNED` - Returned * `EXPIRED` - Expired * `UNACTIVATED` - Unactivated")] = None, updated_at__gte : Optional[datetime] = None, updated_at__lte : Optional[datetime] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """List cards  # noqa: E501

        ## List Cards  Allows current and historic University Cards to be listed.  By default (without any URL parameters included) this method will return all cards, including temporary cards and cards that have expired / been revoked.  Query parameters can be used to refine the cards that are returned. For example, to fetch cards which have been issued and are therefore currently active we can add the query parameter: `status=ISSUED`.  If we want to find Cards with a specific identifier we can specify that identifier as a query parameter as well. For example, adding the following to the query string will return all revoked cards with the mifare ID '123':  `status=REVOKED&identifier=123@<mifare id scheme>`. Identifiers should be provided in the format `<value>@<scheme>`, but if the scheme is not provided the scheme shall be assumed to be the CRSid. See above for the list of supported schemes.  In the case of querying by mifare identifier, any leading zeros within the identifier value included in the query will be ignored - so querying with `identifier=0000000123@<mifare id scheme>` and `identifier=123@<mifare id scheme>` will return the same result.  Alternately the `search` query parameter can be used to search all cards by a single identifier value regardless of the scheme of that identifier.  If cards for multiple identifiers need to be fetched, use the `/cards/filter/` endpoint documented below.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view all cards contained within the card system. Without this permission only cards owned by the authenticated principal will be returned. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_list_with_http_info(card_type, created_at__gte, created_at__lte, cursor, expires_at__gte, expires_at__isnull, expires_at__lte, identifier, institution, issued_at__gte, issued_at__isnull, issued_at__lte, originating_card_request, originating_card_request__isnull, page_size, search, status, updated_at__gte, updated_at__lte, async_req=True)
        >>> result = thread.get()

        :param card_type: Filter by the type of card  * `MIFARE_PERSONAL` - Personal * `MIFARE_TEMPORARY` - Temporary
        :type card_type: str
        :param created_at__gte:
        :type created_at__gte: datetime
        :param created_at__lte:
        :type created_at__lte: datetime
        :param cursor: The pagination cursor value.
        :type cursor: str
        :param expires_at__gte:
        :type expires_at__gte: datetime
        :param expires_at__isnull:
        :type expires_at__isnull: bool
        :param expires_at__lte:
        :type expires_at__lte: datetime
        :param identifier: Filter cards by an identifier in the format {value}@{scheme}
        :type identifier: str
        :param institution: Institution id
        :type institution: str
        :param issued_at__gte:
        :type issued_at__gte: datetime
        :param issued_at__isnull:
        :type issued_at__isnull: bool
        :param issued_at__lte:
        :type issued_at__lte: datetime
        :param originating_card_request: Originating CardRequest UUID
        :type originating_card_request: str
        :param originating_card_request__isnull:
        :type originating_card_request__isnull: bool
        :param page_size: Number of results to return per page.
        :type page_size: int
        :param search: A search term.
        :type search: str
        :param status: Filter cards by their current status  * `ISSUED` - Issued * `REVOKED` - Revoked * `RETURNED` - Returned * `EXPIRED` - Expired * `UNACTIVATED` - Unactivated
        :type status: str
        :param updated_at__gte:
        :type updated_at__gte: datetime
        :param updated_at__lte:
        :type updated_at__lte: datetime
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PaginatedCardSummaryList, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'card_type',
            'created_at__gte',
            'created_at__lte',
            'cursor',
            'expires_at__gte',
            'expires_at__isnull',
            'expires_at__lte',
            'identifier',
            'institution',
            'issued_at__gte',
            'issued_at__isnull',
            'issued_at__lte',
            'originating_card_request',
            'originating_card_request__isnull',
            'page_size',
            'search',
            'status',
            'updated_at__gte',
            'updated_at__lte'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_cards_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('card_type') is not None:  # noqa: E501
            _query_params.append(('card_type', _params['card_type']))

        if _params.get('created_at__gte') is not None:  # noqa: E501
            if isinstance(_params['created_at__gte'], datetime):
                _query_params.append(('created_at__gte', _params['created_at__gte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('created_at__gte', _params['created_at__gte']))

        if _params.get('created_at__lte') is not None:  # noqa: E501
            if isinstance(_params['created_at__lte'], datetime):
                _query_params.append(('created_at__lte', _params['created_at__lte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('created_at__lte', _params['created_at__lte']))

        if _params.get('cursor') is not None:  # noqa: E501
            _query_params.append(('cursor', _params['cursor']))

        if _params.get('expires_at__gte') is not None:  # noqa: E501
            if isinstance(_params['expires_at__gte'], datetime):
                _query_params.append(('expires_at__gte', _params['expires_at__gte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('expires_at__gte', _params['expires_at__gte']))

        if _params.get('expires_at__isnull') is not None:  # noqa: E501
            _query_params.append(('expires_at__isnull', _params['expires_at__isnull']))

        if _params.get('expires_at__lte') is not None:  # noqa: E501
            if isinstance(_params['expires_at__lte'], datetime):
                _query_params.append(('expires_at__lte', _params['expires_at__lte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('expires_at__lte', _params['expires_at__lte']))

        if _params.get('identifier') is not None:  # noqa: E501
            _query_params.append(('identifier', _params['identifier']))

        if _params.get('institution') is not None:  # noqa: E501
            _query_params.append(('institution', _params['institution']))

        if _params.get('issued_at__gte') is not None:  # noqa: E501
            if isinstance(_params['issued_at__gte'], datetime):
                _query_params.append(('issued_at__gte', _params['issued_at__gte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('issued_at__gte', _params['issued_at__gte']))

        if _params.get('issued_at__isnull') is not None:  # noqa: E501
            _query_params.append(('issued_at__isnull', _params['issued_at__isnull']))

        if _params.get('issued_at__lte') is not None:  # noqa: E501
            if isinstance(_params['issued_at__lte'], datetime):
                _query_params.append(('issued_at__lte', _params['issued_at__lte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('issued_at__lte', _params['issued_at__lte']))

        if _params.get('originating_card_request') is not None:  # noqa: E501
            _query_params.append(('originating_card_request', _params['originating_card_request']))

        if _params.get('originating_card_request__isnull') is not None:  # noqa: E501
            _query_params.append(('originating_card_request__isnull', _params['originating_card_request__isnull']))

        if _params.get('page_size') is not None:  # noqa: E501
            _query_params.append(('page_size', _params['page_size']))

        if _params.get('search') is not None:  # noqa: E501
            _query_params.append(('search', _params['search']))

        if _params.get('status') is not None:  # noqa: E501
            _query_params.append(('status', _params['status']))

        if _params.get('updated_at__gte') is not None:  # noqa: E501
            if isinstance(_params['updated_at__gte'], datetime):
                _query_params.append(('updated_at__gte', _params['updated_at__gte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('updated_at__gte', _params['updated_at__gte']))

        if _params.get('updated_at__lte') is not None:  # noqa: E501
            if isinstance(_params['updated_at__lte'], datetime):
                _query_params.append(('updated_at__lte', _params['updated_at__lte'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('updated_at__lte', _params['updated_at__lte']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "PaginatedCardSummaryList",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/cards', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_cards_retrieve(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card.")], **kwargs) -> Card:  # noqa: E501
        """Get card detail  # noqa: E501

         ## Get Card Detail  Allows the detail of a single Card to be retrieved by ID. The Card entity returned contains the same information as presented in the filter and list card operations above, but also contains an array of `cardNotes` containing notes made by administrator users related to the current card.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view the card detail of any card contained within the card system. Principals without this permission are only able to view the card detail for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_retrieve(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: Card
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_cards_retrieve_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_cards_retrieve_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_cards_retrieve_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Get card detail  # noqa: E501

         ## Get Card Detail  Allows the detail of a single Card to be retrieved by ID. The Card entity returned contains the same information as presented in the filter and list card operations above, but also contains an array of `cardNotes` containing notes made by administrator users related to the current card.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view the card detail of any card contained within the card system. Principals without this permission are only able to view the card detail for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_retrieve_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(Card, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_cards_retrieve" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "Card",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/cards/{id}', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_cards_update(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card.")], card_update_request : CardUpdateRequest, **kwargs) -> CardUpdateResponseType:  # noqa: E501
        """Update the card  # noqa: E501

         ## Update the card  This method allows a client to submit an action in the request body and optional note for a given card. The allowed action is `cancel`.  The `cancel` action cancels the card. The client can optionally append a `note` describing the reason for cancelling the card.  The `refresh` action refreshes the card state. If the card is UNACTIVATED and the cardholder does not have an ISSUED card, the card state will be updated to ISSUED.  ### Permissions  Principals with the `CARD_UPDATER` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_update(id, card_update_request, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card. (required)
        :type id: str
        :param card_update_request: (required)
        :type card_update_request: CardUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardUpdateResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_cards_update_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_cards_update_with_http_info(id, card_update_request, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_cards_update_with_http_info(self, id : Annotated[constr(strict=True), Field(..., description="A UUID string identifying this card.")], card_update_request : CardUpdateRequest, **kwargs) -> ApiResponse:  # noqa: E501
        """Update the card  # noqa: E501

         ## Update the card  This method allows a client to submit an action in the request body and optional note for a given card. The allowed action is `cancel`.  The `cancel` action cancels the card. The client can optionally append a `note` describing the reason for cancelling the card.  The `refresh` action refreshes the card state. If the card is UNACTIVATED and the cardholder does not have an ISSUED card, the card state will be updated to ISSUED.  ### Permissions  Principals with the `CARD_UPDATER` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_update_with_http_info(id, card_update_request, async_req=True)
        >>> result = thread.get()

        :param id: A UUID string identifying this card. (required)
        :type id: str
        :param card_update_request: (required)
        :type card_update_request: CardUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardUpdateResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id',
            'card_update_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_cards_update" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['card_update_request'] is not None:
            _body_params = _params['card_update_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardUpdateResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '404': "NotFound",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/cards/{id}', 'PUT',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_cards_update_update(self, card_bulk_update_request : CardBulkUpdateRequest, **kwargs) -> CardBulkUpdateResponseType:  # noqa: E501
        """Update a set of cards  # noqa: E501

         ## Update multiple cards  Allows multiple cards to be updated in one call. For large number of cards, this endpoint will be faster than PUT-ing each update.  Updates are processed in the order they are received. The response includes the detail of the operation, the UUID of the card that was updated, and HTTP status code which would have been returned from separate PUTs. If the status code is 404, the `id` property is omitted.  ### Permissions  Principals with the `CARD_UPDATER` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_update_update(card_bulk_update_request, async_req=True)
        >>> result = thread.get()

        :param card_bulk_update_request: (required)
        :type card_bulk_update_request: CardBulkUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CardBulkUpdateResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_cards_update_update_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_cards_update_update_with_http_info(card_bulk_update_request, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_cards_update_update_with_http_info(self, card_bulk_update_request : CardBulkUpdateRequest, **kwargs) -> ApiResponse:  # noqa: E501
        """Update a set of cards  # noqa: E501

         ## Update multiple cards  Allows multiple cards to be updated in one call. For large number of cards, this endpoint will be faster than PUT-ing each update.  Updates are processed in the order they are received. The response includes the detail of the operation, the UUID of the card that was updated, and HTTP status code which would have been returned from separate PUTs. If the status code is 404, the `id` property is omitted.  ### Permissions  Principals with the `CARD_UPDATER` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_update_update_with_http_info(card_bulk_update_request, async_req=True)
        >>> result = thread.get()

        :param card_bulk_update_request: (required)
        :type card_bulk_update_request: CardBulkUpdateRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CardBulkUpdateResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'card_bulk_update_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_cards_update_update" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['card_bulk_update_request'] is not None:
            _body_params = _params['card_bulk_update_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CardBulkUpdateResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/cards/update', 'PUT',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_college_institution_ids_list(self, **kwargs) -> CollegeInstituionsIdsListResponseType:  # noqa: E501
        """List college and institution ids  # noqa: E501

         ## List College Institution Ids  Returns a list of the college institution ids used to set the card request scarf-code.  ### Permissions  Only principals with the `CARD_DATA_READERS` permission are able to list college institution ids.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_college_institution_ids_list(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CollegeInstituionsIdsListResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_college_institution_ids_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_college_institution_ids_list_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_college_institution_ids_list_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """List college and institution ids  # noqa: E501

         ## List College Institution Ids  Returns a list of the college institution ids used to set the card request scarf-code.  ### Permissions  Only principals with the `CARD_DATA_READERS` permission are able to list college institution ids.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_college_institution_ids_list_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(CollegeInstituionsIdsListResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_college_institution_ids_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "CollegeInstituionsIdsListResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/college-institution-ids', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def v1beta1_metrics_list(self, group_by : Optional[StrictStr] = None, **kwargs) -> MetricsListResponseType:  # noqa: E501
        """List metrics  # noqa: E501

        Detailed metrics about issued cards, revoked cards, etc.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_metrics_list(group_by, async_req=True)
        >>> result = thread.get()

        :param group_by:
        :type group_by: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: MetricsListResponseType
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the v1beta1_metrics_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.v1beta1_metrics_list_with_http_info(group_by, **kwargs)  # noqa: E501

    @validate_arguments
    def v1beta1_metrics_list_with_http_info(self, group_by : Optional[StrictStr] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """List metrics  # noqa: E501

        Detailed metrics about issued cards, revoked cards, etc.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_metrics_list_with_http_info(group_by, async_req=True)
        >>> result = thread.get()

        :param group_by:
        :type group_by: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(MetricsListResponseType, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'group_by'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v1beta1_metrics_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('group_by') is not None:  # noqa: E501
            _query_params.append(('group_by', _params['group_by']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['apiGatewayAuthorizationCodeSecurityScheme', 'apiGatewayClientCredentialsSecurityScheme']  # noqa: E501

        _response_types_map = {
            '200': "MetricsListResponseType",
            '400': "BadRequest",
            '401': "Unauthorized",
            '403': "Forbidden",
            '500': "InternalServerError",
        }

        return self.api_client.call_api(
            '/v1beta1/analytics', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
