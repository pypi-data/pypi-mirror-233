import { type Message } from 'discord.js';
import { type Sharp } from 'sharp';
import crypto from 'crypto';

import { type MidJourneyImageType } from '../MidJourneyImageType';
import { type MidJourneyRequestType } from '../MidJourneyRequest';
import { type RequestPayload } from '../ImaginePayload';
import { shouldNeverGetHere } from '../../../../../shared/tsutils';
import { DiscordInput } from './DiscordInput';
import { waitingRequests } from './waitingRequests';

const discordInput = new DiscordInput();

function typeToResultClassification(type: MidJourneyRequestType): MidJourneyImageType {
  switch (type) {
    case 'UPSCALE':
      return 'MIDJOURNEY_UPSCALE';
    case 'IMAGINE':
      return 'MIDJOURNEY_GRID';
    case 'VARIATIONS':
      return 'MIDJOURNEY_GRID';
    default:
      shouldNeverGetHere(type);
  }
}

export async function processMidJourneyPayload(payload: RequestPayload & { prompt: string }) {
  const imagePromise = new Promise<{ message: Message<boolean>; images: Sharp[] }>(
    // eslint-disable-next-line no-async-promise-executor
    async (resolve, reject) => {
      waitingRequests.push({
        id: crypto.randomUUID(),
        resultClassification: typeToResultClassification(payload.type),
        prompt: payload.prompt,
        reject: () => reject(new Error('reject')),
        resolve: (message: Message<boolean>, images: Sharp[]) => resolve({ message, images }),
      });

      switch (payload.type) {
        case 'UPSCALE': {
          console.log(`UPSCALE`);
          await discordInput.pressImageButton(payload.messageURL, `U${payload.gridIndex + 1}`);
          break;
        }
        case 'VARIATIONS': {
          console.log(`VARIATIONS`);
          if (payload.variationSourceUpscaledOrIndex === 'UPSCALED') {
            await discordInput.pressImageButton(payload.messageURL, 'Make Variations');
          } else {
            await discordInput.pressImageButton(payload.messageURL, `V${payload.variationSourceUpscaledOrIndex + 1}`);
          }
          break;
        }
        case 'IMAGINE': {
          console.log(`IMAGINE ${payload.prompt}`);
          await discordInput.sendPrompt(payload.prompt);
        }
      }
    },
  );

  try {
    return await imagePromise;
  } catch (e) {
    console.error(e);
    return {
      message: undefined,
      images: [] as Sharp[],
    };
  }
}
