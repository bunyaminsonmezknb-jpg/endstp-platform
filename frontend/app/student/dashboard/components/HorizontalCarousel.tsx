'use client';

import { ReactNode, useState } from 'react';

interface HorizontalCarouselProps {
  children: ReactNode[];
  itemsPerView?: number; // desktop
}

export default function HorizontalCarousel({
  children,
  itemsPerView = 3,
}: HorizontalCarouselProps) {
  const [index, setIndex] = useState(0);

  const maxIndex = Math.max(0, children.length - itemsPerView);

  const prev = () => setIndex(i => Math.max(0, i - 1));
  const next = () => setIndex(i => Math.min(maxIndex, i + 1));

  return (
    <div className="relative">
      {/* SOL OK */}
      <button
        onClick={prev}
        disabled={index === 0}
        className="absolute -left-4 top-1/2 -translate-y-1/2 z-10
                   bg-white shadow rounded-full w-9 h-9
                   flex items-center justify-center
                   disabled:opacity-30"
      >
        ◀
      </button>

      {/* SAĞ OK */}
      <button
        onClick={next}
        disabled={index === maxIndex}
        className="absolute -right-4 top-1/2 -translate-y-1/2 z-10
                   bg-white shadow rounded-full w-9 h-9
                   flex items-center justify-center
                   disabled:opacity-30"
      >
        ▶
      </button>

      {/* VIEWPORT */}
      <div className="overflow-hidden">
        <div
          className="flex transition-transform duration-300"
          style={{
            transform: `translateX(-${index * (100 / itemsPerView)}%)`,
            width: `${(children.length * 100) / itemsPerView}%`,
          }}
        >
          {children.map((child, i) => (
            <div
              key={i}
              className="px-2"
              style={{ width: `${100 / children.length}%` }}
            >
              {child}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
