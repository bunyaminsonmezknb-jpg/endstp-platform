'use client';

import { useEffect, useMemo, useState } from 'react';
import { api } from '@/lib/api/client';
import FeedbackButtons from './FeedbackButtons';
import SideDrawer from './SideDrawer';

interface MotorAction {
  topic_name: string;
  subject_name?: string;
  urgency: 'critical' | 'high' | 'medium' | 'low';
  urgency_text: string;
  subtitle: string;
  action: string;
  days_since?: number;
  score?: number;
}

interface MotorData {
  name: string;
  icon: string;
  color: string;       // gradient class
  borderColor: string; // tailwind border class
  actions: MotorAction[];
}

export default function SmartActionCards() {
  const [motorsData, setMotorsData] = useState<MotorData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Drawer state
  const [openMotorName, setOpenMotorName] = useState<string | null>(null);

  useEffect(() => {
    fetchActions();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchActions = async () => {
    try {
      const userStr = localStorage.getItem('user');
      const accessToken = localStorage.getItem('access_token');
      if (!userStr || !accessToken) {
        setIsLoading(false);
        return;
      }

      const data = (await api.post('/student/analyze')) as any;
      const motors: MotorData[] = [];

      // 1) BS-MODEL (Akıllı Tekrar)
      if (data.bs_model?.urgent_topics?.length > 0) {
        const actions: MotorAction[] = data.bs_model.urgent_topics.map((topic: any) => {
          const urgency =
            topic.next_review_urgency === 'HEMEN' ? 'critical' :
            topic.next_review_urgency === 'ACİL' ? 'high' : 'medium';

          return {
            topic_name: topic.topic_name,
            subject_name: topic.subject_name,
            urgency,
            urgency_text: topic.next_review_urgency,
            subtitle: `${topic.days_since_last_test} gün geçti • Hatırlama: %${topic.remembering_rate}`,
            action: 'Hemen Tekrar Et',
            days_since: topic.days_since_last_test,
            score: topic.urgency_score,
          };
        });

        motors.push({
          name: 'Akıllı Tekrar',
          icon: '⏰',
          color: 'from-orange-500 to-orange-600',
          borderColor: 'border-orange-300',
          actions,
        });
      }

      // 2) PRIORITY ENGINE
      if (data.priority_engine?.this_week_topics?.length > 0) {
        const actions: MotorAction[] = data.priority_engine.this_week_topics.map((topic: any) => {
          const urgency =
            topic.priority_level === 'CRITICAL' ? 'critical' :
            topic.priority_level === 'HIGH' ? 'high' : 'medium';

          return {
            topic_name: topic.topic_name,
            subject_name: topic.subject_name,
            urgency,
            urgency_text:
              topic.priority_level === 'CRITICAL' ? 'KRİTİK' :
              topic.priority_level === 'HIGH' ? 'YÜKSEK' : 'ORTA',
            subtitle: `Öncelik Skoru: ${topic.priority_score} • Hatırlama: %${topic.remembering_rate}`,
            action: 'Plan Yap',
            score: topic.priority_score,
          };
        });

        motors.push({
          name: 'Öncelik Motoru',
          icon: '⚡',
          color: 'from-purple-500 to-purple-600',
          borderColor: 'border-purple-300',
          actions,
        });
      }

      // 3) DIFFICULTY ENGINE
      if (data.difficulty_engine?.struggling_topics?.length > 0) {
        const actions: MotorAction[] = data.difficulty_engine.struggling_topics.map((topic: any) => ({
          topic_name: topic.topic_name,
          subject_name: topic.subject_name,
          urgency: 'medium',
          urgency_text: 'ZORLUK',
          subtitle: `Ortalama Başarı: %${Math.round(topic.average_success)} • ${topic.total_tests} test`,
          action: 'Kaynak Değiştir',
          score: topic.difficulty_score,
        }));

        motors.push({
          name: 'Zorluk Analizi',
          icon: '📊',
          color: 'from-red-500 to-red-600',
          borderColor: 'border-red-300',
          actions,
        });
      }

      // 4) TIME ANALYZER
      if (data.time_analyzer?.slow_topics?.length > 0) {
        const actions: MotorAction[] = data.time_analyzer.slow_topics.map((topic: any) => ({
          topic_name: topic.topic_name,
          subject_name: topic.subject_name,
          urgency: 'medium',
          urgency_text: 'YAVAŞ',
          subtitle: `${Math.round(topic.average_interval_days)} gün ara • ${topic.total_tests} test`,
          action: 'Daha Sık Çöz',
          score: topic.average_interval_days,
        }));

        motors.push({
          name: 'Hız Analizi',
          icon: '🐢',
          color: 'from-yellow-500 to-yellow-600',
          borderColor: 'border-yellow-300',
          actions,
        });
      }

      setMotorsData(motors);
    } catch (error) {
      console.error('Action cards fetch error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'critical': return 'bg-red-500 text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-yellow-500 text-white';
      case 'low': return 'bg-green-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  // ✅ Dynamic grid columns (no empty slots)
  const gridClass = useMemo(() => {
    const count = motorsData.length;
    if (count <= 1) return 'grid-cols-1';
    if (count === 2) return 'grid-cols-1 md:grid-cols-2';
    if (count === 3) return 'grid-cols-1 md:grid-cols-3';
    return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4';
  }, [motorsData.length]);

  const openMotor = motorsData.find(m => m.name === openMotorName) ?? null;

  if (isLoading) {
    return (
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">⚡ Akıllı Aksiyonlar</h2>
        <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-purple-600 mx-auto"></div>
          <p className="text-gray-600 mt-3">Yükleniyor...</p>
        </div>
      </div>
    );
  }

  if (motorsData.length === 0) {
    return (
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">⚡ Akıllı Aksiyonlar</h2>
        <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
          <div className="text-5xl mb-3">🎯</div>
          <p className="text-gray-600">Test ekledikçe akıllı öneriler burada görünecek</p>
          <a
            href="/test-entry"
            className="inline-block mt-4 bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700"
          >
            Test Ekle
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="mb-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        ⚡ Akıllı Aksiyonlar
        <span className="text-xs text-purple-600 bg-purple-100 px-2 py-1 rounded-full">
          {motorsData.length} Motor Aktif
        </span>
      </h2>

      {/* ✅ Dynamic grid */}
      <div className={`grid ${gridClass} gap-4`}>
        {motorsData.map((motor) => {
          const topAction = motor.actions[0];

          return (
            <div key={motor.name} className="space-y-2">
              {/* MAIN CARD */}
              <div className={`bg-white rounded-2xl p-5 border-2 ${motor.borderColor} shadow-lg hover:shadow-xl transition-all`}>
                {/* Header */}
                <div className="flex items-center gap-3 mb-3">
                  <div className="text-4xl">{motor.icon}</div>
                  <div className="flex-1">
                    <div className="text-xs text-gray-500 mb-1">{motor.name}</div>

                    <div className="flex items-center justify-between gap-2">
                      <div className={`text-xs font-bold px-2 py-1 rounded inline-block ${getUrgencyColor(topAction.urgency)}`}>
                        {topAction.urgency_text}
                      </div>

                      <div className="text-xs text-gray-500">
                        {motor.actions.length} öneri
                      </div>
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className="mb-3">
                  <div className="font-bold text-gray-800 text-sm mb-1">
                    {topAction.topic_name}
                  </div>
                  {topAction.subject_name && (
                    <div className="text-xs text-gray-600 mb-2">
                      {topAction.subject_name}
                    </div>
                  )}
                  <div className="text-xs text-gray-600">
                    {topAction.subtitle}
                  </div>
                </div>

                {/* Primary Action */}
                <button
                  className={`w-full py-2 rounded-lg font-semibold text-white text-sm bg-gradient-to-r ${motor.color} hover:opacity-90 transition`}
                >
                  {topAction.action} →
                </button>

                {/* Feedback */}
                <div className="mt-3 flex justify-center">
                  <FeedbackButtons
                    componentType="action_card"
                    componentId={topAction.topic_name}
                    variant="rating"
                    size="sm"
                    metadata={{
                      motor: motor.name,
                      topic: topAction.topic_name,
                      urgency: topAction.urgency,
                    }}
                  />
                </div>

                {/* Details button */}
                {motor.actions.length > 1 && (
                  <button
                    type="button"
                    onClick={() => setOpenMotorName(motor.name)}
                    className="mt-3 w-full text-sm font-semibold text-purple-700 bg-purple-50 hover:bg-purple-100 py-2 rounded-lg transition"
                  >
                    Detayları Gör →
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Drawer */}
      <SideDrawer
        open={!!openMotor}
        title={openMotor ? `${openMotor.icon} ${openMotor.name}` : undefined}
        subtitle={openMotor ? `${openMotor.actions.length} aksiyon • hızlı tarama` : undefined}
        onClose={() => setOpenMotorName(null)}
      >
        {openMotor && (
          <div className="space-y-3">
            {openMotor.actions.map((a, idx) => (
              <div
                key={`${a.topic_name}-${idx}`}
                className={`rounded-xl border ${openMotor.borderColor} p-4 shadow-sm hover:shadow transition`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="min-w-0">
                    <div className="font-semibold text-gray-900 text-sm">
                      {a.topic_name}
                    </div>
                    {a.subject_name && (
                      <div className="text-xs text-gray-600">
                        {a.subject_name}
                      </div>
                    )}
                  </div>

                  <span className={`text-xs px-2 py-1 rounded ${getUrgencyColor(a.urgency)}`}>
                    {a.urgency_text}
                  </span>
                </div>

                <div className="text-xs text-gray-600 mt-2">
                  {a.subtitle}
                </div>

                <button
                  className={`mt-3 w-full py-2 rounded-lg font-semibold text-white text-sm bg-gradient-to-r ${openMotor.color} hover:opacity-90`}
                >
                  {a.action}
                </button>

                <div className="mt-2 flex justify-center">
                  <FeedbackButtons
                    componentType="action_card"
                    componentId={a.topic_name}
                    variant="rating"
                    size="sm"
                    metadata={{
                      motor: openMotor.name,
                      topic: a.topic_name,
                      urgency: a.urgency,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </SideDrawer>

      {/* Footer note */}
      <div className="mt-4 text-xs text-gray-500 text-center">
        💡 Bu öneriler 4 motor tarafından belirlenir. Detaylar panelde hızlı taranır.
      </div>
    </div>
  );
}
