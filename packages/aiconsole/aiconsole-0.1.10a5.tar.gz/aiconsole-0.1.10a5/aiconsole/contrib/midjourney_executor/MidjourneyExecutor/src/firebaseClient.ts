import { collection, deleteDoc, doc, type FirestoreDataConverter, getFirestore, updateDoc, addDoc, onSnapshot, query, where, setDoc } from 'firebase/firestore';
import { deleteObject, getDownloadURL, getStorage, ref, uploadBytes } from 'firebase/storage';

import { firebaseApp } from '@/app/lib/firebase';

import { Illustration } from './Illustration';
import { MidJourneyImagineRequest, MidJourneyRequest } from './MidJourneyRequest';
import { getSession } from 'next-auth/react';

export const db = getFirestore(firebaseApp);

export const REQUESTS_COLLECTION = collection(db, `/illustrationRequests`).withConverter(
  MidJourneyRequest.CONVERTER as FirestoreDataConverter<MidJourneyRequest>,
);
export const IMAGES_COLLECTION = collection(db, `/illustrations`).withConverter(Illustration.CONVERTER as FirestoreDataConverter<Illustration>);

export async function getPublicFileUrl(file: string) {
  const storage = getStorage();
  const url = await getDownloadURL(ref(storage, file));
  return url;
}

export function getRequestsCollection() {
  return collection(db, `/illustrationRequests`).withConverter(MidJourneyRequest.CONVERTER as FirestoreDataConverter<MidJourneyRequest>);
}

export function getImagesCollection() {
  return collection(db, `/illustrations`).withConverter(Illustration.CONVERTER as FirestoreDataConverter<Illustration>);
}

export function getRequestDocRef(request: MidJourneyRequest) {
  return doc(db, `/illustrationRequests/${request.id}`).withConverter(MidJourneyRequest.CONVERTER as FirestoreDataConverter<MidJourneyRequest>);
}

export function getImageDocRef(image: Illustration) {
  return doc(db, `/illustrations/${image.id}`).withConverter(Illustration.CONVERTER as FirestoreDataConverter<Illustration>);
}

export function resetRequest(request: MidJourneyRequest) {
  updateDoc(getRequestDocRef(request), {
    acquiredByWorker: '',
  });
}

export function deleteRequest(request: MidJourneyRequest) {
  deleteDoc(getRequestDocRef(request));
}

export async function changeImageRating(image: Illustration, rating?: number) {
  await updateDoc(getImageDocRef(image), {
    rating: (rating == undefined ? null : rating) as any,
  });
}

export async function deleteImage(image: Illustration) {
  const storage = getStorage();
  const storageRef = ref(storage, image.url);
  await deleteObject(storageRef);
  await deleteDoc(getImageDocRef(image));
}

export async function requestImage(prompt: string): Promise<Illustration[]> {
  let session = await getSession();

  let reqRef = await addDoc(
    getRequestsCollection(),
    new MidJourneyImagineRequest({
      user: session?.user?.id ? session.user.id : '',
      prompt,
    }),
  );

  //wait until there is an image with this request id
  let q = query(collection(db, `illustrations`), where('requestId', '==', reqRef.id)).withConverter(
    Illustration.CONVERTER as FirestoreDataConverter<Illustration>,
  );

  return new Promise((resolve, reject) => {
    let unsubscribe = onSnapshot(q, (snapshot) => {
      //replace the content of images with the new images
      let images = snapshot.docs.map((doc) => doc.data());

      if (images.length === 4) {
        unsubscribe();
        resolve(images);
      }

      if (images.length > 4) {
        console.error('Error: unexpected number of images returned from database', images);
        reject();
      }

      //TODO: Maybe some timeout?
    });
  });
}

export async function uploadOldMidjourneyImage(imageFile: File, promptUsedToGenerate: string): Promise<Illustration> {
  //TODO: this should probably happen on backend

  let id = crypto.randomUUID();

  let storage = getStorage();
  let path = `illustrations/${id}.png`;
  let storageRef = ref(storage, path);

  await uploadBytes(storageRef, imageFile);

  //get width and height from image
  let imageDimensions = await new Promise<{ width: number; height: number }>((resolve, reject) => {
    let img = new Image();
    img.onload = () => {
      resolve({ width: img.width, height: img.height });
    };
    img.onerror = reject;
    img.src = URL.createObjectURL(imageFile);
  });

  let illustration = new Illustration({
    id,
    width: imageDimensions.width,
    height: imageDimensions.height,
    url: await getDownloadURL(storageRef),
    requestId: '',
    source: {
      type: 'MIDJOURNEY_UPSCALE',
      prompt: promptUsedToGenerate,
      gridIndex: 0,
      sourceMessageURL: '',
    },
    note: '',
    time: new Date(),
  });

  await setDoc(doc(getImagesCollection(), id), illustration);

  return illustration;
}
