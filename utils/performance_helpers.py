import logging
import time
from typing import Union, List
from pydantic import BaseModel, Field
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


def stopwatch(func):
    """Use this decorator to get times from any function
    example:
        @stopwatch
        get_started_button()

    returns logs:
        STOPWATCH - get_started_button took 3.4566850662231445 seconds
    """
    def wrapper(*args, **kwargs):
        log = logging.getLogger('driver')
        start_time = time.time()
        func(*args, **kwargs)
        stop_time = time.time()
        func_name = func.__name__
        log.info(f'STOPWATCH - {func_name} took {stop_time - start_time} seconds')

    return wrapper


class Performance:
    """ Performance API. Gets useful webpage related information """
    def __init__(self, driver):
        self.driver = driver

    def _wait(self, timeout=30):
        return WebDriverWait(self.driver, timeout=timeout)

    def get(self):
        """ The main method used to generate a WebPerformance object from the current web page.
        Notes:
            Calling this method too soon may create NoneTypes as the browser hasn't generated them yet.
        Examples:
            # Store the entire WebPerformance object and log it
            perf = performance.get()
            log.info(perf.dict())

            # Get a single data point from WebPerformance
            tti = performance.get().time_to_interactive()
        """
        return WebPerformance(
            time_origin=self.get_time_origin(),
            navigation_timing=self.get_navigation_timing(),
            paint_timing=self.get_paint_timing(),
            resources=self.get_resources()
        )

    def get_time_origin(self) -> float:
        """ Returns the timeOrigin.
        This is the high level timestamp of the start time of the performance measurement.
        """
        js = 'return window.performance.timeOrigin;'
        time_origin = self._wait().until(lambda driver: driver.execute_script(js), 'Time Origin not generated yet')
        return time_origin

    def get_navigation_timing(self):
        """ Return the PerformanceNavigationTiming object as a Python object. """
        js = 'return window.performance.getEntriesByType("navigation")[0];'
        navigation = self._wait().until(lambda driver: driver.execute_script(js), 'NavigationTiming not generated yet')
        return NavigationTiming(**navigation)

    def get_paint_timing(self):
        """ Return the PerformancePaintTiming object as a Python object. """
        js = 'return window.performance.getEntriesByName("first-contentful-paint")[0];'
        paint = self._wait().until(lambda driver: driver.execute_script(js), 'PaintTiming not generated yet')
        return PaintTiming(**paint)

    def get_resources(self):
        """ Return a list of PerformanceResourceTiming objects as Python objects. """
        js = 'return window.performance.getEntriesByType("resource");'
        try:
            resources = self._wait().until(
                lambda driver: driver.execute_script(js),
                message='Resources not generated yet or there are none')
            return [ResourceTiming(**resource) for resource in resources]
        except TimeoutException:
            return None  # if there were no Resources captured for the current web page


class NavigationTiming(BaseModel):
    """ PerformanceNavigationTiming
    Metrics regarding the browser's document navigation events
    References:
        https://developer.mozilla.org/en-US/docs/Web/API/PerformanceNavigationTiming
    """
    connect_end: float = Field(alias='connectEnd')
    connect_start: float = Field(alias='connectStart')
    decoded_body_size: Union[int, float] = Field(alias='decodedBodySize')
    dom_complete: float = Field(alias='domComplete')
    dom_content_loaded_event_end: float = Field(alias='domContentLoadedEventEnd')
    dom_content_loaded_event_start: float = Field(alias='domContentLoadedEventStart')
    time_to_interactive: float = Field(alias='domInteractive')
    domain_lookup_end: float = Field(alias='domainLookupEnd')
    domain_lookup_start: float = Field(alias='domainLookupStart')
    duration: float
    encoded_body_size: Union[int, float] = Field(alias='encodedBodySize')
    entry_type: str = Field(alias='entryType')
    fetch_start: float = Field(alias='fetchStart')
    initiator_type: str = Field(alias='initiatorType')
    load_event_end: float = Field(alias='loadEventEnd')
    load_event_start: float = Field(alias='loadEventStart')
    name: str
    next_hop_protocol: str = Field(alias='nextHopProtocol')
    redirect_count: int = Field(alias='redirectCount')
    redirect_end: int = Field(alias='redirectEnd')
    redirect_start: int = Field(alias='redirectStart')
    request_start: float = Field(alias='requestStart')
    response_end: float = Field(alias='responseEnd')
    response_start: float = Field(alias='responseStart')
    secure_connection_start: float = Field(alias='secureConnectionStart')
    server_timing: List = Field(alias='serverTiming')
    start_time: int = Field(alias='startTime')
    transfer_size: Union[int, float] = Field(alias='transferSize')
    type: str
    unload_event_end: int = Field(alias='unloadEventEnd')
    unload_event_start: int = Field(alias='unloadEventStart')
    worker_start: Union[int, float] = Field(alias='workerStart')


