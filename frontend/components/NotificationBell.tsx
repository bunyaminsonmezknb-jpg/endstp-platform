'use client'

import { useState, useRef, useEffect } from 'react'
import { Bell } from 'lucide-react'
import { useReflexNotifications } from '@/hooks/useReflexNotifications'
import { ReflexNotificationCard } from './ReflexNotificationCard'
import toast from 'react-hot-toast'

interface NotificationBellProps {
  studentId: string
}

export function NotificationBell({ studentId }: NotificationBellProps) {
  const { notifications, isSubscribed, dismissNotification } = useReflexNotifications(studentId)
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const prevCountRef = useRef(0)

  // Yeni bildirim geldiğinde toast göster
  useEffect(() => {
    if (notifications.length > prevCountRef.current && prevCountRef.current > 0) {
      const latest = notifications[0]
      if (latest && latest.priority >= 8) {
        toast.error(latest.title, {
          duration: 5000,
          icon: '🔔',
        })
      }
    }
    prevCountRef.current = notifications.length
  }, [notifications])

  // Click outside to close
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isOpen])

  const handleActionClick = (action: string) => {
    console.log('Action clicked:', action)
    setIsOpen(false)
    toast.success(`Aksiyon: ${action}`)
  }

  const unreadCount = notifications.length
  const displayCount = unreadCount > 9 ? '9+' : unreadCount

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Bell Icon Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 hover:bg-gray-100 rounded-full transition-colors"
        aria-label="Notifications"
      >
        <Bell 
          size={24} 
          className={unreadCount > 0 ? 'text-purple-600' : 'text-gray-600'}
        />
        
        {/* Professional Badge with White Border */}
        {unreadCount > 0 && (
          <span 
            className="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] font-bold rounded-full min-w-[20px] h-5 flex items-center justify-center px-1.5 animate-pulse"
            style={{
              border: '2px solid white',
              boxShadow: '0 2px 8px rgba(239, 68, 68, 0.4)'
            }}
          >
            {displayCount}
          </span>
        )}
      </button>

      {/* Dropdown Popover */}
      {isOpen && (
        <div className="absolute top-12 right-0 w-80 max-h-[500px] bg-white rounded-xl shadow-2xl border border-gray-200 z-50 overflow-hidden animate-slideIn">
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-4 py-3 flex items-center justify-between">
            <h3 className="font-semibold text-base">🔔 Bildirimler</h3>
            <span className="text-sm opacity-90">
              {isSubscribed ? 'Aktif' : 'Bağlanıyor...'}
            </span>
          </div>

          {/* Notifications List */}
          <div className="max-h-[400px] overflow-y-auto p-3 space-y-2">
            {notifications.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <div className="text-4xl mb-2">✅</div>
                <p className="text-sm font-medium">Yeni bildirim yok</p>
                <p className="text-xs mt-1 text-gray-400">
                  {isSubscribed ? 'Real-time bağlantı aktif' : 'Bağlanıyor...'}
                </p>
              </div>
            ) : (
              notifications.map((notification) => (
                <ReflexNotificationCard
                  key={notification.id}
                  notification={notification}
                  onDismiss={() => {
                    dismissNotification(notification.id)
                    toast.success('Bildirim kapatıldı', { icon: '✅' })
                  }}
                  onActionClick={handleActionClick}
                />
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}
