import axios from 'axios';
import DiscordJS, { type TextChannel } from 'discord.js';
import sharp from 'sharp';

import { waitingRequests } from './waitingRequests';
import { BackgroundWorkerTask } from '@/src/aiconsole/modules/Workers/src/BackgroundWorker';
import { MidJourneyImageType } from '../MidJourneyImageType';
import { env } from '@/src/env';

async function fetchAllMessages(
  channel: TextChannel,
  options = {
    reverseArray: false,
    userOnly: false,
    botOnly: false,
    pinnedOnly: false,
  },
) {
  // if (!(channel instanceof discord_js_1.TextChannel)) {throw new Error('discord-fetch-all: channel parameter is not a instance of a discord channel.');}
  const { reverseArray, userOnly, botOnly, pinnedOnly } = options;
  let messages: any[] = [];
  let lastID;
  while (true) {
    // eslint-disable-line no-constant-condition
    const fetchedMessages: any = await channel.messages.fetch({
      limit: 100,
      ...(lastID && { before: lastID }),
    });
    if (fetchedMessages.size === 0) {
      if (reverseArray) {
        messages = messages.reverse();
      }
      if (userOnly) {
        messages = messages.filter((msg) => !msg.author.bot);
      }
      if (botOnly) {
        messages = messages.filter((msg) => msg.author.bot);
      }
      if (pinnedOnly) {
        messages = messages.filter((msg) => msg.pinned);
      }
      return messages;
    }
    messages = messages.concat(Array.from(fetchedMessages.values()));
    lastID = fetchedMessages.lastKey();
  }
}

function classifyMidJourneyMessage(message: DiscordJS.Message<boolean>): MidJourneyImageType | undefined {
  const progressRegexp = /\((100|[1-9]?\d)%\)/;
  const imageNumberRegexp = /\*\* - Image #(\d+) <@/;

  if (progressRegexp.test(message.content)) return;

  let imageNumberMatch = message.content.match(imageNumberRegexp);
  if (message.attachments.size > 0 && imageNumberMatch) {
    return 'MIDJOURNEY_UPSCALE';
  }

  if (message.attachments.size > 0 && new RegExp(/\*\* - <@(\d+)> \(/).test(message.content)) return 'MIDJOURNEY_GRID';
  if (message.attachments.size > 0 && new RegExp(/\*\* - Variations by <@(\d+)> \(/).test(message.content)) return 'MIDJOURNEY_GRID';

  return undefined;
}

async function processMidJourneyMessage(message: DiscordJS.Message, historic = false) {
  if (!historic) console.log(`${message.author.username} said: ${message.content}`);

  if (message.channel.id !== env.DISCORD_BOT_CHANNEL_ID) {
    console.log(`Ignoring message from channel ${message.channel.id} (not ${env.DISCORD_BOT_CHANNEL_ID})`);
    return;
  }

  const classificationOrUndefined = classifyMidJourneyMessage(message);
  if (classificationOrUndefined == null) {
    console.log(`Ignoring message: ${message.content}`);
    return;
  }

  const classification = classificationOrUndefined;
  const splitIntoFour = classification === 'MIDJOURNEY_GRID';

  if (message.attachments.size === 1) {
    const attachment = message.attachments.at(0)!;
    const downloadUrl = attachment.url;
    const fileName = attachment.name || 'unknown';
    console.log(`Downloading image: ${fileName}`);
    const sharpImages = await axios.get(downloadUrl, { responseType: 'arraybuffer' }).then(async (response: any) => {
      const image = sharp(response.data);
      const metadata = await image.metadata();
      if (splitIntoFour) {
        return [
          image.clone().extract({
            left: 0,
            top: 0,
            width: metadata.width! / 2,
            height: metadata.height! / 2,
          }),
          image.clone().extract({
            left: metadata.width! / 2,
            top: 0,
            width: metadata.width! / 2,
            height: metadata.height! / 2,
          }),
          image.clone().extract({
            left: 0,
            top: metadata.height! / 2,
            width: metadata.width! / 2,
            height: metadata.height! / 2,
          }),
          image.clone().extract({
            left: metadata.width! / 2,
            top: metadata.height! / 2,
            width: metadata.width! / 2,
            height: metadata.height! / 2,
          }),
        ];
      } else {
        return [image];
      }
    });

    const requestIndex = waitingRequests.findIndex(
      (r) => r.resultClassification === classification && matchMidJourneyPromptIgnoringURLs(r.prompt, message.content),
    );

    const request = requestIndex >= 0 ? waitingRequests[requestIndex] : undefined;

    waitingRequests.splice(requestIndex, 1);

    if (request) {
      request.resolve(message, sharpImages);
    } else {
      console.log(`ERROR No request found for message: ${message.content}`);
      console.log('REQUESTS:', waitingRequests.map((r) => r.prompt).join(`\n`));
    }
  }
}

function matchMidJourneyPromptIgnoringURLs(_input: string, _match: string) {
  const input = _input.toLowerCase().replace(/(<?https?:\/\/[^\s]+>?)/g, '<URL>');
  const match = _match.toLowerCase().replace(/(<?https?:\/\/[^\s]+>?)/g, '<URL>');

  return match.includes(input);
}

const client = new DiscordJS.Client({
  intents: [DiscordJS.GatewayIntentBits.GuildMessages, DiscordJS.GatewayIntentBits.Guilds, DiscordJS.GatewayIntentBits.MessageContent],
});

export async function processHistory() {
  const channel = client.channels.cache.get(env.DISCORD_BOT_CHANNEL_ID!) as DiscordJS.TextChannel;
  const messages = await fetchAllMessages(channel);
  console.log('MESSAGES:', messages.length);
  for (const message of messages) {
    processMidJourneyMessage(message, true);
  }
}

export function getTasks(): BackgroundWorkerTask[] {
  return waitingRequests.map((p) => {
    return {
      id: p.id,
      name: p.prompt,
      status: 'Waiting ...',
    };
  });
}

let isDiscordWatcherStarted = false;

export function startDiscordResultsMonitor() {
  if (isDiscordWatcherStarted) return;
  isDiscordWatcherStarted = true;

  client.on('messageCreate', (message: DiscordJS.Message) => processMidJourneyMessage(message));

  client.on('ready', async () => {
    console.log(`Logged in as ${client.user!.tag}!`);

    await client.channels.fetch(env.DISCORD_BOT_CHANNEL_ID!);
  });

  client.on('error', (error: any) => {
    console.error('ERROR:', error);
  });

  client.login(env.DISCORD_BOT_TOKEN);
}

export function stopDiscordResultsMonitor() {
  client.destroy();
}
