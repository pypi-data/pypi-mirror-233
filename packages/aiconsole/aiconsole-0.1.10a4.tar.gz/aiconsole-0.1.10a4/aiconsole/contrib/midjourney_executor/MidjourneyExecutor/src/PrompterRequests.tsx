'use client';

import { limit, orderBy, query } from 'firebase/firestore';
import { useCollectionData } from 'react-firebase-hooks/firestore';

import { deleteRequest, getRequestsCollection, resetRequest } from '@/src/aiconsole/modules/MidjourneyExecutor/src/firebaseClient';
import { type MidJourneyRequest } from '@/src/aiconsole/modules/MidjourneyExecutor/src/MidJourneyRequest';

export function PrompterRequests({}: {}) {
  const q = query(getRequestsCollection(), orderBy('createdAt', 'desc'), limit(30));
  const [requests, loading, error] = useCollectionData<MidJourneyRequest>(q);
  if (error) throw error;

  return (
    <div className="flex flex-wrap gap-4">
      {requests?.map((request) => (
        <div key={request.id}>
          <p>{request.type}</p>
          <p>{request.prompt}</p>

          {request.acquiredByWorker === '' && <p>Waiting to start</p>}

          {request.acquiredByWorker !== '' && (
            <div className="radial-progress inline-block animate-spin " style={{ '--value': '70', '--size': '1rem' } as any} />
          )}

          {request.acquiredByWorker !== '' && (
            <button className="btn-xs btn" onClick={() => resetRequest(request)} type="button">
              Reset
            </button>
          )}

          <button className="btn-xs btn" onClick={() => deleteRequest(request)} type="button">
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}
