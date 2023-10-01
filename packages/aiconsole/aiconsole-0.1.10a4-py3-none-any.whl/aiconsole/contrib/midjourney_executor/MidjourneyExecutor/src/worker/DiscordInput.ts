import path from 'path';
import puppeteer, { type Browser, type ElementHandle, type Page } from 'puppeteer';

import PQueue from '../../../../../backend/utils/pqueue';
import { BASE_DIR } from '../../../../../shared/global';
import { env } from '@/src/env';

export const discordQueue = new PQueue({ concurrency: 1 });

export class DiscordInput {
  browser?: Browser;
  page?: Page;
  isRecevingSigInt = false;

  async makeSureIsConnected() {
    if (!this.isRecevingSigInt) {
      process.on('SIGINT', async () => {
        console.log('Closing browser ...');

        if (this.browser != null) {
          await this.browser.close();
        }

        process.exit();
      });
      this.isRecevingSigInt = true;
    }

    if (this.browser == null || this.page == null || this.browser.isConnected() === false) {
      if (this.browser != null) {
        await this.browser.close();
      }

      this.browser = await puppeteer.launch({
        headless: false,
        userDataDir: path.join(BASE_DIR, 'tmp', 'browser'),
        timeout: 0,
      });

      this.page = await this.browser.newPage();

      // Go to the Discord login page

      const channelAdress = `https://discord.com/channels/${env.DISCORD_ART_SERVER_ID}/${env.DISCORD_ART_CHANNEL_ID}`;
      await this.page.goto(channelAdress);
      await this.page.waitForNetworkIdle();

      if (await this.page.$('div[class*="centeringWrapper-"] button:last-of-type div[class*="contents-"]')) {
        await this.page.click('div[class*="centeringWrapper-"] button:last-of-type div[class*="contents-"]');
        await this.page.waitForNetworkIdle();
      }

      if (this.page.url().includes('login')) {
        // Fill in the login form and submit it
        await this.page.type('input[name="email"]', env.DISCORD_CLIENT_LOGIN_EMAIL);
        await this.page.type('input[name="password"]', env.DISCORD_CLIENT_LOGIN_PASSWORD);

        do {
          await this.page.click('button[type="submit"]');
          await this.page.waitForTimeout(100);
        } while (await this.page.$('button[type="submit"]'));
      }

      // Wait for the channel page to load
      await this.page.waitForSelector('div[class*="channelTextArea-"]');
    }
  }

  async disconnect() {
    if (this.browser == null) return;

    // Close the browser
    await this.browser.close();

    this.browser = undefined;
    this.page = undefined;
  }

  async pressImageButton(messageURL: string, buttonText: string) {
    await this.makeSureIsConnected();
    if (this.browser == null) throw new Error('Browser not initialized');

    const page = await this.browser.newPage();

    await page.goto(messageURL);
    await page.waitForNetworkIdle();
    await page.waitForSelector('div[class*="backgroundFlash-"] button');

    const [button] = await page.$x(`//div[starts-with(@class, 'backgroundFlash-')]//button[contains(., '${buttonText}')]`);
    console.log(button, `//div[starts-with(@class, 'backgroundFlash-')]//button[contains(., '${buttonText}')]`);
    if (button) {
      await (button as ElementHandle<Element>).click();
      await page.waitForNetworkIdle();
      await (button as ElementHandle<Element>).click();
    }
    await page.waitForNetworkIdle();
    await page.close();
  }

  async sendPrompt(msg: string) {
    await discordQueue.add(async () => {
      await this.makeSureIsConnected();

      if (this.page == null) throw new Error('Page not initialized');

      // Find the message input box and type your message
      const messageInput = await this.page.$('div[class*="channelTextArea-"]');
      await messageInput!.type('/imagine');
      await this.page.waitForSelector('div[class*="autocompleteRowHeading-"]');
      await messageInput?.press('Enter');
      await messageInput!.type(msg);
      await messageInput?.press('Enter');

      //this.browser!.close();
    });
  }
}
