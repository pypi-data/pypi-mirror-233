# coding: utf-8

"""
    Pingdom Public API

    # Welcome to the Pingdom API! The Pingdom API is a way for you to automate your interaction with the Pingdom system. With the API, you can create your own scripts or applications with most of the functionality you can find inside the Pingdom control panel.  The Pingdom API is RESTful and HTTP-based. Basically, this means that the communication is made through normal HTTP requests.  # Authentication Authentication is needed in order to use the Pingdom API, and for this a Pingdom API Token is required. You generate your Pingdom API Token inside My Pingdom. The Pingdom API Token has a property called “Access level” to define its permissions. All operations that create or modify something (e.g. checks) need the Read/Write permission. If you only need to read data using the API token, we recommend to set the access level to “Read access”.  The authentication method for using tokens is HTTP Bearer Authentication (encrypted over HTTPS). This means that you will provide your token every time you make a request. No sessions are used.  Request ``` GET /checks HTTP/1.1 Host: api.pingdom.com Authorization: Bearer ofOhK18Ca6w4S_XmInGv0QPkqly-rbRBBoHsp_2FEH5QnIbH0VZhRPO3tlvrjMIKQ36VapX ```  Response ``` HTTP/1.1 200 OK Content-Length: 13 Content-Type: application/json {\"checks\":[]} ```  ## Basic Auth For compatibility reasons, the Pingdom API allows to use HTTP Basic Authentication with tokens. In cases where this is necessary, input the API token as the username and leave the password field empty.  An example request of how that would look like with the following API token: ofOhK18Ca6w4S_XmInGv0QPkqly-rbRBBoHsp_2FEH5QnIbH0VZhRPO3tlvrjMIKQ36VapX  ``` GET /checks HTTP/1.1 Host: api.pingdom.com Authorization: Basic b2ZPaEsxOENhNnc0U19YbUluR3YwUVBrcWx5LXJiUkJCb0hzcF8yRkVINVFuSWJIMFZaaFJQTzN0bHZyak1JS1EzNlZhcFg6 ```  # Server Address The base server address is: https://api.pingdom.com  Please note that HTTPS is required. You will not be able to connect through unencrypted HTTP.  # Providing Parameters GET requests should provide their parameters as a query string, part of the URL.  POST, PUT and DELETE requests should provide their parameters as a JSON. This should be part of the request body. Remember to add the proper content type header to the request: `Content-Type: application/json`.  We still support providing parameters as a query string for POST, PUT and DELETE requests, but we recommend using JSON going forward. If you are using query strings, they should be part of the body, URL or a combination. The encoding of the query string should be standard URL-encoding, as provided by various programming libraries.  When using `requests` library for Python, use `json` parameter instead of `data`. Due to the inner mechanisms of requests.post() etc. some endpoints may return responses not conforming to the documentation when dealing with `data` body.  # HTTP/1.1 Status Code Definitions The HTTP status code returned by a successful API request is defined in the documentation for that method. Usually, this will be 200 OK.  If something goes wrong, other codes may be returned. The API uses standard HTTP/1.1 status codes defined by [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html).  # JSON Responses All responses are sent JSON-encoded. The specific responses (successful ones) are described in the documentation section for each method.  However, if something goes wrong, our standard JSON error message (together with an appropriate status code) follows this format: ``` {     \"error\": {         \"statuscode\": 403,         \"statusdesc\": \"Forbidden\",         \"errormessage\":\" Something went wrong! This string describes what happened.\"     } } ``` See http://en.wikipedia.org/wiki/Json for more information on JSON.  Please note that all attributes of a method response are not always present. A client application should never assume that a certain attribute is present in a response.  # Limits The Pingdom API has usage limits to avoid individual rampant applications degrading the overall user experience. There are two layers of limits, the first cover a shorter period of time and the second a longer period. This enables you to \"burst\" requests for shorter periods. There are two HTTP headers in every response describing your limits status.  The response headers are: * **Req-Limit-Short** * **Req-Limit-Long**  An example of the values of these headers: * **Req-Limit-Short: Remaining: 394 Time until reset: 3589** * **Req-Limit-Long: Remaining: 71994 Time until reset: 2591989**  In this case, we can see that the user has 394 requests left until the short limit is reached. In 3589 seconds, the short limit will be reset. In similar fashion, the long limit has 71994 requests left, and will be reset in 2591989 seconds.  If limits are exceeded, an HTTP 429 error code with the message \"Request limit exceeded, try again later\" is sent back.  # gzip Responses can be gzip-encoded on demand. This is nice if your bandwidth is limited, or if big results are causing performance issues.  To enable gzip, simply add the following header to your request:  Accept-Encoding: gzip  # Best Practices ## Use caching If you are building a web page using the Pingdom API, we recommend that you do all API request on the server side, and if possible cache them. If you get any substantial traffic, you do not want to call the API each time you get a page hit, since this may cause you to hit the request limit faster than expected. In general, whenever you can cache data, do so.  ## Send your user credentials in a preemptive manner Some HTTP clients omit the authentication header, and make a second request with the header when they get a 401 Unauthorized response. Please make sure you send the credentials directly, to avoid unnecessary requests.  ## Use common sense Should be simple enough. For example, don't check for the status of a check every other second. The highest check resolution is one minute. Checking more often than that won't give you much of an advantage.  ## The Internet is unreliable Networks in general are unreliable, and particularly one as large and complex as the Internet. Your application should not assume it will get an answer. There may be timeouts.  # PHP Code Example **\"This is too much to read. I just want to get started right now! Give me a simple example!\"**  Here is a short example of how you can use the API with PHP. You need the cURL extension for PHP.  The example prints the current status of all your checks. This sample obviously focuses on Pingdom API code and does not worry about any potential problems connecting to the API, but your code should.  Code: ```php <?php     // Init cURL     $curl = curl_init();     // Set target URL     curl_setopt($curl, CURLOPT_URL, \"https://api.pingdom.com/api/3.1/checks\");     // Set the desired HTTP method (GET is default, see the documentation for each request)     curl_setopt($curl, CURLOPT_CUSTOMREQUEST, \"GET\");     // Add header with Bearer Authorization     curl_setopt($curl, CURLOPT_HTTPHEADER, array(\"Authorization: Bearer 907c762e069589c2cd2a229cdae7b8778caa9f07\"));     // Ask cURL to return the result as a string     curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);     // Execute the request and decode the json result into an associative array     $response = json_decode(curl_exec($curl), true);     // Check for errors returned by the API     if (isset($response['error'])) {         print \"Error: \" . $response['error']['errormessage'] . \"\\n\";         exit;     }     // Fetch the list of checks from the response     $checksList = $response['checks'];     // Print the names and statuses of all checks in the list     foreach ($checksList as $check) {         print $check['name'] . \" is \" . $check['status'] . \"\\n\";     } ?> ```  Example output: ``` Ubuntu Packages is up Google is up Pingdom is up My server 1 is down My server 2 is up ```  If you are running PHP on Windows, you need to be sure that you have installed the CA certificates for HTTPS/SSL to work correctly. Please see the cURL manual for more information. As a quick (but unsafe) workaround, you can add the following cURL option to ignore certificate validation.  ` curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0); `  # TMS Steps Vocabulary  There are two types of transaction checks: <ul>     <li><b>script</b>: the legacy TMS check created with predefined commands in the Pingdom UI or via the public API</li>     <li><b>recording</b>: the TMS check created by recording performed actions in WPM recorder.         More information about how to use it can be found in the         <a class=\"default-link\" href=\"https://documentation.solarwinds.com/en/success_center/wpm/Content/WPM-Use-the-WPM3-Recorder.htm\">             WPM recorder documentation</a>     </li> </ul>  ## Script transaction checks    ### Commands   Actions to be performed for the script TMS check    Step Name                                 | \"fn\"                  | Required \"args\"     | Remarks   ----------------------------------------- | --------------------- | --------------      | -------   Go to URL                                 | go_to                 | url                 | There has to be **exactly one** go_to step   Click                                     | click                 | element             | label, name or CSS selector   Fill in field                             | fill                  | input, value        | input: label, name or CSS selector, value: text   Check checkbox                            | check                 | checkbox            | label, name or CSS selector   Uncheck checkbox                          | uncheck               | checkbox            | label, name or CSS selector   Sleep for                                 | sleep                 | seconds             | number (e.g. 0.1)   Select radio button                       | select_radio          | radio               | name of the radio button   Select dropdown                           | select                | select, option      | select: label, name or CSS selector, option: content, value or CSS selector   Basic auth login with                     | basic_auth            | username, password  | username and password as text   Submit form                               | submit                | form                | name or CSS selector   Wait for element                          | wait_for_element      | element             | label, name or CSS selector   Wait for element to contain               | wait_for_contains     | element, value      | element: label, name or CSS selector, value: text    ### Validations   Verify the state of the page    Step Name                                 | \"fn\"                  | Required \"args\"     | Remarks   ----------------------------------------- | --------------------- | --------------      | -------   URL should be                             | url                   | url                 | url to be verified   Element should exist                      | exists                | element             | label, name or CSS selector   Element shouldn't exist                   | not_exists            | element             | label, name or CSS selector   Element should contain                    | contains              | element, value      | element: label, name or CSS selector, value: text   Element shouldn't containt                | not_contains          | element, value      | element: label, name or CSS selector, value: text   Text field should contain                 | field_contains        | input, value        | input: label, name or CSS selector, value: text   Text field shouldn't contain              | field_not_contains    | input, value        | input: label, name or CSS selector, value: text   Checkbox should be checked                | is_checked            | checkbox            | label, name or CSS selector   Checkbox shouldn't be checked             | is_not_checked        | checkbox            | label, name or CSS selector   Radio button should be selected           | radio_selected        | radio               | name of the radio button   Dropdown with name should be selected     | dropdown_selected     | select, option      | select: label, name or CSS selector, option: content, value or CSS selector   Dropdown with name shouldn't be selected  | dropdown_not_selected | select, option      | select: label, name or CSS selector, option: content, value or CSS selector    ### Example steps    ```   \"steps\": [   {     \"fn\": \"go_to\",     \"args\": {       \"url\": \"pingdom.com\"     }   },   {     \"fn\": \"click\",     \"args\": {       \"element\": \"START FREE TRIAL\"     }   },   {     \"fn\": \"url\",     \"args\": {       \"url\": \"https://www.pingdom.com/sign-up/\"     }   }   ]   ```  ## Recording transaction checks  Each of check steps contains: <ul>   <li><b>fn</b>: function name of the step</li>   <li><b>args</b>: function arguments</li>   <li><b>guid</b>: automatically generated identifier</li>   <li><b>contains_navigate</b>: recorder sets it on true if the step would trigger a page navigation</li> </ul>    ### Commands   Actions to be performed for the recording TMS check    Step Name                 | \"fn\"                      | Required \"args\"                 | Remarks   ------------------------- | ------------------------- | ------------------------------- | -------   Go to URL                 | wpm_go_to                 | url                             | Goes to the given url location   Click                     | wpm_click                 | element, offsetX, offsetY       | **element**: label, name or CSS selector,</br> **offsetX/Y**: exact position of a click in the element   Click in a exact location | wpm_click_xy              | element, x, y, scrollX, scrollY | **element**: label, name or CSS selector,</br> **x/y**: coordinates for the click (in viewport),</br> **scrollX/Y**: scrollbar position   Fill                      | wpm_fill                  | input, value                    | **input**: target element,</br> **value**: text to fill the target   Move mouse to element     | wpm_move_mouse_to_element | element, offsetX, offsetY       | **element**: target element,</br> **offsetX/Y**: exact position of the mouse in the element   Select dropdown           | wpm_select_dropdown       | select, option                  | **select**: target element (drop-down),</br> **option**: text of the option to select   Wait                      | wpm_wait                  | seconds                         | **seconds:** numbers of seconds to wait   Close tab                 | wpm_close_tab             | -                               | Closes the latest tab on the tab stack    ### Validations   Verify the state of the page    Step Name              | \"fn\"                     | Required \"args\"                                | Remarks   ---------------------- | ------------------------ | ---------------------------------------------- | -------   Contains text          | wpm_contains_timeout     | element, value, waitTime, useRegularExpression | **element**: label, name or CSS selector,</br> **value**: text to search for,</br> **waitTime**: time to wait for the value to appear,</br> **useRegularExpression**: use the value as a RegEx   Does not contains text | wpm_not_contains_timeout | element, value, waitTime, useRegularExpression | **element**: label, name or CSS selector,</br> **value**: text to search for,</br> **waitTime**: time to wait for the value to appear,</br> **useRegularExpression**: use the value as a RegEx    ### Metadata   Recording checks contain metadata which is automatically generated by the WPM recorder. Modify with caution!   # noqa: E501

    OpenAPI spec version: 3.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CheckWithoutIDGET(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'active': 'bool',
        'contact_ids': 'list[int]',
        'created_at': 'int',
        'modified_at': 'int',
        'last_downtime_start': 'int',
        'last_downtime_end': 'int',
        'custom_message': 'str',
        'interval': 'int',
        'name': 'str',
        'region': 'str',
        'send_notification_when_down': 'int',
        'severity_level': 'str',
        'status': 'str',
        'steps': 'list[Step]',
        'team_ids': 'list[int]',
        'integration_ids': 'list[int]',
        'metadata': 'MetadataGET',
        'tags': 'list[str]',
        'type': 'str'
    }

    attribute_map = {
        'active': 'active',
        'contact_ids': 'contact_ids',
        'created_at': 'created_at',
        'modified_at': 'modified_at',
        'last_downtime_start': 'last_downtime_start',
        'last_downtime_end': 'last_downtime_end',
        'custom_message': 'custom_message',
        'interval': 'interval',
        'name': 'name',
        'region': 'region',
        'send_notification_when_down': 'send_notification_when_down',
        'severity_level': 'severity_level',
        'status': 'status',
        'steps': 'steps',
        'team_ids': 'team_ids',
        'integration_ids': 'integration_ids',
        'metadata': 'metadata',
        'tags': 'tags',
        'type': 'type'
    }

    def __init__(self, active=None, contact_ids=None, created_at=None, modified_at=None, last_downtime_start=None, last_downtime_end=None, custom_message=None, interval=None, name=None, region=None, send_notification_when_down=None, severity_level=None, status=None, steps=None, team_ids=None, integration_ids=None, metadata=None, tags=None, type=None):  # noqa: E501
        """CheckWithoutIDGET - a model defined in Swagger"""  # noqa: E501
        self._active = None
        self._contact_ids = None
        self._created_at = None
        self._modified_at = None
        self._last_downtime_start = None
        self._last_downtime_end = None
        self._custom_message = None
        self._interval = None
        self._name = None
        self._region = None
        self._send_notification_when_down = None
        self._severity_level = None
        self._status = None
        self._steps = None
        self._team_ids = None
        self._integration_ids = None
        self._metadata = None
        self._tags = None
        self._type = None
        self.discriminator = None
        if active is not None:
            self.active = active
        if contact_ids is not None:
            self.contact_ids = contact_ids
        if created_at is not None:
            self.created_at = created_at
        if modified_at is not None:
            self.modified_at = modified_at
        if last_downtime_start is not None:
            self.last_downtime_start = last_downtime_start
        if last_downtime_end is not None:
            self.last_downtime_end = last_downtime_end
        if custom_message is not None:
            self.custom_message = custom_message
        if interval is not None:
            self.interval = interval
        if name is not None:
            self.name = name
        if region is not None:
            self.region = region
        if send_notification_when_down is not None:
            self.send_notification_when_down = send_notification_when_down
        if severity_level is not None:
            self.severity_level = severity_level
        if status is not None:
            self.status = status
        if steps is not None:
            self.steps = steps
        if team_ids is not None:
            self.team_ids = team_ids
        if integration_ids is not None:
            self.integration_ids = integration_ids
        if metadata is not None:
            self.metadata = metadata
        if tags is not None:
            self.tags = tags
        if type is not None:
            self.type = type

    @property
    def active(self):
        """Gets the active of this CheckWithoutIDGET.  # noqa: E501

        Check status - active or inactive  # noqa: E501

        :return: The active of this CheckWithoutIDGET.  # noqa: E501
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this CheckWithoutIDGET.

        Check status - active or inactive  # noqa: E501

        :param active: The active of this CheckWithoutIDGET.  # noqa: E501
        :type: bool
        """

        self._active = active

    @property
    def contact_ids(self):
        """Gets the contact_ids of this CheckWithoutIDGET.  # noqa: E501

        Contacts to alert  # noqa: E501

        :return: The contact_ids of this CheckWithoutIDGET.  # noqa: E501
        :rtype: list[int]
        """
        return self._contact_ids

    @contact_ids.setter
    def contact_ids(self, contact_ids):
        """Sets the contact_ids of this CheckWithoutIDGET.

        Contacts to alert  # noqa: E501

        :param contact_ids: The contact_ids of this CheckWithoutIDGET.  # noqa: E501
        :type: list[int]
        """

        self._contact_ids = contact_ids

    @property
    def created_at(self):
        """Gets the created_at of this CheckWithoutIDGET.  # noqa: E501

        Timestamp when the check was created  # noqa: E501

        :return: The created_at of this CheckWithoutIDGET.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this CheckWithoutIDGET.

        Timestamp when the check was created  # noqa: E501

        :param created_at: The created_at of this CheckWithoutIDGET.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def modified_at(self):
        """Gets the modified_at of this CheckWithoutIDGET.  # noqa: E501

        Timestamp when the check was modified  # noqa: E501

        :return: The modified_at of this CheckWithoutIDGET.  # noqa: E501
        :rtype: int
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this CheckWithoutIDGET.

        Timestamp when the check was modified  # noqa: E501

        :param modified_at: The modified_at of this CheckWithoutIDGET.  # noqa: E501
        :type: int
        """

        self._modified_at = modified_at

    @property
    def last_downtime_start(self):
        """Gets the last_downtime_start of this CheckWithoutIDGET.  # noqa: E501

        Timestamp when the last downtime started. This field is optional  # noqa: E501

        :return: The last_downtime_start of this CheckWithoutIDGET.  # noqa: E501
        :rtype: int
        """
        return self._last_downtime_start

    @last_downtime_start.setter
    def last_downtime_start(self, last_downtime_start):
        """Sets the last_downtime_start of this CheckWithoutIDGET.

        Timestamp when the last downtime started. This field is optional  # noqa: E501

        :param last_downtime_start: The last_downtime_start of this CheckWithoutIDGET.  # noqa: E501
        :type: int
        """

        self._last_downtime_start = last_downtime_start

    @property
    def last_downtime_end(self):
        """Gets the last_downtime_end of this CheckWithoutIDGET.  # noqa: E501

        Timestamp when the last downtime ended. This field is optional  # noqa: E501

        :return: The last_downtime_end of this CheckWithoutIDGET.  # noqa: E501
        :rtype: int
        """
        return self._last_downtime_end

    @last_downtime_end.setter
    def last_downtime_end(self, last_downtime_end):
        """Sets the last_downtime_end of this CheckWithoutIDGET.

        Timestamp when the last downtime ended. This field is optional  # noqa: E501

        :param last_downtime_end: The last_downtime_end of this CheckWithoutIDGET.  # noqa: E501
        :type: int
        """

        self._last_downtime_end = last_downtime_end

    @property
    def custom_message(self):
        """Gets the custom_message of this CheckWithoutIDGET.  # noqa: E501

        Custom message that is part of the email and webhook alerts  # noqa: E501

        :return: The custom_message of this CheckWithoutIDGET.  # noqa: E501
        :rtype: str
        """
        return self._custom_message

    @custom_message.setter
    def custom_message(self, custom_message):
        """Sets the custom_message of this CheckWithoutIDGET.

        Custom message that is part of the email and webhook alerts  # noqa: E501

        :param custom_message: The custom_message of this CheckWithoutIDGET.  # noqa: E501
        :type: str
        """

        self._custom_message = custom_message

    @property
    def interval(self):
        """Gets the interval of this CheckWithoutIDGET.  # noqa: E501

        TMS test intervals in minutes. Allowed intervals: 5,10,20,60,720,1440. The interval you're allowed to set may vary depending on your current plan.  # noqa: E501

        :return: The interval of this CheckWithoutIDGET.  # noqa: E501
        :rtype: int
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this CheckWithoutIDGET.

        TMS test intervals in minutes. Allowed intervals: 5,10,20,60,720,1440. The interval you're allowed to set may vary depending on your current plan.  # noqa: E501

        :param interval: The interval of this CheckWithoutIDGET.  # noqa: E501
        :type: int
        """

        self._interval = interval

    @property
    def name(self):
        """Gets the name of this CheckWithoutIDGET.  # noqa: E501

        Name of the check  # noqa: E501

        :return: The name of this CheckWithoutIDGET.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CheckWithoutIDGET.

        Name of the check  # noqa: E501

        :param name: The name of this CheckWithoutIDGET.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def region(self):
        """Gets the region of this CheckWithoutIDGET.  # noqa: E501

        Name of the region where the check is executed. Supported regions: us-east, us-west, eu, au  # noqa: E501

        :return: The region of this CheckWithoutIDGET.  # noqa: E501
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this CheckWithoutIDGET.

        Name of the region where the check is executed. Supported regions: us-east, us-west, eu, au  # noqa: E501

        :param region: The region of this CheckWithoutIDGET.  # noqa: E501
        :type: str
        """

        self._region = region

    @property
    def send_notification_when_down(self):
        """Gets the send_notification_when_down of this CheckWithoutIDGET.  # noqa: E501

        Send notification when down X times  # noqa: E501

        :return: The send_notification_when_down of this CheckWithoutIDGET.  # noqa: E501
        :rtype: int
        """
        return self._send_notification_when_down

    @send_notification_when_down.setter
    def send_notification_when_down(self, send_notification_when_down):
        """Sets the send_notification_when_down of this CheckWithoutIDGET.

        Send notification when down X times  # noqa: E501

        :param send_notification_when_down: The send_notification_when_down of this CheckWithoutIDGET.  # noqa: E501
        :type: int
        """

        self._send_notification_when_down = send_notification_when_down

    @property
    def severity_level(self):
        """Gets the severity_level of this CheckWithoutIDGET.  # noqa: E501

        Check importance- how important are the alerts when the check fails. Allowed values: low, high  # noqa: E501

        :return: The severity_level of this CheckWithoutIDGET.  # noqa: E501
        :rtype: str
        """
        return self._severity_level

    @severity_level.setter
    def severity_level(self, severity_level):
        """Sets the severity_level of this CheckWithoutIDGET.

        Check importance- how important are the alerts when the check fails. Allowed values: low, high  # noqa: E501

        :param severity_level: The severity_level of this CheckWithoutIDGET.  # noqa: E501
        :type: str
        """

        self._severity_level = severity_level

    @property
    def status(self):
        """Gets the status of this CheckWithoutIDGET.  # noqa: E501

        Whether the check is passing or failing at the moment (successful, failing, unknown)  # noqa: E501

        :return: The status of this CheckWithoutIDGET.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this CheckWithoutIDGET.

        Whether the check is passing or failing at the moment (successful, failing, unknown)  # noqa: E501

        :param status: The status of this CheckWithoutIDGET.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def steps(self):
        """Gets the steps of this CheckWithoutIDGET.  # noqa: E501

        steps to be executed as part of the check  # noqa: E501

        :return: The steps of this CheckWithoutIDGET.  # noqa: E501
        :rtype: list[Step]
        """
        return self._steps

    @steps.setter
    def steps(self, steps):
        """Sets the steps of this CheckWithoutIDGET.

        steps to be executed as part of the check  # noqa: E501

        :param steps: The steps of this CheckWithoutIDGET.  # noqa: E501
        :type: list[Step]
        """

        self._steps = steps

    @property
    def team_ids(self):
        """Gets the team_ids of this CheckWithoutIDGET.  # noqa: E501

        Teams to alert  # noqa: E501

        :return: The team_ids of this CheckWithoutIDGET.  # noqa: E501
        :rtype: list[int]
        """
        return self._team_ids

    @team_ids.setter
    def team_ids(self, team_ids):
        """Sets the team_ids of this CheckWithoutIDGET.

        Teams to alert  # noqa: E501

        :param team_ids: The team_ids of this CheckWithoutIDGET.  # noqa: E501
        :type: list[int]
        """

        self._team_ids = team_ids

    @property
    def integration_ids(self):
        """Gets the integration_ids of this CheckWithoutIDGET.  # noqa: E501

        Integration identifiers.  # noqa: E501

        :return: The integration_ids of this CheckWithoutIDGET.  # noqa: E501
        :rtype: list[int]
        """
        return self._integration_ids

    @integration_ids.setter
    def integration_ids(self, integration_ids):
        """Sets the integration_ids of this CheckWithoutIDGET.

        Integration identifiers.  # noqa: E501

        :param integration_ids: The integration_ids of this CheckWithoutIDGET.  # noqa: E501
        :type: list[int]
        """

        self._integration_ids = integration_ids

    @property
    def metadata(self):
        """Gets the metadata of this CheckWithoutIDGET.  # noqa: E501


        :return: The metadata of this CheckWithoutIDGET.  # noqa: E501
        :rtype: MetadataGET
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this CheckWithoutIDGET.


        :param metadata: The metadata of this CheckWithoutIDGET.  # noqa: E501
        :type: MetadataGET
        """

        self._metadata = metadata

    @property
    def tags(self):
        """Gets the tags of this CheckWithoutIDGET.  # noqa: E501

        List of tags for a check. The tag name may contain the characters 'A-Z', 'a-z', '0-9', '_' and '-'. The maximum length of a tag is 64 characters.  # noqa: E501

        :return: The tags of this CheckWithoutIDGET.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CheckWithoutIDGET.

        List of tags for a check. The tag name may contain the characters 'A-Z', 'a-z', '0-9', '_' and '-'. The maximum length of a tag is 64 characters.  # noqa: E501

        :param tags: The tags of this CheckWithoutIDGET.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def type(self):
        """Gets the type of this CheckWithoutIDGET.  # noqa: E501

        Type of transaction check: \"script\" for regular TMS checks and \"recording\" for checks made using the Transaction Recorder  # noqa: E501

        :return: The type of this CheckWithoutIDGET.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CheckWithoutIDGET.

        Type of transaction check: \"script\" for regular TMS checks and \"recording\" for checks made using the Transaction Recorder  # noqa: E501

        :param type: The type of this CheckWithoutIDGET.  # noqa: E501
        :type: str
        """
        allowed_values = ["script", "recording"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(CheckWithoutIDGET, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CheckWithoutIDGET):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
