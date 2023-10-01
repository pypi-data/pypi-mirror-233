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

class CreditsRespAttrsCredits(object):
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
        'checklimit': 'int',
        'availablechecks': 'int',
        'useddefault': 'int',
        'usedtransaction': 'int',
        'availablesms': 'int',
        'availablesmstests': 'int',
        'autofillsms': 'bool',
        'autofillsms_amount': 'int',
        'autofillsms_when_left': 'int',
        'max_sms_overage': 'int',
        'availablerumsites': 'int',
        'usedrumsites': 'int',
        'maxrumfilters': 'int',
        'maxrumpageviews': 'int'
    }

    attribute_map = {
        'checklimit': 'checklimit',
        'availablechecks': 'availablechecks',
        'useddefault': 'useddefault',
        'usedtransaction': 'usedtransaction',
        'availablesms': 'availablesms',
        'availablesmstests': 'availablesmstests',
        'autofillsms': 'autofillsms',
        'autofillsms_amount': 'autofillsms_amount',
        'autofillsms_when_left': 'autofillsms_when_left',
        'max_sms_overage': 'max_sms_overage',
        'availablerumsites': 'availablerumsites',
        'usedrumsites': 'usedrumsites',
        'maxrumfilters': 'maxrumfilters',
        'maxrumpageviews': 'maxrumpageviews'
    }

    def __init__(self, checklimit=None, availablechecks=None, useddefault=None, usedtransaction=None, availablesms=None, availablesmstests=None, autofillsms=None, autofillsms_amount=None, autofillsms_when_left=None, max_sms_overage=None, availablerumsites=None, usedrumsites=None, maxrumfilters=None, maxrumpageviews=None):  # noqa: E501
        """CreditsRespAttrsCredits - a model defined in Swagger"""  # noqa: E501
        self._checklimit = None
        self._availablechecks = None
        self._useddefault = None
        self._usedtransaction = None
        self._availablesms = None
        self._availablesmstests = None
        self._autofillsms = None
        self._autofillsms_amount = None
        self._autofillsms_when_left = None
        self._max_sms_overage = None
        self._availablerumsites = None
        self._usedrumsites = None
        self._maxrumfilters = None
        self._maxrumpageviews = None
        self.discriminator = None
        if checklimit is not None:
            self.checklimit = checklimit
        if availablechecks is not None:
            self.availablechecks = availablechecks
        if useddefault is not None:
            self.useddefault = useddefault
        if usedtransaction is not None:
            self.usedtransaction = usedtransaction
        if availablesms is not None:
            self.availablesms = availablesms
        if availablesmstests is not None:
            self.availablesmstests = availablesmstests
        if autofillsms is not None:
            self.autofillsms = autofillsms
        if autofillsms_amount is not None:
            self.autofillsms_amount = autofillsms_amount
        if autofillsms_when_left is not None:
            self.autofillsms_when_left = autofillsms_when_left
        if max_sms_overage is not None:
            self.max_sms_overage = max_sms_overage
        if availablerumsites is not None:
            self.availablerumsites = availablerumsites
        if usedrumsites is not None:
            self.usedrumsites = usedrumsites
        if maxrumfilters is not None:
            self.maxrumfilters = maxrumfilters
        if maxrumpageviews is not None:
            self.maxrumpageviews = maxrumpageviews

    @property
    def checklimit(self):
        """Gets the checklimit of this CreditsRespAttrsCredits.  # noqa: E501

        Total number of check slots on this account  # noqa: E501

        :return: The checklimit of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._checklimit

    @checklimit.setter
    def checklimit(self, checklimit):
        """Sets the checklimit of this CreditsRespAttrsCredits.

        Total number of check slots on this account  # noqa: E501

        :param checklimit: The checklimit of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._checklimit = checklimit

    @property
    def availablechecks(self):
        """Gets the availablechecks of this CreditsRespAttrsCredits.  # noqa: E501

        Free check slots available for new checks  # noqa: E501

        :return: The availablechecks of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._availablechecks

    @availablechecks.setter
    def availablechecks(self, availablechecks):
        """Sets the availablechecks of this CreditsRespAttrsCredits.

        Free check slots available for new checks  # noqa: E501

        :param availablechecks: The availablechecks of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._availablechecks = availablechecks

    @property
    def useddefault(self):
        """Gets the useddefault of this CreditsRespAttrsCredits.  # noqa: E501

        Total number of default check slots  # noqa: E501

        :return: The useddefault of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._useddefault

    @useddefault.setter
    def useddefault(self, useddefault):
        """Sets the useddefault of this CreditsRespAttrsCredits.

        Total number of default check slots  # noqa: E501

        :param useddefault: The useddefault of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._useddefault = useddefault

    @property
    def usedtransaction(self):
        """Gets the usedtransaction of this CreditsRespAttrsCredits.  # noqa: E501

        Total number of transaction check slots  # noqa: E501

        :return: The usedtransaction of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._usedtransaction

    @usedtransaction.setter
    def usedtransaction(self, usedtransaction):
        """Sets the usedtransaction of this CreditsRespAttrsCredits.

        Total number of transaction check slots  # noqa: E501

        :param usedtransaction: The usedtransaction of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._usedtransaction = usedtransaction

    @property
    def availablesms(self):
        """Gets the availablesms of this CreditsRespAttrsCredits.  # noqa: E501

        SMS credits remaining on this account  # noqa: E501

        :return: The availablesms of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._availablesms

    @availablesms.setter
    def availablesms(self, availablesms):
        """Sets the availablesms of this CreditsRespAttrsCredits.

        SMS credits remaining on this account  # noqa: E501

        :param availablesms: The availablesms of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._availablesms = availablesms

    @property
    def availablesmstests(self):
        """Gets the availablesmstests of this CreditsRespAttrsCredits.  # noqa: E501

        SMS provider tests remaining on this account  # noqa: E501

        :return: The availablesmstests of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._availablesmstests

    @availablesmstests.setter
    def availablesmstests(self, availablesmstests):
        """Sets the availablesmstests of this CreditsRespAttrsCredits.

        SMS provider tests remaining on this account  # noqa: E501

        :param availablesmstests: The availablesmstests of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._availablesmstests = availablesmstests

    @property
    def autofillsms(self):
        """Gets the autofillsms of this CreditsRespAttrsCredits.  # noqa: E501

        Auto fill SMS  # noqa: E501

        :return: The autofillsms of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: bool
        """
        return self._autofillsms

    @autofillsms.setter
    def autofillsms(self, autofillsms):
        """Sets the autofillsms of this CreditsRespAttrsCredits.

        Auto fill SMS  # noqa: E501

        :param autofillsms: The autofillsms of this CreditsRespAttrsCredits.  # noqa: E501
        :type: bool
        """

        self._autofillsms = autofillsms

    @property
    def autofillsms_amount(self):
        """Gets the autofillsms_amount of this CreditsRespAttrsCredits.  # noqa: E501

        The amount of sms to purchase when \"autofillsms_when_left\" is triggered  # noqa: E501

        :return: The autofillsms_amount of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._autofillsms_amount

    @autofillsms_amount.setter
    def autofillsms_amount(self, autofillsms_amount):
        """Sets the autofillsms_amount of this CreditsRespAttrsCredits.

        The amount of sms to purchase when \"autofillsms_when_left\" is triggered  # noqa: E501

        :param autofillsms_amount: The autofillsms_amount of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._autofillsms_amount = autofillsms_amount

    @property
    def autofillsms_when_left(self):
        """Gets the autofillsms_when_left of this CreditsRespAttrsCredits.  # noqa: E501

        The amount of sms left that is going to trigger purchase of sms  # noqa: E501

        :return: The autofillsms_when_left of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._autofillsms_when_left

    @autofillsms_when_left.setter
    def autofillsms_when_left(self, autofillsms_when_left):
        """Sets the autofillsms_when_left of this CreditsRespAttrsCredits.

        The amount of sms left that is going to trigger purchase of sms  # noqa: E501

        :param autofillsms_when_left: The autofillsms_when_left of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._autofillsms_when_left = autofillsms_when_left

    @property
    def max_sms_overage(self):
        """Gets the max_sms_overage of this CreditsRespAttrsCredits.  # noqa: E501

        The amount of overage SMSes that may be used, or null if SMS overage is not enabled.  # noqa: E501

        :return: The max_sms_overage of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._max_sms_overage

    @max_sms_overage.setter
    def max_sms_overage(self, max_sms_overage):
        """Sets the max_sms_overage of this CreditsRespAttrsCredits.

        The amount of overage SMSes that may be used, or null if SMS overage is not enabled.  # noqa: E501

        :param max_sms_overage: The max_sms_overage of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._max_sms_overage = max_sms_overage

    @property
    def availablerumsites(self):
        """Gets the availablerumsites of this CreditsRespAttrsCredits.  # noqa: E501

        Open RUM site slots available  # noqa: E501

        :return: The availablerumsites of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._availablerumsites

    @availablerumsites.setter
    def availablerumsites(self, availablerumsites):
        """Sets the availablerumsites of this CreditsRespAttrsCredits.

        Open RUM site slots available  # noqa: E501

        :param availablerumsites: The availablerumsites of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._availablerumsites = availablerumsites

    @property
    def usedrumsites(self):
        """Gets the usedrumsites of this CreditsRespAttrsCredits.  # noqa: E501

        Number of used RUM sites  # noqa: E501

        :return: The usedrumsites of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._usedrumsites

    @usedrumsites.setter
    def usedrumsites(self, usedrumsites):
        """Sets the usedrumsites of this CreditsRespAttrsCredits.

        Number of used RUM sites  # noqa: E501

        :param usedrumsites: The usedrumsites of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._usedrumsites = usedrumsites

    @property
    def maxrumfilters(self):
        """Gets the maxrumfilters of this CreditsRespAttrsCredits.  # noqa: E501

        Number of maximum rum filters  # noqa: E501

        :return: The maxrumfilters of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._maxrumfilters

    @maxrumfilters.setter
    def maxrumfilters(self, maxrumfilters):
        """Sets the maxrumfilters of this CreditsRespAttrsCredits.

        Number of maximum rum filters  # noqa: E501

        :param maxrumfilters: The maxrumfilters of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._maxrumfilters = maxrumfilters

    @property
    def maxrumpageviews(self):
        """Gets the maxrumpageviews of this CreditsRespAttrsCredits.  # noqa: E501

        Number of maximum pageviews per month  # noqa: E501

        :return: The maxrumpageviews of this CreditsRespAttrsCredits.  # noqa: E501
        :rtype: int
        """
        return self._maxrumpageviews

    @maxrumpageviews.setter
    def maxrumpageviews(self, maxrumpageviews):
        """Sets the maxrumpageviews of this CreditsRespAttrsCredits.

        Number of maximum pageviews per month  # noqa: E501

        :param maxrumpageviews: The maxrumpageviews of this CreditsRespAttrsCredits.  # noqa: E501
        :type: int
        """

        self._maxrumpageviews = maxrumpageviews

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
        if issubclass(CreditsRespAttrsCredits, dict):
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
        if not isinstance(other, CreditsRespAttrsCredits):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
