'use client';
import { useState, useEffect } from 'react';
import { api } from '@/lib/api/client';
import FeedbackButtons from './FeedbackButtons';

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
  color: string;
  borderColor: string;
  actions: MotorAction[];
}

export default function SmartActionCards() {
  const [motorsData, setMotorsData] = useState<MotorData[]>([]);
  const [expandedMotor, setExpandedMotor] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchActions();
  }, []);

  const fetchActions = async () => {
    try {
      const userStr = localStorage.getItem('user');
      const accessToken = localStorage.getItem('access_token');

      if (!userStr || !accessToken) {
        setIsLoading(false);
        return;
      }

      const user = JSON.parse(userStr);

      const data = await api.post('/student/analyze') as any;
      const motors: MotorData[] = [];

      // 1. BS-MODEL (Akıllı Tekrar)
      if (data.bs_model?.urgent_topics && data.bs_model.urgent_topics.length > 0) {
        const actions = data.bs_model.urgent_topics.map((topic: any) => {
          const urgency = topic.next_review_urgency === 'HEMEN' ? 'critical' : 
                         topic.next_review_urgency === 'ACİL' ? 'high' : 'medium';
          
          return {
            topic_name: topic.topic_name,
            subject_name: topic.subject_name,
            urgency,
            urgency_text: topic.next_review_urgency,
            subtitle: `${topic.days_since_last_test} gün geçti • Hatırlama: %${topic.remembering_rate}`,
            action: 'Hemen Tekrar Et',
            days_since: topic.days_since_last_test,
            score: topic.urgency_score
          };
        });

        motors.push({
          name: 'Akıllı Tekrar',
          icon: '⏰',
          color: 'from-orange-500 to-orange-600',
          borderColor: 'border-orange-300',
          actions
        });
      }

      // 2. PRIORITY ENGINE
      if (data.priority_engine?.this_week_topics && data.priority_engine.this_week_topics.length > 0) {
        const actions = data.priority_engine.this_week_topics.map((topic: any) => {
          const urgency = topic.priority_level === 'CRITICAL' ? 'critical' : 
                         topic.priority_level === 'HIGH' ? 'high' : 'medium';
          
          return {
            topic_name: topic.topic_name,
            subject_name: topic.subject_name,
            urgency,
            urgency_text: topic.priority_level === 'CRITICAL' ? 'KRİTİK' : 
                          topic.priority_level === 'HIGH' ? 'YÜKSEK' : 'ORTA',
            subtitle: `Öncelik Skoru: ${topic.priority_score} • Hatırlama: %${topic.remembering_rate}`,
            action: 'Plan Yap',
            score: topic.priority_score
          };
        });

        motors.push({
          name: 'Öncelik Motoru',
          icon: '⚡',
          color: 'from-purple-500 to-purple-600',
          borderColor: 'border-purple-300',
          actions
        });
      }

      // 3. DIFFICULTY ENGINE
      if (data.difficulty_engine?.struggling_topics && data.difficulty_engine.struggling_topics.length > 0) {
        const actions = data.difficulty_engine.struggling_topics.map((topic: any) => ({
          topic_name: topic.topic_name,
          subject_name: topic.subject_name,
          urgency: 'medium' as const,
          urgency_text: 'ZORLUK',
          subtitle: `Ortalama Başarı: %${Math.round(topic.average_success)} • ${topic.total_tests} test`,
          action: 'Kaynak Değiştir',
          score: topic.difficulty_score
        }));

        motors.push({
          name: 'Zorluk Analizi',
          icon: '📊',
          color: 'from-red-500 to-red-600',
          borderColor: 'border-red-300',
          actions
        });
      }

      // 4. TIME ANALYZER
      if (data.time_analyzer?.slow_topics && data.time_analyzer.slow_topics.length > 0) {
        const actions = data.time_analyzer.slow_topics.map((topic: any) => ({
          topic_name: topic.topic_name,
          subject_name: topic.subject_name,
          urgency: 'medium' as const,
          urgency_text: 'YAVAŞ',
          subtitle: `${Math.round(topic.average_interval_days)} gün ara • ${topic.total_tests} test`,
          action: 'Daha Sık Çöz',
          score: topic.average_interval_days
        }));

        motors.push({
          name: 'Hız Analizi',
          icon: '🐢',
          color: 'from-yellow-500 to-yellow-600',
          borderColor: 'border-yellow-300',
          actions
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
          
           <a href="/test-entry"
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
          4 Motor Önerisi
        </span>
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {motorsData.map((motor, index) => {
          const topAction = motor.actions[0];
          const remainingCount = motor.actions.length - 1;
          const isExpanded = expandedMotor === motor.name;

          return (
            <div key={index} className="space-y-2">
              {/* ANA KART */}
              <div
                className={`bg-white rounded-2xl p-5 border-2 ${motor.borderColor} shadow-lg hover:shadow-xl transition-all`}
              >
                {/* Header */}
                <div className="flex items-center gap-3 mb-3">
                  <div className="text-4xl">{motor.icon}</div>
                  <div className="flex-1">
                    <div className="text-xs text-gray-500 mb-1">{motor.name}</div>
                    <div className={`text-xs font-bold px-2 py-1 rounded inline-block ${getUrgencyColor(topAction.urgency)}`}>
                      {topAction.urgency_text}
                    </div>
                  </div>
                </div>

                {/* Konu Bilgisi */}
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

                {/* Action Button */}
                <button
                  className={`w-full py-2 rounded-lg font-semibold text-white text-sm bg-gradient-to-r ${motor.color} hover:opacity-90 transition`}
                >
                  {topAction.action} →
                </button>

                {/* Rating */}
                <div className="mt-3 flex justify-center">
                  <FeedbackButtons
                    componentType="action_card"
                    componentId={topAction.topic_name}
                    variant="rating"
                    size="sm"
                    metadata={{
                      motor: motor.name,
                      topic: topAction.topic_name,
                      urgency: topAction.urgency
                    }}
                  />
                </div>
              </div>

              {/* Hepsini Gör */}
              {remainingCount > 0 && (
                <div
                  onClick={() => setExpandedMotor(isExpanded ? null : motor.name)}
                  className="text-center text-xs text-purple-600 hover:text-purple-800 cursor-pointer font-semibold transition"
                >
                  {isExpanded ? '▲ Daha azını görüntüle' : `▼ Hepsini Gör (${remainingCount} Aksiyon Daha)`}
                </div>
              )}

              {/* Diğer Aksiyonlar */}
              {isExpanded && remainingCount > 0 && (
                <div className="space-y-2">
                  {motor.actions.slice(1).map((action, idx) => (
                    <div
                      key={idx}
                      className={`bg-white rounded-lg p-3 border ${motor.borderColor} shadow hover:shadow-md transition`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <div className="font-semibold text-gray-800 text-sm">
                            {action.topic_name}
                          </div>
                          {action.subject_name && (
                            <div className="text-xs text-gray-600">
                              {action.subject_name}
                            </div>
                          )}
                        </div>
                        <span className={`text-xs px-2 py-1 rounded ${getUrgencyColor(action.urgency)}`}>
                          {action.urgency_text}
                        </span>
                      </div>
                      <div className="text-xs text-gray-600 mb-2">
                        {action.subtitle}
                      </div>
                      <button
                        className={`w-full py-1.5 rounded text-xs font-semibold text-white bg-gradient-to-r ${motor.color} hover:opacity-90`}
                      >
                        {action.action}
                      </button>
                      {/* Rating için küçük kartlarda */}
                      <div className="mt-2 flex justify-center">
                        <FeedbackButtons
                          componentType="action_card"
                          componentId={action.topic_name}
                          variant="rating"
                          size="sm"
                          metadata={{
                            motor: motor.name,
                            topic: action.topic_name,
                            urgency: action.urgency
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Alt Bilgi */}
      <div className="mt-4 text-xs text-gray-500 text-center">
        💡 Bu öneriler 4 motor tarafından gerçek zamanlı olarak belirleniyor
      </div>
    </div>
  );
}