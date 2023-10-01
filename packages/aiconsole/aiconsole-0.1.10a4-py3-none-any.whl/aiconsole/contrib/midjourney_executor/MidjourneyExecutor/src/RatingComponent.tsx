import { type Illustration } from '@/src/aiconsole/modules/MidjourneyExecutor/src/Illustration';
import { changeImageRating } from './firebaseClient';
import { useState } from 'react';
import { EraserIcon } from '@radix-ui/react-icons';

interface RatingComponentProps {
  image: Illustration;
}

// Custom button component for displaying selected rating
const Button = ({ children, onClick }: { children: React.ReactNode; onClick?: (e: any) => void }) => (
  <button onClick={onClick} className={`btn-square btn-sm btn cursor-pointer p-1 hover:bg-gray-200 active:bg-gray-300`}>
    {children}
  </button>
);

export const RatingComponent = ({ image }: RatingComponentProps) => {
  const [expanded, setExpanded] = useState<boolean>(false);
  const [selectedRating, setSelectedRating] = useState<number | undefined>(image.rating);

  const toggleExpanded = () => setExpanded(!expanded);

  const selectRating = (rating: number) => {
    setSelectedRating(rating);
    setExpanded(false);
    changeImageRating(image, rating);
  };

  return (
    <div className="flex flex-row">
      <div className="relative flex-grow">
        <Button onClick={toggleExpanded}>{selectedRating != 0 ? selectedRating : '?'}</Button>
        {expanded && (
          <div className="bg-base-300 absolute -left-14   top-10 flex flex-row overflow-visible rounded-b-lg p-3 shadow-md">
            {[-2, -1, 0, 1, 2].map((rating) => (
              <div key={rating} className="flex-grow">
                <Button
                  onClick={(e: { preventDefault: () => void }) => {
                    selectRating(rating);
                    e.preventDefault();
                  }}
                >
                  {rating === 0 ? <EraserIcon className="h-6 w-6" /> : rating}
                </Button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
