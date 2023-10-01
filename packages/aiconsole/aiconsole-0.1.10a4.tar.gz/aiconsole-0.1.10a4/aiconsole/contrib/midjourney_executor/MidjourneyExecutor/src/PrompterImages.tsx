'use client';

import { documentId, limit, onSnapshot, orderBy, query, startAfter } from 'firebase/firestore';
import { useEffect, useState } from 'react';

import { type Illustration } from '@/src/aiconsole/modules/MidjourneyExecutor/src/Illustration';

import { ImageCard } from './ImageCard';
import { getImagesCollection } from './firebaseClient';
import { useTemporalilyUsed } from '../../Workspace/src/useTemporalilyUsed';

export function PrompterImages({}: {}) {
  const [images, setImages] = useState<Illustration[]>([]);

  const [loadMoreUsed, markLoadMoreUsed] = useTemporalilyUsed();

  const loadMoreImages = () => {
    markLoadMoreUsed();

    const q = query(
      getImagesCollection(),
      orderBy('createdAt', 'desc'),
      orderBy(documentId(), 'desc'),
      ...(images.length > 0 ? [startAfter(images[images.length - 1].createdAt, images[images.length - 1].id)] : []),
      limit(10),
    );

    const unsubscribe = onSnapshot(q, (newImages) => {
      newImages.docChanges().forEach((change) => {
        const imgData = change.doc.data();
        if (change.type === 'added') {
          setImages((prevImages) => {
            const allData = [...prevImages, imgData];
            const uniqueData = allData.filter((value, index, self) => self.findIndex((v) => v.id === value.id) === index);
            uniqueData.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
            return uniqueData;
          });
        } else if (change.type === 'removed') {
          setImages((prevImages) => prevImages.filter((img) => img.id !== imgData.id));
        } else if (change.type === 'modified') {
          setImages((prevImages) => prevImages.map((img) => (img.id === imgData.id ? imgData : img)));
        }
      });
    });

    return () => {
      unsubscribe();
    };
  };

  useEffect(() => {
    loadMoreImages();
  }, []);

  return (
    <>
      <div className="mb-4 grid grid-cols-3 gap-4">
        <div className="flex flex-col gap-4">
          {images
            .filter((image, index) => index % 3 === 0)
            .map((image) => (
              <ImageCard key={image.id} image={image} />
            ))}
        </div>
        <div className="flex flex-col gap-4">
          {images
            .filter((image, index) => index % 3 === 1)
            .map((image) => (
              <ImageCard key={image.id} image={image} />
            ))}
        </div>
        <div className="flex flex-col gap-4">
          {images
            .filter((image, index) => index % 3 === 2)
            .map((image) => (
              <ImageCard key={image.id} image={image} />
            ))}
        </div>
      </div>
      {!loadMoreUsed && (
        <span onClick={loadMoreImages} className="block cursor-pointer content-center text-center  text-blue-500  hover:text-blue-700">
          Load more ...
        </span>
      )}
    </>
  );
}
