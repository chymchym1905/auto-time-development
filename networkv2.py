import asyncio
import sys
import re
import requests
from pytube import YouTube
from playwright.async_api import async_playwright, Playwright, expect

ytlink, dllink='',''

async def run(playwright: Playwright, yt_url):
    global dllink
    chromium = playwright.firefox
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await browser.new_page()
    print("Loading page...")
    await page.goto("https://y2nb.com/en/")
    await context.clear_cookies()
    await context.clear_permissions()

    await expect(page.get_by_placeholder("Enter Video URL here...")).to_be_visible()
    await page.get_by_placeholder("Enter Video URL here...").fill(yt_url)
    await page.locator("#btn_search").click()
    await page.wait_for_load_state("load")
    print("Getting video...")
    error = await page.locator(".session-error").is_visible()
    if error:
        print("Video Unavailable")
        await context.close()
        await browser.close()
        return
    dllink = await page.locator("#video-downloads").locator(".downloadsTable").nth(1).locator("tr > * > a").first.get_attribute("href")
    print(dllink)
    await context.close()
    await browser.close()

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)
def download(url, ytobject: YouTube):
    print(f"Downloading {ytobject.title}...")
    file = requests.get(url)
    if 'mp4' in url:
        with open('downloadedvideos/'+get_valid_filename(ytobject.title) + ".mp4", 'wb') as f:
            f.write(file.content)
    elif 'webm' in url:
        with open('downloadedvideos/'+get_valid_filename(ytobject.title) + ".webm", 'wb') as f:
            f.write(file.content)

async def main():
    if len(sys.argv) != 2:
        print("Usage: python networkv2.py yt_url")
        return
    global ytlink
    ytlink = sys.argv[1]
    async with async_playwright() as playwright:
        await run(playwright, yt_url=ytlink)
    


if __name__ == "__main__":
    asyncio.run(main())
    if dllink != '':
        download(dllink, YouTube(ytlink))
    
