# coding: utf-8

"""
    Pingdom Public API

    # Welcome to the Pingdom API! The Pingdom API is a way for you to automate your interaction with the Pingdom system. With the API, you can create your own scripts or applications with most of the functionality you can find inside the Pingdom control panel.  The Pingdom API is RESTful and HTTP-based. Basically, this means that the communication is made through normal HTTP requests.  # Authentication Authentication is needed in order to use the Pingdom API, and for this a Pingdom API Token is required. You generate your Pingdom API Token inside My Pingdom. The Pingdom API Token has a property called “Access level” to define its permissions. All operations that create or modify something (e.g. checks) need the Read/Write permission. If you only need to read data using the API token, we recommend to set the access level to “Read access”.  The authentication method for using tokens is HTTP Bearer Authentication (encrypted over HTTPS). This means that you will provide your token every time you make a request. No sessions are used.  Request ``` GET /checks HTTP/1.1 Host: api.pingdom.com Authorization: Bearer ofOhK18Ca6w4S_XmInGv0QPkqly-rbRBBoHsp_2FEH5QnIbH0VZhRPO3tlvrjMIKQ36VapX ```  Response ``` HTTP/1.1 200 OK Content-Length: 13 Content-Type: application/json {\"checks\":[]} ```  ## Basic Auth For compatibility reasons, the Pingdom API allows to use HTTP Basic Authentication with tokens. In cases where this is necessary, input the API token as the username and leave the password field empty.  An example request of how that would look like with the following API token: ofOhK18Ca6w4S_XmInGv0QPkqly-rbRBBoHsp_2FEH5QnIbH0VZhRPO3tlvrjMIKQ36VapX  ``` GET /checks HTTP/1.1 Host: api.pingdom.com Authorization: Basic b2ZPaEsxOENhNnc0U19YbUluR3YwUVBrcWx5LXJiUkJCb0hzcF8yRkVINVFuSWJIMFZaaFJQTzN0bHZyak1JS1EzNlZhcFg6 ```  # Server Address The base server address is: https://api.pingdom.com  Please note that HTTPS is required. You will not be able to connect through unencrypted HTTP.  # Providing Parameters GET requests should provide their parameters as a query string, part of the URL.  POST, PUT and DELETE requests should provide their parameters as a JSON. This should be part of the request body. Remember to add the proper content type header to the request: `Content-Type: application/json`.  We still support providing parameters as a query string for POST, PUT and DELETE requests, but we recommend using JSON going forward. If you are using query strings, they should be part of the body, URL or a combination. The encoding of the query string should be standard URL-encoding, as provided by various programming libraries.  When using `requests` library for Python, use `json` parameter instead of `data`. Due to the inner mechanisms of requests.post() etc. some endpoints may return responses not conforming to the documentation when dealing with `data` body.  # HTTP/1.1 Status Code Definitions The HTTP status code returned by a successful API request is defined in the documentation for that method. Usually, this will be 200 OK.  If something goes wrong, other codes may be returned. The API uses standard HTTP/1.1 status codes defined by [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html).  # JSON Responses All responses are sent JSON-encoded. The specific responses (successful ones) are described in the documentation section for each method.  However, if something goes wrong, our standard JSON error message (together with an appropriate status code) follows this format: ``` {     \"error\": {         \"statuscode\": 403,         \"statusdesc\": \"Forbidden\",         \"errormessage\":\" Something went wrong! This string describes what happened.\"     } } ``` See http://en.wikipedia.org/wiki/Json for more information on JSON.  Please note that all attributes of a method response are not always present. A client application should never assume that a certain attribute is present in a response.  # Limits The Pingdom API has usage limits to avoid individual rampant applications degrading the overall user experience. There are two layers of limits, the first cover a shorter period of time and the second a longer period. This enables you to \"burst\" requests for shorter periods. There are two HTTP headers in every response describing your limits status.  The response headers are: * **Req-Limit-Short** * **Req-Limit-Long**  An example of the values of these headers: * **Req-Limit-Short: Remaining: 394 Time until reset: 3589** * **Req-Limit-Long: Remaining: 71994 Time until reset: 2591989**  In this case, we can see that the user has 394 requests left until the short limit is reached. In 3589 seconds, the short limit will be reset. In similar fashion, the long limit has 71994 requests left, and will be reset in 2591989 seconds.  If limits are exceeded, an HTTP 429 error code with the message \"Request limit exceeded, try again later\" is sent back.  # gzip Responses can be gzip-encoded on demand. This is nice if your bandwidth is limited, or if big results are causing performance issues.  To enable gzip, simply add the following header to your request:  Accept-Encoding: gzip  # Best Practices ## Use caching If you are building a web page using the Pingdom API, we recommend that you do all API request on the server side, and if possible cache them. If you get any substantial traffic, you do not want to call the API each time you get a page hit, since this may cause you to hit the request limit faster than expected. In general, whenever you can cache data, do so.  ## Send your user credentials in a preemptive manner Some HTTP clients omit the authentication header, and make a second request with the header when they get a 401 Unauthorized response. Please make sure you send the credentials directly, to avoid unnecessary requests.  ## Use common sense Should be simple enough. For example, don't check for the status of a check every other second. The highest check resolution is one minute. Checking more often than that won't give you much of an advantage.  ## The Internet is unreliable Networks in general are unreliable, and particularly one as large and complex as the Internet. Your application should not assume it will get an answer. There may be timeouts.  # PHP Code Example **\"This is too much to read. I just want to get started right now! Give me a simple example!\"**  Here is a short example of how you can use the API with PHP. You need the cURL extension for PHP.  The example prints the current status of all your checks. This sample obviously focuses on Pingdom API code and does not worry about any potential problems connecting to the API, but your code should.  Code: ```php <?php     // Init cURL     $curl = curl_init();     // Set target URL     curl_setopt($curl, CURLOPT_URL, \"https://api.pingdom.com/api/3.1/checks\");     // Set the desired HTTP method (GET is default, see the documentation for each request)     curl_setopt($curl, CURLOPT_CUSTOMREQUEST, \"GET\");     // Add header with Bearer Authorization     curl_setopt($curl, CURLOPT_HTTPHEADER, array(\"Authorization: Bearer 907c762e069589c2cd2a229cdae7b8778caa9f07\"));     // Ask cURL to return the result as a string     curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);     // Execute the request and decode the json result into an associative array     $response = json_decode(curl_exec($curl), true);     // Check for errors returned by the API     if (isset($response['error'])) {         print \"Error: \" . $response['error']['errormessage'] . \"\\n\";         exit;     }     // Fetch the list of checks from the response     $checksList = $response['checks'];     // Print the names and statuses of all checks in the list     foreach ($checksList as $check) {         print $check['name'] . \" is \" . $check['status'] . \"\\n\";     } ?> ```  Example output: ``` Ubuntu Packages is up Google is up Pingdom is up My server 1 is down My server 2 is up ```  If you are running PHP on Windows, you need to be sure that you have installed the CA certificates for HTTPS/SSL to work correctly. Please see the cURL manual for more information. As a quick (but unsafe) workaround, you can add the following cURL option to ignore certificate validation.  ` curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0); `  # TMS Steps Vocabulary  There are two types of transaction checks: <ul>     <li><b>script</b>: the legacy TMS check created with predefined commands in the Pingdom UI or via the public API</li>     <li><b>recording</b>: the TMS check created by recording performed actions in WPM recorder.         More information about how to use it can be found in the         <a class=\"default-link\" href=\"https://documentation.solarwinds.com/en/success_center/wpm/Content/WPM-Use-the-WPM3-Recorder.htm\">             WPM recorder documentation</a>     </li> </ul>  ## Script transaction checks    ### Commands   Actions to be performed for the script TMS check    Step Name                                 | \"fn\"                  | Required \"args\"     | Remarks   ----------------------------------------- | --------------------- | --------------      | -------   Go to URL                                 | go_to                 | url                 | There has to be **exactly one** go_to step   Click                                     | click                 | element             | label, name or CSS selector   Fill in field                             | fill                  | input, value        | input: label, name or CSS selector, value: text   Check checkbox                            | check                 | checkbox            | label, name or CSS selector   Uncheck checkbox                          | uncheck               | checkbox            | label, name or CSS selector   Sleep for                                 | sleep                 | seconds             | number (e.g. 0.1)   Select radio button                       | select_radio          | radio               | name of the radio button   Select dropdown                           | select                | select, option      | select: label, name or CSS selector, option: content, value or CSS selector   Basic auth login with                     | basic_auth            | username, password  | username and password as text   Submit form                               | submit                | form                | name or CSS selector   Wait for element                          | wait_for_element      | element             | label, name or CSS selector   Wait for element to contain               | wait_for_contains     | element, value      | element: label, name or CSS selector, value: text    ### Validations   Verify the state of the page    Step Name                                 | \"fn\"                  | Required \"args\"     | Remarks   ----------------------------------------- | --------------------- | --------------      | -------   URL should be                             | url                   | url                 | url to be verified   Element should exist                      | exists                | element             | label, name or CSS selector   Element shouldn't exist                   | not_exists            | element             | label, name or CSS selector   Element should contain                    | contains              | element, value      | element: label, name or CSS selector, value: text   Element shouldn't containt                | not_contains          | element, value      | element: label, name or CSS selector, value: text   Text field should contain                 | field_contains        | input, value        | input: label, name or CSS selector, value: text   Text field shouldn't contain              | field_not_contains    | input, value        | input: label, name or CSS selector, value: text   Checkbox should be checked                | is_checked            | checkbox            | label, name or CSS selector   Checkbox shouldn't be checked             | is_not_checked        | checkbox            | label, name or CSS selector   Radio button should be selected           | radio_selected        | radio               | name of the radio button   Dropdown with name should be selected     | dropdown_selected     | select, option      | select: label, name or CSS selector, option: content, value or CSS selector   Dropdown with name shouldn't be selected  | dropdown_not_selected | select, option      | select: label, name or CSS selector, option: content, value or CSS selector    ### Example steps    ```   \"steps\": [   {     \"fn\": \"go_to\",     \"args\": {       \"url\": \"pingdom.com\"     }   },   {     \"fn\": \"click\",     \"args\": {       \"element\": \"START FREE TRIAL\"     }   },   {     \"fn\": \"url\",     \"args\": {       \"url\": \"https://www.pingdom.com/sign-up/\"     }   }   ]   ```  ## Recording transaction checks  Each of check steps contains: <ul>   <li><b>fn</b>: function name of the step</li>   <li><b>args</b>: function arguments</li>   <li><b>guid</b>: automatically generated identifier</li>   <li><b>contains_navigate</b>: recorder sets it on true if the step would trigger a page navigation</li> </ul>    ### Commands   Actions to be performed for the recording TMS check    Step Name                 | \"fn\"                      | Required \"args\"                 | Remarks   ------------------------- | ------------------------- | ------------------------------- | -------   Go to URL                 | wpm_go_to                 | url                             | Goes to the given url location   Click                     | wpm_click                 | element, offsetX, offsetY       | **element**: label, name or CSS selector,</br> **offsetX/Y**: exact position of a click in the element   Click in a exact location | wpm_click_xy              | element, x, y, scrollX, scrollY | **element**: label, name or CSS selector,</br> **x/y**: coordinates for the click (in viewport),</br> **scrollX/Y**: scrollbar position   Fill                      | wpm_fill                  | input, value                    | **input**: target element,</br> **value**: text to fill the target   Move mouse to element     | wpm_move_mouse_to_element | element, offsetX, offsetY       | **element**: target element,</br> **offsetX/Y**: exact position of the mouse in the element   Select dropdown           | wpm_select_dropdown       | select, option                  | **select**: target element (drop-down),</br> **option**: text of the option to select   Wait                      | wpm_wait                  | seconds                         | **seconds:** numbers of seconds to wait   Close tab                 | wpm_close_tab             | -                               | Closes the latest tab on the tab stack    ### Validations   Verify the state of the page    Step Name              | \"fn\"                     | Required \"args\"                                | Remarks   ---------------------- | ------------------------ | ---------------------------------------------- | -------   Contains text          | wpm_contains_timeout     | element, value, waitTime, useRegularExpression | **element**: label, name or CSS selector,</br> **value**: text to search for,</br> **waitTime**: time to wait for the value to appear,</br> **useRegularExpression**: use the value as a RegEx   Does not contains text | wpm_not_contains_timeout | element, value, waitTime, useRegularExpression | **element**: label, name or CSS selector,</br> **value**: text to search for,</br> **waitTime**: time to wait for the value to appear,</br> **useRegularExpression**: use the value as a RegEx    ### Metadata   Recording checks contain metadata which is automatically generated by the WPM recorder. Modify with caution!   # noqa: E501

    OpenAPI spec version: 3.1

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from unskript.thirdparty.pingdom.swagger_client.api_client import ApiClient


class MaintenanceApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def maintenance_delete(self, maintenanceids, **kwargs):  # noqa: E501
        """Delete multiple maintenance windows.  # noqa: E501

        Delete multiple maintenance windows. Note that only future maintenance windows can be deleted.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_delete(maintenanceids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[int] maintenanceids: Comma-separated list of identifiers of maintenance windows to be deleted. (required)
        :return: MaintenanceDeleteRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.maintenance_delete_with_http_info(maintenanceids, **kwargs)  # noqa: E501
        else:
            (data) = self.maintenance_delete_with_http_info(maintenanceids, **kwargs)  # noqa: E501
            return data

    def maintenance_delete_with_http_info(self, maintenanceids, **kwargs):  # noqa: E501
        """Delete multiple maintenance windows.  # noqa: E501

        Delete multiple maintenance windows. Note that only future maintenance windows can be deleted.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_delete_with_http_info(maintenanceids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[int] maintenanceids: Comma-separated list of identifiers of maintenance windows to be deleted. (required)
        :return: MaintenanceDeleteRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['maintenanceids']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method maintenance_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'maintenanceids' is set
        if ('maintenanceids' not in params or
            params['maintenanceids'] is None):
            raise ValueError(
                "Missing the required parameter `maintenanceids` when calling `maintenance_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'maintenanceids' in params:
            query_params.append(('maintenanceids', params['maintenanceids']))  # noqa: E501
            collection_formats['maintenanceids'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/maintenance', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MaintenanceDeleteRespAttrs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def maintenance_get(self, **kwargs):  # noqa: E501
        """maintenance_get  # noqa: E501

        Returns a list of user's maintenance windows.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MaintenanceLimit limit: Count of items to list.
        :param MaintenanceOffset offset: Offset of the list.
        :param MaintenanceOrderby orderby: Order by the specific property of the maintenance window.
        :param MaintenanceOrder order: Order a-z for asc z-a for desc. Works only if orderby is specified.
        :return: MaintenanceRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.maintenance_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.maintenance_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def maintenance_get_with_http_info(self, **kwargs):  # noqa: E501
        """maintenance_get  # noqa: E501

        Returns a list of user's maintenance windows.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MaintenanceLimit limit: Count of items to list.
        :param MaintenanceOffset offset: Offset of the list.
        :param MaintenanceOrderby orderby: Order by the specific property of the maintenance window.
        :param MaintenanceOrder order: Order a-z for asc z-a for desc. Works only if orderby is specified.
        :return: MaintenanceRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['limit', 'offset', 'orderby', 'order']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method maintenance_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'orderby' in params:
            query_params.append(('orderby', params['orderby']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/maintenance', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MaintenanceRespAttrs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def maintenance_id_delete(self, id, **kwargs):  # noqa: E501
        """Delete the maintenance window.  # noqa: E501

        Delete the maintenance window. Note that only future maintenance window can be deleted.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_id_delete(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MaintenanceId id: id of maintenance window (required)
        :return: MaintenanceIdDeleteRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.maintenance_id_delete_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.maintenance_id_delete_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def maintenance_id_delete_with_http_info(self, id, **kwargs):  # noqa: E501
        """Delete the maintenance window.  # noqa: E501

        Delete the maintenance window. Note that only future maintenance window can be deleted.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_id_delete_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MaintenanceId id: id of maintenance window (required)
        :return: MaintenanceIdDeleteRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method maintenance_id_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
            params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `maintenance_id_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/maintenance/{id}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MaintenanceIdDeleteRespAttrs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def maintenance_id_get(self, id, **kwargs):  # noqa: E501
        """maintenance_id_get  # noqa: E501

        Returns the maintenance window specified by its id.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_id_get(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MaintenanceId id: id of maintenance window (required)
        :return: MaintenanceIdRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.maintenance_id_get_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.maintenance_id_get_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def maintenance_id_get_with_http_info(self, id, **kwargs):  # noqa: E501
        """maintenance_id_get  # noqa: E501

        Returns the maintenance window specified by its id.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_id_get_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MaintenanceId id: id of maintenance window (required)
        :return: MaintenanceIdRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method maintenance_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
            params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `maintenance_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/maintenance/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MaintenanceIdRespAttrs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def maintenance_id_put(self, body, id, **kwargs):  # noqa: E501
        """maintenance_id_put  # noqa: E501

        Modify the maintenance window.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_id_put(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MaintenanceIdPut body: Description (required)
        :param MaintenanceId id: id of maintenance window (required)
        :return: MaintenanceIdPutRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.maintenance_id_put_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.maintenance_id_put_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def maintenance_id_put_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """maintenance_id_put  # noqa: E501

        Modify the maintenance window.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_id_put_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MaintenanceIdPut body: Description (required)
        :param MaintenanceId id: id of maintenance window (required)
        :return: MaintenanceIdPutRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method maintenance_id_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
            params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `maintenance_id_put`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
            params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `maintenance_id_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'description' in params:
            form_params.append(('description', params['description']))  # noqa: E501
        if '_from' in params:
            form_params.append(('from', params['_from']))  # noqa: E501
        if 'to' in params:
            form_params.append(('to', params['to']))  # noqa: E501
        if 'recurrencetype' in params:
            form_params.append(('recurrencetype', params['recurrencetype']))  # noqa: E501
        if 'repeatevery' in params:
            form_params.append(('repeatevery', params['repeatevery']))  # noqa: E501
        if 'effectiveto' in params:
            form_params.append(('effectiveto', params['effectiveto']))  # noqa: E501
        if 'uptimeids' in params:
            form_params.append(('uptimeids', params['uptimeids']))  # noqa: E501
            collection_formats['uptimeids'] = 'multi'  # noqa: E501
        if 'tmsids' in params:
            form_params.append(('tmsids', params['tmsids']))  # noqa: E501
            collection_formats['tmsids'] = 'multi'  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/maintenance/{id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MaintenanceIdPutRespAttrs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def maintenance_post(self, body, **kwargs):  # noqa: E501
        """maintenance_post  # noqa: E501

        Create new maintenance window.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_post(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MaintenancePost body: Description (required)
        :return: MaintenancePostRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.maintenance_post_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.maintenance_post_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def maintenance_post_with_http_info(self, body, **kwargs):  # noqa: E501
        """maintenance_post  # noqa: E501

        Create new maintenance window.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.maintenance_post_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MaintenancePost body: Description (required)
        :return: MaintenancePostRespAttrs
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method maintenance_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
            params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `maintenance_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'description' in params:
            form_params.append(('description', params['description']))  # noqa: E501
        if '_from' in params:
            form_params.append(('from', params['_from']))  # noqa: E501
        if 'to' in params:
            form_params.append(('to', params['to']))  # noqa: E501
        if 'recurrencetype' in params:
            form_params.append(('recurrencetype', params['recurrencetype']))  # noqa: E501
        if 'repeatevery' in params:
            form_params.append(('repeatevery', params['repeatevery']))  # noqa: E501
        if 'effectiveto' in params:
            form_params.append(('effectiveto', params['effectiveto']))  # noqa: E501
        if 'uptimeids' in params:
            form_params.append(('uptimeids', params['uptimeids']))  # noqa: E501
            collection_formats['uptimeids'] = 'multi'  # noqa: E501
        if 'tmsids' in params:
            form_params.append(('tmsids', params['tmsids']))  # noqa: E501
            collection_formats['tmsids'] = 'multi'  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/maintenance', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MaintenancePostRespAttrs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
