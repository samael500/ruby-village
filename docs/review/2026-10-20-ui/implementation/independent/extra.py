from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
 b=p.chromium.launch();pg=b.new_page(viewport={'width':740,'height':360});pg.goto('http://localhost:5392/ruby-village/');pg.locator('#choose-level').click();pg.locator('#map-more').click();print('fresh',pg.locator('#chapter-ending').is_visible(),pg.locator('#letter-open').is_visible(),pg.locator('#reset-open').is_enabled());pg.screenshot(path='/tmp/ui79-independent/740-fresh-adventure.png');b.close()
