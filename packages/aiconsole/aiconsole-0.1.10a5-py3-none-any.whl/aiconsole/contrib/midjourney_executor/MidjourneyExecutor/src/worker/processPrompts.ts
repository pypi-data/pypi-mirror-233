import { randomUUID } from 'crypto';

import { getAllRequestsCollection, saveNewImage } from '@/src/aiconsole/modules/MidjourneyExecutor/src/worker/firebaseAdmin';
import { IllustrationSource } from '../IllustrationSource';
import { type MidJourneyImageType } from '../MidJourneyImageType';
import { type MidJourneyRequest } from '@/src/aiconsole/modules/MidjourneyExecutor/src/MidJourneyRequest';
import { type RequestPayload } from '../ImaginePayload';

import { DocumentProcessor } from '../../../../../worker/DocumentProcessor';
import { uploadStream } from '../../../../../worker/fileStorage';
import { processMidJourneyPayload } from './processMidJourneyPayload';

const MAX_PROMPTS_TO_PROCESS_AT_ONCE = 6;

export const promptProcessor = new DocumentProcessor<MidJourneyRequest>({
  hasNeedsWork: false,
  maxToProcessAtOnce: MAX_PROMPTS_TO_PROCESS_AT_ONCE,
  baseCollectionQuery: getAllRequestsCollection(),
  processFunc: async (acquiredRequest) => {
    console.log(`Processing prompt ${acquiredRequest.id} ...`);

    const request = acquiredRequest.data()!;

    const { message, images } = await processMidJourneyPayload(request as RequestPayload & { prompt: string });

    if (!message) throw new Error('No message returned from midjourney');

    let type: MidJourneyImageType;
    switch (request.type) {
      case 'UPSCALE':
        type = 'MIDJOURNEY_UPSCALE';
        break;
      case 'VARIATIONS':
        type = 'MIDJOURNEY_GRID';
        break;
      case 'IMAGINE':
        type = 'MIDJOURNEY_GRID';
        break;
    }

    for (let imageIndex = 0; imageIndex < images.length; imageIndex++) {
      const image = images[imageIndex];
      const uuid = randomUUID();
      const width = await image.metadata().then((metadata) => metadata.width!);
      const height = await image.metadata().then((metadata) => metadata.height!);
      const url = await uploadStream(image, `illustrations/${uuid}.png`);
      const source: IllustrationSource = {
        type,
        gridIndex: imageIndex,
        prompt: request.prompt,
        sourceMessageURL: message.url,
      };
      await saveNewImage(uuid, request.id, url, source, width, height, request.note);
    }
  },
});
