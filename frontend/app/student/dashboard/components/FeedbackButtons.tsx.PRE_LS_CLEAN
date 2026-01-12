'use client';

import { useState } from 'react';

interface FeedbackButtonsProps {
  componentType: 'motor_analysis' | 'action_card' | 'critical_alert' | 'goal_card' | 'projection_card';
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
  onSuccess
}: FeedbackButtonsProps) {
  const [feedback, setFeedback] = useState<'like' | 'dislike' | number | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showComment, setShowComment] = useState(false);
  const [comment, setComment] = useState('');

  const submitFeedback = async (type: 'like' | 'dislike' | 'rating', rating?: number) => {
    try {
      setIsSubmitting(true);

      const userStr = localStorage.getItem('user');

      if (!userStr) {
        alert('Giriş yapmanız gerekiyor');
        return;
      }

      const user = JSON.parse(userStr);

      const response = await fetch('http://localhost:8000/api/v1/feedback/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          student_id: user.id,
          component_type: componentType,
          component_id: componentId,
          feedback_type: type,
          rating: rating,
          comment: comment || null,
          metadata: metadata,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Feedback gönderilemedi');
      }

      const data = await response.json();

      if (type === 'rating') {
        setFeedback(rating!);
      } else {
        setFeedback(type);
      }

      setShowComment(false);
      setComment('');

      if (data.message) {
        console.log(data.message);
      }

      if (onSuccess) {
        onSuccess();
      }

    } catch (error: any) {
      console.error('Feedback error:', error);
      alert(error.message || 'Geri bildirim gönderilemedi');
    } finally {
      setIsSubmitting(false);
    }
  };

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
      case 5: return 'Mükemmel!';
      case 4: return 'Çok iyi';
      case 3: return 'İyi';
      case 2: return 'Vasat';
      case 1: return 'Kötü';
      default: return '';
    }
  };

  // LIKE/DISLIKE VARIANT
  if (variant === 'like-dislike') {
    return (
      <div className="flex flex-col items-center gap-2">
        {/* Açıklama */}
        <p className="text-xs text-white-600 font-medium">Bu analiz size faydalı oldu mu?</p>
        
        <div className="flex items-center gap-2 bg-gray-50 rounded-lg p-1">
          {/* Like Button */}
          <button
            onClick={() => submitFeedback('like')}
            disabled={isSubmitting || feedback === 'like'}
            className={`${sizeClasses[size]} rounded-lg font-semibold transition-all flex items-center gap-1 ${
              feedback === 'like'
                ? 'bg-green-500 text-white'
                : 'bg-white text-gray-700 hover:bg-green-50 hover:text-green-600'
            } ${isSubmitting ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          >
            <span className={iconSizes[size]}>👍</span>
            <span>Faydalı</span>
          </button>

          {/* Dislike Button */}
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
            } ${isSubmitting ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          >
            <span className={iconSizes[size]}>👎</span>
            <span>Faydalı değil</span>
          </button>
        </div>

        {/* Comment Modal (Dislike için) */}
        {showComment && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl p-6 max-w-md w-full">
              <h3 className="text-lg font-bold text-gray-800 mb-3">
                Neden faydalı bulmadınız?
              </h3>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Lütfen bize bildirin ki geliştirelim... (opsiyonel)"
                className="w-full border border-gray-300 rounded-lg p-3 text-sm text-gray-900 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
                rows={4}
                maxLength={500}
              />
              <div className="flex gap-3 mt-4">
                <button
                  onClick={() => {
                    setShowComment(false);
                    setComment('');
                  }}
                  className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition"
                >
                  İptal
                </button>
                <button
                  onClick={() => submitFeedback('dislike')}
                  disabled={isSubmitting}
                  className="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition disabled:opacity-50"
                >
                  {isSubmitting ? 'Gönderiliyor...' : 'Gönder'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // RATING VARIANT (1-5 Stars)
  return (
    <div className="flex flex-col items-center gap-2">
      {/* Açıklama */}
      <p className="text-xs text-gray-600 font-medium">Bu aksiyon ne kadar işe yaradı?</p>
      
      <div className="flex items-center gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={() => submitFeedback('rating', star)}
            disabled={isSubmitting}
            className={`transition-all ${
              isSubmitting ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:scale-110'
            }`}
          >
            <span
              className={`${iconSizes[size]} ${
                feedback && star <= Number(feedback)
                  ? 'text-yellow-400'
                  : 'text-gray-300 hover:text-yellow-200'
              }`}
            >
              ⭐
            </span>
          </button>
        ))}
      </div>
      
      {/* Rating açıklaması */}
      {feedback && typeof feedback === 'number' ? (
        <span className="text-xs text-gray-600 font-semibold">
          {feedback}/5 - {getRatingText(feedback)}
        </span>
      ) : (
        <span className="text-xs text-gray-500">
          1: Kötü • 3: İyi • 5: Mükemmel
        </span>
      )}
    </div>
  );
}