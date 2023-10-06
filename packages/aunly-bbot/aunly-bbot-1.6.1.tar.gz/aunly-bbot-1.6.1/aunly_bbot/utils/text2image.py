import asyncio
import re
from io import BytesIO
from pathlib import Path

from graia.ariadne.app import Ariadne
from PIL import Image, ImageDraw, ImageFont

from .fonts_provider import get_font_sync
from .strings import get_cut_str

data_path = Path("data", "render")
data_path.mkdir(parents=True, exist_ok=True)
font = ImageFont.truetype(str(get_font_sync("sarasa-mono-sc-semibold.ttf")), size=20)


async def text2image(text: str, cut=64) -> bytes:
    return await asyncio.to_thread(_create_image, text, cut)


def _create_image(text: str, cut: int) -> bytes:
    cut_str = "\n".join(get_cut_str(text, cut))
    textx, texty = font.getsize_multiline(cut_str)
    image = Image.new("RGB", (textx + 40, texty + 40), (235, 235, 235))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), cut_str, font=font, fill=(31, 31, 33))
    imageio = BytesIO()
    image.save(
        imageio,
        format="JPEG",
        quality=90,
        subsampling=2,
        qtables="web_high",
    )
    return imageio.getvalue()


async def rich_text2image(data: str):
    from io import BytesIO

    from dynamicadaptor.Content import RichTextDetail, Text
    from minidynamicrender.DynConfig import ConfigInit
    from minidynamicrender.DynText import DynTextRender

    from .fonts_provider import get_font

    config = ConfigInit(
        data_path=str(data_path),
        font_path={
            "text": str(await get_font("HarmonyOS_Sans_SC_Medium.ttf")),
            "extra_text": str(await get_font("sarasa-mono-sc-bold.ttf")),
            "emoji": str(await get_font("nte.ttf")),
        },
    )
    if config.dyn_color and config.dyn_font and config.dy_size:
        render = DynTextRender(
            config.static_path, config.dyn_color, config.dyn_font, config.dy_size
        )
        image = await render.run(
            Text(
                text=data,
                topic=None,
                rich_text_nodes=[
                    RichTextDetail(
                        type="RICH_TEXT_NODE_TYPE_TEXT", text=data, orig_text=data, emoji=None
                    )
                ],
            )
        )
        if image:
            bio = BytesIO()
            image.convert("RGB").save(bio, "jpeg", optimize=True)
            return bio.getvalue()


async def browser_text2image(data: str):
    import jinja2
    from graiax.playwright.interface import PlaywrightContext

    from .browser_shot import fill_font

    app = Ariadne.current()
    browser_context = app.launch_manager.get_interface(PlaywrightContext).context

    src = "openai"
    data = r"\n".join(data.splitlines())

    summary = Path(__file__).parent.parent.joinpath("static", "summary")
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(summary),
        enable_async=True,
    )
    template_path = f"file:///{summary.joinpath('index.html').absolute()}".replace(
        "////", "///"
    )
    template = template_env.get_template("index.html")
    html = await template.render_async(
        **{
            "data": data,
            "src": src,
        }
    )

    async with await browser_context.new_page() as page:
        await page.route(re.compile("^https://fonts.bbot/(.+)$"), fill_font)
        await page.set_viewport_size({"width": 800, "height": 2000})
        await page.goto(template_path)
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(5)
        img_raw = await page.get_by_alt_text("main").screenshot(
            type="png",
        )
    return img_raw
