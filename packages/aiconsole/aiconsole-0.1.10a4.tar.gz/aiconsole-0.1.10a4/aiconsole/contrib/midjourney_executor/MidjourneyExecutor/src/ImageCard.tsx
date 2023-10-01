'use client';

import { addDoc } from 'firebase/firestore';
import { useSession } from 'next-auth/react';
import Image from 'next/image';

import { cn } from '@/app/utils';
import { changeImageRating, deleteImage, getRequestsCollection } from '@/src/aiconsole/modules/MidjourneyExecutor/src/firebaseClient';
import { type Illustration } from '@/src/aiconsole/modules/MidjourneyExecutor/src/Illustration';

import { ArrowPathIcon, HandThumbDownIcon, HandThumbUpIcon } from '@heroicons/react/24/solid';
import { ArrowUpIcon, CheckIcon, TrashIcon } from '@radix-ui/react-icons';
import { MidJourneyUpscaleRequest, MidJourneyVariationsRequest } from './MidJourneyRequest';
import { useTemporalilyUsed } from '../../Workspace/src/useTemporalilyUsed';
import { RatingComponent } from './RatingComponent';

function mapType(type: Illustration['source']['type']) {
  switch (type) {
    case 'USER':
      return 'User';
    case 'MIDJOURNEY_UPSCALE':
      return 'Upscaled';
    default:
      return '';
  }
}

export function IllustrationDetailsModal({ image }: { image: Illustration }) {
  return (
    <>
      <input type="checkbox" id={`my-modal-${image.id}`} className="modal-toggle" />
      <label htmlFor={`my-modal-${image.id}`} className="modal cursor-pointer">
        <div className="modal-box w-11/12 max-w-5xl">
          <div className="flex flex-col gap-2">
            <Image alt="Generated image" src={image.url} width={image.width / 2} height={image.height / 2} className="w-full" />

            <p>{image.source.type !== 'USER' ? image.source.prompt : 'USER'}</p>

            {image.source.type !== 'USER' && image.source.sourceMessageURL && (
              <a className="btn-xs btn" href={image.source.sourceMessageURL}>
                Visit source
              </a>
            )}

            <a className="btn-xs btn" href={image.url}>
              View original ({image.source.type})
            </a>

            <button className="btn-xs btn" onClick={() => deleteImage(image)} type="button">
              Delete
            </button>
          </div>
          <label htmlFor={`my-modal-${image.id}`} className="btn-sm btn-circle btn absolute right-2 top-2">
            ✕
          </label>
        </div>
      </label>
    </>
  );
}

export function ImageCard({ image }: { image: Illustration }) {
  const session = useSession().data;

  const [justDidVariations, markJustUsedVariations] = useTemporalilyUsed();
  const [justDidUpscale, markJustDidUpscale] = useTemporalilyUsed();

  return (
    <div key={image.id} className={cn('aspect-w-5 aspect-h-4')}>
      <IllustrationDetailsModal image={image} />
      <label htmlFor={`my-modal-${image.id}`}>
        <div className="group relative h-full w-full cursor-pointer overflow-hidden rounded-xl bg-gray-700 object-cover transition">
          <div className="pt-30 absolute inset-x-0 z-10 flex h-full w-full items-end rounded-xl bg-gradient-to-t from-black/80 to-transparent text-white opacity-0 duration-300 ease-in-out group-hover:opacity-100">
            <div className="absolute right-2 top-2 flex flex-row gap-1">
              <RatingComponent image={image} />
              {image.source.type !== 'USER' && image.source.type === 'MIDJOURNEY_GRID' && image.source.sourceMessageURL && (
                <button
                  className={cn('btn-square btn-sm btn cursor-pointer p-1')}
                  onClick={(e) => {
                    if (image.source.type === 'USER') return;

                    markJustDidUpscale();

                    addDoc(
                      getRequestsCollection(),
                      new MidJourneyUpscaleRequest({
                        user: session?.user?.id ? session.user.id : '',
                        messageURL: image.source.sourceMessageURL,
                        gridIndex: image.source.gridIndex,
                        prompt: image.source.prompt,
                      }),
                    );

                    e.preventDefault();
                  }}
                  type="button"
                >
                  {justDidUpscale ? <CheckIcon className="text-info h-6 w-6" /> : <ArrowUpIcon className={cn('h-6 w-6')} />}
                </button>
              )}
              {image.source.type !== 'USER' && image.source.sourceMessageURL && (
                <button
                  className={cn('btn-square btn-sm btn cursor-pointer p-1')}
                  onClick={() => {
                    if (image.source.type === 'USER' || justDidVariations) return;

                    markJustUsedVariations();

                    addDoc(
                      getRequestsCollection(),
                      new MidJourneyVariationsRequest({
                        user: session?.user?.id ? session.user.id : '',
                        messageURL: image.source.sourceMessageURL,
                        variationSourceUpscaledOrIndex: image.source.type === 'MIDJOURNEY_UPSCALE' ? 'UPSCALED' : image.source.gridIndex,
                        prompt: image.source.prompt,
                      }),
                    );
                  }}
                  type="button"
                >
                  <ArrowPathIcon className={cn('h-6 w-6', { 'text-info animate-spin': justDidVariations })} />
                </button>
              )}
              <button
                className={cn('btn-square btn-sm btn cursor-pointer p-1')}
                onClick={() => {
                  if (confirm('Are you sure you want to delete this image?')) deleteImage(image);
                }}
                type="button"
              >
                <TrashIcon className="h-6 w-6" />
              </button>
            </div>
          </div>

          <div className="pt-30 bg-base absolute bottom-2 left-2 z-10 bg-opacity-60  px-2 py-1 opacity-0 duration-300 ease-in-out group-hover:opacity-100">
            {mapType(image.source.type)}
          </div>

          <div className="h-full w-full">
            <Image
              alt="Generated image"
              src={image.url}
              width={500}
              height={400}
              className="h-full w-full object-cover transition duration-300 ease-in-out group-hover:scale-110"
            ></Image>
          </div>
        </div>
      </label>
    </div>
  );
}
