'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'

export interface ReflexNotification {
  id: string
  title: string
  message: string
  action_items: Array<{
    action: string
    label: string
    duration_sec?: number
    count?: number
  }>
  priority: number
  created_at: string
}

export function useReflexNotifications(studentId: string) {
  const [notifications, setNotifications] = useState<ReflexNotification[]>([])
  const [isSubscribed, setIsSubscribed] = useState(false)

  useEffect(() => {
    if (!studentId) return

    // Subscribe to new events
    const channel = supabase
      .channel('reflex-events')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'ui_reflex_events',
          filter: `student_id=eq.${studentId}`
        },
        (payload) => {
          const newNotification = payload.new as ReflexNotification
          setNotifications(prev => [newNotification, ...prev])
          
          // Mark as delivered
          supabase
            .from('ui_reflex_events')
            .update({ delivered: true, delivered_at: new Date().toISOString() })
            .eq('id', newNotification.id)
            .then()
        }
      )
      .subscribe((status) => {
        if (status === 'SUBSCRIBED') {
          setIsSubscribed(true)
        }
      })

    // Fetch undelivered events on mount
    supabase
      .from('ui_reflex_events')
      .select('*')
      .eq('student_id', studentId)
      .eq('delivered', false)
      .order('created_at', { ascending: false })
      .then(({ data }) => {
        if (data) setNotifications(data as ReflexNotification[])
      })

    return () => {
      channel.unsubscribe()
      setIsSubscribed(false)
    }
  }, [studentId])

  const dismissNotification = async (id: string) => {
    // Mark as delivered
    await supabase
      .from('ui_reflex_events')
      .update({ delivered: true, delivered_at: new Date().toISOString() })
      .eq('id', id)
    
    setNotifications(prev => prev.filter(n => n.id !== id))
  }

  return {
    notifications,
    isSubscribed,
    dismissNotification
  }
}
