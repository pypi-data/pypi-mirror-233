import { type SimpleRequestForDesktopWorker } from '../../../../shared/Workable';
import { ImaginePayload, UpscalePayload, VariationsPayload } from './ImaginePayload';

export type MidJourneyRequestType = 'UPSCALE' | 'VARIATIONS' | 'IMAGINE';

export abstract class MidJourneyRequest implements SimpleRequestForDesktopWorker {
  public abstract type: MidJourneyRequestType;

  public id: string;
  public userID: string;

  public prompt: string;

  public createdAt: Date;

  public note: string;
  public acquiredByWorker: string;

  constructor({
    id = '',
    note = '',
    user,
    prompt,
    time = new Date(),
    acquiredByWorker = '',
  }: {
    id?: string;
    note?: string;
    user: string;
    prompt: string;
    time?: Date;
    acquiredByWorker?: string;
  }) {
    this.id = id;
    this.note = note;
    this.userID = user;
    this.prompt = prompt;
    this.createdAt = time;
    this.acquiredByWorker = acquiredByWorker;
  }

  static readonly CONVERTER = {
    toFirestore: (request: MidJourneyRequest) => {
      const { id, ...data } = request;

      return {
        ...data,
      };
    },

    fromFirestore: (snapshot: any): MidJourneyRequest => {
      const { ...data } = snapshot.data();
      const type: 'IMAGINE' | 'UPSCALE' | 'VARIATIONS' = data.type;

      return new TYPE_TO_REQUEST_CLASS_MAPPING[type]({
        ...data,
        id: snapshot.id,
      });
    },
  };
}

export class MidJourneyImagineRequest extends MidJourneyRequest implements ImaginePayload {
  public type = 'IMAGINE' as const;

  constructor({ ...rest }: {} & ConstructorParameters<typeof MidJourneyRequest>[0]) {
    super({ ...rest });
  }
}

export class MidJourneyUpscaleRequest extends MidJourneyRequest implements UpscalePayload {
  public type = 'UPSCALE' as const;
  public messageURL: string;
  public gridIndex: number;

  constructor({
    messageURL,
    gridIndex,
    ...rest
  }: {
    messageURL: string;
    gridIndex: number;
  } & ConstructorParameters<typeof MidJourneyRequest>[0]) {
    super({ ...rest });
    this.messageURL = messageURL;
    this.gridIndex = gridIndex;
  }
}

export class MidJourneyVariationsRequest extends MidJourneyRequest implements VariationsPayload {
  public type = 'VARIATIONS' as const;
  public messageURL: string;
  public variationSourceUpscaledOrIndex: number | 'UPSCALED';

  constructor({
    messageURL,
    variationSourceUpscaledOrIndex,
    ...rest
  }: {
    messageURL: string;
    variationSourceUpscaledOrIndex: number | 'UPSCALED';
  } & ConstructorParameters<typeof MidJourneyRequest>[0]) {
    super({ ...rest });
    this.messageURL = messageURL;
    this.variationSourceUpscaledOrIndex = variationSourceUpscaledOrIndex;
  }
}

export const TYPE_TO_REQUEST_CLASS_MAPPING = {
  IMAGINE: MidJourneyImagineRequest,
  UPSCALE: MidJourneyUpscaleRequest,
  VARIATIONS: MidJourneyVariationsRequest,
};
