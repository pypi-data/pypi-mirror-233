import axios from 'axios';
import { writeFileSync } from 'fs';
import path from 'path';

import { type Deck } from '../../../../../backend/types/Deck';
import { onlyUnique } from '../../../../../shared/utils';
import { processMidJourneyPayload } from './processMidJourneyPayload';
import { FeatureType } from '@/src/shared/models';
import { sanitizePrompt } from './sanitizePrompt';

export async function downloadLocal(downloadURL: string, localPath: string) {
  console.log(`Downloading ${downloadURL}`);
  const response = await axios.get(downloadURL, { responseType: 'arraybuffer' });
  const buffer = Buffer.from(response.data, 'binary');
  console.log(`Writing ${localPath}`);
  writeFileSync(localPath, buffer);
}

export async function renderMidjourneyProfile(deck: Deck, deckDir: string) {
  if (deck.draft.portraitURL) {
    console.log(`Downloading ${deck.draft.portraitURL}`);

    await downloadLocal(deck.draft.portraitURL, path.resolve(deckDir, 'portrait.png'));

    return;
  }

  const portraitPath = path.resolve(deckDir, 'portrait.png');

  console.log(`${'renderMidjourneyProfile'} ...`);

  const simpleTypes = [FeatureType.SEX, FeatureType.CHARACTER, FeatureType.CLASS, FeatureType.RACE];

  const simpleTitleParts: string[] = simpleTypes.flatMap((t) => deck.getFeatures(t)).map((f) => f.artBeat);

  const expression = ['smiling grinning', 'smiling grinning', 'smiling grinning', 'smiling grinning', 'smiling grinning', '', '', 'shouting'];
  const npcExpression = ['evil', 'evil laughing', 'evil', 'evil shouting', '', '', 'shouting'];

  const possibleExpressions = deck.isNPC ? npcExpression : expression;

  const prompt = [
    `portrait of a antorpomorphic ${possibleExpressions[deck.draft.seed % possibleExpressions.length]}  ${simpleTitleParts.join(
      ' ',
    )} in an epic fantasy medieval setting`,
    deck.draft.title,
    ...deck.features
      .filter((f) => !simpleTypes.includes(f.featureType))
      .filter((f) => f.artBeat.length > 0)
      .map((f) => f.artBeat)
      .filter(onlyUnique),
    `funny, cinematic, pixar, disney, game illustration, concept art, trending on pixlr, artstation, cover art`,
    `--ar 2:3 --no text, font, caption, frame, darkest, person --seed ${deck.draft.seed}`,
  ]
    .map((s) => s.trim())
    .filter((s) => s.length > 0)
    .join(', ');

  const { message } = await processMidJourneyPayload({
    type: 'IMAGINE',
    prompt: sanitizePrompt(prompt),
  });

  if (message == null) throw new Error('No message');

  const upscaled = await processMidJourneyPayload({
    type: 'UPSCALE',
    messageURL: message.url,
    gridIndex: 0,
    prompt: sanitizePrompt(prompt),
  });

  if (upscaled && upscaled.images.length > 0) {
    await upscaled.images[0].toFile(portraitPath);
  } else {
    // Retry
    await renderMidjourneyProfile(deck, deckDir);
  }
}
