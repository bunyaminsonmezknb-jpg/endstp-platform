'use client';

import { useState } from 'react';
import { api } from '@/lib/api/client';

interface FeedbackButtonsProps {
  componentType:
    | 'motor_analysis'
    | 'action_card'
    | 'critical_alert'
    | 'goal_card'
    | 'projection_card';
  componentId?: string;
  metadata?: Record<string, any>;
  variant?: 'like-dislike' | 'rating';
  size?: 'sm' | 'md' | 'lg';
  onSuccess?: () => void;
}

export default function FeedbackButtons({
  componentType,
  componentId,
  metadata = {},
  variant = 'like-dislike',
  size = 'md',
  onSuccess,
}: FeedbackButtonsProps) {
  const [feedback, setFeedback] = useState<'like' | 'dislike' | number | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showComment, setShowComment] = useState(false);
  const [comment, setComment] = useState('');

  /* ======================
     SUBMIT
  ====================== */

  const submitFeedback = async (
    type: 'like' | 'dislike' | 'rating',
    rating?: number
  ) => {
    try {
      setIsSubmitting(true);

      /**
       * Auth:
       * api-client cookie/session bazlı çalışır
       * yetkisizse backend 401 döner
       */
      await api.post('/api/v1/feedback/submit', {
        component_type: componentType,
        component_id: componentId,
        feedback_type: type,
        rating: type === 'rating' ? rating : null,
        comment: comment || null,
        metadata,
      });

      setFeedback(type === 'rating' ? rating! : type);
      setShowComment(false);
      setComment('');

      onSuccess?.();
    } catch (err: any) {
      if (err?.status === 401) {
        alert('Giriş yapmanız gerekiyor');
        return;
      }

      console.error('Feedback error:', err);
      alert('Geri bildirim gönderilemedi');
    } finally {
      setIsSubmitting(false);
    }
  };

  /* ======================
     UI HELPERS
  ====================== */

  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1.5',
    lg: 'text-base px-4 py-2',
  };

  const iconSizes = {
    sm: 'text-base',
    md: 'text-lg',
    lg: 'text-xl',
  };

  const getRatingText = (rating: number) => {
    switch (rating) {
      case 5:
        return 'Mükemmel!';
      case 4:
        return 'Çok iyi';
      case 3:
        return 'İyi';
      case 2:
        return 'Vasat';
      case 1:
        return 'Kötü';
      default:
        return '';
    }
  };

  /* ======================
     LIKE / DISLIKE
  ====================== */

  if (variant === 'like-dislike') {
    return (
      <div className="flex flex-col items-center gap-2">
        <p className="text-xs text-white-600 font-medium">
          Bu analiz size faydalı oldu mu?
        </p>

        <div className="flex items-center gap-2 bg-gray-50 rounded-lg p-1">
          <button
            onClick={() => submitFeedback('like')}
            disabled={isSubmitting || feedback === 'like'}
            className={`${sizeClasses[size]} rounded-lg font-semibold transition-all flex items-center gap-1 ${
              feedback === 'like'
                ? 'bg-green-500 text-white'
                : 'bg-white text-gray-700 hover:bg-green-50 hover:text-green-600'
            } ${isSubmitting ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <span className={iconSizes[size]}>👍</span>
            <span>Faydalı</span>
          </button>

          <button
            onClick={() => {
              if (feedback !== 'dislike') {
                setShowComment(true);
              } else {
                submitFeedback('dislike');
              }
            }}
            disabled={isSubmitting}
            className={`${sizeClasses[size]} rounded-lg font-semibold transition-all flex items-center gap-1 ${
              feedback === 'dislike'
                ? 'bg-red-500 text-white'
                : 'bg-white text-gray-700 hover:bg-red-50 hover:text-red-600'
            } ${isSubmitting ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <span className={iconSizes[size]}>👎</span>
            <span>Faydalı değil</span>
          </button>
        </div>

        {showComment && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl p-6 max-w-md w-full">
              <h3 className="text-lg font-bold mb-3">
                Neden faydalı bulmadınız?
              </h3>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                className="w-full border rounded-lg p-3 text-sm"
                rows={4}
              />
              <div className="flex gap-3 mt-4">
                <button
                  onClick={() => {
                    setShowComment(false);
                    setComment('');
                  }}
                  className="flex-1 bg-gray-200 rounded-lg py-2"
                >
                  İptal
                </button>
                <button
                  onClick={() => submitFeedback('dislike')}
                  disabled={isSubmitting}
                  className="flex-1 bg-purple-600 text-white rounded-lg py-2"
                >
                  Gönder
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  /* ======================
     RATING
  ====================== */

  return (
    <div className="flex flex-col items-center gap-2">
      <p className="text-xs text-gray-600 font-medium">
        Bu aksiyon ne kadar işe yaradı?
      </p>

      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={() => submitFeedback('rating', star)}
            disabled={isSubmitting}
          >
            <span
              className={`${iconSizes[size]} ${
                feedback && star <= Number(feedback)
                  ? 'text-yellow-400'
                  : 'text-gray-300'
              }`}
            >
              ⭐
            </span>
          </button>
        ))}
      </div>

      {feedback && typeof feedback === 'number' && (
        <span className="text-xs text-gray-600 font-semibold">
          {feedback}/5 – {getRatingText(feedback)}
        </span>
      )}
    </div>
  );
}
