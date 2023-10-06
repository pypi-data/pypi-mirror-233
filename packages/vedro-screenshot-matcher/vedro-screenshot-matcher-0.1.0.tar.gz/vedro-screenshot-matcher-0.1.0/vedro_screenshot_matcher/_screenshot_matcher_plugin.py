from os import environ
from pathlib import Path
from shutil import rmtree
from typing import Any, Type

from playwright.async_api import Locator
from rtry import retry
from vedro.core import ConfigType, Dispatcher, Plugin, PluginConfig, VirtualScenario
from vedro.events import (
    ArgParsedEvent,
    ArgParseEvent,
    ConfigLoadedEvent,
    ScenarioFailedEvent,
    ScenarioPassedEvent,
    ScenarioRunEvent,
    StartupEvent,
    StepFailedEvent,
    StepPassedEvent,
    StepRunEvent,
)

from ._scheduler import ScreenshotMatcherScheduler
from ._screenshot_matcher import ScreenshotMatcher as _ScreenshotMatcher
from ._screenshot_matcher import ScreenshotMismatchError

__all__ = ("ScreenshotMatcher", "ScreenshotMatcherPlugin", "match_screenshot",)


_screenshot_matcher = _ScreenshotMatcher()


@retry(attempts=10, delay=0.25, swallow=ScreenshotMismatchError, logger=print)
async def match_screenshot(locator: Locator, **kwargs: Any) -> bool:
    return await _screenshot_matcher.match_screenshot(locator, **kwargs)


class ScreenshotMatcherPlugin(Plugin):
    def __init__(self, config: Type["ScreenshotMatcher"], *,
                 screenshot_matcher: _ScreenshotMatcher = _screenshot_matcher) -> None:
        super().__init__(config)
        self._screenshots_dir = config.screenshots_dir
        self._golden_app_url = config.golden_app_url
        self._golden_app_comment = config.golden_app_comment
        self._test_app_url = config.test_app_url
        self._test_app_comment = config.test_app_comment

        self._screenshot_matcher = screenshot_matcher
        self._global_config: ConfigType | None = None
        self._last_scenario_id: str | None = None

        self._skip_screenshots: bool = False

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ConfigLoadedEvent, self.on_config_loaded) \
                  .listen(ArgParseEvent, self.on_arg_parse) \
                  .listen(ArgParsedEvent, self.on_arg_parsed) \
                  .listen(StartupEvent, self.on_startup) \
                  .listen(ScenarioRunEvent, self.on_scenario_run) \
                  .listen(ScenarioPassedEvent, self.on_scenario_end) \
                  .listen(ScenarioFailedEvent, self.on_scenario_end) \
                  .listen(StepRunEvent, self.on_step_run) \
                  .listen(StepPassedEvent, self.on_step_end) \
                  .listen(StepFailedEvent, self.on_step_end)

    def on_config_loaded(self, event: ConfigLoadedEvent) -> None:
        self._global_config = event.config

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        group = event.arg_parser.add_argument_group("ScreenshotMatcher")
        group.add_argument("--skip-screenshots", action="store_true",
                           help="Skip Screenshot Asserts")

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._skip_screenshots = event.args.skip_screenshots

        assert self._golden_app_url and self._test_app_url
        self._set_app_url(self._test_app_url)

        assert self._global_config is not None
        if self._skip_screenshots:
            self._screenshot_matcher.set_current_mode("skip")
        else:
            self._global_config.Registry.ScenarioScheduler.register(ScreenshotMatcherScheduler, self)

        if self._screenshots_dir.exists():
            rmtree(self._screenshots_dir)
        self._screenshot_matcher.set_screenshots_dir(self._screenshots_dir)

    def on_startup(self, event: StartupEvent) -> None:
        self._scheduler = event.scheduler

    def _has_screenshot_asserts(self, scenario: VirtualScenario) -> bool:
        return getattr(scenario._orig_scenario, "__vedro__screenshot_asserts__", False)

    def _skip_screenshot_asserts(self, scenario: VirtualScenario) -> bool:
        return getattr(scenario._orig_scenario, "__vedro__screenshot_asserts_skip__", False)

    def _set_app_url(self, app_url: str | None) -> None:
        assert app_url is not None
        environ["APP_URL"] = app_url

    def on_scenario_run(self, event: ScenarioRunEvent) -> None:
        scenario = event.scenario_result.scenario
        if self._skip_screenshots or not self._has_screenshot_asserts(scenario):
            return

        if self._skip_screenshot_asserts(scenario):
            self._set_app_url(self._test_app_url)
            current_mode = "skip"
            comment = f"{self._test_app_comment} (skip screenshot asserts)"

        elif self._last_scenario_id != scenario.unique_id:
            self._set_app_url(self._golden_app_url)
            current_mode = "golden"
            comment = self._golden_app_comment or current_mode

        else:
            self._set_app_url(self._test_app_url)
            current_mode = "test"
            comment = self._test_app_comment or current_mode

        self._screenshot_matcher.set_current_scenario(scenario)
        self._screenshot_matcher.set_current_mode(current_mode)  # type: ignore
        event.scenario_result.add_extra_details(comment)

    def on_scenario_end(self, event: ScenarioPassedEvent | ScenarioFailedEvent) -> None:
        scenario = event.scenario_result.scenario
        if self._skip_screenshots or not self._has_screenshot_asserts(scenario):
            return

        self._set_app_url(self._test_app_url)
        self._screenshot_matcher.set_current_scenario(None)
        self._screenshot_matcher.set_current_mode(None)

        if self._skip_screenshot_asserts(scenario):
            self._last_scenario_id = scenario.unique_id
        else:
            if self._last_scenario_id != scenario.unique_id:
                if event.scenario_result.is_passed():
                    self._scheduler.schedule(scenario)
            self._last_scenario_id = scenario.unique_id

    def on_step_run(self, event: StepRunEvent) -> None:
        self._screenshot_matcher.set_current_step(event.step_result._step)

    def on_step_end(self, event: StepPassedEvent | StepFailedEvent) -> None:
        self._screenshot_matcher.set_current_step(None)


class ScreenshotMatcher(PluginConfig):
    plugin = ScreenshotMatcherPlugin

    # screenshots directory
    screenshots_dir: Path = Path("./screenshots")

    # golden app url
    golden_app_url: str | None = None

    # golden app comment
    golden_app_comment: str | None = None

    # test app url
    test_app_url: str | None = None

    # test app comment
    test_app_comment: str | None = None
