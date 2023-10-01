import { collection, type FirestoreDataConverter, query, QueryConstraint } from 'firebase/firestore';
import { Illustration } from './Illustration';
import { useCollectionData } from 'react-firebase-hooks/firestore';
import { db } from './firebaseClient';


export function useIllustrations(...queryConstraints: QueryConstraint[]): { data?: Illustration[]; loading: boolean; error?: any; snapshot?: any; } {
  let q = query(collection(db, `illustrations`), ...queryConstraints).withConverter(Illustration.CONVERTER as FirestoreDataConverter<Illustration>);

  const [data, loading, error, snapshot] = useCollectionData(q);

  return { data, loading, error, snapshot };
}
