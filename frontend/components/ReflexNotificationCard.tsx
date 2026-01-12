'use client'

import { X } from 'lucide-react'
import { ReflexNotification } from '@/lib/hooks/useReflexNotifications'

interface ReflexNotificationCardProps {
  notification: ReflexNotification
  onDismiss: () => void
  onActionClick: (action: string) => void
}

export function ReflexNotificationCard({
  notification,
  onDismiss,
  onActionClick
}: ReflexNotificationCardProps) {
  const { title, message, action_items, priority } = notification

  // Priority-based styling
  const bgColor =
    priority >= 8
      ? 'bg-red-50 border-red-300'
      : priority >= 6
      ? 'bg-yellow-50 border-yellow-300'
      : 'bg-blue-50 border-blue-300'

  const iconColor =
    priority >= 8 ? 'text-red-600' : priority >= 6 ? 'text-yellow-600' : 'text-blue-600'

  return (
    <div className={`${bgColor} border-2 rounded-lg p-4 mb-3 relative animate-slideInRightRight`}>
      {/* Dismiss button */}
      <button
        onClick={onDismiss}
        className="absolute top-2 right-2 text-gray-500 hover:text-gray-700 transition-colors"
        aria-label="Dismiss notification"
      >
        <X size={18} />
      </button>

      {/* Title */}
      <h3 className={`font-bold text-lg ${iconColor} pr-6`}>{title}</h3>

      {/* Message */}
      <p className="text-sm text-gray-700 mt-2 leading-relaxed">{message}</p>

      {/* Action items */}
      {action_items && action_items.length > 0 && (
        <div className="mt-3 space-y-2">
          <p className="text-xs font-semibold text-gray-600">Önerilen Aksiyonlar:</p>
          {action_items.map((action, i) => (
            <button
              key={i}
              onClick={() => onActionClick(action.action)}
              className="w-full text-left px-3 py-2 bg-white border border-gray-300 rounded hover:bg-gray-50 hover:border-gray-400 transition-all text-sm"
            >
              {action.label}
              {action.duration_sec && ` (${action.duration_sec}s)`}
            </button>
          ))}
        </div>
      )}

      {/* Priority badge */}
      {priority >= 8 && (
        <div className="mt-2">
          <span className="inline-block px-2 py-1 text-xs font-semibold text-red-700 bg-red-100 rounded">
            YÜKSEK ÖNCELİK
          </span>
        </div>
      )}
    </div>
  )
}
