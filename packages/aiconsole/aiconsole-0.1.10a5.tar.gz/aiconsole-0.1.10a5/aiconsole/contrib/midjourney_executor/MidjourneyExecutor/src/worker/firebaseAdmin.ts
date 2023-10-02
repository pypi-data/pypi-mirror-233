import { type FirestoreDataConverter } from 'firebase-admin/firestore';

import { Illustration } from '../Illustration';
import { type IllustrationSource } from '../IllustrationSource';
import { MidJourneyRequest } from '../MidJourneyRequest';
import { db } from '@/src/backend/firebaseAdmin';

export function getAllRequestsCollection() {
  return db.collectionGroup('illustrationRequests').withConverter(MidJourneyRequest.CONVERTER);
}

export function getAllImagesCollection() {
  return db.collectionGroup('illustrations').withConverter(Illustration.CONVERTER);
}

export function getRequestsCollection() {
  return db.collection(`/illustrationRequests`).withConverter(MidJourneyRequest.CONVERTER as FirestoreDataConverter<MidJourneyRequest>);
}

export function getImagesCollection() {
  return db.collection(`/illustrations`).withConverter(Illustration.CONVERTER as FirestoreDataConverter<Illustration>);
}

export async function getImage(imageId: string) {
  const image = await getImagesCollection().doc(imageId).get();

  if (!image.exists) throw new Error(`Image ${imageId} does not exist`);

  return image.data()!;
}

export function getImageDocRef(image: Illustration) {
  return db.doc(`/illustrations/${image.id}`).withConverter(Illustration.CONVERTER as FirestoreDataConverter<Illustration>);
}

export function saveNewImage(id: string, requestId: string, url: string, source: IllustrationSource, width: number, height: number, note: string) {
  return getImagesCollection()
    .doc(id)
    .set(
      new Illustration({
        id,
        requestId,
        url,
        width,
        height,
        source,
        note,
        time: new Date(),
      }),
    );
}
