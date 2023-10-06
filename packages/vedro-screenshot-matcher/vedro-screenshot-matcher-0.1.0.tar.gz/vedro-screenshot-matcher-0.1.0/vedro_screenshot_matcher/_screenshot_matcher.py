from io import BytesIO
from pathlib import Path
from typing import Any, Literal, Tuple

from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
from playwright.async_api import Locator
from vedro.core import FileArtifact, VirtualScenario, VirtualStep
from vedro.plugins.artifacted import attach_step_artifact

__all__ = ("ScreenshotMatcher", "ScreenshotMismatchError",)


ModeType = Literal["test", "golden", "skip"]


class ScreenshotMatcherError(Exception):
    pass


class ScreenshotMismatchError(ScreenshotMatcherError, AssertionError):
    pass


class ScreenshotMatcher:
    def __init__(self) -> None:
        self._screenshots_dir: Path | None = None
        self._current_step: VirtualStep | None = None
        self._current_scenario: VirtualScenario | None = None
        self._current_mode: ModeType | None = None

    def set_screenshots_dir(self, dir: Path) -> None:
        self._screenshots_dir = dir

    def set_current_step(self, step: VirtualStep | None) -> None:
        self._current_step = step

    def set_current_scenario(self, scenario: VirtualScenario | None) -> None:
        self._current_scenario = scenario

    def set_current_mode(self, mode: ModeType | None) -> None:
        self._current_mode = mode

    def _gen_screenshot_path(self, suffix: str = "") -> Path:
        scenario = self._current_scenario
        step = self._current_step
        assert (scenario is not None) and (step is not None)

        screenshots_dir = self._screenshots_dir
        assert screenshots_dir is not None

        path = screenshots_dir / scenario.rel_path.with_suffix("")
        template = f"{scenario.template_index}" if scenario.template_index else ""
        filename = f"{scenario.name}{template}__{step.name}__{suffix}.png"
        return path / filename

    def _create_result_image(self, golden_img: Image, test_img: Image, diff_img: Image) -> Image:
        images = (golden_img, diff_img, test_img)
        width = sum(x.width for x in images)
        height = max(x.height for x in images)

        result = Image.new("RGBA", (width, height))
        for idx, image in enumerate(images):
            w = sum(x.width for x in images[:idx])
            result.paste(image, box=(w, 0))
        return result

    def _resize_images(self, golden_img: Image, test_img: Image) -> Tuple[Any, Any]:
        # 1. Берём max_width/max_height среди golden_img и test_img
        max_height = max(golden_img.height, test_img.height)
        max_width = max(golden_img.width, test_img.width)

        # 2. Вписываем golden_img в заглушку размером max_width/max_height
        golden_img_resized = Image.new("RGB", (max_width, max_height))
        golden_img_resized.paste(golden_img)

        # 3. Вписываем test_img в заглушку размером max_width/max_height
        test_img_resized = Image.new("RGB", (max_width, max_height))
        test_img_resized.paste(test_img)

        return golden_img_resized, test_img_resized

    async def match_screenshot(self, locator: Locator, **kwargs: Any) -> bool:
        if self._current_mode is None:
            raise ScreenshotMatcherError("add @screenshot_asserts() to use match_screenshot()")
        elif self._current_mode == "skip":
            return True

        golden_screenshot_path = self._gen_screenshot_path("golden")
        if self._current_mode == "golden":
            await locator.screenshot(path=golden_screenshot_path, **kwargs)
            return True

        golden_img = Image.open(golden_screenshot_path)

        branch_screenshot = await locator.screenshot(**kwargs)
        branch_img = Image.open(BytesIO(branch_screenshot))
        if golden_img == branch_img:
            return True

        # Размер элемента на ветке может быть больше/меньше
        # pixelmatch не умеет сравнивать изображения разных размеров и вместо диффа кидает:
        # - ValueError: ('Image sizes do not match.', 9800, 6560)
        # Поэтому приводим изображения к одному размеру
        golden_img, branch_img = self._resize_images(golden_img, branch_img)

        diff_img = Image.new("RGBA", golden_img.size)
        mismatch = pixelmatch(golden_img, branch_img, diff_img, includeAA=True)
        if mismatch == 0:
            return True

        result_img = self._create_result_image(golden_img, branch_img, diff_img)
        result_path = self._gen_screenshot_path("diff")
        result_img.save(result_path)

        artifact = FileArtifact(result_path.name, "image/png", result_path)
        attach_step_artifact(artifact)

        rel_path = result_path.relative_to(Path())
        message = f"./{rel_path} (missmatch {mismatch})"
        raise ScreenshotMismatchError(message)