class PaintTiming(BaseModel):
    """ PerformancePaintTiming.
    Provides timing information about "paint" (also called "render") operations during web page construction.
    References:
        https://developer.mozilla.org/en-US/docs/Web/API/PerformancePaintTiming
    """
    duration: float
    entry_type: str = Field(alias='entryType', default='paint')
    name: str = Field(default='first-contentful-paint')
    start_time: float = Field(alias='startTime')


class ResourceTiming(BaseModel):
    """ PerformanceResourceTiming.
    Detailed network timing data regarding the loading of an application's resources.
    An application can use the timing metrics to determine, for example, the length of time it takes
    to fetch a specific resource, such as an HttpRequest, <SVG>, image, or script.
    References:
        https://developer.mozilla.org/en-US/docs/web/api/performanceresourcetiming
    """
    connect_end: float = Field(alias='connectEnd')
    connect_start: float = Field(alias='connectStart')
    decoded_body_size: int = Field(alias='decodedBodySize')
    domain_lookup_end: float = Field(alias='domainLookupEnd')
    domain_lookup_start: float = Field(alias='domainLookupStart')
    duration: float
    encoded_body_size: int = Field(alias='encodedBodySize')
    entry_type: str = Field(alias='entryType', default='resource')
    fetch_start: float = Field(alias='fetchStart')
    initiator_type: str = Field(alias='initiatorType')
    name: str
    next_hop_protocol: str = Field(alias='nextHopProtocol')
    redirect_end: float = Field(alias='redirectEnd')
    redirect_start: float = Field(alias='redirectStart')
    request_start: float = Field(alias='requestStart')
    response_end: float = Field(alias='responseEnd')
    response_start: float = Field(alias='responseStart')
    secure_connection_start: float = Field(alias='secureConnectionStart')
    server_timing: List = Field(alias='serverTiming')
    start_time: float = Field(alias='startTime')
    transfer_size: int = Field(alias='transferSize')
    worker_start: float = Field(alias='workerStart')


class WebPerformance(BaseModel):
    """ WebPerformance Object.
    This is built using multiple W3C Performance Timing objects to provide
    custom data points like:
    * Page Load Time
    * Time to First Contentful Paint
    * Time to Interactive (TTI)
    """
    time_origin: float  # Timestamp for the start time of the Performance measurement
    navigation_timing: NavigationTiming
    paint_timing: PaintTiming
    resources: List[ResourceTiming]

    def page_load_time(self) -> float:
        """ The time it takes for the page to load as experienced by the user. """
        return self.navigation_timing.load_event_end - self.navigation_timing.start_time

    def time_to_first_byte(self) -> float:
        """ The time it takes before the first byte of response is received from the server. """
        return self.navigation_timing.response_start

    def time_to_first_contentful_paint(self) -> float:
        """ The time it takes for the majority of content to be fully rendered and consumable by the user. """
        return self.paint_timing.start_time

    def time_to_interactive(self) -> float:
        """ The time it takes for the layout to be stabilized and the page is responsive. """
        return self.navigation_timing.dom_complete

    def number_of_requests(self) -> int:
        """ The number of requests sent from start of navigation until end of page load. """
        return len(self.resources)

    def time_to_dom_content_loaded(self) -> float:
        return self.navigation_timing.dom_content_loaded_event_end

    def page_weight(self) -> float:
        """ The amount of bytes transferred for the page to be loaded. """
        resource_transfer_size = sum([r.transfer_size for r in self.resources])
        return self.navigation_timing.transfer_size + resource_transfer_size

    def connection_time(self) -> float:
        """ The time taken to connect to the server. """
        return self.navigation_timing.connect_end - self.navigation_timing.connect_start

    def request_time(self) -> float:
        """ The time taken to send a request to the server and receive the response. """
        return self.navigation_timing.response_end - self.navigation_timing.response_start

    def fetch_time(self) -> float:
        """ The time to complete the document fetch (including accessing any caches, etc.). """
        return self.navigation_timing.response_end - self.navigation_timing.fetch_start
