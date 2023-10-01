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


class TMSChecksApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_check(self, body, **kwargs):  # noqa: E501
        """Creates a new transaction check.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_check(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CheckWithoutID body: Specifies the check to be added (required)
        :return: CheckSimple
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.add_check_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.add_check_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def add_check_with_http_info(self, body, **kwargs):  # noqa: E501
        """Creates a new transaction check.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_check_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CheckWithoutID body: Specifies the check to be added (required)
        :return: CheckSimple
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
                    " to method add_check" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
            params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `add_check`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tms/check', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CheckSimple',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_check(self, cid, **kwargs):  # noqa: E501
        """Deletes a transaction check.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_check(cid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int cid: Specifies the id of the check to be deleted (required)
        :return: InlineResponse2009
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_check_with_http_info(cid, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_check_with_http_info(cid, **kwargs)  # noqa: E501
            return data

    def delete_check_with_http_info(self, cid, **kwargs):  # noqa: E501
        """Deletes a transaction check.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_check_with_http_info(cid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int cid: Specifies the id of the check to be deleted (required)
        :return: InlineResponse2009
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_check" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'cid' is set
        if ('cid' not in params or
            params['cid'] is None):
            raise ValueError("Missing the required parameter `cid` when calling `delete_check`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cid' in params:
            path_params['cid'] = params['cid']  # noqa: E501

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
            '/tms/check/{cid}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2009',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_all_checks(self, **kwargs):  # noqa: E501
        """Returns a list overview of all transaction checks.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_checks(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool extended_tags: Specifies whether to return an extended tags representation in the response (with type and count).
        :param list[str] tags: Tag list separated by commas. As an example \"nginx,apache\" would filter out all responses except those tagged nginx or apache
        :param str type: Filter to return only checks of a given type (a TMS `script` or a WPM `recording`). If not provided, all checks are returned.
        :param str limit: Limit of returned checks
        :param str offset: Offset of returned checks
        :return: ChecksAll
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_checks_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_checks_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_checks_with_http_info(self, **kwargs):  # noqa: E501
        """Returns a list overview of all transaction checks.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_checks_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool extended_tags: Specifies whether to return an extended tags representation in the response (with type and count).
        :param list[str] tags: Tag list separated by commas. As an example \"nginx,apache\" would filter out all responses except those tagged nginx or apache
        :param str type: Filter to return only checks of a given type (a TMS `script` or a WPM `recording`). If not provided, all checks are returned.
        :param str limit: Limit of returned checks
        :param str offset: Offset of returned checks
        :return: ChecksAll
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['extended_tags', 'tags', 'type', 'limit', 'offset']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_checks" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'extended_tags' in params:
            query_params.append(('extended_tags', params['extended_tags']))  # noqa: E501
        if 'tags' in params and params['tags'] != None:
            query_params.append(('tags', params['tags']))  # noqa: E501
            collection_formats['tags'] = 'csv'  # noqa: E501
        if 'type' in params and params['type'] != None:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501

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
            '/tms/check', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ChecksAll',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_check(self, cid, **kwargs):  # noqa: E501
        """Returns a single transaction check.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_check(cid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int cid: Specifies the id of the check to be fetched (required)
        :param bool extended_tags: Specifies whether to return an extended tags representation in the response (with type and count).
        :return: CheckWithoutIDGET
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_check_with_http_info(cid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_check_with_http_info(cid, **kwargs)  # noqa: E501
            return data

    def get_check_with_http_info(self, cid, **kwargs):  # noqa: E501
        """Returns a single transaction check.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_check_with_http_info(cid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int cid: Specifies the id of the check to be fetched (required)
        :param bool extended_tags: Specifies whether to return an extended tags representation in the response (with type and count).
        :return: CheckWithoutIDGET
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cid', 'extended_tags']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_check" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'cid' is set
        if ('cid' not in params or
            params['cid'] is None):
            raise ValueError("Missing the required parameter `cid` when calling `get_check`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cid' in params:
            path_params['cid'] = params['cid']  # noqa: E501

        query_params = []
        if 'extended_tags' in params:
            query_params.append(('extended_tags', params['extended_tags']))  # noqa: E501

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
            '/tms/check/{cid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CheckWithoutIDGET',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_check_report_performance(self, check_id, **kwargs):  # noqa: E501
        """Returns a performance report for a single transaction check  # noqa: E501

        For a given period of time, return a list of time intervals with the given resolution. An interval may be a week, a day or an hour depending on the chosen resolution. It can be used to display a detailed view of a check with information about its steps and generate graphs.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_check_report_performance(check_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int check_id: Specifies the id of the check for which the performance report will be fetched (required)
        :param datetime _from: Start time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is 10 times the resolution (10 hours, 10 day, 10 weeks) earlier than `to`. The value is extended to the nearest hour, day or week, depending on the 'resolution' parameter and configured time zone of the account.
        :param datetime to: End time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is the current time. The value is extended to the nearest hour, day or week, depending on the 'resolution' parameter and configured time zone of the account.
        :param str order: Sorting order of outages. Ascending or descending
        :param str resolution: Size of an interval for which the results are calculated. For the `hour` resolution, the max allowed period is one week and 1 day. For the `day` resolution, the max allowed period is 6 months and 1 day.
        :param bool include_uptime: Include uptime information. Adds field downtime, uptime, and unmonitored to the interval array objects.
        :return: ReportPerformance
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_check_report_performance_with_http_info(check_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_check_report_performance_with_http_info(check_id, **kwargs)  # noqa: E501
            return data

    def get_check_report_performance_with_http_info(self, check_id, **kwargs):  # noqa: E501
        """Returns a performance report for a single transaction check  # noqa: E501

        For a given period of time, return a list of time intervals with the given resolution. An interval may be a week, a day or an hour depending on the chosen resolution. It can be used to display a detailed view of a check with information about its steps and generate graphs.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_check_report_performance_with_http_info(check_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int check_id: Specifies the id of the check for which the performance report will be fetched (required)
        :param datetime _from: Start time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is 10 times the resolution (10 hours, 10 day, 10 weeks) earlier than `to`. The value is extended to the nearest hour, day or week, depending on the 'resolution' parameter and configured time zone of the account.
        :param datetime to: End time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is the current time. The value is extended to the nearest hour, day or week, depending on the 'resolution' parameter and configured time zone of the account.
        :param str order: Sorting order of outages. Ascending or descending
        :param str resolution: Size of an interval for which the results are calculated. For the `hour` resolution, the max allowed period is one week and 1 day. For the `day` resolution, the max allowed period is 6 months and 1 day.
        :param bool include_uptime: Include uptime information. Adds field downtime, uptime, and unmonitored to the interval array objects.
        :return: ReportPerformance
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['check_id', '_from', 'to', 'order', 'resolution', 'include_uptime']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_check_report_performance" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'check_id' is set
        if ('check_id' not in params or
            params['check_id'] is None):
            raise ValueError(
                "Missing the required parameter `check_id` when calling `get_check_report_performance`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'check_id' in params:
            path_params['check_id'] = params['check_id']  # noqa: E501

        query_params = []
        if '_from' in params:
            query_params.append(('from', params['_from']))  # noqa: E501
        if 'to' in params:
            query_params.append(('to', params['to']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'resolution' in params:
            query_params.append(('resolution', params['resolution']))  # noqa: E501
        if 'include_uptime' in params:
            query_params.append(('include_uptime', params['include_uptime']))  # noqa: E501

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
            '/tms/check/{check_id}/report/performance', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ReportPerformance',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_check_report_status(self, check_id, **kwargs):  # noqa: E501
        """Returns a status change report for a single transaction check  # noqa: E501

        Get a list of status changes for a specified check and time period. If order is speficied to descending, the list is ordered by newest first. (The default is ordered by oldest first.) It can be used to display a detailed view of a check.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_check_report_status(check_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int check_id: Specifies the id of the check for which the status change report will be fetched (required)
        :param datetime _from: Start time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is one week earlier than `to`
        :param datetime to: End time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is the current time
        :param str order: Sorting order of outages. Ascending or descending
        :return: ReportStatusSingle
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_check_report_status_with_http_info(check_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_check_report_status_with_http_info(check_id, **kwargs)  # noqa: E501
            return data

    def get_check_report_status_with_http_info(self, check_id, **kwargs):  # noqa: E501
        """Returns a status change report for a single transaction check  # noqa: E501

        Get a list of status changes for a specified check and time period. If order is speficied to descending, the list is ordered by newest first. (The default is ordered by oldest first.) It can be used to display a detailed view of a check.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_check_report_status_with_http_info(check_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int check_id: Specifies the id of the check for which the status change report will be fetched (required)
        :param datetime _from: Start time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is one week earlier than `to`
        :param datetime to: End time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is the current time
        :param str order: Sorting order of outages. Ascending or descending
        :return: ReportStatusSingle
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['check_id', '_from', 'to', 'order']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_check_report_status" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'check_id' is set
        if ('check_id' not in params or
            params['check_id'] is None):
            raise ValueError(
                "Missing the required parameter `check_id` when calling `get_check_report_status`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'check_id' in params:
            path_params['check_id'] = params['check_id']  # noqa: E501

        query_params = []
        if '_from' in params:
            query_params.append(('from', params['_from']))  # noqa: E501
        if 'to' in params:
            query_params.append(('to', params['to']))  # noqa: E501
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
            '/tms/check/{check_id}/report/status', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ReportStatusSingle',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_check_report_status_all(self, **kwargs):  # noqa: E501
        """Returns a status change report for all transaction checks in the current organization  # noqa: E501

        Get a list of status changes for all transaction check in the current organization from the requested time period. If order is speficied to descending, the list of statuses within each check is ordered by newest first. (The default is ordered by oldest first.) It can be used to display a list view of all checks and their current status.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_check_report_status_all(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime _from: Start time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is one week earlier than `to`
        :param datetime to: End time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is the current time
        :param str order: Sorting order of outages. Ascending or descending
        :param str limit: Limit of returned checks
        :param str offset: Offset of returned checks
        :param bool omit_empty: Omits checks without any results within specified time
        :return: ReportStatusAll
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_check_report_status_all_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_check_report_status_all_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_check_report_status_all_with_http_info(self, **kwargs):  # noqa: E501
        """Returns a status change report for all transaction checks in the current organization  # noqa: E501

        Get a list of status changes for all transaction check in the current organization from the requested time period. If order is speficied to descending, the list of statuses within each check is ordered by newest first. (The default is ordered by oldest first.) It can be used to display a list view of all checks and their current status.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_check_report_status_all_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime _from: Start time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is one week earlier than `to`
        :param datetime to: End time of period. The format is `RFC 3339` (properly URL-encoded!). The default value is the current time
        :param str order: Sorting order of outages. Ascending or descending
        :param str limit: Limit of returned checks
        :param str offset: Offset of returned checks
        :param bool omit_empty: Omits checks without any results within specified time
        :return: ReportStatusAll
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['_from', 'to', 'order', 'limit', 'offset', 'omit_empty']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_check_report_status_all" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if '_from' in params:
            query_params.append(('from', params['_from']))  # noqa: E501
        if 'to' in params:
            query_params.append(('to', params['to']))  # noqa: E501
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'omit_empty' in params:
            query_params.append(('omit_empty', params['omit_empty']))  # noqa: E501

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
            '/tms/check/report/status', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ReportStatusAll',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def modify_check(self, body, cid, **kwargs):  # noqa: E501
        """Modify settings for transaction check.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.modify_check(body, cid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CheckWithoutIDPUT body: Specifies the data to be modified for the check (required)
        :param int cid: Specifies the id of the check to be modified (required)
        :return: CheckWithoutIDGET
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.modify_check_with_http_info(body, cid, **kwargs)  # noqa: E501
        else:
            (data) = self.modify_check_with_http_info(body, cid, **kwargs)  # noqa: E501
            return data

    def modify_check_with_http_info(self, body, cid, **kwargs):  # noqa: E501
        """Modify settings for transaction check.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.modify_check_with_http_info(body, cid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CheckWithoutIDPUT body: Specifies the data to be modified for the check (required)
        :param int cid: Specifies the id of the check to be modified (required)
        :return: CheckWithoutIDGET
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'cid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method modify_check" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
            params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `modify_check`")  # noqa: E501
        # verify the required parameter 'cid' is set
        if ('cid' not in params or
            params['cid'] is None):
            raise ValueError("Missing the required parameter `cid` when calling `modify_check`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cid' in params:
            path_params['cid'] = params['cid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tms/check/{cid}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CheckWithoutIDGET',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
