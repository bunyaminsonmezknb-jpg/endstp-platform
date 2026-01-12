'use client'

import { useState } from 'react'
import { useReflexNotifications } from '@/lib/hooks/useReflexNotifications'
import { ReflexNotificationCard } from './ReflexNotificationCard'
import { Bell, BellOff, ChevronDown, ChevronUp } from 'lucide-react'

interface ReflexNotificationContainerProps {
  studentId: string
}

export function ReflexNotificationContainer({
  studentId
}: ReflexNotificationContainerProps) {
  const { notifications, isSubscribed, dismissNotification } =
    useReflexNotifications(studentId)
  
  const [isOpen, setIsOpen] = useState(false)

  const handleActionClick = (action: string) => {
    console.log('Action clicked:', action)
    alert(`Aksiyon: ${action}\n\nBu özellik yakında eklenecek!`)
  }

  return (
    <div className="w-full mb-4">
      {/* Tıklanabilir Başlık */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`w-full flex items-center justify-between px-5 py-3 rounded-xl shadow-lg transition-all ${
          notifications.length > 0
            ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:shadow-xl'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        }`}
      >
        <div className="flex items-center gap-3">
          {isSubscribed ? (
            <>
              <Bell size={20} className={notifications.length > 0 ? 'animate-bounce' : ''} />
              <span className="font-semibold text-base">
                {notifications.length > 0 ? '🔔 Yeni Bildirimler' : '📭 Bildirimler'}
              </span>
              {notifications.length > 0 && (
                <span className="bg-white text-purple-600 text-sm font-bold px-3 py-1 rounded-full">
                  {notifications.length}
                </span>
              )}
            </>
          ) : (
            <>
              <BellOff size={20} />
              <span className="font-semibold">Bağlanıyor...</span>
            </>
          )}
        </div>
        
        <div className="flex items-center gap-2">
          <span className="text-sm opacity-90">
            {isOpen ? 'Gizle' : 'Göster'}
          </span>
          {isOpen ? (
            <ChevronUp size={20} />
          ) : (
            <ChevronDown size={20} />
          )}
        </div>
      </button>

      {/* Accordion İçeriği */}
      {isOpen && (
        <div className="mt-2 space-y-3 animate-slideIn">
          {notifications.length === 0 ? (
            <div className="bg-white rounded-xl p-6 text-center border-2 border-dashed border-gray-300">
              <div className="text-4xl mb-2">✅</div>
              <p className="text-gray-600 font-medium">Yeni bildirim yok</p>
              <p className="text-sm text-gray-500 mt-1">
                {isSubscribed ? 'Real-time bağlantı aktif' : 'Bağlantı kuruluyor...'}
              </p>
            </div>
          ) : (
            notifications.map((notification) => (
              <ReflexNotificationCard
                key={notification.id}
                notification={notification}
                onDismiss={() => dismissNotification(notification.id)}
                onActionClick={handleActionClick}
              />
            ))
          )}
        </div>
      )}
    </div>
  )
}
