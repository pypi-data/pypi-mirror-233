import { type Message } from 'discord.js';
import { type Sharp } from 'sharp';

import { type MidJourneyImageType } from '../MidJourneyImageType';

type RequestWithCallback = {
  id: string;
  resultClassification: MidJourneyImageType;
  prompt: string;

  resolve: (message: Message<boolean>, images: Sharp[]) => void;
  reject: (reason: any) => void;
};

export const waitingRequests: RequestWithCallback[] = [];
