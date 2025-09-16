import asyncio
import requests
import re
from pytube import YouTube
from typing import List
from playwright.async_api import async_playwright, Playwright, Page, Request, expect, Locator
downloaded = False
geturl = ''
QUALITY_REGEX = r'(Auto|144p|240p|360p|480p|720p60|1080p60 HD|1440p60 HD|2160p60 4K)'
QUALITY_PRIORITY = {
        "Auto": 0,
        "144p": 1,
        "240p": 2,
        "360p": 3,
        "480p": 4,
        "720p": 5,
        "720p60": 6,
        "1080p HD": 7,
        "1080p60 HD": 8,
        "1440p HD": 9,
        "1440p60 HD": 10,
        "2160p 4K": 11,
        "2160p60 4K": 12
    }

def trim_url(url: str):
    try:
        index = url.index('&range=')
        trimmed_url = url[:index]
        return trimmed_url
    except ValueError as e:
        return e
    
async def get_video_url(request: Request, page: Page):
    print(">>", request.method, request.url)
    global downloaded
    # if 'ad' in request.url:
    #     page.route(request.url, lambda route: route.abort())
    if 'mime=video' in request.url and downloaded==False:
        x=trim_url(request.url)
        if x != 'substring not found':
            downloaded =  True
            global geturl
            geturl = x
        else: geturl=''

async def changeres(page: Page):
    video = page.locator('.html5-video-player')
    await video.wait_for()

    # Click the settings button
    await expect(page.locator(".ytp-settings-button")).to_be_visible()
    await page.locator(".ytp-settings-button").click()
    
    # Wait for the settings menu to appear and click the quality button
    await page.locator('.ytp-panel-menu').wait_for()
    await expect(page.locator('.ytp-panel-menu')).to_have_attribute('role','menu')
    await expect(page.locator('.ytp-menuitem').last).to_have_attribute('role', 'menuitem')
    await expect(page.locator(".ytp-menuitem-label", has_text="Quality")).to_have_text("Quality")
    qualityMenu = page.locator(".ytp-menuitem-label", has_text="Quality")
    # Get all the available quality options
    # print(quality)
    await qualityMenu.click()
    await page.locator(".ytp-panel.ytp-quality-menu").wait_for()

    # allqualities = await page.locator(".ytp-menuitem").all()
    # #Exclude non visible qualities options
    # allqualities = [i for i in allqualities if await i.is_visible()]
    await expect(page.locator('.ytp-menuitem[role="menuitemradio"]').first).to_be_visible()
    result = page.locator('.ytp-menuitem[role="menuitemradio"]').first 
    # qlisttext = [await i.text_content() for i in allqualities]
    # desired_quality =  max(qlisttext, key=lambda x: QUALITY_PRIORITY.get(x, 0))
    # result = await get_max_quality_option(allqualities, desired_quality)
    print(await result.inner_text())
    await result.click()
    print('------------------Changed res!------------------')

async def get_max_quality_option(listqual: List[Locator], desired_quality):
    for i in listqual:
        if await i.inner_text() == desired_quality:
            return i
        continue
async def watch_variable():
    global geturl
    while geturl == '' or geturl == 'substring not found':
        await asyncio.sleep(1)
    return geturl

async def run(playwright: Playwright):
    chromium = playwright.firefox
    browser = await chromium.launch(headless=False)
    context = await browser.new_context()
    
    page = await browser.new_page()
    
    
    # page.set_default_timeout(40000)
    # while geturl == '':
    print("Loading page...")
    await page.goto(yt_url)
    print("Changing res...")
    await changeres(page)
    await asyncio.sleep(1)
    callback = lambda request: get_video_url(request, page)
    page.on("request", callback)
    print("VIDEO URL: ",await watch_variable())
        # if geturl != '':
        #     break
        # else:
        #     print("Reloading page...")
        #     await page.reload()

    await context.close()
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)
def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)
def download(url):
    print(url)
    print("Downloading...")
    file = requests.get(url)
    if 'mp4' in url:
        with open('downloadedvideos/'+get_valid_filename(x.title) + ".mp4", 'wb') as f:
            f.write(file.content)
    elif 'webm' in url:
        with open('downloadedvideos/'+get_valid_filename(x.title) + ".webm", 'wb') as f:
            f.write(file.content)

yt_url = 'https://youtu.be/OXMpTlOQYD4'
x = YouTube(yt_url)
asyncio.run(main())
# download(geturl)
#https://www.youtube.com/watch?v=m-NjoFrLkbQ