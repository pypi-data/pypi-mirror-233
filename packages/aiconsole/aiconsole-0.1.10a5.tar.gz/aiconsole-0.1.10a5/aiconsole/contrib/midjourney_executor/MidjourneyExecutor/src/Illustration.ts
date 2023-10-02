import { IllustrationSource } from './IllustrationSource';

export class Illustration {
  public id: string;
  public requestId: string; //empty if there was no request
  public url: string;
  public rating: number; // Scale -2 to 2

  public source: IllustrationSource;

  public width: number;
  public height: number;

  public note: string;
  public createdAt: Date;

  constructor({
    id,
    requestId,
    url,
    rating = 0,
    source,
    width,
    height,
    note,
    time,
  }: {
    id: string;
    requestId?: string;
    url: string;
    rating?: number;
    source: IllustrationSource;
    width: number;
    height: number;
    note: string;
    time: Date;
  }) {
    this.id = id;
    this.requestId = requestId || '';
    this.url = url;
    this.rating = rating;
    this.source = source;
    this.width = width;
    this.height = height;
    this.note = note;
    this.createdAt = time;
  }

  static readonly CONVERTER = {
    toFirestore: (image: Illustration) => {
      const { id, ...data } = image;
      return {
        ...data,
      };
    },

    fromFirestore: (snapshot: any): Illustration => {
      const data = snapshot.data();

      return new Illustration({
        ...data,
        id: snapshot.id,
        time: data.createdAt.toDate(),
        rating: data.rating != null ? data.rating : 0,
      });
    },
  };
}
